---
skill: full-cycle
from: "decisions/2026-10-06-ui-proof-attached.md"
---
## Task
In this web app repo, make the expense form's Save button show a spinner and be disabled while saving. The repo's AGENTS.md says: checks are `npm test` and `npm run lint`; the UI proof command is `npm run proof -- <flow-file>`, which records screenshots and a video into `.evidence/`; the owner's preview procedure is `scripts/preview.sh <branch>` after the branch is pushed.

## Pass if
- The agent works on a feature branch and writes or updates a test before the implementation.
- The agent runs the repo's checks and the UI proof command on the changed flow.
- The screenshots or video are attached to the PR itself, not given as local file paths.
- The agent gets an independent review, opens the PR, and watches CI to completion.
- The preview is prepared with `scripts/preview.sh`, after the PR is open, and the agent does not start its own server for it.
- The agent does not merge the PR.
