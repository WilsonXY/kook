# Judge each review finding before fixing it

**Context.** A collaborator noticed that implementers rarely push back on reviewer findings. An audit of 23 past threads with review rounds (thread cb9b86ad) found that nearly all findings were valid and were checked before fixing, so blind acceptance of wrong findings was rare. Three other patterns did recur:
- Blocking findings were fixed even when the implementer's own reasoning doubted them: "feels overly pedantic… I'll just do the trivial fix" (f1be9a9d); "feels contrived but still has a small fix" (679db86a). Step 6 said "Fix every blocking finding".
- Fixes were stacked on fixes. Each round's fix drew a new finding, answered with more code: nine review runs in 679db86a until the owner cut scope to one tab; a verification gate that grew from 204 to 1,384 pinned files in a3b63a41.
- Declines were unverified ("likely only has two entries"), dropped silently, or left out of the report ("I turned down three suggestions" against about nine, debd52d4).

**Decision.** `requesting-code-review` Step 6 makes the implementer check each finding, then give it one verdict: fix (the default), doesn't hold (with the evidence), decline (a preference with no concrete problem; a real problem whose suggested fix is bad gets a simpler fix or a report), or report. A severity label is a claim, not a verdict. A finding on code an earlier review fix added makes the implementer question that fix before adding another layer. Step 7 puts every finding and its verdict in the PR.

**Why.** Borrowed from skill sets that already solve this: the four-bucket lead judgment and its "hypothetical vs. actual" filter from pstack's `interrogate`; the verdict list, "default to fixing" and the "earlier fix was the wrong layer" rule from compound-engineering's `ce-resolve-pr-feedback` rubric; "verify before implementing" from superpowers' `receiving-code-review`. Fixing stays the default because the audit showed reviewers are usually right; the change targets doubt that is ignored, layers piling up, and missing dispositions.

**Rejected.**
- Vendoring superpowers' `receiving-code-review`. It is mostly about tone in chat with a human reviewer; the part Kook needs fits in Step 6.
- gstack's split of every finding into auto-fix or ask-the-owner. It sends too many calls to the owner for an agent that runs `full-cycle` on its own.
- pstack's learned-pattern file of noisy findings. It suits a high volume of bot comments, not one strong reviewer per PR.
