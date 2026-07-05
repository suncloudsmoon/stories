---
description: File a source or research result into docs/stories/library/ — read it, write a page, dedupe, cross-link, update the Atlas and log.
argument-hint: <path | url | topic, or paste the content>
---

Ingest knowledge into the **library** of the stories wiki.

Input: $ARGUMENTS

Read the `stories` and `writing-a-story` skills first.

## 1. Take in the source
Resolve `$ARGUMENTS`:
- a file path → read it,
- a URL → fetch it,
- a topic with no source attached → say so, and offer to run deep research instead,
- pasted content → use it directly.

## 2. Pick the kind
- `source` — a faithful summary of one external source (faithful + tight, no dressing up).
- `research` / `concept` — a synthesis across sources, or a concept page (full soul).
- `reference` — just a pointer: title, link, one line.

## 3. Write the page
Create `docs/stories/library/<slug>.md` to the craft bar for its kind. Frontmatter with `kind`, `sources:`, `links:`, `refreshed:` (today).

## 4. Integrate
- Dedupe/merge against existing library pages — don't create a near-duplicate; extend the existing page instead.
- Cross-link `[[...]]` to related sagas, concepts, and library pages. Add back-links where they help.

## 5. Atlas & log
Add the page to `index.md` under `## Library` with a one-line hook. Append `## [<today>] ingest | <title>` to `log.md`. If a canon linter is available (`scripts/lint-canon.py`), run it and fix what it flags. Report what landed and what it linked to.
