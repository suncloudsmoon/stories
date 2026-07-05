---
name: stories-ingest
description: File a source or research result into the stories library (docs/stories/library/) — read it, write a page, dedupe, cross-link, update the Atlas and log. Use when the user wants to file a source, knowledge, or research. Invoke with $stories-ingest and name the source in your message.
---

Ingest knowledge into the **library** of the stories wiki. (Mirrors the Claude Code `/stories-ingest` command — keep the two in sync.) Codex skills take no `$ARGUMENTS` placeholder — read the source the user names in their message. Read the `stories` and `writing-a-story` skills first.

1. **Take in the source.** From the user's message: a file path → read it; a URL → fetch it; a topic with no source attached → say so and offer to run deep research; pasted content → use it directly.
2. **Pick the kind.** `source` (a faithful summary of one source — faithful + tight, no dressing up); `research`/`concept` (a synthesis or concept page — full soul); `reference` (just a pointer: title, link, one line).
3. **Write the page** at `docs/stories/library/<slug>.md` to the craft bar for its kind; frontmatter with `kind`, `sources:`, `links:`, `refreshed:` (today).
4. **Integrate.** Dedupe/merge against existing library pages — extend, don't duplicate; cross-link `[[...]]` to related sagas, concepts, and library pages.
5. **Atlas & log.** Add the page to `index.md` under `## Library`; append `## [<today>] ingest | <title>` to `log.md`; if a canon linter is available (`scripts/lint-canon.py`), run it and fix what it flags; report what landed and what it linked to.
