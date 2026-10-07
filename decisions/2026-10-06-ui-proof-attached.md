# UI changes carry attached proof

**Context.** UI changes were verified by tests only, or proven with local file paths the reviewer couldn't open (PR #5).

**Decision.** UI and user-visible changes are exercised in the running app with the repo's proof command, and the screenshots or recording are attached to the PR (`gh` 2.99+ `--attach`). Re-record only when a later fix touches the proved flow.

**Rejected.** Re-recording after every commit: costly, and lint-only fixes don't change behaviour.
