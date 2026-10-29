---
name: stories
description: Use in a repo that has a docs/stories/ wiki — before changing code a story covers (or when a hook names a story), after such a change, when filing research or a source to keep, and when updating ARCHITECTURE.md. Without docs/stories/, stay dormant.
---

# Stories — the why of this codebase

A **story** says *why* code is the way it is: the tension it resolved, the road not taken, what would betray it. The code already says *what*. Stories live in `docs/stories/`, and you keep them true.

**Dormant by default.** No `docs/stories/` in the repo? Work normally. Suggest `stories-init` at most once; never scaffold a wiki nobody asked for.

## The canon

```
ARCHITECTURE.md      # the shape: summary, diagram, block table, invariants
docs/stories/
  index.md           # the Atlas — one line per page:  - [[name]] — hook
  origin.md          # why the project exists; the maker's preferences
  sagas/             # stories about code
  library/           # knowledge: research, sources, concepts
```

A page with `covers:` is a story about code — and only such a page gates changes:

```yaml
---
covers: ["src/auth/**", "src/session.ts"]   # on one line
refreshed: 2026-10-29                        # last verified against the code
---
# Why tokens rotate
```

Library pages may carry `sources: [...]`. The title is the H1; links are `[[page-name]]` in the text. Nothing else goes in frontmatter.

## Before you change code

1. **Read the story first.** The plugin's hook names the story covering a file when you read or edit it. Read that story before you change the file. (No hook message? `grep -rn "^covers:" docs/stories` lists every story's globs.)
2. **Conflict stops you; doubt does not.** If the request contradicts a story, or two stories contradict each other, stop and ask the user. Otherwise proceed, asking only when something truly deserves their attention.

## After you change code

In the same session, as part of the work:

1. **The why changed** → rewrite the story and set `refreshed:` to today. New code with a why worth keeping → write a new saga.
2. **A block was added, removed, or rewired** → update `ARCHITECTURE.md`.
3. **A page was added, removed, or renamed** → update its line in `index.md`.
4. **The repo has `scripts/lint-canon.py`** → run it and fix what it flags.

If the why did not change, you are done — say so in one line.

Before writing or rewriting any page, read [writing.md](writing.md): the craft.

## Citations are anchors

Cite code as `` `path#anchor` ``, where the anchor is text that appears verbatim in that file — a function, a constant, a heading, a key. Find it with `grep -n`. Never cite line numbers: they break on every edit above them, while an anchor breaks only when the thing it names is renamed or deleted — exactly when the story needs a look. Checking citations is a grep or the linter, never a file read and never a subagent.

## Filing knowledge

When deep research finishes, or the user hands you a source to keep, write a `library/` page (see `writing.md`) and add its Atlas line. No asking.

## Upkeep

`stories-refresh` — `/stories:stories-refresh` in Claude Code, `$stories-refresh` in Codex — reconciles the whole wiki: stale stories, dead pages, the Atlas, the map.
