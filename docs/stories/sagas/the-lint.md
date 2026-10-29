---
covers: ["scripts/**", ".github/**", "skills/stories-refresh/SKILL.md"]
refreshed: 2026-10-29
---

# The Lint — Making Drift Visible

**The hook.** A wiki kept by a model can fall behind the code without anyone noticing. Lint is the canary — it makes that drift *visible* without pretending to prevent it.

**The world before.** v1's linter grew one check at a time, and many of them policed copies: the Atlas's inline `covers:` against each page's frontmatter, the default-exempt list across three files, each command against its Codex twin. Every check was correct, and every one existed because a fact lived in two places. A checker that mostly referees duplicates is a symptom, not a safeguard.

**The decision.** 2.0 deleted the copies, and their checks went with them. What remains checks only facts that can rot on their own: `[[links]]` that point nowhere, `covers:` globs that match nothing or span lines the gate can't read, anchors whose text has left the file (`scripts/lint-canon.py#def check_citations`), pages missing from the Atlas, `ARCHITECTURE.md` links, and — in this repo — the two manifests and the Codex symlinks. It reads `covers:` with the hook's own parser (`scripts/lint-canon.py#One parser for covers:`), so it can never accept a line the gate can't read. A story whose covered files were committed after its `refreshed:` date gets a REVIEW line, which is exactly the work list `stories-refresh` starts from (`skills/stories-refresh/SKILL.md#its REVIEW lines are this list`). Each verdict is proven on a throwaway canon (`scripts/lint-canon.py#def self_test`), and CI runs both self-tests before the lint itself (`.github/workflows/lint.yml#Self-tests`).

**What it means.** Lint diagnoses; refresh treats. The script is dev tooling, not something the plugin ships — users get the skills and the hook. The standing test still holds: if lint passes while the canon is plainly wrong, a check is missing; but if a new check would compare two copies of a fact, delete a copy instead.

See [[the-gate]] for what a dead `covers:` does to the hook, [[codex-port]] for the two homes it watches.
