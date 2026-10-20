# Ponytail applies to implementation, not creative work

**Context.** In T3 thread `4280c8e5-a94b-4aed-98b1-e677b7f9d48c`, the owner asked to narrow the "every coding task" rule so Ponytail cannot restrict frontend design or creative work. This updates `2026-10-10-ponytail-by-default.md`.

**Decision.** `profile.md` applies Ponytail at full intensity to actual coding/implementation only. Frontend design and creative work are excluded even when expressed in code or following an implementation step. Mixed tasks apply it only to implementation mechanics and preserve the chosen design. Tests, review and the PR still happen.

**Why here.** This is the owner's activation preference. The third-party skill stays unmodified; the profile overrides its broad activation and persistence rules.

**Rejected.** Exempting only prose or design discussions: frontend design can involve HTML/CSS and animations. Exempting all frontend coding: functional work such as bug fixes and keyboard navigation still benefits from simpler implementation.

**Verification.** `evals/full-cycle/ponytail-creative-boundary.md` exercises a bug fix, HTML/CSS design exploration after the fix, and functional implementation of the chosen design. Run `scripts/eval.sh --runs 3 --with ponytail evals/full-cycle/ponytail-creative-boundary.md`. Before/after trials use the old/new Coding style excerpt in the scenario: the evaluator isolates itself from the real profile, and `--ref` changes skill text, not that excerpt. Results go in the PR.
