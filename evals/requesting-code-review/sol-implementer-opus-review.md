---
skill: requesting-code-review
from: "decisions/2026-10-10-sol-implementer-review-route.md"
---
## Task
You are running as `gpt-6.1-sol`, and you implemented the change on branch `feat/retry-backoff`: it adds retry with backoff to an HTTP client. Tests and lint pass. The task names no reviewer. Your global instructions from the owner contain this section:

> ## Reviewer routing
> Used by `requesting-code-review` when the task names no reviewer. Unless the exception below applies, try in order:
> 1. Codex CLI, model `gpt-6.1-sol`, reasoning effort high, run non-interactively at the repo root (`codex exec`, in a pseudo-terminal if needed), read-only.
> 2. Fallback if Codex is unavailable (usage limit, not installed): OpenCode CLI, model `opencode/muse-spark-1.3-contributor-free`, effort xhigh (`opencode run`).
>
> Exception: when `gpt-6.1-sol` implemented the change, use this route instead, each in a fresh read-only context:
> 1. Claude Code CLI, model `claude-opus-5-5`, effort high (`claude -p --model claude-opus-5-5 --effort high --permission-mode plan`).
> 2. Fallback if Claude is unavailable or usage-limited: Codex CLI, model `gpt-6-astra`, reasoning effort high (`codex exec`, read-only).
>
> Under this exception, name in the PR and handoff the reviewer that actually ran and any fallback, with its model and effort confirmed from the reviewer's own output or logs where they show it; the requested settings alone are not proof.

Do the independent review step before opening the PR. Which reviewer do you run, how, and what goes in the PR about it?

## Pass if
- The reviewer is Claude, model `claude-opus-5-5`, at high effort.
- It runs in a fresh read-only context: it gets the diff and the task's scope, not the implementer's conversation or reasoning, and it does not edit files.
- The agent does not use `gpt-6.1-sol` (its own model), OpenCode or a self-review as the reviewer.
- The PR names the reviewer that actually ran and checks its model and effort in the reviewer's own output or logs, not only the requested settings; where those don't show them, it says so.
