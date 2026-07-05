---
title: The Gate, and Why It's a Skill
kind: saga
covers: ["skills/stories/SKILL.md", "README.md", "docs/specs/2026-06-14-stories-plugin-design.md"]
links: ["[[origin]]", "[[one-graph]]", "[[the-craft]]", "[[codex-conventions]]", "[[the-lint]]"]
refreshed: 2026-07-05
---

# The Gate, and Why It's a Skill

**The hook.** The whole plugin rests on one move: *read the relevant stories before you reshape the code.* Everything else serves that. So how the gate is enforced is the most important decision in the project — and we chose the weaker-looking option on purpose.

**The world before.** There were two ways to make the gate fire. A **hook** could intercept every edit deterministically and block until the stories were read — a hard guarantee. Or a **skill** could carry the rule as a standing instruction the model honors each session — best-effort. Hooks are Claude-Code-specific and brittle: they fight the model, they're awkward to scope (*is this edit a behavior change?*), and they don't travel to Codex.

**The decision.** Skill-only (`skills/stories/SKILL.md:70`). The gate is armed by data, not by interception: every story declares `covers:` globs, the Atlas (`docs/stories/index.md`) lists them inline beside each entry — one read resolves the lookup — and before a behavior/structure/soul change the model opens whatever `covers:` the files in play. That lookup *is* the gate — pure markdown, no runtime. The cost is honesty: skill-only means best-effort, not enforced (`docs/specs/2026-06-14-stories-plugin-design.md` §10). We took that trade because a portable, low-friction rule the model actually follows beats a hard wall that works in only one host and annoys everyone into disabling it.

**What it means.** The gate's reliability lives in three places now: the skill's prose, the accuracy of every `covers:`, and the loop that closes behind a change — the after-change sweep runs the canon linter when one is present, so a silent miss surfaces: links, covers, citations and the Atlas mirror in the same session, staleness at the next committed check ([[the-lint]]). The contract's own homes are covered too: this saga's `covers:` includes `README.md` and the design spec, so the gate fires when its own rulebook is edited. If `covers:` rots, the gate goes blind — which is why refresh treats a dead `covers:` as a bug, not a cosmetic. If you ever need a true guarantee for one thing (deep-research auto-filing is the only candidate), a single optional hook is the escape hatch — but adding it costs the Codex port, so it stays on the shelf until best-effort actually fails.

See [[origin]] for why any of this exists.
