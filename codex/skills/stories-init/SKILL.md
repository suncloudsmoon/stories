---
name: stories-init
description: Bootstrap the stories wiki (docs/stories/) in this repo — create the canon skeleton, interview the maker, and write the origin saga. Use when the user asks to set up or initialize stories. Invoke with $stories-init.
---

Bootstrap the **stories** wiki for this repo. (Mirrors the Claude Code `/stories-init` command — keep the two in sync.)

1. **Refuse to clobber.** If `docs/stories/` already exists, stop and report; offer stories-refresh instead.
2. **Create the skeleton** (today's date, YYYY-MM-DD): `docs/stories/index.md` (the Atlas, with sections `## Origin`, `## Sagas`, `## Vignettes`, `## Library`); `docs/stories/log.md` (`# Log` then `## [<today>] init | canon bootstrapped`); `docs/stories/origin.md` (written in step 4); and dirs `sagas/`, `vignettes/`, `library/`, each with a `.gitkeep`.
3. **Interview the maker.** Read the `stories` and `writing-a-story` skills. First pull what's already on record (README, docs, recent commits, the conversation) — don't ask what you already know. Then ask, one question at a time: why the project exists; its core philosophy / what it must never become; the maker's durable preferences (to become lore); what success looks like.
4. **Write the origin saga** to the craft bar: kind `origin`, the light spine, grounded, tight, with soul; weave preferences in as lore.
5. **Wire it up.** Add `origin.md` to the Atlas under `## Origin`; append a log entry; report the tree.
