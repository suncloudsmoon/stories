#!/usr/bin/env python3
"""Canon health-check for the stories plugin. Read-only. Exit 1 on errors.

A DEV/CI tool, not plugin runtime — the skill-only discipline still ships
untouched (see docs/stories/sagas/the-gate.md). This just makes drift visible.

Run from anywhere:  python3 scripts/lint-canon.py [repo-path]
(no arg = this plugin's repo; pass a path to lint a consumer repo's docs/stories/)
"""
import json
import re
import subprocess
import sys
from glob import glob
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
STORIES = ROOT / "docs" / "stories"
# Manifest/command-drift checks are specific to THIS plugin's repo. In a
# consumer repo (just a docs/stories/ wiki) they're skipped automatically.
IS_PLUGIN_REPO = (ROOT / ".claude-plugin" / "plugin.json").exists() and (
    ROOT / "codex" / ".codex-plugin" / "plugin.json"
).exists()

# What counts as "source" for the coverage-gap check (INFO only). Tune freely.
SOURCE_GLOBS = ["skills/*/SKILL.md", "scripts/*.py"]

# CC command  <->  Codex command-skill. Kept in sync by hand; checked here.
COMMAND_PAIRS = [
    ("commands/stories-init.md", "codex/skills/stories-init/SKILL.md"),
    ("commands/stories-refresh.md", "codex/skills/stories-refresh/SKILL.md"),
    ("commands/stories-ingest.md", "codex/skills/stories-ingest/SKILL.md"),
    ("commands/stories-lint.md", "codex/skills/stories-lint/SKILL.md"),
]
MANIFESTS = (".claude-plugin/plugin.json", "codex/.codex-plugin/plugin.json")
MANIFEST_FIELDS = ["name", "version", "description", "keywords"]
CODE_KINDS = {"saga", "vignette"}

errors, warns, infos = [], [], []


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def fm_list(fm, key):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


def fm_scalar(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None


def wikilinks(fm):
    m = re.search(r"^links:\s*(.*)$", fm, re.M)
    return re.findall(r"\[\[([^\]]+)\]\]", m.group(1)) if m else []


def git_last_date(rel):
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--", rel],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or None
    except Exception:
        return None


def step_titles(text):
    """Ordered, normalized step titles from a command/skill body.
    Handles '## 3. Title' (CC) and '3. **Title.**' (Codex)."""
    titles = []
    for line in text.splitlines():
        m = re.match(r"^#{1,4}\s*\d+\.?\s*(.+?)\s*$", line)
        if not m:
            m = re.match(r"^\d+\.\s*\*\*(.+?)[.*]", line)
        if m:
            titles.append(re.sub(r"[^a-z0-9 ]", "", m.group(1).lower()).strip())
    return titles


# ---- canon pages: frontmatter, covers, citations, links, staleness ----
pages = {p.stem: p for p in STORIES.rglob("*.md")}
inbound = {name: 0 for name in pages}

for name, p in sorted(pages.items()):
    if name in ("index", "log"):
        continue
    rel = p.relative_to(ROOT).as_posix()
    text = read(rel)
    fm = frontmatter(text)
    if not fm:
        errors.append(f"{name}: no frontmatter")
        continue
    kind = fm_scalar(fm, "kind")
    if not kind:
        errors.append(f"{name}: missing 'kind'")
    refreshed = fm_scalar(fm, "refreshed")
    if not (refreshed and re.match(r"\d{4}-\d{2}-\d{2}$", refreshed)):
        errors.append(f"{name}: missing/invalid 'refreshed' date")
        refreshed = None
    covers = fm_list(fm, "covers")
    if kind in CODE_KINDS and not covers:
        errors.append(f"{name}: kind '{kind}' has no 'covers:'")
    for g in covers:
        matched = glob(str(ROOT / g), recursive=True)
        if not matched:
            errors.append(f"{name}: covers '{g}' matches no file")
            continue
        if refreshed:
            newest = max((git_last_date(Path(m).relative_to(ROOT).as_posix())
                          or "0000-00-00") for m in matched)
            if newest > refreshed:
                warns.append(f"{name}: STALE — covered code changed {newest} > refreshed {refreshed}")
    for t in wikilinks(fm):
        if t not in pages:
            errors.append(f"{name}: link [[{t}]] -> no page")
        else:
            inbound[t] += 1
    for cp, ln in re.findall(r"`([\w./-]+):(\d+)`", text):
        fp = ROOT / cp
        if not fp.exists():
            if "/" in cp or cp.endswith((".md", ".py", ".ts", ".js", ".json")):
                errors.append(f"{name}: citation `{cp}:{ln}` -> missing file")
        elif int(ln) > sum(1 for _ in fp.open(encoding="utf-8", errors="ignore")):
            warns.append(f"{name}: citation `{cp}:{ln}` past end of file")

for name in pages:
    if name not in ("index", "log", "origin") and inbound.get(name, 0) == 0:
        warns.append(f"{name}: orphan (no inbound [[links]])")

# ---- manifest + command drift (this plugin's repo only) ----
if IS_PLUGIN_REPO:
    try:
        a, b = json.loads(read(MANIFESTS[0])), json.loads(read(MANIFESTS[1]))
        for f in MANIFEST_FIELDS:
            if a.get(f) != b.get(f):
                errors.append(f"manifest drift on '{f}': {a.get(f)!r} (claude) != {b.get(f)!r} (codex)")
    except Exception as e:
        errors.append(f"manifest read failed: {e}")
    for cc, cx in COMMAND_PAIRS:
        if not (ROOT / cc).exists():
            errors.append(f"missing CC command: {cc}")
        elif not (ROOT / cx).exists():
            errors.append(f"missing Codex skill: {cx}")
        elif step_titles(read(cc)) != step_titles(read(cx)):
            warns.append(f"command drift: {cc} and {cx} have different step structure")

# ---- coverage gap (INFO) ----
covered = set()
for p in pages.values():
    fm = frontmatter(read(p.relative_to(ROOT).as_posix())) or ""
    for g in fm_list(fm, "covers"):
        covered.update(Path(m).resolve() for m in glob(str(ROOT / g), recursive=True))
for sg in SOURCE_GLOBS:
    for f in glob(str(ROOT / sg), recursive=True):
        if Path(f).resolve() not in covered:
            infos.append(f"uncovered: {Path(f).relative_to(ROOT).as_posix()} (no story)")


def section(title, items):
    print(f"{title} ({len(items)})")
    for x in items:
        print(f"  - {x}")


print(f"stories-lint — {len(pages)} canon pages")
section("ERRORS", errors)
section("WARN", warns)
section("INFO", infos)
print("RESULT:", "FAILED" if errors else "OK")
sys.exit(1 if errors else 0)
