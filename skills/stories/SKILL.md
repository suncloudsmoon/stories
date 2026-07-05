---
name: stories
description: Use when working in a repo that HAS a docs/stories/ wiki — BEFORE any behavior/structure/soul change (new feature, refactor, interface/API change, moving or deleting code) read the covering stories, and AFTER such a change rewrite them. Also when filing deep-research results, sources, or knowledge, and when creating or updating the shape-map (ARCHITECTURE.md / docs/stories/systems/). Establishes the read-before-change gate, the conflict-only ask rule, auto-authoring, the systems layer, and the soul-bearing canon conventions. If the repo has no docs/stories/, stay dormant — suggest stories-init at most once, never force it.
---

# Stories — the soul of this codebase

A **story** captures the *why* of code, not the *what*. The code already says what it does; a story says why it exists, what tension it resolved, what roads were not taken, and what the maker cares about. Stories live in `docs/stories/` and you — the model — own them. You read them before you change things, and you rewrite them after.

The same wiki also holds **knowledge**: deep-research results, syntheses, sources, concepts. One interlinked graph. A `kind:` field decides how each page behaves.

> Craft matters. When you write or rewrite any page, follow the **`writing-a-story`** skill. A story is a work of art, not a changelog.

## Dormant by default

This discipline is **opt-in per repo.** If `docs/stories/` exists, honor it fully — the read-gate, auto-authoring, and the rules below. If it does **not** exist, stay dormant: do the user's work normally, and at most **suggest** `stories-init` once, when a project would clearly benefit. Never nag, and never scaffold a wiki the user did not ask for.

## The canon on disk

```
docs/stories/
  index.md      # the Atlas — every page, one-line hook (+ covers: globs on gate-bearing pages), grouped by kind. Read FIRST.
  log.md        # the chronicle — append-only "## [YYYY-MM-DD] <type> | <title>"
  origin.md     # the origin saga — why this project exists, its soul, the maker's preferences as lore
  sagas/        # code subsystem & flow soul (cross-file)
  vignettes/    # optional file-level shorts
  systems/      # the shape-map — one block-diagram page per segment (kind: system)
  library/      # knowledge: research, syntheses, sources, concepts
```

Plus one artifact **outside** the wiki: `ARCHITECTURE.md` at the repo root — the shape-map's human face, derived from the `systems/` pages (see *The systems layer* below).

When the user wants a wiki, run **stories-init** (Claude Code `/stories-init`, Codex `$stories-init`) to create the structure — never scaffold it ad hoc. If `docs/stories/` is absent and the user has not asked, stay dormant (see above).

### Frontmatter (every page)

```yaml
---
title:     <string>
kind:      origin | saga | vignette | system | research | concept | source | reference
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
| `system` | init, refresh, or a structural change (auto) | **YES** (`covers:`) | legible + complete (shape, not soul) |
| `research`, `concept` | ingest / query | no | full soul (synthesis) |
| `source` | ingest | no | faithful + tight |
| `reference` | manual | no | pointer only |

## The systems layer — the shape-map

Stories carry the *why*; **system pages** carry the *shape*: block-diagram maps of how the app is put together — exhaustive where stories are curated. Everything in the program is accounted for by some block. Two artifacts:

- **`docs/stories/systems/<segment>.md` — source of truth.** One page per top-level block; you choose the segmentation (frontend/backend, pipeline stages, packages — whatever the repo's true shape is). Body: plain-language lead (one breath) → a segment-level Mermaid diagram if inner structure earns one → the parts and what each does, cited `path:line` → boundaries (what it exposes, what it must not know) → `[[links]]` to the sagas carrying its why. Block granularity always — the moment a page reads like a directory listing it has failed its bar.
- **`ARCHITECTURE.md` at the repo root — the face,** derived by you from the systems pages (never a script). Contents in order: one plain-language paragraph on what the app is (the top level stays jargon-free; technicals live one link down); the top-level Mermaid `flowchart` (node id = page slug with `-`→`_`); a **legend table** — block → one-line plain description → link to its systems page (the legend is the guaranteed "click"; also emit Mermaid `click <id> "<path>"` directives — a bonus some renderers strip); a `## New since <YYYY-MM-DD>` section naming recently added/reshaped blocks, styled `classDef new` in the diagram and aged out at refresh once older than ~14 days (dates from `log.md`); and the footer marker `<!-- derived by the stories plugin — source of truth: docs/stories/systems/ -->`.

Rules: **never overwrite** a hand-written `ARCHITECTURE.md` that lacks the marker — that is a conflict, surface it. A tiny repo may carry the whole map in the root file and grow `systems/` pages only when a segment earns one. Structural change ⇒ update the affected system pages in the same session, and re-derive the root file when the top-level picture moves.

## The gate — read before you change

Before a change that reshapes the repo's **behavior, structure, or soul**, read the relevant stories first:
new feature · refactor · interface/API change · moving or deleting code · anything that changes how the system behaves or is shaped.

**Default-exempt** (usually just go): bug fixes, typos, formatting, comments, dependency bumps, test-only edits.

**Significance overrides the category.** A "bug fix" that changes behavior, or a cleanup big enough to reshape the repo, is gated and storied like any other change. The test isn't the label you'd put on the change — it's: *does this alter the soul or the shape of things?* If yes, it counts.

**How to find the relevant stories:** read `index.md` — the Atlas lists each gate-bearing page's `covers:` globs inline, so one read tells you which pages match the paths you are about to touch. Open every page that matches. That index-plus-`covers` lookup *is* the gate. Reading never interrupts the user — it is silent preparation.

## When to ask (two channels)

- **MUST ask** — a real conflict: the request contradicts a story, or two stories contradict each other. Stop, surface it, get the user's call.
- **MAY ask (your discretion)** — anything worth the user's attention: a consequential fork, a soul-level ambiguity, something surprising. Bar: *"would the user want to have known?"* — not *"am I slightly unsure?"*
- **Otherwise** — proceed on best judgment. Doubt does not stop you; conflict does.

## After the change — author the canon (auto)

A gated change is not done until the canon reflects it. In the **same session, as part of the work** (no separate prompt):

- update every story whose soul shifted, and every system page whose shape shifted (re-derive `ARCHITECTURE.md` when the top-level picture moved),
- write a new saga (or vignette) if you introduced new soul,
- update `index.md` (keep each entry's inline `covers:` true to its page) and append to `log.md`,
- fix any `[[links]]` you broke,
- **close the loop:** if the repo carries a canon linter (e.g. `scripts/lint-canon.py`), run it and fix what it flags — a gated change is not done while the canon lints dirty.

Author per the **`writing-a-story`** skill — which means **reading the changed code and the related stories first**, then writing from knowledge, never a guess.

## Deep research → auto-file (standing rule)

When a deep-research run completes, **file its results into `library/` automatically** — no asking:

- write a `research` page (per `writing-a-story`),
- dedupe/merge against existing library pages; cross-link to related sagas and concepts,
- update `index.md`, append to `log.md`,
- report what landed.

The discretionary-ask channel still applies if the findings conflict with existing canon.

## Refresh & ingest

Invoke by name — Claude Code: `/stories-refresh`; Codex: `$stories-refresh`.

- **stories-refresh** — full cleanup across all kinds. Reconcile every page against the code, rewrite stale stories, **delete dead canon and orphans without hesitation**, rebuild the Atlas and the links.
- **stories-ingest** `<source|research>` — file knowledge into `library/` by hand.

## Prime directives

1. **Soul over facts.** Capture the why. The code already holds the what.
2. **Read before you reshape.** A behavior/structure change ⇒ read the covering stories first.
3. **Leave the canon true.** Every gated change updates the stories in the same breath.
4. **Delete without fear.** Stale canon is worse than no canon. Refresh prunes hard.
5. **Conflict stops you; doubt does not.** Ask on conflict or when it truly matters; otherwise move.
