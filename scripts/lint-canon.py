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

# Fallback "source" allowlist for non-git checkouts; in a git repo the
# coverage-gap check walks `git ls-files` minus COVERAGE_EXEMPT instead.
SOURCE_GLOBS = ["skills/*/SKILL.md", "scripts/*.py"]

# CC command  <->  Codex command-skill. Kept in sync by hand; checked here.
COMMAND_PAIRS = [
    ("commands/stories-init.md", "codex/skills/stories-init/SKILL.md"),
    ("commands/stories-refresh.md", "codex/skills/stories-refresh/SKILL.md"),
    ("commands/stories-ingest.md", "codex/skills/stories-ingest/SKILL.md"),
    ("commands/stories-lint.md", "codex/skills/stories-lint/SKILL.md"),
]
MANIFESTS = (".claude-plugin/plugin.json", "codex/.codex-plugin/plugin.json")
MANIFEST_FIELDS = ["name", "version", "description", "keywords", "author", "homepage", "repository", "license"]
CODE_KINDS = {"saga", "vignette", "system"}

# The behavioral contract's default-exempt list, restated in three homes.
# Drift between them is this repo's self-declared likeliest bug — diffed here.
EXEMPT_ITEMS = ["bug fixes", "typos", "formatting", "comments",
                "dependency bumps", "test-only edits"]
CONTRACT_HOMES = ["skills/stories/SKILL.md", "README.md",
                  "docs/specs/2026-06-14-stories-plugin-design.md"]

# Paths no story needs to cover: the canon itself, assets, frozen history.
COVERAGE_EXEMPT = ("docs/stories/", "docs/assets/", "docs/plans/",
                   "docs/superpowers/", "LICENSE", ".gitignore", ".ref/")

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
            newest, culprit = "0000-00-00", None
            for m in matched:
                if not Path(m).is_file():
                    continue  # glob('**') yields directories too — name files, not dirs
                rel_m = Path(m).relative_to(ROOT).as_posix()
                d = git_last_date(rel_m) or "0000-00-00"
                if d > newest:
                    newest, culprit = d, rel_m
            if newest > refreshed:
                warns.append(f"{name}: STALE — {culprit} changed {newest} > refreshed {refreshed}")
    for t in wikilinks(fm):
        if t not in pages:
            errors.append(f"{name}: link [[{t}]] -> no page")
        else:
            inbound[t] += 1
    citations = re.findall(r"`([\w./-]+):(\d+)`", text)
    if kind in CODE_KINDS and not citations:
        warns.append(f"{name}: no `path:line` citation — gate-bearing pages must cite the code they cover")
    for cp, ln in citations:
        fp = ROOT / cp
        if not fp.exists():
            if "/" in cp or cp.endswith((".md", ".py", ".ts", ".js", ".json")):
                errors.append(f"{name}: citation `{cp}:{ln}` -> missing file")
        elif int(ln) > sum(1 for _ in fp.open(encoding="utf-8", errors="ignore")):
            warns.append(f"{name}: citation `{cp}:{ln}` past end of file")

for name in pages:
    if name not in ("index", "log", "origin") and inbound.get(name, 0) == 0:
        warns.append(f"{name}: orphan (no inbound [[links]])")

# ---- Atlas mirror: inline covers in index.md must match page frontmatter ----
idx_path = STORIES / "index.md"
if idx_path.exists():
    inline_covers = {}
    for m in re.finditer(r"^\s*-\s*\[\[([\w-]+)\]\].*—\s*covers\s+(.+)$",
                         idx_path.read_text(encoding="utf-8"), re.M):
        inline_covers[m.group(1)] = re.findall(r"`([^`]+)`", m.group(2))
    for name, p in sorted(pages.items()):
        if name in ("index", "log"):
            continue
        fm = frontmatter(read(p.relative_to(ROOT).as_posix())) or ""
        if fm_scalar(fm, "kind") in CODE_KINDS:
            covers = fm_list(fm, "covers")
            if name not in inline_covers:
                warns.append(f"index: [[{name}]] carries covers: but the Atlas lists none inline")
            elif set(inline_covers[name]) != set(covers):
                errors.append(f"index: [[{name}]] inline covers != frontmatter covers "
                              f"({sorted(inline_covers[name])} vs {sorted(covers)})")

# ---- manifest + command drift (this plugin's repo only) ----
if IS_PLUGIN_REPO:
    try:
        a, b = json.loads(read(MANIFESTS[0])), json.loads(read(MANIFESTS[1]))
        for f in MANIFEST_FIELDS:
            if a.get(f) != b.get(f):
                errors.append(f"manifest drift on '{f}': {a.get(f)!r} (claude) != {b.get(f)!r} (codex)")
    except Exception as e:
        errors.append(f"manifest read failed: {e}")
    for home in CONTRACT_HOMES:
        try:
            body_l = read(home).lower()
        except (OSError, UnicodeDecodeError) as e:
            errors.append(f"contract home unreadable: {home}: {e}")
            continue
        gate_lines = [l for l in body_l.splitlines() if "default-exempt" in l]
        if not gate_lines:
            errors.append(f"exempt-list drift: {home} has no 'default-exempt' line")
        for gl in gate_lines:
            missing = [i for i in EXEMPT_ITEMS if i not in gl]
            if missing:
                errors.append(f"exempt-list drift: a 'default-exempt' line in {home} is missing: {', '.join(missing)}")
    for cc, cx in COMMAND_PAIRS:
        if not (ROOT / cc).exists():
            errors.append(f"missing CC command: {cc}")
        elif not (ROOT / cx).exists():
            errors.append(f"missing Codex skill: {cx}")
        else:
            ta, tb = step_titles(read(cc)), step_titles(read(cx))
            if ta != tb:
                i = next((k for k, (x, y) in enumerate(zip(ta, tb)) if x != y),
                         min(len(ta), len(tb)))
                got_cc = ta[i] if i < len(ta) else "<missing>"
                got_cx = tb[i] if i < len(tb) else "<missing>"
                warns.append(f"command drift: {cc} vs {cx} — step {i + 1}: "
                             f"{got_cc!r} (claude) != {got_cx!r} (codex)")

# ---- systems layer: ARCHITECTURE.md <-> docs/stories/systems/ ----
ARCH_FILE = ROOT / "ARCHITECTURE.md"
MARKER = "derived by the stories plugin"
SKIP_DIRS = {"docs", "node_modules", "vendor", "dist", "build", "target"}
MERMAID_KEYWORDS = {"flowchart", "graph", "subgraph", "end", "classDef", "class", "click", "style", "direction"}
sys_dir = STORIES / "systems"
system_pages = sorted(sys_dir.glob("*.md")) if sys_dir.is_dir() else []

if system_pages and not ARCH_FILE.exists():
    errors.append("systems: pages exist under docs/stories/systems/ but ARCHITECTURE.md missing at repo root")

if ARCH_FILE.exists():
    body = ARCH_FILE.read_text(encoding="utf-8")
    if MARKER not in body:
        warns.append("ARCHITECTURE.md: no derived-by marker — hand-written? never overwrite it")
    linked = set(re.findall(r"\(docs/stories/systems/([\w-]+)\.md\)", body))
    for p in system_pages:
        if p.stem not in linked:
            errors.append(f"ARCHITECTURE.md: system page '{p.stem}' not linked from the legend")
    for slug in sorted(linked):
        if not (sys_dir / f"{slug}.md").exists():
            errors.append(f"ARCHITECTURE.md: legend links missing page docs/stories/systems/{slug}.md")
    blocks = re.findall(r"```mermaid\n(.*?)```", body, re.S)
    if blocks:
        ids = {i for i in re.findall(r"^\s*([A-Za-z]\w*)\s*[\[(]", blocks[0], re.M)
               if i not in MERMAID_KEYWORDS}
        legend_ids = {s.replace("-", "_") for s in linked}
        for i in sorted(ids - legend_ids):
            warns.append(f"ARCHITECTURE.md: diagram node '{i}' has no legend link")

if system_pages:
    sys_cover_roots = set()
    for p in system_pages:
        fmp = frontmatter(p.read_text(encoding="utf-8")) or ""
        for g in fm_list(fmp, "covers"):
            root_seg = g.split("/")[0]
            if root_seg and "*" not in root_seg:
                sys_cover_roots.add(root_seg)
    for d in sorted(ROOT.iterdir()):
        if (d.is_dir() and not d.name.startswith(".")
                and d.name not in SKIP_DIRS and d.name not in sys_cover_roots):
            warns.append(f"systems: top-level dir '{d.name}/' not covered by any system page")

# ---- coverage gap (INFO) ----
covered = set()
for p in pages.values():
    fm = frontmatter(read(p.relative_to(ROOT).as_posix())) or ""
    for g in fm_list(fm, "covers"):
        covered.update(Path(m).resolve() for m in glob(str(ROOT / g), recursive=True))
def git_files(*args):
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", *args],  # -z: NUL-split, no C-quoting
            capture_output=True, text=True, timeout=10,
        )
        return [f for f in out.stdout.split("\0") if f]
    except Exception:
        return []


tracked = git_files() + git_files("--others", "--exclude-standard")
if tracked:
    uncovered = []
    for f in tracked:
        if f.startswith(COVERAGE_EXEMPT) or f.endswith(".gitkeep"):
            continue
        if not (ROOT / f).is_file():
            continue  # still in the index but gone from the worktree
        if (ROOT / f).resolve() not in covered:
            uncovered.append(f)
    for f in uncovered[:20]:
        infos.append(f"uncovered: {f} (no story covers it)")
    if len(uncovered) > 20:
        infos.append(f"uncovered: …and {len(uncovered) - 20} more")
else:  # not a git checkout — fall back to the allowlist probe
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
