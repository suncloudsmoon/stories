---
title: The Lint — Making Drift Visible
kind: saga
covers: ["scripts/lint-canon.py", "commands/stories-lint.md"]
links: ["[[origin]]", "[[the-gate]]", "[[codex-port]]"]
refreshed: 2026-07-01
---

# The Lint — Making Drift Visible

**The hook.** A skill-only discipline ([[the-gate]]) has exactly one failure mode: it is best-effort, so the canon can quietly fall behind the code and no one notices. Lint is the canary — it makes that drift *visible* without pretending to prevent it.

**The world before.** Refresh already rewrites stale canon, but refresh is heavy and you run it deliberately. Between refreshes nothing told you a story had gone stale, a `covers:` had gone dead, or — once Codex arrived ([[codex-port]]) — that the two homes had drifted apart. A trust-based system that can rot silently fails in the worst way: invisibly.

**The decision.** Split diagnosis from treatment. `scripts/lint-canon.py` is a read-only mechanical pass: broken `[[links]]`, dead `covers:` and `path:line` citations, manifest drift between the two `plugin.json`, **command drift** (each Claude Code command vs its Codex skill, compared by step structure — the sync rule from [[codex-port]] made mechanical), staleness (a covered file's git commit newer than the story's `refreshed:` date), coverage gaps, and the systems layer (BLOCK_DIAGRAM.md ↔ systems pages ↔ legend). It exits non-zero on errors so CI can hold the line. `/stories-lint` wraps it with the judgment regex can't have — *is this contradiction real? does this gap deserve a story?* — and routes rewrites to refresh. **Lint diagnoses; refresh treats.**

**What it means.** This is the one script in a deliberately script-free system — and it earns the exception by being *tooling, not runtime*. The portable skill-only discipline ([[the-gate]]) still ships untouched; lint is a dev/CI aid for keeping the canon honest, never part of what travels to users. It runs on any repo with a `docs/stories/` (pass the path as an argument); the plugin-only checks — manifest and command drift — skip themselves when those files are absent, so a consumer's wiki lints just as well as this one. The standing test: if lint ever passes while the canon is plainly wrong, a check is too weak — add one. Drift you can see is drift you can fix.

See [[the-gate]] for the failure mode it guards, [[codex-port]] for the sync it enforces.
