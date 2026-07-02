---
title: The Map — Shape Joins the Canon
kind: saga
covers: ["ARCHITECTURE.md", "docs/stories/systems/*.md"]
links: ["[[origin]]", "[[one-graph]]", "[[the-gate]]", "[[the-lint]]", "[[the-craft]]", "[[core-skills]]", "[[claude-code-home]]", "[[codex-home]]", "[[canon-tooling]]"]
refreshed: 2026-07-01
---

# The Map — Shape Joins the Canon

**The hook.** The canon carried the *why* beautifully and the *shape* not at all. A newcomer could learn what would break the project's heart before they could learn what talks to what.

**The world before.** The maker asked for block diagrams: a root `ARCHITECTURE.md` anyone can read, every part of the program accounted for, new blocks highlighted, each block one click from its explanation. Two stories pushed back. [[one-graph]] had already rejected "a second wiki bolted alongside" — and a separate `docs/systems/` tree is exactly that. And [[origin]] swore the canon would never become "a verbose auto-doc that restates the code" — which an exhaustive diagram flirts with.

**The decision.** Shape joined the graph instead of standing beside it (`skills/stories/SKILL.md`, the systems-layer section). A new kind, `system`: pages under `docs/stories/systems/`, one per block, `covers:` armed like a saga's — so the gate now reads the map before structure moves, and the write-sweep redraws it after. The root `ARCHITECTURE.md` is not canon but a **derived face**: plain-language lead, Mermaid flowchart, a legend table as the guaranteed "click" (renderers strip Mermaid `click` directives; a table never fails), `classDef new` highlights aged out after ~14 days. The origin decree survived by narrowing, not breaking: a system page restates *shape at block granularity* — the moment it reads like a directory listing it has failed its bar ([[the-craft]]). Exhaustiveness, stories' vice, is the map's *duty* — `scripts/lint-canon.py` now errors on an unmapped systems page and warns on an uncovered top-level dir ([[the-lint]]).

**What it means.** The canon now holds two bars in tension: stories stay curated, the map stays complete, and neither may do the other's job. A structural change that redraws no diagram is as unfinished as a soul change that rewrites no story. If the map ever sprawls into per-file inventory, cut it back — the legend, not the diagram, carries a reader to depth.

See [[one-graph]] for the seam this almost tore, [[origin]] for the decree it had to honor.
