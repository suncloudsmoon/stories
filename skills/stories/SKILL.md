---
name: stories
description: Use whenever working in a repo that has (or should have) a docs/stories/ wiki — BEFORE any behavior-or-structure change (new feature, refactor, interface/API change, moving or deleting code) read the relevant stories, and AFTER such a change rewrite them. Also when filing deep-research results, sources, or knowledge. Establishes the read-before-change gate, the conflict-only ask rule, auto-authoring, and the soul-bearing canon conventions.
---

# Stories — the soul of this codebase

A **story** captures the *why* of code, not the *what*. The code already says what it does; a story says why it exists, what tension it resolved, what roads were not taken, and what the maker cares about. Stories live in `docs/stories/` and you — the model — own them. You read them before you change things, and you rewrite them after.

The same wiki also holds **knowledge**: deep-research results, syntheses, sources, concepts. One interlinked graph. A `kind:` field decides how each page behaves.

> Craft matters. When you write or rewrite any page, follow the **`writing-a-story`** skill. A story is a work of art, not a changelog.

## The canon on disk

```
docs/stories/
  index.md      # the Atlas — every page, one-line hook, grouped by kind. Read FIRST.
  log.md        # the chronicle — append-only "## [YYYY-MM-DD] <type> | <title>"
  origin.md     # the origin saga — why this project exists, its soul, the maker's preferences as lore
  sagas/        # code subsystem & flow soul (cross-file)
  vignettes/    # optional file-level shorts
  library/      # knowledge: research, syntheses, sources, concepts
```

If `docs/stories/` does not exist yet, run `/stories-init` — do not scaffold it ad hoc.

### Frontmatter (every page)

```yaml
---
title:     <string>
kind:      origin | saga | vignette | research | concept | source | reference
covers:    ["<glob>", ...]      # CODE kinds only — this is what arms the gate
sources:   ["<url|path>", ...]  # KNOWLEDGE kinds only — provenance
links:     ["[[other-page]]"]
refreshed: YYYY-MM-DD
---
```

Cross-link pages with `[[page-name]]`. Cite code as `path:line`.

### Kinds

| kind | born when | gates code? | craft bar |
|---|---|---|---|
| `origin` | `/stories-init`, refresh | — | full soul |
| `saga`, `vignette` | a code change (auto) | **YES** (`covers:`) | full soul |
| `research`, `concept` | ingest / query | no | full soul (synthesis) |
| `source` | ingest | no | faithful + tight |
| `reference` | manual | no | pointer only |

## The gate — read before you change

Before a change that reshapes the repo's **behavior, structure, or soul**, read the relevant stories first:
new feature · refactor · interface/API change · moving or deleting code · anything that changes how the system behaves or is shaped.

**Default-exempt** (usually just go): bug fixes, typos, formatting, comments, dependency bumps, test-only edits.

**Significance overrides the category.** A "bug fix" that changes behavior, or a cleanup big enough to reshape the repo, is gated and storied like any other change. The test isn't the label you'd put on the change — it's: *does this alter the soul or the shape of things?* If yes, it counts.

**How to find the relevant stories:** read `index.md`, then open every page whose `covers:` matches the paths you are about to touch. That index-plus-`covers` lookup *is* the gate. Reading never interrupts the user — it is silent preparation.

## When to ask (two channels)

- **MUST ask** — a real conflict: the request contradicts a story, or two stories contradict each other. Stop, surface it, get the user's call.
- **MAY ask (your discretion)** — anything worth the user's attention: a consequential fork, a soul-level ambiguity, something surprising. Bar: *"would the user want to have known?"* — not *"am I slightly unsure?"*
- **Otherwise** — proceed on best judgment. Doubt does not stop you; conflict does.

## After the change — author the canon (auto)

A gated change is not done until the canon reflects it. In the **same session, as part of the work** (no separate prompt):

- update every story whose soul shifted,
- write a new saga (or vignette) if you introduced new soul,
- update `index.md` and append to `log.md`,
- fix any `[[links]]` you broke.

Author per the **`writing-a-story`** skill — which means **reading the changed code and the related stories first**, then writing from knowledge, never a guess.

## Deep research → auto-file (standing rule)

When a deep-research run completes, **file its results into `library/` automatically** — no asking:

- write a `research` page (per `writing-a-story`),
- dedupe/merge against existing library pages; cross-link to related sagas and concepts,
- update `index.md`, append to `log.md`,
- report what landed.

The discretionary-ask channel still applies if the findings conflict with existing canon.

## Refresh & ingest

- `/stories-refresh` — full cleanup across all kinds. Reconcile every page against the code, rewrite stale stories, **delete dead canon and orphans without hesitation**, rebuild the Atlas and the links.
- `/stories-ingest <source|research>` — file knowledge into `library/` by hand.

## Prime directives

1. **Soul over facts.** Capture the why. The code already holds the what.
2. **Read before you reshape.** A behavior/structure change ⇒ read the covering stories first.
3. **Leave the canon true.** Every gated change updates the stories in the same breath.
4. **Delete without fear.** Stale canon is worse than no canon. Refresh prunes hard.
5. **Conflict stops you; doubt does not.** Ask on conflict or when it truly matters; otherwise move.
