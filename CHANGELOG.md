# Changelog

One line per merged PR, newest first: what changed for agents or the owner, and why. Decisions behind a change are in `decisions/`.

- **#25** `full-cycle`: the PR body and the report open with a few plain sentences for the owner (what changes, the risk, the decision needed), leave out labels coined in the session, and put test and reviewer details after. `profile.md` keeps reviewer proof to one line in the PR. A Codex PR about database changes was unreadable to the owner; on a scenario built from it, `gpt-6.1-sol` passed 0 of 3 runs before and 3 of 3 after (see `decisions/2026-10-10-pr-body-for-the-owner.md`).
- **#24** Claude Code gets `profile-claude.md`, linked into `~/.claude/rules/` so Codex never reads it. Its first rule: fan out five or more independent items (PRs, files, questions) to subagents on Haiku at high effort, and keep judgement and edits in the main agent. On a 12-PR audit, 0 of 2 runs spawned subagents without it and 2 of 2 with it (see `decisions/2026-10-10-claude-subagents.md`).
- **#23** Reviewer routing: when `gpt-6.1-sol` implemented a change, review with Claude `claude-opus-5-5` (high), falling back to Codex `gpt-6-astra` (high); other implementers keep the Sol-then-OpenCode route. Three `requesting-code-review` scenarios check the choice (see `decisions/2026-10-10-sol-implementer-review-route.md`).
- **#22** Every bucket is installed: `writing/` and `vendor/` skills link into `~/.claude/skills/` and `~/.agents/skills/` like `dev-skills/`, and `~/.agents/skills` is now a folder of links, so installers writing there no longer dirty the live copy. `doctor.py` fails on duplicate skill names; `eval.sh --with <skill>` tests two skills together. ponytail next to `full-cycle` made no scenario worse (see `decisions/2026-10-10-install-every-bucket.md`).
- **#21** `wilson-humanizer`: the Lever 3 "Do write" example keeps the same facts as "Don't write", so it no longer teaches adding details (review note on #20).
- **#20** Report server binds to `127.0.0.1` with backups kept out of the served folder; `html-communicate` says when it couldn't render a page; `wilson-humanizer` never invents specifics and flags unsupported claims. HumanLayer's show-me added unchanged to `vendor/`; the proposed rewrites are rejected (see `decisions/2026-10-09-borrow-reviews-small-fixes.md`).
- **#19** `eval.sh --skill-only` tests the worst case where an agent reads only `SKILL.md`. A trial split of `full-cycle` was dropped (see `decisions/2026-10-09-full-cycle-not-split.md`).
- **#18** CI pins shellcheck v0.11.0 by checksum, the same binary as local runs, so lint results match (inbox #16).
- **#17** `html-communicate`: lead with the recommendation and what stays unchanged, show one before -> action -> result example, omit unrequested speculative alternatives, and give a reading order when delivering several pages (inbox #12, #13).
- **#15** Behaviour evals: `scripts/eval.sh` grades a skill on a scenario with two fresh agents (task without criteria, then a judge). Six scenarios in `evals/`, from inbox #12–#14 and two decisions; the doctor checks their format.
- **#11** Re-landed #10 on `main` (it had merged into #9's branch).
- **#10** `retro` skill files lessons from a session as `inbox` issues; `scripts/t3-thread.sh` reads a T3 thread by id. The profile says where both live.
- **#9** Repo shape: writing skills to `writing/`, ponytail to `vendor/`. Add `SCOPE.md`, `decisions/`, this changelog and `SOURCES.md`. The GitHub skill keeps only PR, CI and commit-style guides.
- **#8** `scripts/doctor.py` and CI. `profile.md` holds personal setup and is loaded by Claude and Codex. Fixed a dead route to `github-pr-workflow`.
- **#6** Agents load skills from `~/.local/share/kook`, which a 5-minute timer keeps on `origin/main`.
- **#5** `full-cycle`: exercise UI changes in the running app and attach screenshots or recordings to the PR.
- **#4** `html-communicate` moved into `dev-skills/`.
- **#3** `full-cycle` preview step follows the repo's own preview procedure.
- **#2** Agents never merge by default. Docs-only changes still get independent review.
- **#1** `full-cycle` skill, default reviewer routing, `scripts/link-skills.sh`.
