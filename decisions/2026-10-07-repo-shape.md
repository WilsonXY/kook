# Repo shape: buckets, records, GitHub trim

**Context.** Kook mixed dev skills, writing skills and a vendored skill at the root, and kept decisions only in PR bodies.

**Decision.**
- Writing skills move to `writing/`, ponytail to `vendor/`. `dev-skills/` keeps its name.
- `SCOPE.md`, `decisions/`, `CHANGELOG.md` and `SOURCES.md` hold the bar, decisions, history and borrowed work.
- The GitHub skill keeps `pr-workflow`, `ci-troubleshooting` and `conventional-commits`. Outside sessions auditing Kook, only `pr-workflow.md` was ever opened; the other 9 references, the templates and the auth scripts were never read.

**Why.** Renaming `dev-skills/` would break the live sync, the `~/.agents/skills` link and per-project links for no behaviour gain.

**Rejected.**
- Splitting the writing skills into their own repo: two installs for one owner.
- Splitting `full-cycle` into phase files now: deferred until behaviour evals existed, because it is the most-used skill. Tried in #19 and dropped: see `2026-10-09-full-cycle-not-split.md`.
