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

## 3. Prune
Delete orphans and dead canon **confidently** — stale canon is worse than none. Merge duplicates. Only pause to ask if a page might carry standalone value the code doesn't capture (a discretionary MAY-ask). Flag contradictions between pages; resolve the clear ones, surface the rest.

## 4. Repair the graph
- Fix every broken `[[link]]` and `path:line` citation.
- Find code with real soul that has no covering story, and write one.

## 5. Rebuild & log
Regenerate `index.md` from what now exists. Append `## [<today>] refresh | <summary>` to `log.md`, noting what was rewritten, deleted, and added. Report the changes in plain terms.
