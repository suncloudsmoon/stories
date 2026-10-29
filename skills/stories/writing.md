# Writing a page

A story is a work of art with a job: carry the *why* tightly enough that a reader — human or model — understands intent in one pass.

## Read before you write

Open and read the code the story covers, the stories it links to, and whatever else holds the why: the spec, commit messages, the conversation. Write from knowledge, never from a guess. A why invented from a hunch misleads with authority; if the knowledge is out of reach and the guess matters, ask.

When a why is your own inference — not something the maker said, nor something a commit, spec, or comment records — mark it *(inferred)*.

## The light spine

A spine you bend, not a template:

1. **The hook** — one or two lines naming the tension. Why should anyone care?
2. **The world before** — the problem; the constraint that forced a decision.
3. **The decision & why** — what was chosen, and why this and not that. Cite the code with anchors. This is the load-bearing section.
4. **What it means** — the value underneath; what it asks of future changes; what would betray it.
5. **Links onward** — `[[related-page]]`.

A short story folds 1, 2, and 4 into a few sentences; the origin may dwell. Bend the spine; don't pad it.

## The bar

- **One meaning per story.** If it sprawls, split it.
- **Grounded.** Real code, real decisions, anchors that resolve.
- **Deep.** The why and the trade-offs. Cut any sentence that restates what the code obviously does.
- **Tight.** Two hundred strong words beat six hundred limp ones.
- **Cause → effect prose**, not bullet soup.
- **Myth, sparingly** — only when a metaphor makes a hard idea land.

By folder: `origin.md` and `sagas/` carry full soul. In `library/`, a synthesis carries full soul with citations to its `sources:`; a raw source stays faithful and tight — don't dress it up; a pointer is a title, a link, and one line.

## ARCHITECTURE.md

The shape of the program, at the repo root, in this order:

1. One plain-language paragraph: what the app is, no jargon.
2. One top-level Mermaid `flowchart` of the blocks.
3. A block table: block · one plain line, including what it must not touch · a link to the story that carries its why.
4. **Invariants** — a short list of rules stated as absences ("the hook never edits a file").
5. The footer `<!-- derived by the stories plugin — source of truth: the code and docs/stories/ -->`.

Name modules and symbols; never link lines. Stay at block granularity — the moment it reads like a directory listing, it has failed. Never overwrite an `ARCHITECTURE.md` that lacks the footer marker: it is hand-written. Surface it instead.

## Exemplar

> ```yaml
> ---
> covers: ["src/cache/lru.ts"]
> refreshed: 2026-06-14
> ---
> ```
> # The LRU That Refused to Forget
>
> The cache was supposed to be small. It kept everything anyway — and that was the point.
>
> The render loop re-fetched the same tiles every frame; the network was the bottleneck, not the GPU. A plain LRU would have evicted exactly the tiles a panning user was about to need again.
>
> So we pin the last-touched *region*, not the last-touched entry (`src/cache/lru.ts#pinRegion`): eviction skips anything inside the viewport's halo. Users pan; they don't teleport — recency is a bad proxy for "needed next" here.
>
> This cache trades memory for predictability. Make it strictly recency-based to save RAM and the stutter comes back — measure panning FPS before you touch the eviction rule.
>
> See also [[render-pipeline]].

One idea, a real anchor, the why in front, a warning to the next changer — and it's short.
