---
covers: ["skills/stories/SKILL.md"]
refreshed: 2026-10-29
---

# One Graph, One Rule

**The hook.** The wiki holds two very different things — the *soul of the code* and a *pile of researched knowledge* — and the obvious move was to build two tools. We built one, and in 2.0 we stopped needing a taxonomy to hold it together.

**The world before.** The ancestor pattern, the LLM-wiki, was a knowledge base of external sources. This project started narrower: stories about code. Then the maker asked for the wiki to hold deep-research results too. One graph absorbed both, and v1 told the pages apart with an eight-row `kind:` table — origin, saga, vignette, system, research, concept, source, reference — each with its own behavior and craft bar. The table worked, but it was a vocabulary every model had to learn, and `kind:` repeated what the folder already said.

**The decision.** One rule replaces the table: a page with `covers:` is a story about code, and only such a page gates changes (`skills/stories/SKILL.md#only such a page gates changes`). Everything else is knowledge, living in `library/`, free to carry `sources:`, never blocking an edit. Stories and knowledge still share one web of `[[links]]`, and deep research still files itself into the library.

**What it means.** The payoff is the link that crosses the seam: a research page can point at the story of the code it justified, and that story can cite the research that bore it. Two tools would have severed that thread. The one discipline left is honesty about `covers:` — it is now the only fact that decides whether a page gates, so a page that claims code it doesn't explain, or explains code it doesn't claim, misleads the gate.

See [[origin]] for why the graph exists, [[the-gate]] for what `covers:` arms, [[the-craft]] for how a page is written.
