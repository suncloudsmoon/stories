# AGENTS.md

Guidance for AI coding agents working in this repository — Codex reads this file directly; Claude Code reads it through `CLAUDE.md`.

## What this repo is

This repo **is** the `stories` plugin: it keeps a wiki of a codebase's *why* in `docs/stories/`. A hook names the story that covers a file before the model changes it; the model rewrites the story after. There is no application code — the deliverable is three skills, one hook, and two manifests.

- `skills/stories/SKILL.md` — the discipline: the canon, the before/after procedure, anchors, filing knowledge. The rules live here and nowhere else.
- `skills/stories/writing.md` — the craft, loaded only when a page is written; also the `ARCHITECTURE.md` format.
- `skills/stories-init/`, `skills/stories-refresh/` — the two procedures (`/stories:stories-init` · `$stories-init`, and so on).
- `hooks/stories.py` + `hooks/hooks.json` — the gate: names the covering story on Read, holds back an unannounced edit once, reminds once at Stop. Python 3.9+ stdlib; fails open.
- `scripts/lint-canon.py` — dev/CI health-check. Not shipped behavior.

Design and evidence: `docs/specs/2026-10-29-stories-2-simplify-design.md`.

## One fact, one place

The principle behind the 2.0 design: every fact lives in exactly one place. Before adding a field, a file, or a restated rule, find where that fact already lives and point there instead.

## Two homes, one copy

The Codex bundle in `codex/` is symlinks to the root (`skills/*`, `hooks/`) plus its own manifest. Only the two manifests (`.claude-plugin/plugin.json` ↔ `codex/.codex-plugin/plugin.json`) are kept by hand; the linter checks them and the symlinks. A new skill needs a matching symlink in `codex/skills/`.

## Dogfood — this repo is under its own discipline

`docs/stories/` is this repo's own canon. When the hook names a story, read it before changing the file. After a change, rewrite any story whose why shifted (and its `refreshed:`), update `ARCHITECTURE.md` if the shape moved, and keep `docs/stories/index.md` current. Cite code as `path#anchor`, never `path:line`.

## Validate

No build. Run before every commit (CI runs the same):

```bash
python3 hooks/stories.py --self-test
python3 scripts/lint-canon.py --self-test
python3 scripts/lint-canon.py
```
