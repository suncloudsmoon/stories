# Why `stories` exists

**The hook.** Code says *what*. It almost never says *why* — and the why is the first thing to rot. A month later the comment is stale, the author is gone, and the next change quietly betrays a decision no one remembered making.

**The world before.** The LLM-wiki pattern showed that an LLM will happily do the bookkeeping humans abandon: read a source, file it, cross-reference it, keep a knowledge base *true* as it grows. The real insight was that maintenance — not reading, not thinking — is what kills a wiki, and maintenance is exactly what an LLM doesn't get bored doing. `stories` takes that engine and repoints it: instead of cataloguing external sources, it keeps the **soul of a codebase** — the intent, the tensions, the roads not taken.

**The decision.** A *story* is a work of art with a job: carry the why tightly enough that a reader gets it in one pass. The model reads the covering story before it reshapes anything, and rewrites it in the same breath after — so the canon never drifts behind the code. The discipline is written in a skill and armed by a hook ([[the-gate]]): the skill says *what* to do, the hook says *when*.

**The maker's decrees** — the preferences this project is built to honor, kept here as lore:
- *Low friction over ceremony.* Reading is silent; the model asks only on a real conflict, or when something genuinely deserves your attention. Doubt does not stop the work.
- *Auto over manual.* Keeping the canon true is part of doing the work, not a chore you trigger. Deep research files itself into the library.
- *Delete without fear.* Stale canon is worse than none. `stories-refresh` prunes hard.
- *One graph.* Code-soul and knowledge live in the same interlinked web, so a finding can point at the code it shaped ([[one-graph]]).
- *Grounded, with room for myth.* Rooted in real code and cited; a mythic frame is allowed only when it makes a hard idea land ([[the-craft]]).
- *Simple enough for any model.* Every fact lives in exactly one place, and the procedure fits on one screen. A rule a model cannot follow on first read is a rule it will break — and a fact kept in two places is a fact that will disagree with itself.

**What it must never become.** A changelog. A verbose auto-doc that restates the code — the map ([[the-map]]) restates *shape* at block granularity, and the moment it reads like a directory listing it has failed. A nagging gate that interrupts. A place where the model invents soul it was never told.

**What success looks like.** Someone — a teammate, or a future model with no memory of today — opens `docs/stories/`, reads for five minutes, and *understands* this project: not just how it's wired, but what it values and what would break its heart. And the canon is still true, because keeping it true cost almost nothing.
