# PR bodies and reports open with a plain summary for the owner

**Context.** Codex (`gpt-6.1-sol`) implemented a database PR and wrote its description and final report for a reviewer: labels it coined during the session ("frozen layouts", "private sidecar", "owner gates", later-phase codes), and paragraphs of proof about checks and reviewer settings before saying what the change does. The owner could not follow it and asked another agent to explain the PR (T3 threads 4e67dac2 and 8ce4c6e4). Claude sessions rarely do this, but nothing in `full-cycle` named the reader. Step 6 only listed what the body must contain, and Codex filled each item densely.

**Decision.** `full-cycle` gets a short section: the PR body and the report open with a few plain sentences (what changes for the app or its users, the risk, what the owner must decide); details follow; labels coined in the session are left out or explained; a check before posting. `profile.md` keeps the reviewer-proof rule but limits it to one line in the PR, with fuller evidence in the final report, because that rule produced a paragraph of model-confirmation proof at the top of the PR.

**Why here.** Who reads a PR, and in what order, is a judgement that recurs in every repo, so it goes in a portable skill, not in a project's `AGENTS.md`. It goes in `full-cycle` because that skill owns the PR body and the report; `github` only routes to PR mechanics.

**Rejected.**
- A Codex-only rule: there's no Codex-only profile, and the rule costs Claude nothing.
- Codex verbosity settings: they change length, not jargon, and the problem PR was dense rather than long.
- A doctor check for banned words: the jargon depends on the project, so no fixed list catches it.

**Rollback.** Revert this PR, with the owner's approval like any other change.
