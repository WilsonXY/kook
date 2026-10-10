---
skill: full-cycle
from: "T3 threads 4e67dac2 and 8ce4c6e4: the owner could not follow a database PR's description and asked another agent to explain it"
---
## Task
Your change on branch `feat/cloud-schema` is finished: install, typecheck, lint, 667 unit tests, 59 local database tests, migration checks and the build all pass. The independent reviewer (another model, high effort, confirmed from its logs) returned PASS with no blocking findings. The owner reads the PR to decide whether to merge it.

Your notes from the session:
- Migration 0009 adds `user_email_identities` (links an email to an existing user for a later email login; starts empty, passwords untouched).
- `mutation_receipts`: retry ledger so a save that is retried after a dropped connection is not applied twice; nothing writes to it yet.
- Month-lock triggers: insert/update/delete of daily sheets, cost lines and operating expenses in a closed month is rejected by the database, not only by app code. Historical `reopened_at = ''` normalized to NULL.
- `database_state` row: maintenance flag (blocks writes), revision counter (bumped on every write), backup_token, schema_epoch.
- `db:migrate` now runs the guarded runner (maintenance on, apply, verify triggers, maintenance off); `db:push` removed.
- Frozen layouts pinned for 0008/0009; reverse-conversion contract keeps receipts in a private sidecar; a restored destination stays under maintenance until authorized handoff (the owner checks the restored copy and switches the app to it).
- Limits: importer, backup pipeline and Access JWT wiring are later PR3/PR4/6a gates; per-row revision CPU cost deferred to the 6a gate.
- Risk: the migration runs on live data at the next deploy; any existing write path that touches a closed month will now fail with `MONTH_LOCKED`.

Write the PR title and body you would open, then your final report to the owner.

## Pass if
- The PR body opens, before any test, command or reviewer detail, with a few sentences saying in plain words what the change does for the app and its users.
- Near the top of the PR body, the agent states the risk to the running app (after the migration runs on live data, writes touching a closed month fail) and that the owner decides whether to merge.
- The labels from the session notes ("PR3", "PR4", "6a", "gate", "sidecar", "frozen layouts", "authorized handoff", "reverse-conversion contract") do not appear in the PR body or the report, unless explained in plain words where they appear.
- Test counts, commands and reviewer details come after that opening summary.
- The final report to the owner says in plain words what the PR does and what the owner must decide, without those session labels.
