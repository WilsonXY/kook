# Behaviour scenarios

Each file tests one decision a skill should make. `scripts/eval.sh evals/<skill>/<scenario>.md` gives a fresh agent the skill and the **Task** as a dry run, never the **Pass if** list. A second fresh agent then grades the reply against that list.

- **Start from evidence.** `from:` names the inbox issue, decision or PR the scenario came from.
- **Watch it fail first.** Run a scenario against the current skill before changing the skill (RED), then again after (GREEN). Before/after on one skill: `scripts/eval.sh --runs 3 --ref origin/main <scenario>` and `scripts/eval.sh --runs 3 <scenario>`.
- **One run is not evidence.** The same scenario can pass once and fail the next time. `--runs N` reports a pass rate and passes only on a majority. Act on rates, never on a single run.
- **The agent under test is isolated.** It runs from an empty folder with a throwaway home, so neither this repo's `AGENTS.md` nor the owner's installed skills and profile leak in. That's why results can differ from a real session.
- **Grade the declared decision, not a whole session.** Ask what the agent would do and say; keep criteria checkable from that reply.
- **Results are evidence, not CI.** Runs cost model calls and vary between runs. Put the results in the PR that changes the skill.
