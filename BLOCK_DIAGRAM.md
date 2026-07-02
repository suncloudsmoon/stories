# Block diagram — the `stories` plugin

This repo is a **plugin** that keeps a living, story-shaped wiki of any codebase it's installed into. There is no application code here — the product is a set of markdown rule-files ("skills"), shipped into two AI coding tools (Claude Code and Codex), plus one small health-check script. The map below shows the four parts and how they depend on each other.

```mermaid
flowchart TB
    claude_code_home["Claude Code home\n(manifest + slash commands)"] --> core_skills["Core skills\n(the discipline + the craft)"]
    codex_home["Codex home\n(mirrored bundle)"] -- symlinks --> core_skills
    canon_tooling["Canon & tooling\n(dogfood wiki + lint)"] -. checks .-> claude_code_home
    canon_tooling -. checks .-> codex_home
    click core_skills "docs/stories/systems/core-skills.md"
    click claude_code_home "docs/stories/systems/claude-code-home.md"
    click codex_home "docs/stories/systems/codex-home.md"
    click canon_tooling "docs/stories/systems/canon-tooling.md"
    classDef new fill:#e8f5e9,stroke:#2e7d32;
    class core_skills,claude_code_home,codex_home,canon_tooling new;
```

| block | in plain words | more |
|---|---|---|
| Core skills | The rule-files that are the actual product — how the wiki is kept and how its pages are written | [core-skills](docs/stories/systems/core-skills.md) |
| Claude Code home | The packaging that installs those rules into Claude Code, plus its four `/stories-*` commands | [claude-code-home](docs/stories/systems/claude-code-home.md) |
| Codex home | A mirror of the same plugin for the Codex tool — same rules via symlinks, own packaging | [codex-home](docs/stories/systems/codex-home.md) |
| Canon & tooling | This repo's own wiki (the plugin used on itself) and the script that checks nothing has drifted | [canon-tooling](docs/stories/systems/canon-tooling.md) |

## New since 2026-07-01

All four blocks — the shape-map itself is new (see `docs/stories/sagas/the-map.md`).

---

Deeper: `docs/stories/index.md` (the Atlas).

<!-- derived by the stories plugin — source of truth: docs/stories/systems/ -->
