# Changelog

One line per merged PR, newest first: what changed for agents or the owner, and why. Decisions behind a change are in `decisions/`.

- **#10** `retro` skill files lessons from a session as `inbox` issues; `scripts/t3-thread.sh` reads a T3 thread by id. The profile says where both live.
- **#9** Repo shape: writing skills to `writing/`, ponytail to `vendor/`. Add `SCOPE.md`, `decisions/`, this changelog and `SOURCES.md`. The GitHub skill keeps only PR, CI and commit-style guides.
- **#8** `scripts/doctor.py` and CI. `profile.md` holds personal setup and is loaded by Claude and Codex. Fixed a dead route to `github-pr-workflow`.
- **#6** Agents load skills from `~/.local/share/kook`, which a 5-minute timer keeps on `origin/main`.
- **#5** `full-cycle`: exercise UI changes in the running app and attach screenshots or recordings to the PR.
- **#4** `html-communicate` moved into `dev-skills/`.
- **#3** `full-cycle` preview step follows the repo's own preview procedure.
- **#2** Agents never merge by default. Docs-only changes still get independent review.
- **#1** `full-cycle` skill, default reviewer routing, `scripts/link-skills.sh`.
