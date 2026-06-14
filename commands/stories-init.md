---
description: Bootstrap docs/stories/ — create the canon skeleton, interview the maker, and write the origin saga.
---

Bootstrap the **stories** wiki for this repo.

## 1. Refuse to clobber
If `docs/stories/` already exists, stop and report what's there. Offer `/stories-refresh` instead. Never overwrite an existing canon.

## 2. Create the skeleton
Create, using today's real date (YYYY-MM-DD):
- `docs/stories/index.md` — the Atlas. A heading plus empty sections: `## Origin`, `## Sagas`, `## Vignettes`, `## Library`.
- `docs/stories/log.md` — the chronicle: `# Log` then the first entry `## [<today>] init | canon bootstrapped`.
- `docs/stories/origin.md` — the origin saga (written in step 4).
- empty dirs `docs/stories/sagas/`, `docs/stories/vignettes/`, `docs/stories/library/`, each with a `.gitkeep`.

## 3. Interview the maker
Read the `stories` and `writing-a-story` skills first. Then, to source the soul of `origin.md`, ask the user — one question at a time — about:
- why this project exists (the itch, the bet),
- the core philosophy / what it must never become,
- the maker's durable preferences (so they become lore),
- what success looks like.

First pull anything already on record (README, existing docs, recent commits, this conversation). Don't ask what you already know.

## 4. Write the origin saga
Write `docs/stories/origin.md` to the craft bar (`writing-a-story`): kind `origin`, the light spine, grounded, tight, with soul. Weave the maker's preferences in as lore.

## 5. Wire it up
Add `origin.md` to the Atlas under `## Origin` with a one-line hook. Append a log entry. Report the tree you created.
