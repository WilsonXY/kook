---
name: pr-body
description: "Use when writing a PR body, or the final report on a change."
version: 1.0.0
author: WilsonXY
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [pull-request, writing, review, report]
---

# PR body: written for the owner who decides

The owner reads the PR body and your final report to decide, and has not followed your session. Every rule about what a PR body says lives here.

## Template

```markdown
<A few plain sentences: what changes for the app or its users, the risk, and the decision you need from the owner, asked directly (for example: merge it or not).>

## Merge danger
**Door:** one-way or two-way. <What a revert would not undo, if anything.>
**Blast radius:** <What could break once merged, by name.>

## Evidence
**Before:** <the failing test, output or screenshot>
**After:** <the same check, now passing>

## Verification
<Checks run and their results, kept short.>

## Review
<Reviewer used (and any fallback and why), findings with severity, how each was handled.>

## Not verified
<What you did not check, and why.>
```

## Sections
- **Opening.** No heading, no preamble. Could the owner say what the PR does and what they must decide from it alone? If not, rewrite it.
- **Door.** Two-way: reverting the PR puts everything back. One-way: something a revert can't undo, such as data migrated or deleted on a live system, a message sent, or a format or API others now depend on. Say which part is one-way.
- **Blast radius.** Name the users, screens, jobs, callers or deploys affected if the change is wrong, and which of them you did not test. "Low" is not an answer.
- **Evidence.** The same check before and after. Visible change: screenshots or a recording, attached to the PR, never a local file path the reader cannot open (see `github`). Otherwise the test that failed before and passes now, or the output. Nothing to show before (a new feature): show the after and say so.
- **Verification, Review, Not verified.** After the opening and evidence, kept short. A section with nothing to say gets one line, not silence.

## Plain words
- Use the owner's words, not the session's. Leave out labels you or the task coined (phase numbers, "gates", "contracts", nicknames for files or designs), or explain each in plain words where it first appears.
- Before posting, reread for every term the owner didn't use themselves, and replace or explain each.

## The final report
Same reader, same rules. Open with what changed, the door and blast radius in a sentence, and the decision needed; then the PR link. Proof the PR keeps to one line can be given in full here.

## Common mistakes
- A PR body written for a reviewer: session jargon and proof of diligence (commands, test counts, reviewer settings) before what the change does.
- A risk line that says "low" or "none" without the door and blast radius.
- A one-way step (a data rewrite, a deletion) mentioned only near the bottom.
