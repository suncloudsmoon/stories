---
description: Full cleanup of docs/stories/ — reconcile every page against the code, rewrite stale stories, delete dead canon, rebuild the Atlas and links.
---

Run a full **refresh** of the stories wiki. This is the manual deep-clean. Be thorough and unafraid to delete.

Read the `stories` and `writing-a-story` skills first.

## 1. Take inventory
List every page under `docs/stories/`. Read `index.md` (the Atlas) and `log.md`.

## 2. Reconcile against the code
For each `saga`/`vignette`, check its `covers:` paths still exist and that the story still matches reality:
- code moved/renamed → fix `covers:` and `path:line` citations,
- code deleted → the story is dead canon; **delete the page**,
- soul drifted → rewrite the story to the current truth, to the craft bar.

For each `library` page, check `sources:` and links are still valid.

For each `system` page, walk the code it covers: blocks appeared, vanished, or reshaped → update the page, then re-derive `ARCHITECTURE.md` (diagram, legend, `New since` section — age out entries older than ~14 days). Verify everything in the program is still accounted for — a segment with no block is a gap to fill; if the repo has no systems layer yet, offer to build one, once.

## 3. Prune
Delete orphans and dead canon **confidently** — stale canon is worse than none. Merge duplicates. Only pause to ask if a page might carry standalone value the code doesn't capture (a discretionary MAY-ask). Flag contradictions between pages; resolve the clear ones, surface the rest.

## 4. Repair the graph
- Fix every broken `[[link]]` and `path:line` citation.
- Find code with real soul that has no covering story, and write one.

## 5. Rebuild & log
Regenerate `index.md` from what now exists (systems pages under `## Systems`; every gate-bearing entry lists its `covers:` globs inline). Append `## [<today>] refresh | <summary>` to `log.md`, noting what was rewritten, deleted, and added. If a canon linter is available (`scripts/lint-canon.py`), run it — a refresh is not done while it reports errors. Report the changes in plain terms.
