# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo **is** the `stories` Claude Code plugin — a skill-only plugin that maintains a "soul-bearing wiki" (`docs/stories/`) of a codebase: the model reads the relevant stories before a non-trivial change and rewrites them after. There is no application code; the deliverable is markdown skills + slash commands + one JSON manifest. It ships in **two homes** — the Claude Code plugin at the repo root (`.claude-plugin/`, `skills/`, `commands/`) and a Codex plugin bundle in `codex/` (`.codex-plugin/`, with the two core skills symlinked back to the root `skills/`).

Design and the reasoning behind every decision: `docs/specs/2026-06-14-stories-plugin-design.md` (§9 is the locked-decisions table — treat it as the source of truth). Build plan: `docs/plans/2026-06-14-stories-plugin-v1.md`.

## Dogfooding — you are under the plugin's own discipline

`docs/stories/` is this repo's own canon (`origin.md` = why the project exists; `sagas/the-gate.md` = why it's skill-only). Per the plugin's own rules: **before a behavior/structure/soul change to the plugin, read the covering stories; after, update them plus the Atlas (`index.md`) and log (`log.md`).** Not ceremony — the product proving itself on itself.

## Architecture

- `skills/stories/SKILL.md` — the **discipline**: the read-before-change gate, the conflict-only ask rule, auto-authoring, deep-research auto-ingest, and the on-disk canon conventions (frontmatter + `kind` table). The heart of the plugin.
- `skills/writing-a-story/SKILL.md` — the **craft**: the light spine + quality bar for writing a story, with a worked exemplar.
- `commands/stories-{init,refresh,ingest}.md` — the slash commands (bootstrap / full cleanup / manual knowledge ingest).
- `.claude-plugin/plugin.json` — the manifest.

The gate is armed by **data, not interception**: each story's `covers:` frontmatter plus the Atlas let the model find which stories cover the files it's about to touch. No hooks. Keep `covers:` accurate or the gate goes blind.

## The defining invariant: skill-only, portable

The decision that shapes everything is **no hooks, no scripts** — the discipline is best-effort skill prose so it ports to Codex later (`sagas/the-gate.md` explains the trade-off). Don't add hooks to "enforce" behavior without revisiting that decision; it costs the Codex port. The one sanctioned exception on the shelf is a single optional hook for deep-research auto-filing.

## Two homes — keep Codex in sync

The Codex bundle in `codex/` mirrors the Claude Code plugin. **When you change the CC plugin, update `codex/` to match.** The two core skills (`stories`, `writing-a-story`) are symlinked there, so they can't drift — but the command procedures (`commands/*.md` ↔ `codex/skills/stories-*/SKILL.md`) and the two manifests (`.claude-plugin/plugin.json` ↔ `codex/.codex-plugin/plugin.json`) are duplicated and must be hand-synced. `python3 scripts/lint-canon.py` checks both mechanically. `AGENTS.md` is the Codex sibling of this file — keep the two aligned. Codex porting notes live in `docs/stories/library/codex-conventions.md`.

## Editing the rules — keep them in sync

The behavioral contract — especially the gate-line and its default-exempt list — is stated in **three places**: `skills/stories/SKILL.md`, `README.md`, and the spec (plus the spec's §9 decision table). Change the behavior ⇒ update all of them. Drift between these is the most likely bug in this repo.

## Validate

No build, no test framework. Sanity checks:
- `python3 scripts/lint-canon.py` — full canon health-check (links, covers, citations, manifest + command drift, git-staleness, coverage); exits nonzero on errors. Run before commits / in CI. `/stories-lint` adds model judgment on top.
- `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"` — manifest parses.
- Skills and commands are markdown with YAML frontmatter (`name`/`description`); the frontmatter block must be the first thing in the file.
