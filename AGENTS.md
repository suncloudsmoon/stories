# AGENTS.md

Guidance for AI coding agents (Codex and other AGENTS.md-aware tools) working in this repository. Codex auto-loads this at session start. The Claude Code equivalent is `CLAUDE.md`.

## What this repo is

This repo **is** the `stories` plugin — a skill-only plugin that maintains a "soul-bearing wiki" (`docs/stories/`) of a codebase: read the relevant stories before a non-trivial change, rewrite them after. It ships in two homes:

- **Claude Code** plugin at the repo root (`.claude-plugin/`, `skills/`, `commands/`).
- **Codex** plugin bundle in `codex/` (`.codex-plugin/`, `skills/` — the two core skills are symlinks back to the root `skills/`).

The systems layer is the shape-map: `docs/stories/systems/` pages (`kind: system`, gated via `covers:`) plus a model-derived `ARCHITECTURE.md` face at the repo root — spec: `docs/specs/2026-07-01-systems-layer-design.md`.

Design + decisions: `docs/specs/2026-06-14-stories-plugin-design.md` (§9 is the locked-decisions table). Codex porting notes: `docs/stories/library/codex-conventions.md`.

## Honor the stories discipline (dogfood)

`docs/stories/` is this repo's own canon. Before a behavior/structure/soul change, read the covering stories — open `docs/stories/index.md` (the Atlas) and any story whose `covers:` matches the files you'll touch. After the change, update those stories plus the Atlas and `docs/stories/log.md`. The full discipline is the `stories` skill (`skills/stories/SKILL.md`); the craft is `writing-a-story`. Write stories from knowledge — read the code first, never guess.

## Editing the rules — keep them in sync

The behavioral contract — especially the gate-line and its default-exempt list — is stated in **three places**: `skills/stories/SKILL.md`, `README.md`, and the design spec (plus its §9 decision table). Change the behavior ⇒ update all of them. Drift between these is the most likely bug in this repo — the linter diffs the default-exempt list across all three homes (an error, not a warning).

## Keep the two homes in sync

When the Claude Code plugin changes, update the Codex bundle in `codex/` to match (and vice versa). The two core skills are symlinked, so they can't drift. The command procedures (`commands/*.md` ↔ `codex/skills/stories-*/SKILL.md`) and the two manifests (`.claude-plugin/plugin.json` ↔ `codex/.codex-plugin/plugin.json`) are duplicated and MUST be hand-synced. Run `python3 scripts/lint-canon.py` (or `$stories-lint`) to verify the two homes haven't drifted.
