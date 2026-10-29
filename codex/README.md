# stories — Codex bundle

The Codex packaging of **stories** — the same plugin as the repo root, not a port. What the plugin does: [the root README](../README.md).

## What's here

- `.codex-plugin/plugin.json` — the Codex manifest, the one file kept by hand (the linter checks it against `.claude-plugin/plugin.json`).
- `skills/stories`, `skills/stories-init`, `skills/stories-refresh` and `hooks/` — **symlinks** to the repo root. One copy; they cannot drift. Invoke the skills as `$stories-init` and `$stories-refresh`.
- The hooks need `python3` on your `PATH`, and Codex asks once to trust them.

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

Everything except the manifest is a symlink, so there is nothing else to sync. When the Claude Code manifest changes, mirror it in `.codex-plugin/plugin.json`; `python3 scripts/lint-canon.py` flags any drift.
