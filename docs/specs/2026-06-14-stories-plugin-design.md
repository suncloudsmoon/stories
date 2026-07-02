# Design Spec — the `stories` plugin

**Date:** 2026-06-14
**Status:** Draft, pending user review
**Reference:** `.ref/llm-wiki.md` (Karpathy's LLM-wiki pattern — the ancestor of this idea)

---

## 1. Vision

A Claude Code plugin (Codex port later) that maintains a **soul-bearing wiki** of a project under `docs/stories/`. It carries two natures in **one interlinked graph**:

1. **Code-soul** — narrative *stories* that convey the *why* of the code: intent, tensions, roads not taken, and the maker's preferences rendered as lore. The model reads the relevant stories before any non-trivial change and updates them after.
2. **Knowledge** — a general LLM-wiki (the `.ref/llm-wiki.md` pattern) for deep-research results, syntheses, sources, and concept pages.

The unifying idea: **everything is a soul-bearing page.** A research page is simply a story about what you *learned* instead of about *code*. A `kind:` field decides each page's behavior. Because both natures live in the same graph, research can link directly to the code it shaped, and code-soul can cite the research that justified it.

This is the LLM-wiki engine, repointed from "a knowledge base of external sources" to "the soul of a codebase, plus the knowledge that surrounds it."

## 2. Soul / philosophy

A **story** is not documentation of *what* the code does — the code already says what. A story carries the **why**: the decision, the tension it resolved, the alternatives rejected, the values underneath. It is:

- **grounded** — rooted in real code and real decisions; cites `path:line`. Myth is allowed but rare — illustration, never filler.
- **deep** — it explains the *why* and the tradeoffs, not the surface.
- **tight** — no verbosity; every line earns its place.
- **engaging + logical** — cause→effect narrative, not a bullet dump.
- **a work of art** — real effort goes into each one.

The craft bar **scales by kind**: raw source notes stay faithful and dense (no forced artistry — that would betray the source); syntheses and code-soul stories get the full treatment.

## 3. Behavioral contract

The heart of the plugin. Carried entirely by an always-on skill (no hooks, no scripts).

### 3.1 Read gate
Before a change that reshapes the repo's **behavior, structure, or soul** — a new feature, a refactor, an interface/API change, moving or deleting code — the model reads the relevant stories first.

- **Default-exempt:** bug fixes, typos, formatting, comments, dependency bumps, test-only edits — *unless* the change is significant enough to change the repository, in which case it gates and gets storied like any other change. Significance overrides the category; the test is "does this alter the soul or shape of things?", not the label.
- **How relevant stories are found:** the model reads `index.md` (the Atlas), then matches the target paths against each story's `covers:` frontmatter. This index-plus-`covers` lookup *is* the gate — pure markdown, no hooks required.

### 3.2 Friction — two ask-channels
- **MUST ask** — on a real conflict: the request contradicts a story, or two stories contradict each other.
- **MAY ask (discretion)** — anything the model judges worth the user's attention: a consequential fork, a soul-level ambiguity, something surprising. Bar: *"would the user want to have known?"* — not *"am I slightly unsure?"*
- **Otherwise** — proceed on best judgment. Reading stories never interrupts the user.

### 3.3 Write side (auto)
After a gated change lands, the model updates or authors the affected stories **in the same session, as part of the work** — no separate prompt. Authoring first reads the changed code and related stories (see §5) — write from knowledge, not a guess. New soul (a new subsystem) earns a new saga or vignette; the Atlas and log are updated.

### 3.4 Deep-research auto-ingest
When a `deep-research` run completes, the model **automatically** files the results into `library/` as a `research` page — dedupe/merge against existing pages, cross-link to related sagas and concepts, update Atlas + log, then report what landed. No permission prompt (the discretionary-ask channel still applies on conflict).

- This is a **standing rule** in the discipline skill, not a hook. The model knows it just ran the research (in-session), so the rule fires reliably.
- An optional single CC-specific hook could make this a *hard* guarantee, but it breaks the Codex port. **Default: off.** Revisit only if best-effort proves insufficient.

### 3.5 Refresh (manual)
`/stories-refresh` performs a full cleanup across **all** kinds: reconcile every page against the code, rewrite stale stories, **delete dead canon and orphans freely**, fix broken `[[links]]`, rebuild the Atlas. Aggressive by design — unafraid to delete.

## 4. On-disk structure — `docs/stories/`

Coexists with `docs/superpowers/`; never touches it.

```
docs/stories/
  index.md      # the Atlas — every page, one-line hook, grouped by kind/layer. Read first.
  log.md        # the chronicle — append-only "## [YYYY-MM-DD] <type> | <title>" (grep-able)
  origin.md     # the origin saga — why this project exists, its soul, the maker's preferences as lore
  sagas/        # code subsystem & flow soul (cross-file): auth.md, render-pipeline.md, ...
  vignettes/    # optional file-level shorts, only where one file has real soul: parser.md
  library/      # knowledge realm: deep research, syntheses, sources, concepts
```

### 4.1 Frontmatter schema
```yaml
---
title:     <string>
kind:      origin | saga | vignette | research | concept | source | reference
covers:    [<glob>, ...]   # CODE kinds only — drives the read-gate
sources:   [<url|path>, ...]  # KNOWLEDGE kinds only — provenance
links:     ["[[other-story]]", ...]
refreshed: YYYY-MM-DD
---
```
- Cross-links between pages use `[[story-name]]` (Obsidian-style).
- Code citations use `path:line`.

### 4.2 Behavior by kind
| kind | how it's born | code-gate? | craft bar |
|---|---|---|---|
| `origin` | `/stories-init`, refresh | — | full soul |
| `saga` | code change → auto-authored | **yes** (`covers:`) | full soul |
| `vignette` | code change → auto-authored | **yes** (`covers:`) | full soul |
| `system` | init / refresh / structural change → auto | **yes** (`covers:`) | legible + complete (shape, not soul) |
| `research` | ingest (manual or deep-research auto) | no | full soul (synthesis) |
| `concept` | ingest / query | no | full soul (synthesis) |
| `source` | ingest | no | faithful + tight (no forced art) |
| `reference` | manual | no | pointer only |

The read-gate fires **only** on kinds with `covers:`. Knowledge pages never block a code edit.

## 5. Story craft — the `writing-a-story` skill

Owns *how* a story is written, to the bar in §2. Uses a **light spine** (not a rigid template — templates kill art; not pure freeform — that drifts):

> **hook** → **the world before** (the problem/tension) → **the decision & why** (cite `path:line`) → **what it means** (the soul) → **links onward** (`[[...]]`)

**Read before writing:** the model first reads the code the story covers (and the related stories/sources), then writes from knowledge — never guessing about code it hasn't read. A guessed story misleads with authority and is worse than none. If the needed knowledge is unreachable and the gap matters, that is a discretionary ask.

Includes a quality checklist and guidance on voice, citation, and using myth sparingly. The bar scales by `kind` per §4.2.

## 6. Operations & commands

- **(ambient, via the discipline skill)** read-before-change · author-after-change · conflict-ask · deep-research auto-ingest
- **`/stories-init`** — bootstrap `docs/stories/` in a repo: create the skeleton, interview the user, write the origin saga.
- **`/stories-refresh`** — full cleanup/refresh across all kinds (§3.5).
- **`/stories-ingest <source | research>`** — manually file knowledge into `library/`: read it → write a page → update neighbors + Atlas + log + cross-link.
- **`/stories-lint`** — read-only canon health-check: runs `scripts/lint-canon.py` (links, covers, citations, manifest + command drift, git-staleness, coverage), then adds judgment and routes rewrites to refresh.
- **`/stories-ask <question>`** *(v1.1)* — query the whole graph → synthesize with citations → optionally file the answer back as a new page, so explorations compound.

## 7. Packaging

A Claude Code plugin:
```
.claude-plugin/plugin.json     # manifest: name, version, description
skills/
  stories/SKILL.md             # the discipline/schema skill (the contract, §3 + §4 conventions)
  writing-a-story/SKILL.md     # the craft skill (§5)
commands/
  stories-init.md
  stories-refresh.md
  stories-ingest.md
```
- The `stories` skill's `description` triggers on building/refactoring/researching so it loads at the right moment.
- Own skill namespace, own `docs/` subdir. **Works with or without superpowers; never replaces it.**
- **Codex port (shipped):** a separate bundle in `codex/` — `.codex-plugin/plugin.json` + `skills/` (the two core skills symlinked to the root `skills/`; the three commands re-expressed as Codex skills, since Codex has no user-defined `/commands`). A root `AGENTS.md` carries the dogfood discipline for Codex. The CC plugin is untouched. Symlinks keep the core from drifting; the command skills + manifests are hand-synced. Research: `docs/stories/library/codex-conventions.md`.
- **Dogfood:** this repo is the plugin's source *and* grows its own `docs/stories/` describing the plugin's own soul — the plugin documents itself with itself.

## 8. v1 scope

**In:** manifest · both skills · `/stories-init` · `/stories-refresh` · `/stories-ingest` (incl. deep-research auto-ingest) · the index/log/origin/sagas/library conventions · `kind:` frontmatter.

**Deferred:** `/stories-ask` compounding (v1.1) · file-level vignettes (add when a file earns one) · any search CLI (the Atlas suffices at this scale, per `.ref/llm-wiki.md`) · the optional deep-research hardening hook.

*Update (2026-06-14): the Codex port, originally deferred, shipped — see §7 and decision #12.*

*Update (2026-07-01): the systems layer (shape-map) shipped — `kind: system` + root `ARCHITECTURE.md`. See `2026-07-01-systems-layer-design.md`.*

## 9. Decisions locked (from brainstorming)

| # | Decision | Choice |
|---|---|---|
| 1 | Story unit | Layered canon (origin → sagas → vignettes) |
| 2 | Maintenance mechanism | Skill-only (no hooks/scripts) |
| 3 | Read-gate line | Behavior/structure/soul changes; bug fixes & cosmetics default-exempt *unless* significant enough to change the repo |
| 4 | Ask rule | Conflict-only + discretionary escalation |
| 5 | Authoring trigger | Auto, same session |
| 6 | Story shape | Light spine |
| 7 | Names | origin / sagas / vignettes / Atlas / library |
| 8 | Preferences placement | Woven into `origin.md` as lore (promote to `lore.md` only if they pile up) |
| 9 | General-wiki accommodation | Unified graph via `kind:`; `library/` realm |
| 10 | Deep-research | Auto-ingested via standing skill rule |
| 11 | Authoring | Read-before-write — ground each story in the actual code/sources; never guess |
| 12 | Codex port | Separate `codex/` bundle; core skills symlinked (no drift); commands → Codex skills; root `AGENTS.md` dogfood config; CC untouched; command skills + manifests hand-synced |
| 13 | Canon lint | Read-only `scripts/lint-canon.py` + `/stories-lint`; dev/CI tool, not shipped runtime (skill-only invariant holds); lint diagnoses, refresh treats |
| 14 | Activation | Dormant by default — active only where `docs/stories/` exists; suggest init at most once, never force |
| 15 | Systems layer | Canon kind `system` under `docs/stories/systems/` + model-derived root `ARCHITECTURE.md`; legend = guaranteed click; lint enforces coverage. Full decisions: `2026-07-01-systems-layer-design.md` §9 |

## 10. Risks & notes

- **Skill-only "auto" is best-effort**, not enforced — it depends on the model honoring the skill each session. Accepted per decision #2. The optional hook (§3.4) is the escape hatch if reliability disappoints.
- **Craft quality can't be forced** by tooling; it comes from the model + the `writing-a-story` skill. The skill must carry strong exemplars.
- **Scope creep risk:** the general-wiki nature could balloon. v1 keeps query/compounding (`/stories-ask`) deferred to hold the line.
