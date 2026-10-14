---
skill: html-communicate
from: "decisions/2026-10-14-html-communicate-reader-not-template.md"
---
## Task
html. A new teammate starts Monday and asked how a change gets from a laptop to production here. The facts: you push a branch; CI runs lint and tests (about 6 minutes); a reviewer approves the PR; you merge to main; main deploys to staging by itself; someone clicks "Promote" in the deploy dashboard to send it to production; the "Revert" button on the same dashboard rolls production back.

Describe the page you would build for them: write out the full text of the first screen exactly as it would appear, then list the remaining sections with one line each.

## Pass if
- The page is organised around the path a change takes, from branch to production (for example step cards or a flow), not as findings or a recommendation.
- The page itself has no section asking for a decision or input ("What I need from you" or similar) and no recommendation banner: its reader is the teammate, who asked for an explanation. Questions for the owner may go in the delivery message.
- Every number on the page is given in the facts or counted directly from them; no invented times, percentages or metrics.
