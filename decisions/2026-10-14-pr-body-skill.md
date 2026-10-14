# PR body rules get their own skill

**Context.** What a PR body says was spread over three places: `full-cycle` (step 6 and "Write the PR and the report for the owner"), `requesting-code-review` (steps 5 and 7) and the example body in `github`'s `pr-workflow.md`, which taught a different shape ("Summary" bullets, "Test Plan" checklist). The owner sees `full-cycle` as the orchestrator and wants it to route, not grow a section for every artefact it produces. Matt Pocock's `pr` skill (mattpocock/skills `skills/engineering/pr`) gave the template ideas below.

**Decision.** A new `dev-skills/pr-body` owns every rule about the PR body and the final report: the plain opening from `2026-10-10-pr-body-for-the-owner.md`, then Merge danger (one-way or two-way door, blast radius), Evidence (before and after), Verification, Review, Not verified. `full-cycle`, `requesting-code-review` and `github` route to it and keep no body rules of their own. This supersedes the "Why here" of `2026-10-10-pr-body-for-the-owner.md`.

**Evidence for the new sections.** In WilsonXY/Bokli#70 the one-way parts of a live-data migration (closed months reject writes; empty markers rewritten to NULL) sat in the last paragraphs, under "Compatibility and limits", after the test counts and reviewer proof. The plain-opening rule asks for "the risk" but not what a revert can't undo or what could break. The scenario `evals/full-cycle/merge-danger-and-evidence.md` is built from it.

**Rejected.**
- Installing Matt's skill unchanged: it opens with a diagram instead of plain sentences, and has no place for the review, what was not verified, or the decision asked of the owner.
- Its menu of visuals (call trees, Mermaid, diffs): it is HumanLayer's show-me, already in `vendor/`, and wiring it into the PR workflow was rejected in `2026-10-09-borrow-reviews-small-fixes.md`. Same reopen condition.
- Blast radius as one word, as upstream has it: "low" tells the owner nothing; the skill asks for names.
