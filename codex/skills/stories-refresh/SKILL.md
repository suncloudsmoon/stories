---
name: stories-refresh
description: Full cleanup of the stories wiki (docs/stories/) — reconcile every page against the code, rewrite stale stories, delete dead canon, rebuild the Atlas and links. Use when the user asks to refresh or clean up stories. Invoke with $stories-refresh.
---

Run a full **refresh** of the stories wiki — the manual deep-clean. Be thorough and unafraid to delete. (Mirrors the Claude Code `/stories-refresh` command — keep the two in sync.) Read the `stories` and `writing-a-story` skills first.

1. **Take inventory.** List every page under `docs/stories/`; read `index.md` (the Atlas) and `log.md`.
2. **Reconcile against the code.** For each `saga`/`vignette`: code moved/renamed → fix `covers:` and `path:line`; code deleted → delete the page (dead canon); soul drifted → rewrite to the current truth, to the craft bar. For `library` pages: check `sources:` and links still hold. For `system` pages: blocks appeared/vanished/reshaped → update the page and re-derive `ARCHITECTURE.md` (age out `New since` entries older than ~14 days); everything accounted for — no systems layer yet → offer to build one, once.
3. **Prune.** Delete orphans and dead canon confidently — stale canon is worse than none. Merge duplicates. Only pause to ask if a page might carry standalone value the code doesn't capture. Flag contradictions; resolve the clear ones, surface the rest.
4. **Repair the graph.** Fix every broken `[[link]]` and citation; write a story for any code with real soul that lacks one.
5. **Rebuild & log.** Regenerate `index.md` (systems pages under `## Systems`; every gate-bearing entry lists its `covers:` globs inline); append `## [<today>] refresh | <summary>` to `log.md`; if a canon linter is available (`scripts/lint-canon.py`), run it — a refresh is not done while it reports errors; report the changes in plain terms.
