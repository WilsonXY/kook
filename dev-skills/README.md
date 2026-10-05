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

Install: run `scripts/link-skills.sh` (repo root) after every pull. It links each skill into `~/.claude/skills/` (user level, so every worktree sees them). Re-running is safe: it adds new skills and removes links to deleted ones.

Rules for this directory:
- No references to a specific agent harness, orchestrator, harness-specific tool names, or any project/person. Say "search the codebase", not a tool name. Do not assume one language.
- Where a skill mentions subagents, it must also say what to do without them.
- Project facts belong in each project's `AGENTS.md`, not here.
- Add a skill only with evidence an agent needed it. Fewer skills beat more.

Removed 2026-10-02 as noise for this workflow (still in git history): spike, dogfood, stacked-prs, codebase-inspection, node-inspect-debugger, python-debugpy, service-monitoring, linux-user-services.

Attribution: systematic-debugging, test-driven-development and requesting-code-review are adapted from obra/superpowers (MIT); github originates from Hermes Agent (Nous Research, MIT).
