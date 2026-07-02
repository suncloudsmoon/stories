---
title: The Codex Port — One Soul, Two Homes
kind: saga
covers: ["codex/**", "AGENTS.md"]
links: ["[[origin]]", "[[the-gate]]", "[[codex-conventions]]", "[[the-lint]]"]
refreshed: 2026-07-01
---

# The Codex Port — One Soul, Two Homes

**The hook.** Porting to Codex was supposed to be the hard part — a second tool, a second format, a second thing to keep alive. It turned out to be mostly a symlink and a manifest, because the bet we made on day one paid off.

**The world before.** The skill-only decision ([[the-gate]]) was made *for* this moment: keep the discipline in portable `SKILL.md` prose, not in Claude-Code-only hooks, so it could travel. When the time came, research ([[codex-conventions]]) confirmed Codex speaks the same Agent-Skills standard — same `name`/`description`, same auto-selection. The two core skills could move with zero rewriting.

**The decision.** A **separate bundle** in `codex/`, not a merged dual-manifest repo — the maker chose to leave the shipped Claude Code plugin untouched. To honor that without paying the drift tax the choice invites, the two core skills are **symlinks** back to the root `skills/` (`codex/skills/stories` → `../../skills/stories`): one source of truth, physically unable to diverge. Only the genuinely host-specific parts are new — a `codex/.codex-plugin/plugin.json` manifest, and the commands re-expressed as Codex skills (`codex/skills/stories-*/SKILL.md`), because Codex has no user-defined `/commands` and invokes them as `$stories-init` instead. A root `AGENTS.md` gives Codex the same dogfood discipline `CLAUDE.md` gives Claude Code.

**What it means.** Two homes, one soul — but the seams need tending. The symlinked core can't drift; the command skills and the two manifests *are* duplicated, so **drift is now the failure mode to guard against** — which is what [[the-lint]] exists to catch. The standing rule, written into `CLAUDE.md`, `AGENTS.md`, and each command skill: *when the Claude Code plugin changes, update `codex/` to match.* If you ever find the two homes telling different stories, the canon has already failed — refresh, and make them one again.

See [[the-gate]] for why the port was cheap, [[codex-conventions]] for the Codex specifics.
