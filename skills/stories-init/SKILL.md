---
name: stories-init
description: Use when the user asks to start a stories wiki for this repo (Claude Code /stories:stories-init, Codex $stories-init) — creates docs/stories/, interviews the maker, and writes the origin story and ARCHITECTURE.md.
---

# Start a stories wiki

Read the `stories` skill and its `writing.md` first.

1. **Refuse to clobber.** If `docs/stories/` already exists, stop and report what's there; offer `stories-refresh` instead.
2. **Create the canon.** `docs/stories/index.md` — `# Atlas` with empty `## Origin`, `## Sagas`, and `## Library` sections — plus `docs/stories/sagas/` and `docs/stories/library/`, each holding a `.gitkeep`.
3. **Interview the maker.** First pull what's on record: the README, existing docs, recent commits, this conversation. Then ask, one question at a time, only what you still need — why the project exists, what it must never become, the maker's lasting preferences, what success looks like.
4. **Write `origin.md`** to the craft bar, weaving the maker's preferences in as lore. It has no `covers:` — the origin gates nothing.
5. **Map the shape.** Write `ARCHITECTURE.md` from the repo's real blocks (format in `writing.md`). If one already exists without the derived-by marker, leave it alone and say so.
6. **Seed stories, if earned.** Where the code's why is evident and worth keeping, write a saga with `covers:` and anchors. Never invent a why to fill a page.
7. **Finish.** Fill in the Atlas, run `scripts/lint-canon.py` if the repo has it, and report the tree you created.
