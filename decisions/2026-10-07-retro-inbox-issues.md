# Lessons go to an inbox of GitHub issues

**Context.** Corrections and confusion in sessions never reached the skills. In thread e23c2096, 6–7 of 13 owner messages asked what a report meant, and `html-communicate` didn't change. Lessons were scattered across chat, scratch reports and one harness's memory.

**Decision.** The owner-invoked `retro` skill reads a session (`scripts/t3-thread.sh` for T3 threads) and files each lasting lesson as a GitHub issue on kook labelled `inbox`, with evidence and a proposed home. Triage turns each into a PR, a decision, or a closed issue.

**Why.** Issues are easy to triage and to hand to another agent, as with #7. Each change then starts from an observed failure, which is the bar in `SCOPE.md`.

**Rejected.**
- An `inbox/` folder in the repo: every finding would need its own PR.
- A local folder outside git: private, but invisible to other agents and nothing tracks its status.

The repo is public, so `retro` paraphrases and leaves out private details.
