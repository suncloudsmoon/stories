# Atlas — the stories of `stories`

The map of this wiki. Read me first: match the paths you are about to touch against the `covers:` globs below — every page that matches is required reading before the change.

## Origin
- [[origin]] — why `stories` exists: keep the *why* of code alive, the way a wiki keeps knowledge alive.

## Sagas
- [[the-gate]] — the read-before-change gate, and why it's carried by a skill instead of a hook. — covers `skills/stories/SKILL.md`, `README.md`, `docs/specs/2026-06-14-stories-plugin-design.md`
- [[one-graph]] — why code-soul and knowledge live in one graph, split only by `kind`. — covers `skills/stories/SKILL.md`, `commands/stories-ingest.md`
- [[the-craft]] — why stories use a light spine (not a template), read-before-write, a kind-scaled bar. — covers `skills/writing-a-story/SKILL.md`
- [[codex-port]] — one soul, two homes: shipping to Codex via a separate symlinked bundle, and the sync obligation it creates. — covers `codex/**`, `AGENTS.md`
- [[the-lint]] — the health-check that makes silent drift visible — now run at the close of every write path. — covers `scripts/lint-canon.py`, `commands/stories-lint.md`
- [[the-map]] — shape joins the canon: the systems layer (kind: system) + the derived ARCHITECTURE.md face. — covers `ARCHITECTURE.md`, `docs/stories/systems/*.md`, `docs/specs/2026-07-01-systems-layer-design.md`

## Vignettes
_(none yet — a vignette is born when a single file earns one.)_

## Systems
The shape-map. Root face: `ARCHITECTURE.md`.
- [[core-skills]] — the two rule-files that are the product (discipline + craft). — covers `skills/**`
- [[claude-code-home]] — manifest, slash commands, dogfood guidance, release ledger. — covers `.claude-plugin/**`, `commands/*.md`, `CLAUDE.md`, `CHANGELOG.md`
- [[codex-home]] — the mirrored Codex bundle (symlinked core, hand-synced rest). — covers `codex/**`, `codex/.codex-plugin/*`, `AGENTS.md`
- [[canon-tooling]] — the dogfood wiki, the lint canary, and the CI that runs it. — covers `scripts/*.py`, `.github/**`

## Library
- [[codex-conventions]] — porting to Codex: what maps cleanly (skills, plugins, AGENTS.md) and what must adapt (commands→skills).
