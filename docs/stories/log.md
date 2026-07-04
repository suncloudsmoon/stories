# Log

The chronicle of this wiki. Newest at the bottom.

## [2026-06-14] init | canon bootstrapped
Created the Atlas, the origin saga, and the first saga ([[the-gate]]). Soul sourced from the founding conversation — the brief that defined `stories` as a soul-bearing wiki built on the LLM-wiki pattern.

## [2026-06-14] author | internal sagas
Wrote [[one-graph]] (the unified-kinds decision) and [[the-craft]] (spine-not-template + read-before-write). Narrowed [[the-gate]] `covers:` to the discipline skill and wired the saga cross-links. The canon now covers: why it exists, how the gate is enforced, the one-graph unification, and the craft.

## [2026-06-14] research | codex-conventions
Three-agent sweep on Codex porting (skills/plugins, AGENTS.md, config/commands), filed to [[codex-conventions]]. Verdict: Codex shares the Agent-Skills standard — the port is mostly mechanical, and the skill-only bet ([[the-gate]]) holds. Pending: exact `.codex-plugin/plugin.json` schema (fetch `/codex/plugins/build` before writing the manifest).

## [2026-06-14] author | codex-port saga + bundle
Shipped the Codex bundle (`codex/`: `.codex-plugin` manifest, symlinked core skills, three command-skills) + root `AGENTS.md`. Filed [[codex-port]] and wired it to [[the-gate]] + [[codex-conventions]]. Standing rule recorded (CLAUDE.md / AGENTS.md / each command skill): update `codex/` when the CC plugin changes.

## [2026-06-14] feat | canon lint + dormant-by-default
Added the read-only health-check — `scripts/lint-canon.py` + `/stories-lint` (and the Codex mirror) — filed [[the-lint]]. It checks links, covers, citations, manifest + command drift, git-staleness, and coverage, making silent drift visible and enforcing the two-homes sync mechanically. Also made the discipline **dormant by default**: no `docs/stories/` ⇒ stay quiet, suggest init at most once. The new command pair brings the hand-synced set to four; manifests bumped to 0.2.0.

## [2026-07-01] feat | systems layer (the shape-map)
Shape joined the canon: new kind `system`, `docs/stories/systems/` pages + derived root `BLOCK_DIAGRAM.md` (legend as the guaranteed click, `new` highlights, 14-day aging). Discipline + craft skills extended, init/refresh/lint updated in both homes, manifests to 0.3.0. Filed [[the-map]]; carved the auto-doc decree in [[origin]]; dogfooded the map onto this repo (four blocks). Spec: `docs/specs/2026-07-01-systems-layer-design.md`.

## [2026-07-01] refactor | shape-map face renamed to ARCHITECTURE.md
The maker chose the community convention (matklad's ARCHITECTURE.md pattern) over the working name BLOCK_DIAGRAM.md. Renamed the root face + every living reference (skills, commands both homes, lint, README, CLAUDE.md, manifests, specs, [[the-map]], the Atlas); plan doc and earlier log entries keep the old name as history.

## [2026-07-03] chore | publication packaging (v1.0.0)
Made both homes publishable: added an MIT `LICENSE`, and `license` / `homepage` / `repository` to both manifests and the marketplace entry. Filled the `<owner>` placeholders with the real slug (`suncloudsmoon/stories`) across the READMEs and marketplace, and wired a GitHub Actions workflow (`.github/workflows/lint.yml`) that runs the linter on every push/PR. Version → 1.0.0. Packaging only — no soul or behavior change, so per [[origin]] ("never a changelog") this stays a log line, not a saga. Also added `CHANGELOG.md`, README badges, and a hero diagram (`docs/assets/hero.svg`) for the listing. The public `git push` and `claude plugin marketplace add suncloudsmoon/stories` remain the maker's to run.
