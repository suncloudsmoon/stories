#!/usr/bin/env python3
"""Canon health-check for the stories plugin. Read-only. Exit 1 on errors.

A dev/CI tool, not plugin runtime: the plugin ships skills and one hook; this
script keeps a docs/stories/ canon honest — links, covers, anchors, the Atlas,
ARCHITECTURE.md, and (in this repo) the two homes.

    python3 scripts/lint-canon.py [repo-path]     lint a canon (default: this repo)
    python3 scripts/lint-canon.py --self-test     prove each verdict on a temporary canon
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# One parser and one matcher for covers: — the hook's — so the linter never disagrees with the gate.
_spec = importlib.util.spec_from_file_location("stories_hook", Path(__file__).resolve().parent.parent / "hooks" / "stories.py")
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)

MANIFESTS = (".claude-plugin/plugin.json", "codex/.codex-plugin/plugin.json")
MANIFEST_FIELDS = ["name", "version", "description", "keywords", "author", "homepage", "repository", "license"]
MARKER = "derived by the stories plugin"
LINK = re.compile(r"\[\[([^\]|#]+)\]\]")
ANCHOR = re.compile(r"`([\w./-]+)#([^`]+)`")
LINE = re.compile(r"`([\w./-]+):(\d+)`")
CODE_SPAN = re.compile(r"`[^`\n]*`")  # prose may name `[[links]]` without linking


def git(root, *args):
    try:
        out = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=30)
        return out.stdout if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def repo_files(root):
    """Every file a covers: glob could mean — git's view (tracked + untracked, not ignored), else a walk."""
    listed = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if listed is not None:
        return sorted(f for f in set(listed.split("\0")) if f and (root / f).is_file())
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and ".git" not in p.relative_to(root).parts)


def last_commit(root, files):
    """(date, file) of the newest commit touching any of files — one git call, not one per file."""
    out = git(root, "log", "-1", "--format=%cs", "--name-only", "--", *files) or ""
    lines = [line for line in out.splitlines() if line.strip()]
    return (lines[0], lines[1] if len(lines) > 1 else files[0]) if lines else ("", None)


def is_code_path(path):
    """`path#x` in prose names a citation only when it looks like a real path."""
    return "/" in path or re.search(r"\.\w+$", path) is not None


def check_citations(root, where, text, errors, warns):
    for path, anchor in ANCHOR.findall(text):
        if not is_code_path(path):
            continue
        file = root / path
        if not file.is_file():
            errors.append(f"{where}: citation `{path}#{anchor}` -> missing file")
            continue
        count = file.read_text(encoding="utf-8", errors="replace").count(anchor)
        if count == 0:
            errors.append(f"{where}: anchor gone — `{anchor}` no longer appears in {path}")
        elif count > 1:
            warns.append(f"{where}: anchor ambiguous — `{anchor}` appears {count}× in {path}")
    for path, line in LINE.findall(text):
        if is_code_path(path):
            errors.append(f"{where}: line citation `{path}:{line}` — cite `{path}#<anchor>` instead")


def lint(root):
    errors, warns, infos = [], [], []
    files = repo_files(root)
    canon = root / "docs" / "stories"
    pages = {p.stem: p for p in canon.rglob("*.md")} if canon.is_dir() else {}
    index = pages.pop("index", None)
    atlas = set(LINK.findall(index.read_text(encoding="utf-8"))) if index else set()
    if canon.is_dir() and not index:
        errors.append("index.md (the Atlas) is missing")
    inbound = {name: 0 for name in pages}

    for name, page in sorted(pages.items()):
        text = page.read_text(encoding="utf-8")
        front, _ = hook.split_page(text)
        globs = hook.parse_covers(front)
        if globs is None and page.parent.name == "sagas":
            errors.append(f"{name}: pages in sagas/ need covers: — without it the gate never sees them")
        if globs is not None:
            if not globs:
                errors.append(f'{name}: covers: yields no globs — it must be a single-line list like covers: ["src/**"]')
            refreshed = re.search(r"^refreshed:\s*(\d{4}-\d{2}-\d{2})\s*$", front, re.M)
            if not refreshed:
                errors.append(f"{name}: story needs a valid refreshed: YYYY-MM-DD")
            covered = []
            for g in globs:  # the hook's own matcher, so lint and gate agree on every path
                matched = [f for f in files if hook.glob_regex(g).fullmatch(f)]
                if not matched:
                    errors.append(f"{name}: covers '{g}' matches no file")
                covered += matched
            if covered and refreshed:
                newest, culprit = last_commit(root, sorted(set(covered)))
                if newest > refreshed.group(1):
                    warns.append(f"REVIEW {name} — {culprit} committed {newest} > refreshed {refreshed.group(1)}")
        for target in LINK.findall(CODE_SPAN.sub("", text)):
            if target in pages:
                inbound[target] += 1
            elif target != "index":
                errors.append(f"{name}: link [[{target}]] -> no page")
        check_citations(root, name, text, errors, warns)
        if index and name not in atlas:
            errors.append(f"{name}: missing from the Atlas (index.md)")

    for name in sorted(atlas - set(pages)):
        errors.append(f"index: Atlas lists [[{name}]] but no page exists")
    for name, count in sorted(inbound.items()):
        if count == 0 and name != "origin":
            warns.append(f"{name}: orphan (no inbound [[links]])")

    architecture = root / "ARCHITECTURE.md"
    if architecture.is_file():
        body = architecture.read_text(encoding="utf-8")
        if MARKER in body:
            for ref in sorted(set(re.findall(r"(docs/stories/[\w./-]+\.md)", body))):
                if not (root / ref).is_file():
                    errors.append(f"ARCHITECTURE.md: links missing page {ref}")
            check_citations(root, "ARCHITECTURE.md", body, errors, warns)
        else:
            infos.append("ARCHITECTURE.md: hand-written (no marker) — never overwrite it")

    if all((root / m).is_file() for m in MANIFESTS):  # this plugin's own repo
        check_plugin(root, errors)
    return errors, warns, infos


def check_plugin(root, errors):
    try:
        claude, codex = (json.loads((root / m).read_text()) for m in MANIFESTS)
        for field in MANIFEST_FIELDS:
            if claude.get(field) != codex.get(field):
                errors.append(f"manifest drift on '{field}': {claude.get(field)!r} != {codex.get(field)!r}")
    except ValueError as e:
        errors.append(f"manifest does not parse: {e}")
    homes = [root / "codex" / "skills" / s.name for s in sorted((root / "skills").iterdir()) if s.is_dir()]
    for link in homes + [root / "codex" / "hooks"]:
        if not link.is_symlink():
            errors.append(f"{link.relative_to(root)}: must be a symlink into the root plugin (one copy, both homes)")
        elif not link.exists():
            errors.append(f"{link.relative_to(root)}: broken symlink")
    try:
        events = json.loads((root / "hooks" / "hooks.json").read_text()).get("hooks", {})
    except (OSError, ValueError) as e:
        errors.append(f"hooks/hooks.json: {e}")
        return
    for missing in sorted({"PostToolUse", "PreToolUse", "Stop"} - set(events)):
        errors.append(f"hooks/hooks.json: no {missing} hook — the gate needs all three events")
    commands = [h.get("command", "") for groups in events.values() for group in groups for h in group.get("hooks", [])]
    for script in sorted(set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", " ".join(commands)))):
        if not (root / script).is_file():
            errors.append(f"hooks/hooks.json: runs {script}, which does not exist")


def main(root):
    errors, warns, infos = lint(root)
    for title, items in (("ERRORS", errors), ("WARN", warns), ("INFO", infos)):
        print(f"{title} ({len(items)})")
        for item in items:
            print(f"  - {item}")
    print("RESULT:", "FAILED" if errors else "OK")
    return 1 if errors else 0


# ---------------------------------------------------------------- self-test

def self_test():
    atlas = "# Atlas\n- [[origin]] — why\n- [[auth]] — tokens\n"
    origin = "# Origin\nSee [[auth]].\n"
    story = ('---\ncovers: ["src/auth.py"]\nrefreshed: 2026-10-29\n---\n# Why tokens rotate\n'
             "The check lives in `src/auth.py#verify_token`. See [[origin]].\n")
    code = "def verify_token():\n    pass\n"
    passed = 0

    def case(name, mutate, expect):
        nonlocal passed
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "docs/stories/sagas").mkdir(parents=True)
            (tmp / "src").mkdir()
            (tmp / "docs/stories/index.md").write_text(atlas)
            (tmp / "docs/stories/origin.md").write_text(origin)
            (tmp / "docs/stories/sagas/auth.md").write_text(story)
            (tmp / "src/auth.py").write_text(code)
            mutate(tmp)
            errors, warns, _ = lint(tmp)
            if not expect(errors, warns):
                raise AssertionError(f"{name}: errors={errors} warns={warns}")
            passed += 1
        finally:
            shutil.rmtree(tmp)

    def edit(rel, old, new):
        def mutate(root):
            p = root / rel
            p.write_text(p.read_text().replace(old, new))
        return mutate

    def has(items, word):
        return any(word in x for x in items)

    case("valid canon", lambda r: None, lambda e, w: e == [] and w == [])
    case("anchor gone", edit("src/auth.py", "verify_token", "other"), lambda e, w: has(e, "anchor"))
    case("anchor ambiguous", edit("src/auth.py", "pass", "verify_token()"), lambda e, w: has(w, "ambiguous"))
    case("line citation", edit("docs/stories/sagas/auth.md", "See [[origin]]", "`src/auth.py:1` [[origin]]"),
         lambda e, w: has(e, "line citation"))
    case("block-style covers", edit("docs/stories/sagas/auth.md", 'covers: ["src/auth.py"]', 'covers:\n  - "src/auth.py"'),
         lambda e, w: has(e, "single-line"))
    case("glob matches nothing", edit("docs/stories/sagas/auth.md", "src/auth.py\"]", "src/nope/**\"]"),
         lambda e, w: has(e, "matches no file"))
    case("story without refreshed", edit("docs/stories/sagas/auth.md", "refreshed: 2026-10-29\n", ""),
         lambda e, w: has(e, "refreshed"))
    case("page missing from Atlas", edit("docs/stories/index.md", "- [[auth]] — tokens\n", ""),
         lambda e, w: has(e, "Atlas"))
    case("covers with nothing usable", edit("docs/stories/sagas/auth.md", 'covers: ["src/auth.py"]', "covers: []"),
         lambda e, w: has(e, "no globs"))
    case("covers with a comment and single quotes", edit("docs/stories/sagas/auth.md", 'covers: ["src/auth.py"]',
                                                         "covers: ['src/auth.py']   # why"), lambda e, w: e == [])
    case("saga without covers", edit("docs/stories/sagas/auth.md", 'covers: ["src/auth.py"]\n', ""),
         lambda e, w: has(e, "sagas/"))

    def hidden_only(root):
        (root / "conf").mkdir()
        (root / "conf/.settings.py").write_text("x = 1\n")
        edit("docs/stories/sagas/auth.md", '["src/auth.py"]', '["src/auth.py", "conf/**"]')(root)
    case("glob matches a hidden file, like the hook", hidden_only, lambda e, w: e == [])

    def plugin_with_dead_hook(root):
        for m in (".claude-plugin", "codex/.codex-plugin"):
            (root / m).mkdir(parents=True)
            (root / m / "plugin.json").write_text('{"name": "x"}')
        (root / "skills").mkdir()
        (root / "hooks").mkdir()
        (root / "codex/hooks").symlink_to("../hooks")
        (root / "hooks/hooks.json").write_text(json.dumps({"hooks": {e: [{"hooks": [
            {"type": "command", "command": 'python3 "${CLAUDE_PLUGIN_ROOT}/hooks/missing.py"'}]}]
            for e in ("PostToolUse", "PreToolUse", "Stop")}}))
    case("hooks.json names a missing script", plugin_with_dead_hook, lambda e, w: has(e, "missing.py"))
    case("broken link", edit("docs/stories/origin.md", "[[auth]]", "[[auth]] [[ghost]]"),
         lambda e, w: has(e, "ghost"))
    case("link syntax named in code is not a link", edit("docs/stories/origin.md", "[[auth]]", "[[auth]] `[[links]]`"),
         lambda e, w: e == [])
    print(f"self-test: {passed} passed")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--self-test"]:
        sys.exit(self_test())
    sys.exit(main(Path(args[0]).resolve() if args else Path(__file__).resolve().parent.parent))
