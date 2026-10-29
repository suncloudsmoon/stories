---
covers: ["ARCHITECTURE.md"]
refreshed: 2026-10-29
---

# The Map — The Shape in One File

**The hook.** The canon carried the *why* beautifully and the *shape* not at all — a newcomer could learn what would break the project's heart before they could learn what talks to what.

**The world before.** The maker asked for block diagrams anyone can read, every part accounted for, each block one click from its explanation. v1 answered with a whole layer: a `system` page per block under `docs/stories/systems/`, a root `ARCHITECTURE.md` derived from them, a legend table, Mermaid `click` directives, and a "New since" section aged out after fourteen days. The shape was stated twice — once in the pages, once in the face — and every structural change meant updating both and re-deriving one from the other.

**The decision.** One file. `ARCHITECTURE.md` at the repo root holds the whole shape: a plain paragraph, one diagram, and a block table whose last column links each block to the story that carries its why — the one click the maker asked for, without a second page in between. From matklad's ARCHITECTURE.md it takes two habits: name modules and symbols rather than linking lines, and keep a short list of **invariants** stated as absences (`ARCHITECTURE.md#Invariants`) — the rules most worth knowing and least likely to show up in the code. The format lives with the craft (`skills/stories/writing.md#Invariants`).

**What it means.** The map stays coarse on purpose. Stories are curated and carry soul; the map is complete and carries shape, and neither does the other's job. When a block appears, vanishes, or rewires, update the map in the same session. If it ever sprawls into a per-file inventory, cut it back — the table, not the diagram, carries a reader to depth.

See [[one-graph]] for the seam between shape and soul, [[origin]] for the auto-doc it must never become.
