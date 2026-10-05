---
name: full-cycle
description: "Use for any coding task: own it from first edit to open PR."
version: 1.0.0
author: WilsonXY
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [workflow, pull-request, verification, review, ci]
---

# Full cycle: a task is done when the PR is open and CI is green

You own the task end to end. Do not stop after the code works and ask "should I commit / open a PR?". The answer is already yes. Stop only for the limits at the bottom.

## Steps (in order)
1. **Understand.** Read the repo's AGENTS.md and the code around the change. If the request is ambiguous in a way that changes the result, ask once, up front.
2. **Implement on a feature branch** (never the default branch). New behaviour or a bug fix: use `test-driven-development`. Something fails and the cause is unknown: use `systematic-debugging`. Keep the diff inside the task's scope.
3. **Verify.** Run the repo's own checks (named in AGENTS.md / README): type-check, tests, build, lint. If a run takes over a minute, follow `long-running-commands`. For UI changes, also look at it running, not only the tests. Report real results, never "should pass".
4. **Independent review.** Follow `requesting-code-review`: a reviewer other than you, fix findings, re-verify.
5. **Commit and push** the branch (see `github` for commit style). A branch created from `origin/<default>` tracks the default branch, so a bare `git push` would aim at it: push with `git push -u origin HEAD` or unset the tracking first (`git branch --unset-upstream`).
6. **Open the PR** against the default branch (see `github`). Body: what and why, how it was verified, review result (reviewer used, findings, any fallback), what was NOT verified.
7. **Watch CI** until it finishes (`gh pr checks`). Fix failures and push. Answer or fix every review comment.
8. **Preview (UI or user-visible changes).** If the owner will want to try the change, follow the preview procedure in the repo's AGENTS.md (push the branch first). If AGENTS.md has none, do not start your own server or expose ports; say in the report how to try it and ask. Never restart a shared dev server another session may be using.
9. **Report** in plain language: PR link, what changed, verification and review results, anything the owner must decide.

## Limits (the only reasons to stop and ask)
- Never merge, tag, deploy or push to the default branch. The owner approves those.
- A finding that needs a decision, conflicts with the task, or changes scope: stop and report it, with options and a recommendation. Do not guess.
- A step is impossible (no push access, reviewer unavailable): say so plainly in the report; never fake it.

## Common mistakes
- Ending the turn while a test run is still going.
- Calling your own review "independent".
- Reporting done with no PR, or with CI not checked.
- Starting your own dev server for a preview when the repo documents a shared one.
- Unrelated changes sneaking into the diff.
