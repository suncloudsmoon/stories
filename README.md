# stories

A Claude Code plugin that maintains a **soul-bearing wiki** of your codebase under `docs/stories/`.

Most docs describe *what* the code does. Stories capture the ***why*** — the tension a decision resolved, the road not taken, what the maker cares about. The model reads the relevant stories before any non-trivial change and rewrites them after, so the canon stays true as the code moves. The same wiki doubles as a general knowledge base for deep-research results, syntheses, and sources — one interlinked graph where research links to the code it shaped.

It's a storytelling take on the LLM-wiki pattern — an LLM-maintained, compounding markdown knowledge base — repointed from "a knowledge base of sources" to "the soul of a codebase."

## How it works

- **Skill-only.** No hooks, no scripts — an always-on skill carries the discipline. Portable, with a Codex port planned.
- **Read-before-change gate.** Before a change that reshapes the repo's behavior, structure, or soul (feature, refactor, interface change, moving/deleting code) the model reads the stories whose `covers:` matches the files in play. Routine bug fixes and cosmetics are exempt — *unless* they're significant enough to change the repository, in which case they're storied too.
- **Low friction.** Reading never interrupts you. The model proceeds on judgment and stops to ask only on a real conflict — or when something genuinely warrants your attention.
- **Auto-author.** After a gated change, the model rewrites the affected stories in the same session.
- **Deep research auto-files.** A deep-research run lands as a `research` page in the library, cross-linked into the graph.

## Layout

```
docs/stories/
  index.md      # the Atlas — read first
  log.md        # the chronicle
  origin.md     # why this project exists, its soul, your preferences as lore
  sagas/        # code subsystem & flow soul
  vignettes/    # optional file-level shorts
  library/      # deep research, syntheses, sources, concepts
```

## Commands

- `/stories-init` — bootstrap `docs/stories/`, interview you, write the origin saga.
- `/stories-refresh` — full cleanup: reconcile against the code, rewrite stale, delete dead canon, rebuild the Atlas.
- `/stories-ingest <source|research>` — file knowledge into the library by hand.

## Coexistence

`stories` lives in its own namespace and its own `docs/` subdir. It works **with or without** superpowers and never replaces it.

## Design

See `docs/specs/2026-06-14-stories-plugin-design.md` for the full design and the decisions behind it.
