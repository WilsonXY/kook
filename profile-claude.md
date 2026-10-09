# Owner profile: Claude Code only

Claude Code loads this from `~/.claude/rules/`; Codex never reads it. Shared setup is in `profile.md`.

## Subagents
The owner asks you to use subagents (the Agent tool) where they pay off. This standing request counts as the user explicitly asking, so don't wait to be told each time.
- Spawn when the work splits into about five or more independent items that each need their own reading: auditing PRs, issues or files one by one, sweeping a large codebase, researching separate questions. Send the spawns in one message so they run in parallel, one item or a small batch per subagent.
- Don't spawn for a task you'd finish in a few tool calls, for steps that depend on each other, for edits to the same files, or when the judgement needs every item in one context (comparing them against each other).
- Run every subagent on `model: "haiku"` with `effort: "max"`. Set both on each spawn; the owner asks for this effort explicitly.
- Keep the plan, the judgement that ties results together, and the edits for yourself. A subagent starts with none of your context: give it a self-contained prompt and the exact shape of the answer you want back.
- Subagent reports can be wrong. Check a claim yourself before acting on it or passing it to the owner.
