# dev-skills

Harness-agnostic software-development skills for coding agents (any harness that reads `SKILL.md` folders). Kept deliberately small: only skills that change what an agent does in an implement -> test -> review -> PR cycle.

| Skill | Use it for |
|---|---|
| test-driven-development | RED-GREEN-REFACTOR, tests first |
| systematic-debugging | Find the root cause before fixing |
| long-running-commands | Don't end your turn while a test/build runs; poll until the result is in |
| requesting-code-review | Independent review of your diff before opening the PR |
| github | gh CLI: PRs, issues, CI, review comments |
| full-cycle | Own a task from first edit to open PR with green CI; routes to the skills above |
| html-communicate | Present HTML reports as visual, easy-to-scan pages with working links |

Install once: run `scripts/install-skills.sh` from any kook checkout. It clones kook to `~/.local/share/kook`, the copy agents load skills from, and links each skill there (`~/.claude/skills/*`, `~/.agents/skills`). A systemd user timer then runs `scripts/sync-skills.sh` in that copy every 5 minutes: it fast-forwards to `origin/main` and relinks, so a merged PR goes live on its own. Never work in `~/.local/share/kook`; sync refuses to touch it if it is dirty or off `main`. Check for drift with `~/.local/share/kook/scripts/sync-skills.sh --check`.

Rules for this directory:
- No references to a specific agent harness, orchestrator, harness-specific tool names, or any project/person. Say "search the codebase", not a tool name. Do not assume one language.
- Where a skill mentions subagents, it must also say what to do without them.
- Project facts belong in each project's `AGENTS.md`, not here. The owner's own setup (reviewer models, hosts, machine quirks) belongs in `profile.md` at the repo root.
- `scripts/doctor.py` checks these rules where it can (CI runs it on every PR).
- Add a skill only with evidence an agent needed it. Fewer skills beat more.

Removed 2026-10-02 as noise for this workflow (still in git history): spike, dogfood, stacked-prs, codebase-inspection, node-inspect-debugger, python-debugpy, service-monitoring, linux-user-services.

Attribution: systematic-debugging, test-driven-development and requesting-code-review are adapted from obra/superpowers (MIT); github originates from Hermes Agent (Nous Research, MIT).
