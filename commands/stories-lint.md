---
description: Health-check the stories canon (read-only) — run the linter, add judgment, report drift/staleness, and route fixes to refresh.
---

Diagnose the health of the stories wiki. Read-only — diagnose, don't rewrite (that's `/stories-refresh`).

## 1. Run the engine
Run `python3 scripts/lint-canon.py`. It checks broken `[[links]]`, dead `covers:` and `path:line` citations, manifest drift, command drift (Claude Code ↔ Codex), staleness (git), and coverage gaps. It exits non-zero on errors.

## 2. Read what it flagged
Open each named page or file. The engine is mechanical — confirm a finding is real before acting on it.

## 3. Judge what it can't
Add the semantic checks regex cannot make: do two pages contradict in meaning? is a "stale" story actually wrong, or just date-lagged? does a coverage gap name code with real soul that deserves a story?

## 4. Report & route
Present a prioritized summary (errors → warnings → info). Fix the trivially-clear items (dead links, dead citations, a stale date); for anything needing a rewrite, hand off to `/stories-refresh`. Never rewrite canon here.
