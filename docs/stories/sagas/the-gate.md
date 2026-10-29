---
covers: ["skills/stories/SKILL.md", "hooks/**"]
refreshed: 2026-10-29
---

# The Gate — From the Model's Judgment to a Hook

**The hook.** The whole plugin rests on one move: *read the story before you reshape the code.* How that move gets triggered is the most important decision in the project — and in 2.0 we reversed it.

**The world before.** v1 was skill-only. A hook would have been deterministic, but hooks were Claude-Code-only, and the plugin was meant to travel to Codex. So the skill asked the model to do two things on its own: decide whether its change was significant enough to count (behavior, structure, or soul — with six default-exempt categories and a rule that significance overrides the category), then look up which stories covered the files in play. Both steps are judgment, and judgment is where a best-effort gate leaks: a model that files its change under "bug fix" never opens the story the fix betrays.

**The decision.** Two things changed. Codex began running plugin hooks from the same `hooks/hooks.json`, honoring the same outputs — so portability stopped arguing against a hook. And the maker asked for a plugin that any model finds easy to use. So 2.0 moves *when to read* from the model's judgment into the harness (`hooks/stories.py#def handle`):

- When the model **reads** a covered file, the hook names its story — the moment Claude Code's own path-scoped rules fire, before any edit is planned.
- An **edit** that arrives before its story was named is held back once (exit 2). Blocking is the only way to get ahead of the edit: context a hook adds there lands after the tool has already run.
- At the **end of a turn**, if covered code changed and its story didn't, the hook asks once whether the why changed.

Each message is one line that names the page, never its body, and each fires at most once per story per session. That restraint is deliberate: Graphify's hooks, which fire on every search, are what users call spammy and models learn to ignore. And the hook fails open (`hooks/stories.py#fail open`) — a bug in the gate must never block the work it guards.

**What it means.** The skill still says *what* to do (`skills/stories/SKILL.md#Before you change code`); the hook only says *when*. The exempt list is gone because nothing needs classifying — reading a story costs a few hundred tokens, skipping the one that mattered costs the soul. The hook sees only what `covers:` tells it, so a dead or missing `covers:` blinds the gate. And if the hook ever starts talking on every read, or blocking twice, it has become the nag [[origin]] forbids — cut it back.

See [[the-lint]] for how drift surfaces, [[codex-port]] for the shared hooks, [[one-graph]] for what `covers:` means.
