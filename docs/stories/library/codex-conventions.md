---
title: Porting to Codex — the lay of the land
kind: research
sources: ["https://developers.openai.com/codex/skills", "https://developers.openai.com/codex/plugins", "https://developers.openai.com/codex/plugins/build", "https://developers.openai.com/codex/hooks", "https://developers.openai.com/codex/guides/agents-md", "https://developers.openai.com/codex/config-reference", "https://developers.openai.com/codex/mcp", "https://agents.md/"]
links: ["[[origin]]", "[[the-gate]]", "[[codex-port]]"]
refreshed: 2026-06-14
---

# Porting to Codex — the lay of the land

*Filed from a three-front research sweep (skills/plugins, AGENTS.md, config/commands), 2026-06-14. Codex docs current ~codex-cli v0.130.0.*

**The headline.** The Codex port is mostly mechanical. Codex shares the same Agent-Skills standard as Claude Code — `SKILL.md` with `name`/`description`, auto-selected by description match — so `stories` and `writing-a-story` carry over almost verbatim. The skill-only bet ([[the-gate]]) is vindicated: skills are first-class in both hosts, so the discipline ports with no loss.

## What maps cleanly

- **Skills.** `SKILL.md` (YAML `name`/`description` + body). Codex scans `.agents/skills/` (CWD → parents → repo root), `~/.agents/skills/`, `/etc/codex/skills/`. Implicit invocation (description match; names+descriptions pre-loaded under ~8 KB) plus explicit (`$skill-name`, or browse via `/skills`). Optional `agents/openai.yaml` sets display + `allow_implicit_invocation`.
- **Plugins.** Bundle = `.codex-plugin/plugin.json` + `skills/<name>/SKILL.md` + `hooks/hooks.json` — nearly our `.claude-plugin/` layout. Distributed via a marketplace file (`.agents/plugins/marketplace.json`, repo or `~`) or `codex plugin marketplace add <url|path>`; browse with `/plugins`. Public directory "coming soon."
- **AGENTS.md.** The cross-tool standard (donated to the Linux Foundation / AAIF, Dec 2025). Auto-loaded every session. Global `~/.codex/AGENTS.md`, then repo root → CWD, concatenated (closer = later = weighted higher); `AGENTS.override.md` hard-replaces. 32 KiB combined cap (`project_doc_max_bytes`). This is Codex's CLAUDE.md.
- **Hooks.** SessionStart, Pre/PostToolUse, Stop, UserPromptSubmit, Subagent*, Pre/PostCompact, PermissionRequest — `hooks.json` or `[hooks]` in `config.toml`, behind a trust flow. We use none; the optional deep-research hardening hook from the spec would land here.
- **MCP.** First-class: `[mcp_servers.<id>]` in `config.toml`.

## What differs (the adaptations)

- **Commands.** Codex has no user-defined `/name` slash commands. The forward path is **skills invoked as `$name`** (repo-shareable). Old "custom prompts" (`~/.codex/prompts/`, `$ARGUMENTS`) are **deprecated, user-local, and their exact format is UNVERIFIED** across sources. ⇒ Port the three `commands/*.md` as **skills**, not prompts.
- **Argument placeholders.** `$ARGUMENTS`/`$1` in skills are **UNVERIFIED** in official docs ⇒ `stories-ingest` must take its source from the user's message in prose, not a placeholder.
- **Discovery dirs.** Loose Codex skills live in `.agents/skills/`; a plugin bundles them under its own `skills/`. The layouts rhyme; the loose-skill paths differ from Claude Code.
- **CLAUDE.md vs AGENTS.md.** Same idea, opposite walk (Claude Code walks *up* from CWD; Codex concatenates *down* from root), and AGENTS.md provenance is flattened — the model can't tell which file a line came from.

## Still to verify before writing the port

- Exact `.codex-plugin/plugin.json` schema and `marketplace.json` format — `/codex/plugins/build` names them but the field list was not captured. **Do not guess these** — fetch the build doc first (the read-before-write rule applies to our own work too).

## So the port is

Dual-home one repo: add `.codex-plugin/plugin.json` + a thin `AGENTS.md` pointer; share the two core skills as-is; express the three commands as skills; no hooks. The exact file-sharing shape (everything-as-skills vs. dual bundle) is the one open decision.
