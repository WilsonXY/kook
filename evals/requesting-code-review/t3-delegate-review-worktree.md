---
skill: requesting-code-review
from: "https://github.com/WilsonXY/kook/issues/38"
---
## Task
You are running as Claude `claude-opus-5-5` inside T3 Code, and you implemented the change on branch `feat/retry-backoff`: it adds retry with backoff to an HTTP client. Tests and lint pass. Your last fix, to `client.py`, is not committed yet. The task names no reviewer. Your harness gives you this tool, and the Codex provider with model `gpt-6.1-sol` is available through it:

> `delegate_task`: Delegate one task to a T3-owned child agent of THIS thread and run it with only the supplied task prompt. Choose providers and models from orchestrator_capabilities. Set isolation to worktree for a separate checkout based on the parent local commit; uncommitted edits are not copied; omitted isolation shares the parent checkout. Provider, model, model options, runtime mode and interaction mode inherit unless target overrides them. Parameters: `task`, `role` (implementation, research, review, design, test, general), `isolation` (shared, worktree), `target` (`providerInstanceId`, `model`, `options` such as `reasoningEffort`), `runtimeMode`, `interactionMode`, `mode` (async, wait). An async child's completion wakes this thread.

Your global instructions from the owner contain this section:

> ## Reviewer routing
> Used by `requesting-code-review` when the task names no reviewer. Unless the exception below applies, try in order:
> 1. Codex CLI, model `gpt-6.1-sol`, reasoning effort high, run non-interactively at the repo root (`codex exec`, in a pseudo-terminal if needed), read-only.
> 2. Fallback if Codex is unavailable (usage limit, not installed): OpenCode CLI, model `opencode/muse-spark-1.3-contributor-free`, effort xhigh (`opencode run`).
>
> Exception: when `gpt-6.1-sol` implemented the change (wrote the diff, itself or as a delegated child), use this route instead, each in a fresh read-only context:
> 1. Claude Code CLI, model `claude-opus-5-5`, effort high (`claude -p --model claude-opus-5-5 --effort high --permission-mode plan`).
> 2. Fallback if Claude is unavailable or usage-limited: Codex CLI, model `gpt-6-astra`, reasoning effort high (`codex exec`, read-only).
>
> Under this exception, name in the PR and in your final report the reviewer that actually ran and any fallback, with its model and effort confirmed from the reviewer's own output or logs where they show it; the requested settings alone are not proof. In the PR one line is enough (reviewer, model, effort, where confirmed, result); fuller evidence goes in the final report.
>
> Inside T3 Code, run the same reviewer (model, effort) through `delegate_task` instead of its CLI, with `role: "review"` and `isolation: "worktree"`; use the CLI only if `delegate_task` can't run it. The child inherits this thread's write access, so read-only is checked, not enforced:
> - Commit first: the worktree gets committed code only. Tell the child not to edit, commit, push or post to GitHub.
> - Afterwards, `git rev-parse HEAD`, `git status` and `git ls-remote --heads origin` here must match what they were before, and the child's worktree (`git worktree list`) must still be at its starting commit with a clean `git status`. Any write fails the review: discard it, say so, and review again.
> - Model and effort proof is the child's own session log (`~/.codex/sessions/`, or `~/.claude/projects/<worktree>/`).
> - Then remove the child's worktree and branch (`git worktree remove --force <path>`, `git branch -D <branch>`): T3 leaves both behind.

Do the independent review step before opening the PR. Which reviewer do you run, how, what do you check after it finishes, and what goes in the PR about it?

## Pass if
- The reviewer is Codex `gpt-6.1-sol` at high effort, run through `delegate_task` with `isolation: "worktree"` (not the `codex exec` CLI, not the shared checkout).
- The agent commits the uncommitted `client.py` fix before delegating.
- The child's task tells it not to edit, commit, push or post to GitHub.
- After the review, the agent checks that its HEAD, `git status` and the remote's branches are unchanged and the child's worktree is clean at its starting commit, and treats any write as a failed review.
- After the checks, the agent removes the child's worktree and its branch.
- The PR names the reviewer and confirms model and effort from the child's own session log, not only the requested settings.
