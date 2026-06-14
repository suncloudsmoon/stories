---
name: writing-a-story
description: Use when writing or rewriting any page in docs/stories/ (a saga, vignette, origin, or library page). Defines the craft — the light spine, the quality bar, kind-aware scaling, citations, and using myth sparingly — with a worked exemplar.
---

# Writing a story

A story in `docs/stories/` is a work of art with a job: carry the *soul* of the code — the why, the tension, the road not taken — tightly enough that a reader (human or model) understands intent in one pass.

## Read before you write

Before you write a single line, **read what you're writing about.** Open and actually read:
- the code the story will `covers:` — read it, don't infer from the filename,
- the stories it will link to, and any `sources:` it draws on,
- whatever else it takes to know the *why*: neighbouring code, the spec, the log.

Write from **knowledge and wisdom, never from a guess.** A story invented from a plausible hunch about what the code "probably" does is worse than no story — it misleads the next reader with authority. If the knowledge you'd need isn't reachable and you would be guessing about something that matters, that is a discretionary ask, not a place to improvise.

## The light spine

Not a template (templates kill art), not freeform (freeform drifts). A spine you bend to fit:

1. **The hook** — one or two lines naming the tension or the stakes. Why should anyone care?
2. **The world before** — what the problem looked like; the constraint or pressure that forced a decision.
3. **The decision & why** — what was chosen, and *why this and not that*. Cite the code: `path:line`. This is the load-bearing section.
4. **What it means** — the soul: the value underneath, what it asks of future changes, what would betray it.
5. **Links onward** — `[[related-page]]` connections into the graph.

A short vignette may collapse steps 1–2 and 4 into a few sentences. An origin saga may dwell. Bend the spine; don't pad it.

## The quality bar

- **One meaning per story.** A clear soul, not a grab-bag. If it sprawls, split it.
- **Grounded.** Rooted in real code and real decisions. Cite `path:line`. Don't narrate fiction about code that isn't there.
- **Deep.** The why and the tradeoffs, not the surface. If a sentence restates what the code obviously does, cut it.
- **Tight.** Every line earns its place. Prefer 200 strong words to 600 limp ones.
- **Engaging + logical.** Cause → effect prose, not bullet soup.
- **Myth, sparingly.** A mythic frame is allowed when it illuminates — a metaphor that makes a hard idea land. Never as filler, never more than seasoning.

## Kind-aware bar

| kind | how hard to craft |
|---|---|
| `origin`, `saga`, `vignette` | full soul — the spine, the why, the art |
| `research`, `concept` | full soul — synthesis with citations to `sources:` |
| `source` | faithful + tight — capture the source honestly; do not dress it up |
| `reference` | a pointer — title, link, one line. No story. |

Forcing artistry onto a raw source betrays it. Match the bar to the kind.

## Mechanics

- **Frontmatter** on every page (schema lives in the `stories` skill). Keep `covers:`/`sources:`, `links:`, and `refreshed:` accurate — the gate and the graph depend on them.
- **Citations:** `path:line` (e.g. `src/auth/token.ts:42`). Update them when refreshing; a dead citation is a bug.
- **Cross-links:** `[[page-name]]`, matching the target file's name without `.md`.

## Exemplar

A vignette for a fictional `src/cache/lru.ts`, written to the bar:

> ---
> title: The LRU That Refused to Forget
> kind: vignette
> covers: ["src/cache/lru.ts"]
> links: ["[[render-pipeline]]"]
> refreshed: 2026-06-14
> ---
>
> **The hook.** The cache was supposed to be small. It kept everything anyway — and that was the point.
>
> **Before.** The render loop re-fetched the same tiles every frame; the network was the bottleneck, not the GPU. A plain LRU would have evicted exactly the tiles a panning user was about to need again.
>
> **The decision.** We pin the last-touched *region*, not the last-touched *entry* (`src/cache/lru.ts:31`). Eviction skips anything inside the active viewport's halo. We chose spatial locality over strict recency because users pan, they don't teleport — recency is a bad proxy for "needed next" here.
>
> **What it means.** This cache trades memory for predictability under panning. If you ever make it strictly recency-based to save RAM, you will bring back the stutter we built this to kill — measure panning FPS before you touch the eviction rule.
>
> See also [[render-pipeline]].

Notice: one idea, a real citation, the *why* in front, a warning to the next changer — and it's short.
