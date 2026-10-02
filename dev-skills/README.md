# dev-skills

Harness-agnostic software-development skills. Each folder is a `SKILL.md` (plus optional `references/`, `scripts/`, `templates/`) that any coding agent can read: Claude Code, Codex, OpenCode, Antigravity, T3 Code, Hermes, etc.

Rules for this directory:
- No references to a specific agent harness, orchestrator, tool name (`delegate_task`, etc.) or project.
- Where a skill mentions subagents, it must also say what to do without them.
- Project facts belong in each project's `AGENTS.md`, not here.

| Skill | Use it for |
|---|---|
| systematic-debugging | Find the root cause before fixing |
| test-driven-development | RED-GREEN-REFACTOR, tests first |
| spike | Throwaway experiments before committing to a build |
| codebase-inspection | LOC / language stats with pygount |
| dogfood | Exploratory QA of a web app |
| node-inspect-debugger | Debug Node.js with --inspect / CDP |
| python-debugpy | Debug Python with pdb / debugpy |
| github | gh CLI: PRs, issues, reviews, CI, repo management |
| stacked-prs | Rebase / retarget stacked or conflicting PRs |
| linux-user-services | Run daemons without root (systemd --user) |
| service-monitoring | Downtime alerting for a hosted service |

Attribution: systematic-debugging and test-driven-development are adapted from obra/superpowers (MIT); spike from gsd-build/get-shit-done (MIT); github, dogfood, debugger and inspection skills originate from Hermes Agent (Nous Research, MIT).
