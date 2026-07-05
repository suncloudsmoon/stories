# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-07-05

The verification loop closes — the audit found the discipline trusted and
never verified; now every write path verifies.

### Added
- The Atlas (`docs/stories/index.md`) lists each gate-bearing page's
  `covers:` globs inline — the gate lookup is one read instead of N.
- The after-change sweep and the init/refresh/ingest procedures (both
  homes) close by running the canon linter when the repo carries one.
- Linter checks: default-exempt-list sync across the three contract homes
  (error, anchored to each home's gate-line); the Atlas's inline covers
  diffed against every page's frontmatter (error on mismatch); required
  `path:line` citation on gate-bearing pages (warn); coverage sweep over
  tracked + untracked files minus an exempt list (info, capped);
  staleness messages name the file that moved; command-drift messages
  name the differing step; manifest drift now compares all eight shared
  fields.
- Gate coverage for the contract's own homes: `README.md` + the design
  spec (the-gate), `CLAUDE.md` + `CHANGELOG.md` (claude-code-home), CI
  (canon-tooling), the systems spec (the-map).

### Fixed
- CI workflow no longer parses the removed `marketplace.json` — the job
  had failed on every push since 2026-07-04.
- Codex `stories-ingest` offers **deep** research again (wording drift).
- `AGENTS.md` carries the three-places sync rule and the systems layer;
  `CLAUDE.md` names all four commands.
- README states the full default-exempt list (was "cosmetics").
- Canon no longer cites the removed `marketplace.json`; its 2026-07-04
  removal is now chronicled in `docs/stories/log.md`.

## [1.0.0] — 2026-07-03

First public release.

### Added
- MIT `LICENSE`.
- `license`, `homepage`, and `repository` metadata on both the Claude Code and
  Codex manifests, and on the marketplace entry.
- `.github/workflows/lint.yml` — CI runs `scripts/lint-canon.py` (plus a
  manifest-parse check) on every push and pull request.
- `CHANGELOG.md`, README badges, and a hero diagram (`docs/assets/hero.svg`).

### Changed
- Filled the `<owner>` placeholders with the real slug (`suncloudsmoon/stories`)
  across the READMEs and the marketplace file.

## [0.3.0] — 2026-07-01

### Added
- **Systems layer (the shape-map).** New `kind: system`, `docs/stories/systems/`
  pages, and a derived root `ARCHITECTURE.md` face — legend as the guaranteed
  click, `new` highlights, 14-day aging. Discipline and craft skills extended;
  `init`/`refresh`/`lint` updated in both homes.

### Changed
- Renamed the shape-map's root face `BLOCK_DIAGRAM.md` → `ARCHITECTURE.md`
  (matklad's community convention).

## [0.2.0] — 2026-06-14

### Added
- Read-only canon health-check: `scripts/lint-canon.py` and `/stories-lint`
  (with the Codex mirror) — checks links, `covers:`, citations, manifest and
  command drift, git-staleness, and coverage.
- Codex bundle under `codex/` (`.codex-plugin` manifest, symlinked core skills,
  command-skills) and a root `AGENTS.md`.

### Changed
- Made the discipline **dormant by default**: with no `docs/stories/`, stay
  quiet and suggest `/stories-init` at most once.

## [0.1.0] — 2026-06-14

### Added
- Initial `stories` plugin: the two core skills (`stories`, `writing-a-story`),
  the four slash commands, the Claude Code manifest, and the bootstrapped
  `docs/stories/` canon.

[1.1.0]: https://github.com/suncloudsmoon/stories/releases/tag/v1.1.0
[1.0.0]: https://github.com/suncloudsmoon/stories/releases/tag/v1.0.0
[0.3.0]: https://github.com/suncloudsmoon/stories/releases/tag/v0.3.0
[0.2.0]: https://github.com/suncloudsmoon/stories/releases/tag/v0.2.0
[0.1.0]: https://github.com/suncloudsmoon/stories/releases/tag/v0.1.0
