---
title: Canon & tooling — the wiki and its canary
kind: system
covers: ["scripts/*.py"]
links: ["[[the-lint]]", "[[origin]]", "[[the-map]]"]
refreshed: 2026-07-01
---

# Canon & tooling

The repo's own wiki (`docs/stories/` — this very canon) and the one script allowed to exist. This segment exists because a best-effort discipline needs a canary ([[the-lint]]).

- `docs/stories/` — the dogfood canon: Atlas, log, origin, sagas, this systems layer, library.
- `scripts/lint-canon.py` — read-only health-check: links, covers, citations, staleness, manifest + command drift, coverage, and the systems layer itself. Dev/CI tool only — it ships to no one.

**Boundaries.** The script may diagnose, never treat, and never becomes plugin runtime — the skill-only invariant ([[the-gate]]) holds. If lint passes while the canon is plainly wrong, a check is missing: add one.

Why the exception is allowed: [[the-lint]].
