# Preview follows the repo's own procedure

**Context.** Agents started their own dev servers for previews, colliding with shared ones (PR #3).

**Decision.** `full-cycle` step 8 follows the preview procedure in the repo's `AGENTS.md`. With none, the agent doesn't start a server or expose ports; it says how to try the change and asks.

**Why.** Preview setup is a project fact, not a portable one.
