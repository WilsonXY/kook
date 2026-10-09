# Claude Code uses Haiku subagents for fan-out work

**Context.** In the 14 days to 2026-10-10, 2 of 66 Claude Code sessions on this machine spawned any subagent, and none chose a model, including sessions with 200 to 490 tool calls. Claude Code's Agent tool description tells the model not to spawn unless the user asks, and that a "thorough" or many-part task is no such request. The owner wants Claude to fan out to cheap subagents the way Theo's PR-audit prompt does: Haiku 5.5 at max effort (owner, thread 6bf1af55). Codex should not get this rule.

**Decision.** `profile-claude.md` holds Claude-Code-only setup. `sync-skills.sh` links it as `~/.claude/rules/kook-profile.md`, which Claude Code loads at session start and Codex never reads. Its first rule: a standing request to spawn subagents for five or more independent items that each need their own reading, on `model: "haiku"` with `effort: "max"`, while the main agent keeps the plan, the cross-item judgement, the edits, and checks claims before acting on them.

**Evidence.** `claude -p --model opus` in a throwaway config dir, with and without the rule, read-only:
- Audit the last 12 merged PRs (verification stated? CHANGELOG line matches diff?): 0 spawns in 2 runs without; 6 Haiku/max spawns in 2 of 2 runs with. With the rule both runs read every diff; without, one run spot-checked 3 diffs. One run with the rule caught and corrected a wrong subagent finding. Cost about $1.00 vs $0.50 per run; one run with the rule took 8 minutes against about 1.5.
- Two-sentence question about one script: 0 spawns with or without, as intended.
- A first wording ("standing request", no size threshold, no "counts as the user asking") spawned nothing on a 13-skill audit, the same as no rule.

**Rejected.**
- A "Claude only" section in `profile.md`: Codex loads that file too and would read it.
- An `@import` line in `profile.md`: Codex would see a stray line, and Claude Code already loads `~/.claude/rules/` on its own.
- Letting the model pick a subagent model per piece: the owner asked for Haiku at max effort for every subagent. Reopen if a session shows Haiku failing a piece that needed a stronger model.
