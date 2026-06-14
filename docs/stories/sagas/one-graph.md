---
title: One Graph, Many Kinds
kind: saga
covers: ["skills/stories/SKILL.md", "commands/stories-ingest.md"]
links: ["[[origin]]", "[[the-gate]]", "[[the-craft]]"]
refreshed: 2026-06-14
---

# One Graph, Many Kinds

**The hook.** The wiki holds two very different things — the *soul of the code* and a *pile of researched knowledge* — and the obvious move was to build two tools. We built one.

**The world before.** The ancestor pattern (the LLM-wiki) was a knowledge base of external sources. This project started narrower: stories about code. Partway in, the maker asked for the wiki to also hold deep-research results "among other things." Two shapes presented themselves — a second, separate wiki bolted alongside, or one graph that absorbs both.

**The decision.** One graph. A page's `kind:` decides its behavior, not which tool or folder owns it (`skills/stories/SKILL.md`, the kinds table). Code kinds (`saga`, `vignette`) carry `covers:` globs and arm the gate; knowledge kinds (`research`, `concept`, `source`) carry `sources:` and never block a code edit. `/stories-ingest` (`commands/stories-ingest.md`) and deep-research auto-filing both drop their output into `library/` as just-another-kind.

**What it means.** The payoff is the link that crosses the seam: a `research` page can point at the `saga` of the code it justified, and that code's soul can cite the research that bore it. Two tools would have severed that thread forever. The cost is discipline — `kind:` must be set honestly, or a knowledge page could wrongly arm (or wrongly escape) the gate. When you add a page, choose its kind first; everything else follows from it.

See [[origin]] for why this exists, [[the-gate]] for what `covers:` does, [[the-craft]] for how the kind sets the writing bar.
