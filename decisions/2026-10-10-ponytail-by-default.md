# Ponytail at full on every coding task

**Context.** The owner wants every coding task to use `ponytail` at full intensity (thread 1510a373). It has been installed since #22, but agents rarely pick it on their own. In the 14 days to 2026-10-10, Claude Code loaded `full-cycle` in 12 sessions and `ponytail` in none; Codex read `full-cycle` in 35 sessions and `ponytail` in 6.

**Decision.** `profile.md` tells every agent to load `ponytail` at full next to `full-cycle` on any coding task, unasked, and says ponytail shortens the code, never the workflow (tests, review, PR). `vendor/ponytail` stays unmodified.

**Evidence.** `claude -p --model claude-opus-5-5 --permission-mode plan` in a throwaway config with every Kook skill installed, task "`formatPrice(1.5)` returns `$1.5` instead of `$1.50`. Fix it.", 3 runs each. Old profile: 0 of 3 loaded `ponytail` (or `full-cycle`). New profile: 3 of 3 loaded `ponytail` with `full` and `full-cycle`, and all three plans still wrote a failing test first, planned a review and named the PR step. `eval.sh` cannot test this: it isolates the agent from the profile.

**Rejected.**
- Editing `vendor/ponytail`: vendor skills stay unmodified, and its description already says "use on ANY coding task".
- Putting it in `profile-claude.md`: Codex should apply it too.
