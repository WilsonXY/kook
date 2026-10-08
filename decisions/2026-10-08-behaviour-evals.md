# Skill behaviour changes are tested with scenarios

**Context.** Skill edits were judged by reading them. Nothing showed whether an edit changed what agents do. Splitting `full-cycle`, the most-used skill, was deferred for exactly this reason.

**Decision.** `evals/<skill>/<scenario>.md` holds a task and a "Pass if" list, both taken from real evidence (an inbox issue or a decision). `scripts/eval.sh` gives a fresh agent the skill and the task as a dry run, never the criteria. A second fresh agent grades the reply. A behaviour change runs its scenarios before (`--ref origin/main`) and after, and puts both results in the PR.

**Learned while building it.** Single runs vary: in the first baselines, the same scenario flipped between PASS and FAIL. The agent under test also picked up the repo's `AGENTS.md` and installed skills until runs were isolated. So results are pass rates over 3+ isolated runs (`--runs`).

**Why.** If you haven't watched the agent fail without the change, you don't know the change teaches the right thing (superpowers `writing-skills`). Grading the declared plan instead of a full session keeps a run to a few minutes (compound-engineering `evaluate.md`).

**Rejected.**
- Running evals in CI: they cost model calls and vary between runs. CI only tests the runner, with stub agents.
- Full-session evals that drive a real repo: much slower, and they aren't needed for decisions an agent declares up front.
