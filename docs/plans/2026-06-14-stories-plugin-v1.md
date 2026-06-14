# Stories Plugin v1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v1 of the `stories` Claude Code plugin — a skill-only, soul-bearing wiki for a codebase that doubles as a general knowledge wiki.

**Architecture:** Pure markdown + one JSON manifest. Two skills carry all behavior (no hooks, no scripts): a discipline skill (the contract) and a craft skill (how to write a story). Three slash commands cover bootstrap, refresh, and manual ingest. The repo is the plugin's source and is dogfooded with its own `docs/stories/`.

**Tech Stack:** Claude Code plugin format (`.claude-plugin/plugin.json`, `skills/*/SKILL.md`, `commands/*.md`). No runtime code. Verification = JSON validity + frontmatter/structure assertions via shell.

Spec: `docs/specs/2026-06-14-stories-plugin-design.md`.

**Note on TDD:** This deliverable is prose + config, not executable code — there is nothing to unit-test. Each task's "test" is a concrete structural acceptance check (valid JSON, required frontmatter keys, required sections present), which is the honest analogue here.

---

### Task 1: Plugin manifest

**Files:**
- Create: `.claude-plugin/plugin.json`

- [ ] **Step 1: Write the manifest** — valid JSON with `name`, `version`, `description`, `author`. Description states the dual nature (code-soul + knowledge wiki) and the read-before-change ethos.
- [ ] **Step 2: Verify valid JSON + keys**

Run: `python3 -c "import json;d=json.load(open('.claude-plugin/plugin.json'));assert {'name','version','description'} <= d.keys();print('ok',d['name'])"`
Expected: `ok stories`

- [ ] **Step 3: Commit** (batched with later tasks).

---

### Task 2: Discipline skill (the core)

**Files:**
- Create: `skills/stories/SKILL.md`

Responsibility: the full behavioral contract + the on-disk conventions. This is the heart of the plugin.

Must contain:
- YAML frontmatter: `name: stories`, a `description` that triggers on building/refactoring/interface-change/deleting-code AND on filing research.
- **Philosophy** — story = the *why*, not the *what*; soul; grounded; tight; art.
- **Read gate** — fires before behavior/structure/soul changes; default-exempt (bug fixes, cosmetics, deps, test-only) *unless* significant enough to change the repo; how to find relevant stories (read `index.md`, match `covers:`).
- **Two ask-channels** — MUST ask on conflict; MAY ask at discretion ("would the user want to know?"); else proceed.
- **Auto-author** — after a gated change, update/author affected stories same session.
- **Deep-research auto-ingest** — standing rule: on deep-research completion, file results into `library/`, dedupe/link/log, report, don't ask.
- **Refresh** — what `/stories-refresh` does; delete freely.
- **On-disk structure + frontmatter schema + kinds table** (from spec §4).
- Pointer to `writing-a-story` skill for craft.

- [ ] **Step 1: Write `skills/stories/SKILL.md`.**
- [ ] **Step 2: Verify frontmatter + key sections**

Run: `head -5 skills/stories/SKILL.md | grep -q '^name: stories' && grep -qi 'read gate\|read-before' skills/stories/SKILL.md && grep -qi 'covers:' skills/stories/SKILL.md && grep -qi 'deep.research' skills/stories/SKILL.md && echo ok`
Expected: `ok`

---

### Task 3: Craft skill

**Files:**
- Create: `skills/writing-a-story/SKILL.md`

Responsibility: *how* to write a story to the bar. Must contain frontmatter, the **light spine** (hook → world before → decision & why → what it means → links onward), the quality bar, kind-aware scaling, citation rules (`path:line`, `[[links]]`), myth-sparingly, and **one worked exemplar** story.

- [ ] **Step 1: Write `skills/writing-a-story/SKILL.md`.**
- [ ] **Step 2: Verify**

Run: `head -5 skills/writing-a-story/SKILL.md | grep -q '^name:' && grep -qi 'spine' skills/writing-a-story/SKILL.md && grep -qi 'exemplar\|example' skills/writing-a-story/SKILL.md && echo ok`
Expected: `ok`

---

### Task 4–6: Commands

**Files:**
- Create: `commands/stories-init.md` — bootstrap `docs/stories/` skeleton, interview user, write origin saga, log it.
- Create: `commands/stories-refresh.md` — full cleanup across all kinds; rewrite stale, delete orphans, rebuild Atlas + links, log it.
- Create: `commands/stories-ingest.md` — file a source/research into `library/`: read → write page (pick `kind`) → dedupe/merge → cross-link → update Atlas + log. Takes `$ARGUMENTS`.

Each: YAML frontmatter with `description` (+ `argument-hint` where it takes input).

- [ ] **Step 1: Write all three command files.**
- [ ] **Step 2: Verify each has a description frontmatter**

Run: `for f in commands/stories-init.md commands/stories-refresh.md commands/stories-ingest.md; do grep -q '^description:' "$f" || echo "MISSING $f"; done; echo done`
Expected: `done` (no MISSING lines)

---

### Task 7: README

**Files:**
- Create: `README.md`

Responsibility: what `stories` is, install, the contract in a nutshell, structure, commands, relation to `.ref/llm-wiki.md` and superpowers.

- [ ] **Step 1: Write `README.md`.**
- [ ] **Step 2: Commit** the manifest + skills + commands + README as `feat: stories plugin v1`.

---

### Task 8: Dogfood — this repo's own canon

**Files:**
- Create: `docs/stories/index.md`, `docs/stories/log.md`, `docs/stories/origin.md`, dirs `sagas/`, `vignettes/`, `library/` (with `.gitkeep`).

Responsibility: prove the plugin on itself. `origin.md` is a real, crafted origin saga for the `stories` plugin, grounded in the user's brief (the soul is user-sourced). Atlas lists it; log records the bootstrap.

- [ ] **Step 1: Create the skeleton + write a real `origin.md` to the craft bar.**
- [ ] **Step 2: Verify structure**

Run: `test -f docs/stories/index.md && test -f docs/stories/origin.md && head -3 docs/stories/origin.md | grep -q '^---' && echo ok`
Expected: `ok`

- [ ] **Step 3: Commit** as `docs: dogfood stories canon for this repo`.

---

## Self-Review

- **Spec coverage:** manifest (§7) → T1; discipline contract (§3) + structure (§4) → T2; craft (§5) → T3; commands (§6) → T4–6; packaging/README (§7) → T7; dogfood (§7) → T8. v1 scope (§8) fully covered. `/stories-ask` correctly deferred (not a task). ✔
- **Placeholders:** none — each task names exact files, responsibilities, and a runnable acceptance check. Prose content is authored at execution (duplicating final skill prose into the plan would be waste).
- **Consistency:** file paths, `kind`/`covers`/`[[links]]` naming match the spec throughout. ✔
