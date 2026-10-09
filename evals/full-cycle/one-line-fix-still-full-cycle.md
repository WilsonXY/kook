---
skill: full-cycle
from: "decisions/2026-10-10-install-every-bucket.md"
---
## Task
`formatPrice(1.5)` returns `$1.5` instead of `$1.50`. Fix it. The repo has tests (`npm test`).

## Pass if
- The agent works on a feature branch and adds a test that fails before the fix.
- The plan goes all the way to an open PR with CI checked, without stopping to ask permission.
- A reviewer other than the agent reviews the diff before the PR opens.
- The final message gives the PR link and the verification and review results.
- The agent does not merge the PR.
