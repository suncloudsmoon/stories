#!/usr/bin/env python3
"""The stories gate — points the model at the story that covers a file.

One script, three hook events (hooks/hooks.json), Claude Code and Codex alike:
  PostToolUse Read  — a covered file was read: name its story, once per session.
  PreToolUse edits  — an edit to a covered file arrived unannounced: block it once.
  Stop              — covered files changed but their story wasn't touched: remind once.
Dormant in a repo without docs/stories/. Fails open: an internal error never blocks work.

Self-test:  python3 hooks/stories.py --self-test
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

try:
    import fcntl
except ImportError:  # shortcut: Windows has no flock; parallel events there may repeat a pointer — use msvcrt.locking if asked.
    fcntl = None

Story = namedtuple("Story", "path title globs")  # path: root-relative posix; globs: compiled patterns

CANON = "docs/stories/"
QUIET = (0, "", "")
COVERS = re.compile(r"^covers:(.*)$", re.M)
FRONT = re.compile(r"---\n(.*?)\n---(?:\n|$)", re.S)
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "apply_patch"}
PATCH_PATH = re.compile(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", re.M)


def glob_regex(pattern):
    """Translate a covers: glob to a regex: ** spans directories, * and ? never cross '/'."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(out)


def find_root(cwd):
    """The project root: the nearest directory holding docs/stories/, else None (dormant)."""
    for start in filter(None, [os.environ.get("CLAUDE_PROJECT_DIR"), cwd]):
        here = Path(start).resolve()
        for directory in (here, *here.parents):
            if (directory / "docs" / "stories").is_dir():
                return directory
    return None


def parse_covers(front):
    """Globs from a one-line covers: — ["a", 'b', c], optional # comment. None when absent; [] when unusable."""
    line = COVERS.search(front)
    if not line:
        return None
    listed = re.match(r"\s*\[([^\]]*)\]\s*(?:#.*)?$", line.group(1))
    items = (g.strip().strip("\"'").strip() for g in listed.group(1).split(",")) if listed else ()
    return [g for g in items if g]


def split_page(text):
    """(frontmatter, body) of a page — tolerant of CRLF and a missing final newline."""
    text = text.replace("\r\n", "\n")
    m = FRONT.match(text)
    return (m.group(1), text[m.end():]) if m else ("", text)


def load_stories(root):
    # shortcut: re-reads the canon on every event (~30 ms here); cache on docs/stories mtimes if canons reach hundreds of pages.
    stories = []
    for page in sorted((root / "docs" / "stories").rglob("*.md")):
        front, body = split_page(page.read_text(encoding="utf-8", errors="replace"))
        globs = parse_covers(front)
        if not globs:
            continue
        heading = re.search(r"^# (.+)$", body, re.M)
        stories.append(Story(page.relative_to(root).as_posix(),
                             heading.group(1).strip() if heading else page.stem,
                             [glob_regex(g) for g in globs]))
    return stories


def relative(root, file_path):
    """Root-relative posix path, or None when the file lies outside the project."""
    try:
        return Path(file_path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return None


def edit_targets(tool_name, tool_input):
    if tool_name == "apply_patch":  # Codex: paths live in the patch text
        command = tool_input.get("command", "")
        if isinstance(command, list):
            command = "\n".join(command)
        return [p.strip() for p in PATCH_PATH.findall(command)]
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    return [path] if path else []


def covering(stories, rel):
    return [s for s in stories if any(g.fullmatch(rel) for g in s.globs)]


def pointers(stories):
    unique = {s.path: s for s in stories}.values()
    return "; ".join(f"{s.path} — “{s.title}”" for s in unique)


def handle(event, root, state):
    """One hook event -> (exit code, stdout, stderr). Mutates the session state."""
    name = event.get("hook_event_name")
    base = event.get("cwd") or str(root)
    tool_input = event.get("tool_input") or {}
    stories = load_stories(root)

    def resolve(path):
        return relative(root, os.path.join(base, path))

    tool = event.get("tool_name", "")

    if name == "PostToolUse" and tool in EDIT_TOOLS:  # the edit landed — only now does it count
        for rel in filter(None, map(resolve, edit_targets(tool, tool_input))):
            if rel.startswith(CANON):
                if rel not in state["touched"]:
                    state["touched"].append(rel)
                continue
            for s in covering(stories, rel):
                files = state["edited"].setdefault(s.path, [])
                if rel not in files:
                    files.append(rel)
                if s.path in state["touched"]:  # the story predates this change: ask again at Stop
                    state["touched"].remove(s.path)
        return QUIET

    if name == "PostToolUse":  # a Read
        rel = resolve(tool_input["file_path"]) if tool_input.get("file_path") else None
        if rel is None:
            return QUIET
        if rel in {s.path for s in stories}:  # reading the story itself is the point
            if rel not in state["announced"]:
                state["announced"].append(rel)
            return QUIET
        new = [s for s in covering(stories, rel) if s.path not in state["announced"]]
        if not new or rel.startswith(CANON):
            return QUIET
        state["announced"] += [s.path for s in new]
        them = "it" if len(new) == 1 else "them"
        message = f"`{rel}` is covered by {pointers(new)}. Read {them} before you change this file."
        return 0, json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                     "additionalContext": message}}), ""

    if name == "PreToolUse":  # the gate only; edits are recorded when they land (PostToolUse)
        targets = [r for r in map(resolve, edit_targets(tool, tool_input)) if r]
        blocked = [(rel, s) for rel in targets if not rel.startswith(CANON)
                   for s in covering(stories, rel) if s.path not in state["announced"]]
        if blocked:
            # Known limit: parallel edits under one story pass once the first is blocked; the
            # pointer reaches the model in that same turn, and Codex emits no Read to wait for.
            for _, s in blocked:
                if s.path not in state["announced"]:
                    state["announced"].append(s.path)
            files = ", ".join(f"`{f}`" for f in dict.fromkeys(rel for rel, _ in blocked))
            return 2, "", f"Before editing {files}, read {pointers([s for _, s in blocked])}. Then retry."
        return QUIET

    if name == "Stop":
        if event.get("stop_hook_active"):
            return QUIET
        due = [p for p in state["edited"] if p not in state["touched"] and p not in state["reminded"]]
        if not due:
            return QUIET
        state["reminded"] += due
        changes = "; ".join(", ".join(f"`{f}`" for f in state["edited"][p]) + f", covered by {p}" for p in due)
        reason = (f"You changed {changes}. If the why changed, rewrite it and set refreshed: to today; "
                  "if not, you're done.")
        return 0, json.dumps({"decision": "block", "reason": reason}), ""

    return QUIET


def load_state(path):
    state = {"announced": [], "edited": {}, "touched": [], "reminded": []}
    try:
        saved = json.loads(Path(path).read_text())
        if isinstance(saved, dict):
            state.update({k: saved[k] for k in state if isinstance(saved.get(k), type(state[k]))})
    except (OSError, ValueError):
        pass  # missing or corrupt: start the session fresh
    return state


def run(stdin_text, data_dir):
    try:
        event = json.loads(stdin_text)
        root = find_root(event.get("cwd") or os.getcwd())
        if root is None:
            return QUIET
        session = re.sub(r"[^\w-]", "", str(event.get("session_id") or "session"))  # no path tricks
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        path = Path(data_dir) / f"stories-{session}.json"
        with open(path.with_suffix(".lock"), "a") as lock:  # hosts run hooks in parallel; one session, one writer
            if fcntl:
                fcntl.flock(lock, fcntl.LOCK_EX)
            state = load_state(path)
            result = handle(event, root, state)
            scratch = path.with_suffix(f".{os.getpid()}.tmp")
            scratch.write_text(json.dumps(state))
            os.replace(scratch, path)
        return result
    except Exception:
        return QUIET  # fail open: a bug in this hook must never block the user's work


def main():
    # shortcut: hooks.json invokes `python3`; Windows without python3 on PATH gets no gate — add commandWindows if asked.
    code, out, err = run(sys.stdin.read(), os.environ.get("CLAUDE_PLUGIN_DATA") or tempfile.gettempdir())
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return code


# ---------------------------------------------------------------- self-test

def self_test():
    passed = 0

    def check(name, condition):
        nonlocal passed
        if not condition:
            raise AssertionError(name)
        passed += 1

    story = '---\ncovers: ["src/auth/**", "src/session.py"]\nrefreshed: 2026-10-29\n---\n# Why tokens rotate\n'

    def repo(tmp, text=story):
        root = Path(tmp)
        (root / "docs/stories/sagas").mkdir(parents=True)
        (root / "docs/stories/sagas/auth.md").write_text(text)
        (root / "src/auth").mkdir(parents=True)
        return root

    def event(root, name, tool=None, **tool_input):
        e = {"session_id": "t", "cwd": str(root), "hook_event_name": name}
        if tool:
            e.update(tool_name=tool, tool_input=tool_input)
        return e

    def fresh():
        return {"announced": [], "edited": {}, "touched": [], "reminded": []}

    check("globs", glob_regex("src/**").fullmatch("src/a/b.py")
          and glob_regex("src/**/x.py").fullmatch("src/x.py")
          and not glob_regex("src/*.py").fullmatch("src/a/b.py")
          and glob_regex(".github/**").fullmatch(".github/workflows/lint.yml"))

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        code, out, _ = handle(event(root, "PostToolUse", "Read", file_path="src/auth/t.py"), root, state)
        check("read_announces_once", code == 0 and "docs/stories/sagas/auth.md" in out
              and "Why tokens rotate" in out)
        check("read_announces_once (repeat)",
              handle(event(root, "PostToolUse", "Read", file_path="src/auth/t.py"), root, state)[1] == "")

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        handle(event(root, "PostToolUse", "Read", file_path="docs/stories/sagas/auth.md"), root, state)
        check("reading_story_counts",
              handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)[0] == 0)

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        code, _, err = handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)
        check("edit_blocks_once", code == 2 and "docs/stories/sagas/auth.md" in err
              and handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)[0] == 0)

    check("apply_patch", edit_targets("apply_patch", {
        "command": "*** Begin Patch\n*** Update File: src/auth/t.py\n@@\n*** End Patch"}) == ["src/auth/t.py"])

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)  # blocked: never happened
        check("blocked_edit_not_recorded", handle(event(root, "Stop"), root, dict(state))[1] == "")
        handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)  # the retry passes the gate
        handle(event(root, "PostToolUse", "Edit", file_path="src/session.py"), root, state)  # ...and lands
        _, out, _ = handle(event(root, "Stop"), root, state)
        check("stop_reminds_once", json.loads(out)["decision"] == "block"
              and "src/session.py" in json.loads(out)["reason"]
              and handle(event(root, "Stop"), root, state)[1] == ""
              and handle(dict(event(root, "Stop"), stop_hook_active=True), root, fresh())[1] == "")

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        handle(event(root, "PostToolUse", "Edit", file_path="src/session.py"), root, state)
        handle(event(root, "PostToolUse", "Edit", file_path="docs/stories/sagas/auth.md"), root, state)
        check("touched_story_silences_stop", handle(event(root, "Stop"), root, state)[1] == "")

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        handle(event(root, "PostToolUse", "Edit", file_path="docs/stories/sagas/auth.md"), root, state)
        handle(event(root, "PostToolUse", "Edit", file_path="src/session.py"), root, state)
        check("story_touched_before_code_still_reminds", handle(event(root, "Stop"), root, state)[1] != "")

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        handle(event(root, "PostToolUse", "Read", file_path="docs/stories/sagas/auth.md"), root, state)
        handle(event(root, "PreToolUse", "Edit", file_path="src/session.py"), root, state)  # allowed, then fails
        check("failed_edit_not_recorded", handle(event(root, "Stop"), root, state)[1] == "")

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp, '---\ncovers: ["src/session.py"]  # see [x]\nrefreshed: 2026-10-29\n---\n# T\n')
        check("covers_comment_with_brackets", covering(load_stories(root), "src/session.py") != [])

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp, story.replace("\n", "\r\n"))
        check("crlf_frontmatter", covering(load_stories(root), "src/session.py") != [])

    with tempfile.TemporaryDirectory() as tmp:
        root, state = repo(tmp), fresh()
        check("paths", relative(root, str(root / "src/session.py")) == "src/session.py"
              and relative(root, "/etc/hosts") is None
              and handle(event(root, "PreToolUse", "Edit", file_path="/etc/hosts"), root, state) == (0, "", ""))

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp).resolve()
        saved = os.environ.pop("CLAUDE_PROJECT_DIR", None)
        try:
            check("subdirectory_cwd", find_root(str(root / "src")) == root)
        finally:
            if saved is not None:
                os.environ["CLAUDE_PROJECT_DIR"] = saved

    with tempfile.TemporaryDirectory() as tmp:
        saved = os.environ.pop("CLAUDE_PROJECT_DIR", None)
        try:
            check("dormant", find_root(tmp) is None)
        finally:
            if saved is not None:
                os.environ["CLAUDE_PROJECT_DIR"] = saved

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp)
        (Path(tmp) / "stories-t.json").write_text("{broken")
        check("fails_open", run("not json", tmp) == (0, "", "")
              and load_state(Path(tmp) / "stories-t.json") == fresh())

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp, '---\ncovers: ["src/**"]\nrefreshed: 2026-10-29\n---\nNo heading.\n')
        check("title_fallback", load_stories(root)[0].title == "auth")

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp, "---\ncovers: ['src/auth/**', src/session.py]   # a comment\nrefreshed: 2026-10-29\n---\n# T\n")
        check("covers_spellings", [s.path for s in covering(load_stories(root), "src/session.py")]
              == ["docs/stories/sagas/auth.md"] and covering(load_stories(root), "src/auth/x.py") != [])

    with tempfile.TemporaryDirectory() as tmp:
        root = repo(tmp)
        for i in range(12):
            (root / f"docs/stories/sagas/s{i}.md").write_text(f'---\ncovers: ["src/f{i}.py"]\nrefreshed: 2026-10-29\n---\n# S{i}\n')
        data = Path(tmp) / "data"
        script = str(Path(__file__).resolve())
        env = dict(os.environ, CLAUDE_PLUGIN_DATA=str(data))
        env.pop("CLAUDE_PROJECT_DIR", None)
        procs = [subprocess.Popen([sys.executable, script], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, env=env)
                 for _ in range(12)]
        for i, p in enumerate(procs):
            p.stdin.write(json.dumps(event(root, "PostToolUse", "Read", file_path=f"src/f{i}.py")).encode())
            p.stdin.close()
        for p in procs:
            p.wait()
        check("parallel_events_keep_state", len(load_state(data / "stories-t.json")["announced"]) == 12)

    print(f"self-test: {passed} passed")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    sys.exit(main())
