---
covers: ["skills/stories/writing.md", "skills/stories-init/SKILL.md"]
refreshed: 2026-10-29
---

# The Craft — A Spine, Not a Template

**The hook.** A story must be a work of art *and* be produced reliably, on every code change, by a machine. Those goals pull against each other — and how we resolved the tension is the whole craft.

**The world before.** Two failure modes loomed. A **rigid template** ("Problem / Solution / Notes") makes output consistent but kills the art — every story reads like a filled-in form. **Pure freeform** keeps the art but drifts: it skips the why, buries the lede, sprawls. Then a third failure arrived in practice: stories cited code by line number, every edit above a cited line made it lie, and keeping citations honest cost models whole subagent runs.

**The decision.** A **light spine**, not a template (`skills/stories/writing.md#The light spine`): hook → the world before → the decision & why → what it means → links onward — bent to fit, never padded. Three guards keep it honest. The model **reads before it writes**, and a why it inferred rather than was told is marked `*(inferred)*` (`skills/stories/writing.md#(inferred)`), borrowing Graphify's line between extracted and inferred. Citations are **anchors** — text that appears in the file — so they survive edits and break only when the thing they name is renamed or deleted. And the craft lives in a file the model opens only when it writes a page, so it costs nothing on the turns that don't. `stories-init` holds the origin to the same rule: pull what's on record, ask the maker, and never invent a why (`skills/stories-init/SKILL.md#Never invent a why`).

**What it means.** Consistency comes from the spine and the bar, not from a fill-in-the-blanks shape, so the art survives. The load-bearing section is always *the decision & why*, and its anchors are promises the linter keeps. If a story drifts into restating what the code obviously does, cut it rather than pad it. Tight beats long; grounded beats clever.

See [[origin]] for the values, [[the-gate]] for when stories get read, [[one-graph]] for what makes a page a story.
