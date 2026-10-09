# Sol-implemented changes get a Claude reviewer

**Context.** The default reviewer route starts with `gpt-6.1-sol`. When `gpt-6.1-sol` also wrote the change, the review comes from the same model that made it, so it shares the implementer's blind spots even in a fresh context.

**Decision.** Owner-approved exception, in `profile.md`: when `gpt-6.1-sol` implemented the change, review with Claude `claude-opus-5-5` at high effort, falling back to Codex `gpt-6-astra` at high effort if Claude is unavailable or usage-limited. Both run read-only in a fresh context and never edit the fix. The PR and handoff name the reviewer that actually ran and any fallback, with model and effort confirmed from the reviewer's output or logs where they show it. Every other implementer keeps the existing route (`gpt-6.1-sol` high, then OpenCode Muse Spark xhigh). Implementation defaults don't change.

**Why here.** Model names are owner setup, so they go in `profile.md`. `requesting-code-review` already uses a reviewer the task names, or else the owner's routing, so it needs no edit. Scenarios in `evals/requesting-code-review/` check that an agent picks the right route from the profile text.

**Rejected.**
- Naming the exception in `requesting-code-review`: the doctor bans model names in portable skills, and the skill already defers to the profile.
- Claude as reviewer for every implementer: not approved; only Sol implementations change.

**Rollback.** Revert this PR, with the owner's approval like any other change. Until it merges, installed copies keep the old route.
