---
name: stories-refresh
description: Use when the user asks to refresh, clean up, or health-check the stories wiki (Claude Code /stories:stories-refresh, Codex $stories-refresh) — reconciles stale stories with the code, prunes dead pages, and rebuilds the Atlas and ARCHITECTURE.md.
---

# Refresh the stories wiki

Read the `stories` skill and its `writing.md` first. Be thorough and unafraid to delete: stale canon is worse than none.

1. **Find what moved.** A story is stale when a file it covers was committed after its `refreshed:` date — `git log -1 --format=%cs -- <covered paths>`. If the repo has `scripts/lint-canon.py`, its REVIEW lines are this list. Without git, every story is stale.
2. **Reconcile only the stale stories.** Re-read their code. Rewrite what drifted, confirm what still holds, delete a story whose code is gone — and set `refreshed:` to today on each one you checked.
3. **Check every page mechanically** — by grep or the linter, never by re-reading code: `covers:` globs match files, anchors resolve, `[[links]]` point at pages, every page has an Atlas line. Turn any line-number citation into an anchor and any multi-line `covers:` into one line.
4. **Prune.** Delete orphans and dead pages; merge duplicates. Resolve clear contradictions between pages and bring the rest to the user.
5. **Rebuild and report.** Rewrite `index.md` from what exists, update `ARCHITECTURE.md` if the shape moved, run the linter until it is clean, and report what you rewrote, deleted, and added — in plain words.
