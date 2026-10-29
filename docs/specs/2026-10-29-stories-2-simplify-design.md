# Design Spec — stories 2.0: one fact, one place

**Date:** 2026-10-29
**Status:** Approved by the maker (hooks: both; backwards compatibility: none)
**Supersedes:** `2026-06-14-stories-plugin-design.md` and `2026-07-01-systems-layer-design.md` (kept as history). Still binding from them: conflict-only asking (#4), auto-authoring in the same session (#5), light spine (#6), read-before-write (#11), dormant by default (#14). **Reversed:** skill-only (#2) — see §4.3.

---

## 1. Intent

The maker wants the plugin **simpler, so LLMs find it easier to use**. The test: a model with no memory reads the skill once and does the right thing — few judgment calls, few files to keep in sync, nothing it must decode.

v1 fails that test in one recurring way: the same fact lives in several places, and a growing linter polices the copies. `covers:` sits on every page *and* in the Atlas. The exempt list lives in three files. Command procedures exist twice (Claude Code, Codex) and have already drifted. Titles repeat the H1, `links:` repeats the body's `[[links]]`, `kind:` repeats the folder. Line-number citations repeat what the code already knows — and go wrong on every edit above them, which is why the model spends subagents repairing them. The shape is stated twice (system pages *and* a derived `ARCHITECTURE.md`), and the log repeats git history.

**The principle: every fact lives in exactly one place.** Delete the copies and the checks that police them go with them.

Two supporting rules: the procedure fits on one screen; and the harness, not the model's memory, says *when* to read a story.

## 2. Evidence

- **Anthropic.** *Effective context engineering* (2025-09-29): "the smallest set of high-signal tokens"; lightweight identifiers resolved just-in-time. *Agent Skills* (2025-10-16): progressive disclosure. *Agent Harness Design* (Lance Martin, 2026-04-02): "what can I stop doing?" Claude Code docs: plugin skills are invoked as `/plugin:skill` — the name a plugin command already has — and may carry reference files loaded on demand.
- **Codex parity.** Codex now runs plugin hooks by default from the same `hooks/hooks.json`, honors exit-2 blocking, `hookSpecificOutput.additionalContext`, Stop `decision: block`, and sets `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA` "for compatibility with existing plugin hooks". The one reason v1 refused hooks — portability — is gone.
- **Graphify on Reddit.** −8.9% output tokens under Codex; called 3 times in 15 tasks under Claude Code; one tester measured it costlier than baseline; users report Claude ignores it and its hooks are "spammy". Lesson: don't fire on searches; don't ask the model to adopt a new tool. **Non-goal.**
- **Prior art** (`.ref/prior-art/stories-2.md`): Claude Code path-scoped rules, Cursor `globs`, Kiro `fileMatch`, Windsurf, Cline, Copilot all load glob-scoped docs — Claude Code's fires on **Read**, before any edit. Plugins can't ship those rules and Codex has none, so a hook is the only cross-host gate. Adopted: fire on Read; thin pointers; one-line reminders; ambiguous-anchor lint (Swimm, matklad); an Invariants list (matklad); `*(inferred)*` marks (Graphify confidence tags).
- **This repo today (≈ chars ÷ 4).** Always-on descriptions (6): 341 tokens. Discipline skill body: 2,322. Atlas: 544. 12 line citations, every one naming a heading, constant, or key.

## 3. Goals, non-goals, anti-goals

**Goals:** one home per fact; a one-screen procedure; the harness points at the story (no model judgment for reading); zero model effort on citation upkeep; no hand-synced prose between the two homes; fewer tokens always-on and per change.

**Non-goals:** Graphify, code indexes, MCP servers; generated per-harness rule stubs; backwards compatibility with v1 canons or command names; shipping the linter to users.

**Anti-goals:** losing the soul — stories still carry the why, to the full craft bar; a hook that speaks on every read or search; a hook bug that blocks the user's work (it fails open).

## 4. The design

### 4.1 What ships (one copy, both homes)

```
hooks/hooks.json            # PostToolUse Read · PreToolUse edits · Stop
hooks/stories.py            # the gate (stdlib Python 3); --self-test
skills/stories/SKILL.md     # the discipline — one-screen procedure + conventions
skills/stories/writing.md   # the craft + ARCHITECTURE.md format — loaded only when writing
skills/stories-init/SKILL.md     # /stories:stories-init · $stories-init
skills/stories-refresh/SKILL.md  # /stories:stories-refresh · $stories-refresh
codex/hooks -> ../hooks ; codex/skills/<each> -> ../../skills/<each>
```

Removed: `commands/`, `skills/writing-a-story/`, `stories-lint`, `stories-ingest`, the hand-written Codex command skills. The two manifests are the only hand-synced pair; the linter checks them. Skill text names both invocations where needed, so one file serves both hosts.

### 4.2 The canon on disk

```
ARCHITECTURE.md       # summary · Mermaid diagram · block table → stories · invariants · marker
docs/stories/
  index.md            # the Atlas: - [[name]] — hook   (grouped: Origin · Sagas · Library)
  origin.md           # why the project exists
  sagas/              # code stories
  library/            # knowledge — research, sources, concepts
```

Frontmatter carries only facts nothing else holds:

```yaml
---
covers: ["src/auth/**", "src/session.ts"]   # stories: one line, flow style
refreshed: 2026-10-29                        # stories: last verified against the code
---
```
```yaml
---
sources: ["https://…", "docs/notes.pdf"]     # library pages (optional)
---
```

- **A page with `covers:` is a story and gates. Nothing else gates.** This replaces the eight-row kinds table.
- The title is the H1. Links are the body's `[[links]]`. The folder says what a page is. `refreshed:` records when the story was last verified — a fact git cannot know.
- No `log.md` (git history is the chronicle). No `systems/` pages, no vignettes.
- `ARCHITECTURE.md` (repo root): one plain-language paragraph; one top-level Mermaid diagram; a block table — block · one plain line with its boundary · link to the story carrying its why; a short **Invariants** list ("X must never depend on Y"); the `<!-- derived by the stories plugin -->` marker. Never overwrite a hand-written `ARCHITECTURE.md` (no marker) — surface it.

### 4.3 The hooks (`hooks/stories.py`)

One script, three events, stdlib only. Dormant (exit 0, no output) when the project has no `docs/stories/`. Reads each story's one-line `covers:` and H1. State per session in `$CLAUDE_PLUGIN_DATA` (else the temp dir): which stories were announced, which covered files were edited, which stories were touched, which were reminded.

1. **PostToolUse · Read.** When the model reads a covered file whose story wasn't announced this session, add context: ``"`src/auth/token.ts` is covered by docs/stories/sagas/auth.md — “Why tokens rotate”. Read it before you change this file."`` Reading a story file itself marks it announced. Silent otherwise.
2. **PreToolUse · Edit|Write|MultiEdit|NotebookEdit|apply_patch.** Targets come from `tool_input.file_path` / `notebook_path`, or the `*** Add|Update|Delete File:` lines of an `apply_patch` command. Edits under `docs/stories/` mark that story touched. For a covered target: record the edit; if a covering story was never announced, announce it now and **block this one edit** (exit 2): "Before editing `<file>`, read docs/stories/sagas/x.md — “<H1>”. Then retry." This is the fallback for edits with no prior Read (Codex patches, new files).
3. **Stop.** If `stop_hook_active`, exit. If covered files were edited and their story was neither touched nor reminded, remind once (`decision: block`): "You changed `<files>`, covered by docs/stories/sagas/x.md. If the why changed, rewrite it and set `refreshed:` to today; if not, you're done."

Every message is one line and names the page — a thin pointer, never the page body. Any internal error exits 0: the hook never blocks work because of its own bug. Glob matching is a small `**`/`*`/`?`→regex translator (Python ≥ 3.9; `glob.translate` is 3.13+), exercised by `--self-test`. *shortcut: invoked as `python3`; Windows without `python3` on PATH gets no gate — add `commandWindows` if users ask.*

### 4.4 The procedure (`skills/stories/SKILL.md`)

Dormant without `docs/stories/`; suggest `stories-init` at most once.

**Before you change code:** when the hook names a story, read it before changing that file. (No hook running? `grep -rn "^covers:" docs/stories` finds them.) If the request contradicts a story — or two stories contradict each other — stop and ask. Otherwise proceed; doubt does not stop you.

**After:**
1. The why changed → rewrite the story (read `writing.md` first), set `refreshed:` to today. New code with a why worth keeping → new saga.
2. Added, removed, or rewired a block → update `ARCHITECTURE.md`.
3. Added, removed, or renamed a page → update its Atlas line.
4. The repo has `scripts/lint-canon.py` → run it and fix what it flags.

**Filing knowledge:** when deep research completes, or the user hands you a source to keep, write a `library/` page and its Atlas line — no asking.

**Citations are anchors:** `` `path#anchor` `` — text that appears verbatim in the file (a symbol, heading, or key), resolved with `grep -n`. Never line numbers. Checking citations is a grep or the linter — never a file read, never a subagent.

### 4.5 `writing.md` (the craft)

Read-before-write; the light spine (hook → world before → decision & why → what it means → links); the quality bar; anchors; mark a why you inferred — rather than heard from the maker or read in a commit or spec — as `*(inferred)*`; the bar by folder (sagas and origin: full soul; library synthesis: full soul; a raw source: faithful and tight); the `ARCHITECTURE.md` format; the exemplar.

### 4.6 `stories-init` and `stories-refresh`

**Init:** refuse to clobber an existing `docs/stories/`; create `index.md`, `sagas/`, `library/`; interview the maker one question at a time (pull what's on record first); write `origin.md`; write `ARCHITECTURE.md` (never over a hand-written one); optionally sagas where the why is evident; run the linter if present; report the tree.

**Refresh:** (1) find stale stories — a covered file's last commit date newer than `refreshed:` (the linter's REVIEW lines give the list; without git, all); (2) re-read only those, then rewrite, confirm, or delete, and set `refreshed:`; (3) mechanical pass over every page — globs match, anchors resolve, `[[links]]` resolve — by grep or linter; (4) prune dead pages and orphans, merge duplicates, surface contradictions; (5) rebuild the Atlas, update `ARCHITECTURE.md` if the shape moved, run the linter, report.

### 4.7 The linter (`scripts/lint-canon.py`, dev/CI)

Errors: a `[[link]]` with no page; a `covers:` glob matching no file; `covers:` not single-line; a story without a valid `refreshed:`; an anchor whose text is gone or whose file is missing; any line citation; a page missing from the Atlas or an Atlas entry with no page; `ARCHITECTURE.md` (with marker) linking a missing page; manifest drift; a Codex symlink that doesn't resolve; `hooks/hooks.json` that doesn't parse.
Warnings: an anchor matching more than once; REVIEW — a covered file committed after `refreshed:` (commits only, names the file); an orphan page.
`--self-test` builds a temporary canon and asserts each verdict. Plugin-only checks skip themselves in user repos. CI runs both self-tests and the lint.

### 4.8 One home for each repo document

The rules live only in `skills/stories/SKILL.md`; `README.md` describes the plugin and links there. `AGENTS.md` is the single repo guide (host-neutral, both invocation forms); `CLAUDE.md` is the line `@AGENTS.md`. `codex/README.md` shrinks to Codex install steps plus a link.

## 5. This repo's canon (dogfood)

- **Origin:** add the decree *Simple enough for any model: one fact, one place.* No new saga.
- **Rewrite to the new truth:** `the-gate` (hooks, and why the skill-only decision was reversed), `one-graph` (covers-or-not replaces kinds), `the-craft` (`writing.md`; anchors; `*(inferred)*`), `codex-port` (everything symlinked; manifests only), `the-lint` (the new check set; self-tests), `the-map` (the shape is one file).
- **Fold** the four `systems/` pages into `ARCHITECTURE.md`; delete them and `vignettes/`. Re-home their `covers:` (`.github/**` → `the-lint`; `.claude-plugin/**`, `CLAUDE.md` → `codex-port`).
- **Trim** frontmatter to `covers:` + `refreshed:` / `sources:`; convert the 12 citations to anchors; rebuild the Atlas; **delete `log.md`**.
- `CHANGELOG.md` 2.0.0 entry; both manifests → `2.0.0`. The two older specs get a dated "superseded by" note at the top.

## 6. Verification

1. `python3 hooks/stories.py --self-test`, `python3 scripts/lint-canon.py --self-test`, and `python3 scripts/lint-canon.py` exit 0; both scripts compile clean (`pyflakes` if available, else `py_compile`); manifests and `hooks/hooks.json` parse; Codex symlinks resolve.
2. **Hook, live:** pipe recorded event JSON through the hook against this repo — Read of a covered file announces once; an unannounced edit blocks once; Stop reminds once, then stays quiet.
3. **Drift demo:** insert ten lines atop a cited file in a scratch copy — line citations go silently wrong, anchors still resolve.
4. **Token table:** always-on descriptions, `SKILL.md` body, Atlas — before vs after.
5. **Easier for LLMs:** a fresh Haiku subagent given only the new `skills/stories/SKILL.md` answers three scenarios — (a) the hook said `scripts/lint-canon.py` is covered by `the-lint`, and you're adding a check; (b) the user pastes a research summary to keep; (c) you renamed a block's main module. Pass = it names the right steps. A failing scenario means the prose is unclear and gets rewritten until it passes.

## 7. Left to the builder

Exact prose of every skill and story (meaning per this spec; the craft bar holds); anchor text; `ARCHITECTURE.md` contents; the self-tests' shape (stdlib only); state-file format.
