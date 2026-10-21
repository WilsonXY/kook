---
skill: full-cycle
from: "WilsonXY/Bokli#74: six recordings of 2.4–6.5 s each; whole flows (double tap, lost reply, retry) played too fast for the owner to follow"
---
## Task
In this web app repo, you fixed the expense form: a double tap on Save now adds one expense, and a lost reply shows "Not sure it saved" with a Retry button. Tests pass and the independent review is done. The repo's AGENTS.md says: the UI proof command is `node scripts/verify.mjs <flow.mjs>`; it opens a headless browser, runs your flow file's default export with `{ page, shot }`, and records `flow.webm` plus screenshots into `.evidence/`.

Write the flow file you would run, then say what you check before attaching the files to the PR, and what you attach.

## Pass if
- The flow is paced for a person to follow: pauses or a slow-motion setting between steps, and a hold on each result that proves the change (the single expense, the "Not sure it saved" message, the state after Retry).
- Before attaching, the agent checks the recording itself (watches it or checks its length), not only that the command passed.
- The recording is attached to the PR itself, not given as a local file path; screenshots may also be attached.
