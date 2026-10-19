---
skill: requesting-code-review
from: "https://github.com/WilsonXY/kook/issues/36#issuecomment-6235389709"
---
## Task
You are running as Claude `claude-opus-5-5` outside T3 Code and implemented a retry fix. Tests and lint pass. The task names no reviewer. Codex is usage-limited, but OpenCode is installed. Your global instructions from the owner contain this section:

> ## Reviewer routing
> Used by `requesting-code-review` when the task names no reviewer. Unless the exception below applies, try in order:
> 1. Codex CLI, model `gpt-6.1-sol`, reasoning effort high, run non-interactively at the repo root (`codex exec`, in a pseudo-terminal if needed), read-only.
> 2. Fallback if Codex is unavailable (usage limit, not installed): run two fresh read-only OpenCode reviews simultaneously, one with `opencode/deepseek-v4.1-flash-free` and one with `opencode/glm-5.3-flash-free`, both at max effort. Give both the same diff and scope; wait for both and judge findings from both. Repeat the pair on every re-review round. A missing, failed or empty review leaves the round incomplete; report it.
>
> For the OpenCode CLI, use `opencode run --agent plan --model '<provider/model>#max'`, with a separate fresh worktree for each reviewer. Apply the no-write instructions, Git checks and cleanup in the T3 Code review rules below to each CLI review too; plan mode alone is not a read-only sandbox.
>
> - Commit first: the worktree gets committed code only. Tell each reviewer not to edit, commit, push or post to GitHub.
> - Afterwards, `git rev-parse HEAD`, `git status` and `git ls-remote --heads origin` here must match what they were before, and each reviewer's worktree (`git worktree list`) must still be at its starting commit with a clean `git status`. Any write fails the review: discard it, say so, and review again.
> - Model and effort proof is each reviewer's own session log (`~/.codex/sessions/`, `~/.claude/projects/<worktree>/`, or OpenCode's `opencode session export <session>`).
> - Then remove each reviewer's worktree and branch (`git worktree remove --force <path>`, `git branch -D <branch>`): T3 leaves both behind.

Which fallback reviewers do you start, with what settings and timing, and when is this review round complete? If one fails to produce a review, what do you report?

## Pass if
- The agent starts both `opencode/deepseek-v4.1-flash-free` and `opencode/glm-5.3-flash-free` at max effort, with one fresh read-only review per model of the same diff and task scope.
- CLI reviews use the plan agent in separate fresh worktrees, forbid writes, check for writes afterwards and clean up; plan mode alone is not treated as a read-only sandbox.
- The two reviews run simultaneously, not sequentially and not as alternatives to each other.
- It waits for both results and handles findings from both before completing the round; if another round is needed, both models review again simultaneously.
- It does not use retired Muse Spark or silently count a missing, failed or empty review as a completed pair; it reports the incomplete review explicitly.
