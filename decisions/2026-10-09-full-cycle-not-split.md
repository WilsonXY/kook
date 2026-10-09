# full-cycle stays one file

**Context.** Four of the first five PRs edited `full-cycle/SKILL.md`. The plan was to keep the steps in `SKILL.md` and move the how-to into reference files.

**Decision.** Don't split it. `full-cycle` is nearly all rules, with little how-to to move. New how-to lessons go into a reference file only when they really are how-to; rules stay in `SKILL.md`.

**Evidence.** A trial split, with one line per step plus `references/verify.md`, `ship.md` and `preview.md`, passed the behaviour scenarios, including `eval.sh --skill-only`. Independent review still found 8 rules lost or changed by the compression:
- proof attachment narrowed from UI or user-visible changes to UI only, and lost "capture after review fixes"
- `long-running-commands` routing dropped
- the UI proof command made unconditional
- the review details required in the PR body dropped
- "fix and push" became "fix"
- the preview conditions and their fallback changed
- the safe push alternative removed

Restoring them would put each rule in two places, which then drift. The scenarios check only the main rules, so line-by-line review is what catches this kind of loss.

**Kept from the trial.** `scripts/eval.sh --skill-only`: it gives the agent only `SKILL.md`, the worst case for any skill that does move text into references.
