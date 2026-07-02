---
title: Claude Code home — manifest and slash commands
kind: system
covers: [".claude-plugin/**", "commands/*.md"]
links: ["[[the-gate]]", "[[codex-port]]", "[[the-map]]"]
refreshed: 2026-07-01
---

# Claude Code home

The packaging that makes this repo installable in Claude Code. This segment exists so the core skills stay host-agnostic while the host-specific surface lives in one place.

- `.claude-plugin/plugin.json` — the manifest (name, version, description; hand-synced with the Codex manifest).
- `commands/stories-{init,refresh,ingest,lint}.md` — the four slash commands: bootstrap, deep-clean, manual ingest, health-check.

**Boundaries.** Commands orchestrate; the rules live in the core skills. Every command edit must land identically in `codex/skills/stories-*/SKILL.md` — the sync obligation of [[codex-port]], enforced by lint's command-drift check.

Why two homes: [[codex-port]].
