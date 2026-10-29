---
covers: ["codex/**", "AGENTS.md", "CLAUDE.md", ".claude-plugin/**"]
refreshed: 2026-10-29
---

# The Codex Port — Two Homes, One Copy

**The hook.** Shipping to a second tool usually means maintaining a second product. We spent v1 learning that a half-shared port is the worst of both — and 2.0 shares everything but the label on the box.

**The world before.** Research ([[codex-conventions]]) showed Codex speaks the same Agent-Skills standard as Claude Code, so v1 symlinked the two core skills into `codex/`. But the four commands had no Codex equivalent and were rewritten by hand as Codex skills, with a standing rule to keep both copies in sync and a linter check comparing their step titles. The copies drifted anyway — the Codex versions were condensed rewrites from the first day, a second wording of the same procedure — because a sync rule is a fact kept in two places.

**The decision.** Make everything a skill, then symlink everything. Claude Code invokes a plugin's skills as `/stories:stories-init`, the same name the command had, so the procedures moved into `skills/` and `codex/skills/` became pure symlinks. The hooks directory is a symlink too: Codex reads `hooks/hooks.json` from the plugin root and sets `CLAUDE_PLUGIN_ROOT` for compatibility, so one script serves both hosts. The only file kept by hand is the manifest (`codex/.codex-plugin/plugin.json#"skills"`), and the linter checks it against its twin. The repo guide followed the same rule: `AGENTS.md` holds it, and `CLAUDE.md` is a single import (`CLAUDE.md#@AGENTS.md`).

**What it means.** Drift between the homes is no longer something to guard against; it is structurally impossible outside two manifests. A new skill needs one thing in `codex/`: a symlink. If you ever find yourself writing Codex-specific prose, stop — name both invocation forms in the shared file instead.

See [[the-gate]] for the hooks both homes share, [[the-lint]] for the manifest and symlink checks.
