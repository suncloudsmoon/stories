---
title: Claude Code home — manifest and slash commands
kind: system
covers: [".claude-plugin/**", "commands/*.md", "CLAUDE.md", "CHANGELOG.md"]
links: ["[[the-gate]]", "[[codex-port]]", "[[the-map]]"]
refreshed: 2026-07-05
---

# Claude Code home

The packaging that makes this repo installable in Claude Code. This segment exists so the core skills stay host-agnostic while the host-specific surface lives in one place.

- `.claude-plugin/plugin.json` — the manifest; `.claude-plugin/plugin.json:3` carries the version the Codex twin must match, hand-synced. The marketplace entry moved out-of-repo (`suncloudsmoon/plugins`) just after v1.0.0 (`f38da00`, 2026-07-04).
- `commands/stories-{init,refresh,ingest,lint}.md` — the four slash commands: bootstrap, deep-clean, manual ingest, health-check. Each write-path command closes by running the canon linter when present.
- `CLAUDE.md` — the dogfood guidance this host loads every session; sibling of `AGENTS.md` in the Codex home.
- `CHANGELOG.md` — the release ledger: every behavior change bumps both manifests and lands an entry here.

**Boundaries.** Commands orchestrate; the rules live in the core skills. Every command edit must land identically in `codex/skills/stories-*/SKILL.md` — the sync obligation of [[codex-port]], enforced by lint's command-drift check.

Why two homes: [[codex-port]].
