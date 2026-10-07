---
skill: github
from: "#14"
---
## Task
Your PR #21 (branch `feat/a`, base `main`) is open and waiting for me to merge. You've finished a follow-up change on branch `feat/b`, built on top of `feat/a`. Open the PR for `feat/b` now, and tell me how the two should be merged.

## Pass if
- The agent either avoids stacking (for example waits for #21, or bases the new PR on `main` and explains the extra diff) or opens it with base `feat/a` and says so.
- If stacked: the agent does not promise that GitHub will retarget the new PR to `main` on its own. (GitHub does so only when the merged branch is deleted, which isn't guaranteed.)
- If stacked: the agent says that after #21 merges it will check the new PR's base and retarget it to `main` itself if needed (for example `gh pr edit <n> --base main`), or tell the owner to, before the new PR is merged.
- The merge order (#21 first) is stated to the owner.
