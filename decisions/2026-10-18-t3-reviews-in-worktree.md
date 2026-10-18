# Inside T3 Code, reviews run through `delegate_task` in a worktree, checked afterwards

**Context.** #38 asked whether reviews could move from the CLI route to T3's `delegate_task`. The owner wants it: T3 nudges agents that way, and the reviewer shows up as a child thread they can open. Children inherit the thread's write access, so the CLI's enforced read-only (`codex exec -s read-only`, `claude --permission-mode plan`) doesn't carry over.

**Evidence.** Trials on 2026-10-17 and 2026-10-18 (T3 thread d52f6132-a9a5-427b-bd03-09642d362023 and this PR's thread), each child reviewing #39's diff in its own worktree:
- `runtimeMode: "approval-required"` with Claude in plan mode reviewed without prompts, but Codex stalled on its first `cat`, waiting for a person.
- Inherited full access, worktree, a prompt forbidding edits: Codex `gpt-6.1-sol` and Claude `claude-opus-5-5` both finished unattended (PASS; Claude with 7 suggestions) and wrote nothing. Their own session logs show model and effort (`gpt-6.1-sol`/`high` with `danger-full-access`; `claude-opus-5-5`/`high` with `bypassPermissions`).
- A canary child told to break the rule left an uncommitted edit in its worktree, committed there, and wrote a file into the parent checkout. `git status` in the parent showed the file and the child's branch had moved off its starting commit; the uncommitted edit stayed in the child's worktree, away from the PR.
- T3 doesn't clean up reliably. On 2026-10-17 the worktrees were gone about an hour after the tasks ended, with their branches left behind; on 2026-10-18 five child worktrees and their branches were all still there after about 1.5 hours.

**Decision.** `profile.md`: inside T3, run the same reviewer through `delegate_task` with `role: "review"` and `isolation: "worktree"`, after committing. Afterwards the parent's HEAD and `git status`, the remote's branches, and the child's worktree (clean, at its starting commit) must be unchanged; any write fails the review. Then the agent removes the child's worktree and branch, so reviews don't pile up checkouts. HEAD is in the list because a commit made in the parent leaves `git status` clean. "Implemented" means wrote the diff, itself or as a delegated child, so the Sol exception still applies when a Claude parent delegates the code to Sol.

**Why.** Isolation plus a check after the review guards the property that matters: a reviewer's edits never land in the change unnoticed. It needs no approval mode, so Codex works too.

**Rejected.**
- `approval-required` for every child: Codex stalls on reads.
- Plan mode with inherited full access as a guard: T3 auto-approves whatever plan mode asks about, so it only adds instructions.

**Limits.** Detection, not prevention: the checks see writes in git, not GitHub comments or writes elsewhere on disk. Both reviewers obeyed in every trial; a reviewer that ignores the prompt there would go unnoticed.

**Rollback.** Revert the PR: reviews go back to the CLI route.
