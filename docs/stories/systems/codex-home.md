---
title: Codex home — the mirrored bundle
kind: system
covers: ["codex/**", "AGENTS.md"]
links: ["[[codex-port]]", "[[the-map]]"]
refreshed: 2026-07-01
---

# Codex home

The second home: a Codex plugin bundle mirroring the Claude Code plugin. This segment exists because the maker chose a separate bundle over a merged dual-manifest repo ([[codex-port]]).

- `codex/.codex-plugin/plugin.json` — the Codex manifest (hand-synced twin).
- `codex/skills/stories`, `codex/skills/writing-a-story` — **symlinks** to the root `skills/` (cannot drift).
- `codex/skills/stories-*/SKILL.md` — the four commands re-expressed as Codex skills (`$stories-init` …), hand-synced.
- `AGENTS.md` — the dogfood discipline for Codex, sibling of `CLAUDE.md`.

**Boundaries.** Nothing original lives here except packaging: rules come from the symlinked core; procedures mirror `commands/`. If this home tells a different story than the root, that is drift — lint flags it, refresh heals it.

The full why: [[codex-port]].
