---
name: stories-lint
description: Health-check the stories canon (read-only) — run the linter, add judgment, report drift/staleness, and route fixes to refresh. Use when the user wants to check canon health or detect drift. Invoke with $stories-lint.
---

Diagnose the health of the stories wiki. Read-only — diagnose, don't rewrite (that's `$stories-refresh`). (Mirrors the Claude Code `/stories-lint` command — keep the two in sync.)

1. **Run the engine.** Run `python3 scripts/lint-canon.py` — it checks broken `[[links]]`, dead `covers:` and `path:line` citations, manifest drift, command drift (Claude Code ↔ Codex), staleness (git), coverage gaps, and the systems layer (ARCHITECTURE.md ↔ systems pages ↔ legend, top-level coverage). It exits non-zero on errors.
2. **Read what it flagged.** Open each named page or file; the engine is mechanical, so confirm a finding is real before acting on it.
3. **Judge what it can't.** Add the semantic checks regex cannot make: do two pages contradict in meaning? is a "stale" story actually wrong, or just date-lagged? does a coverage gap name code with real soul?
4. **Report & route.** Present a prioritized summary (errors → warnings → info). Fix trivially-clear items; hand rewrites to `$stories-refresh`. Never rewrite canon here.
