# stories — Codex bundle

The Codex plugin packaging of **stories**. The Claude Code version lives at the repo root; this is the Codex port. Same behavior, Codex-native shape.

## What's here

- `.codex-plugin/plugin.json` — the Codex plugin manifest (`skills: "./skills/"`).
- `skills/stories`, `skills/writing-a-story` — **symlinks** to the repo-root `skills/`. Single source of truth; they cannot drift.
- `skills/stories-init`, `skills/stories-refresh`, `skills/stories-ingest`, `skills/stories-lint` — the commands, as Codex skills. Codex has no user-defined `/commands`, so these are invoked as `$stories-init` … `$stories-lint` (or auto-selected by description).

## Install

Codex distributes plugins through a marketplace. Once this repo is pushed:

```bash
codex plugin marketplace add suncloudsmoon/stories
# then browse/enable installed plugins:
/plugins
```

To register via a marketplace file, add an entry pointing at this bundle with a git-subdir source and path `./codex`:

```json
{
  "name": "suncloudsmoon",
  "plugins": [
    {
      "name": "stories",
      "source": { "source": "git-subdir", "url": "https://github.com/suncloudsmoon/stories.git", "path": "./codex", "ref": "main" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

(Kept inline rather than as a committed live marketplace file: the local-source form requires the bundle to sit inside the marketplace root, which a repo-root `codex/` does not, so the git-subdir form above is the right shape — copy it into your marketplace once the repo is pushed.)

## Keeping in sync

When the Claude Code plugin changes, update this bundle to match. The two core skills are symlinked (auto-synced). The command skills here mirror the root `commands/*.md`, and the manifest mirrors `.claude-plugin/plugin.json` — both must be hand-synced. `python3 scripts/lint-canon.py` checks for drift.
