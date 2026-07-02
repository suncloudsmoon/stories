# Design Spec — the systems layer (`BLOCK_DIAGRAM.md` + `kind: system`)

**Date:** 2026-07-01
**Status:** Draft, pending user review
**Extends:** `2026-06-14-stories-plugin-design.md` — decisions #2 (skill-only), #9 (one graph), #13 (lint diagnoses / refresh treats), #14 (dormant by default) remain binding.

---

## 1. Vision

Stories carry the *why*; nothing in the canon carries the *shape*. The systems layer adds the missing technical-doc nature: an auto-maintained map of how the app is put together — block diagrams a non-developer can read at the top, technical depth one link down, every part of the program accounted for. Same engine, third nature: after code-soul and knowledge, now **structure**.

## 2. The two natures, distinguished (research)

| | story | system page |
|---|---|---|
| carries | why — decision, tension, values | what-shape — blocks, boundaries, flows |
| coverage | curated; restating code **fails** its bar | exhaustive; omitting a part **fails** its bar |
| rots when | decisions change (rare) | structure changes (constant) |
| Diátaxis | explanation | reference / architecture description |
| craft bar | full soul | legible + complete, plain-language lead |

Complementary, cross-linked: a system page says *what the Auth segment is and touches*; the saga it links says *why it's shaped that way*. The `source` kind already proved the pattern that not every kind carries full soul — the bar scales by job. The diagram shape is C4-model-lite: root file at context/container altitude, segment pages at component altitude, the model choosing segmentation per the repo's real shape.

## 3. Placement (locked with user, 2026-07-01)

One graph holds (base decision #9). System pages are canon pages:

```
BLOCK_DIAGRAM.md              # repo root — the face (derived view)
docs/stories/
  systems/                    # NEW realm — kind: system
    <segment>.md              # one per top-level block
```

- **`docs/stories/systems/<segment>.md`** — source of truth. One per block. Frontmatter `kind: system`, `covers:` globs for the code it maps, `links:` to the sagas that carry its why and to sibling systems.
- **`BLOCK_DIAGRAM.md`** (repo root) — the human face, **derived from the systems pages by the model** (never a script; skill-only invariant). Root placement is deliberate: "understood by everyone" requires being findable by everyone.
- **Rejected:** separate `docs/systems/` tree — contradicts the one-graph saga (a second wiki bolted alongside; severs why↔what links). Also rejected: canon-only with no root file — kills discoverability for non-developers.
- **Naming — open question:** `BLOCK_DIAGRAM.md` per the maker's notes. Community convention is `ARCHITECTURE.md` (matklad's pattern; readers and tools already look for it). Confirm or rename before implementation.

## 4. Page anatomy

### 4.1 `BLOCK_DIAGRAM.md` (root)

1. One-paragraph plain-language summary of what the app is. Top level is 99% plaintext by decree; jargon lives one link down.
2. Top-level Mermaid `flowchart` — segments as blocks. Segmentation is the model's call (frontend/backend, pipeline stages, packages — whatever the repo's true shape is).
3. **Legend table** — block → one-line plain description → link to its systems page. This is the universal "click": Mermaid `click <id> "<path>"` directives are also emitted, but many renderers (GitHub included) strip them, so the legend is the guarantee and the click is the bonus.
4. `## New since <YYYY-MM-DD>` — recently added/reshaped blocks, styled in-diagram via `classDef new` and listed here with dates from `log.md`. Aged out at refresh once older than the window (default **14 days**).
5. Footer: maintained-by marker + pointer to `docs/stories/index.md`.

### 4.2 `docs/stories/systems/<segment>.md`

Frontmatter per base spec §4.1 with `kind: system`. Body spine:

> plain-language lead (what this segment is, one breath) → segment-level Mermaid diagram if inner structure earns one → the parts and what each does, cited `path:line` → boundaries (what it exposes, what it must not know) → `[[links]]` onward to the sagas carrying its why.

Technical language allowed below the lead. Block granularity throughout — **never** per-file/per-function inventories.

## 5. Contract changes (three-places rule applies)

New row in the kinds table:

| kind | born when | gates code? | craft bar |
|---|---|---|---|
| `system` | init, refresh, structural change (auto) | **YES** (`covers:`) | legible + complete; plain lead; exhaustive within its block |

- **Read gate:** the gate-line is unchanged; the covering set found via Atlas + `covers:` now naturally includes system pages, so before reshaping structure the model reads the shape-map too.
- **Write side (§3.3 of base spec) extends:** update every story whose soul shifted **and every system page whose shape shifted**, and re-derive `BLOCK_DIAGRAM.md` when the top-level picture moved.
- **Origin-decree carve-out:** origin.md's "never become a verbose auto-doc that restates the code" gains a clause — *system pages restate **shape**, at block granularity, and that is their job; the moment one reads like a directory listing it has failed its bar.* Updating origin.md is a soul change and gets storied.

## 6. Lifecycle

- **`/stories-init`** — after the interview: scan the repo, choose segments, author all systems pages + root `BLOCK_DIAGRAM.md`. Everything accounted for from day one.
- **Ambient (the gate's write side)** — structural change ⇒ affected systems pages updated in the same session; root file re-derived when the top-level picture changes; new segment ⇒ new page + `new` styling + log entry.
- **`/stories-refresh`** — reconcile diagram vs reality (walk the repo's real top-level structure ↔ blocks), rewrite stale pages, delete dead blocks without fear, age out `new` highlights, rebuild legend + Atlas. Repos initialized before this feature: refresh offers to build the layer once; never forces it.
- **`/stories-lint` / `scripts/lint-canon.py`** — mechanical checks: every diagram node ↔ a systems page ↔ a legend row; `systems/` pages ⇒ `BLOCK_DIAGRAM.md` exists (a root file *without* `systems/` is valid — tiny-repo mode, §7); union of system `covers:` vs top-level code dirs (coverage **warning**); consumer-aware skip when no systems layer exists (dormancy, base decision #14, holds).

## 7. Edge cases

- Pre-existing hand-written `BLOCK_DIAGRAM.md`/`ARCHITECTURE.md` not made by the plugin: **never overwrite** — surface via the conflict channel.
- Tiny repo: root file only; no `systems/` pages until a segment earns one (mirrors the vignette discipline).
- Renderer without Mermaid: plain summary + legend still carry the full content.
- Monorepo: segments = packages/apps at root altitude; layers within each package's own page.

## 8. Packaging & sync obligations

- `skills/stories/SKILL.md` — kind row, systems conventions, extended write-sweep, root-file conventions.
- `skills/writing-a-story/SKILL.md` — the system-page bar + a worked exemplar.
- `commands/stories-init.md`, `commands/stories-refresh.md` — lifecycle steps (§6).
- `scripts/lint-canon.py` — §6 checks.
- `README.md` + base spec §9 — contract restated (three-places rule).
- `codex/` — core skills carry via symlink; command-skills + manifests hand-synced.
- **Dogfood:** this repo gets its own `BLOCK_DIAGRAM.md` + systems pages (segments ≈ skills / commands / codex / scripts) + a new saga (`the-map`) carrying this decision + the origin.md carve-out + Atlas/log updates.

## 9. Decisions (this spec)

| # | Decision | Choice |
|---|---|---|
| S1 | Placement | Canon kind `system` under `docs/stories/systems/` + root `BLOCK_DIAGRAM.md` face (one-graph holds) |
| S2 | Source of truth | systems pages; root file is a model-derived view |
| S3 | Gate | system pages carry `covers:`; gated read+write like sagas |
| S4 | Bar | legible + complete, plain lead — not full soul; block granularity, never per-file |
| S5 | Clickability | legend links guaranteed; Mermaid `click` directives best-effort |
| S6 | Recency | `classDef new` + "New since" section; aged at refresh; 14-day default window |
| S7 | Coverage enforcement | lint diagnoses (node↔page↔legend, covers-vs-dirs), refresh treats |
| S8 | Surface | no new skills or commands — folded into the two skills + init/refresh + lint |

## 10. Risks & open questions

- **Churn:** structural changes now touch two artifacts. Mitigated by block granularity and re-deriving the root file only when the top-level picture moves.
- **Auto-doc creep:** guarded by S4, the origin carve-out language, and refresh pruning.
- **Best-effort staleness:** same trade as the-gate; lint's coverage warning is the tripwire.
- **Open:** root-file name (`BLOCK_DIAGRAM.md` vs `ARCHITECTURE.md`, §3); the 14-day recency window default (S6).
