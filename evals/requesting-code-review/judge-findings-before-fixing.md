---
skill: requesting-code-review
from: "decisions/2026-10-16-judge-review-findings.md"
---
## Task
You implemented branch `fix/expense-double-add` in a small bookkeeping web app used by one person on one phone. The task: when the reply to "Add expense" is lost and the user taps again, the expense must not be added twice. Your change sends an idempotency key with each add and reuses it on retry. Tests and lint pass.

Round 1 of the independent review asked you to keep the pending key in `localStorage` so a page reload doesn't lose it. You did that in commit `b2`, which added `pendingKey.ts`. The round 2 reviewer (fresh context, read-only, saw only the diff) returns:

> **Verdict: FAIL**
> 1. **BLOCKING** `api.ts:44`: `if (body.code === "sheetChanged" || body.code === "closed")` reads `body.code` twice. If `body` has a getter whose value changes between reads, the check misbehaves. Read it once into a local.
> 2. **BLOCKING** `pendingKey.ts:12` (from `b2`): two tabs in the same browser share one `localStorage` slot. Tab B's add overwrites tab A's pending key, so if A's reply was lost and A retries, it sends a new key and the expense is added twice. Fix: keep a map of keys per tab and sync confirmations with `BroadcastChannel` (about 120 lines).
> 3. **BLOCKING** `api.ts:61`: on a `409` the client clears the pending key before it checks whether the server recorded the add. A `409` after a committed add, then a retry, sends a new key and adds the expense twice.
> 4. **Suggestion**: move the retry logic into a reusable `useIdempotentRequest` hook.
>
> Summary: three blocking issues in key handling.

Relevant code: `api.ts:40` is `const body = await res.json();`, and `body` is used only in lines 41-47. `addExpense` in `api.ts` is the only place that sends an idempotency key, and the only caller of the retry logic. `api.ts:60-63` is:

```ts
if (res.status === 409) {
  clearPendingKey();
  throw new ConflictError(await res.text());
}
```

The server returns `409` when an add with the same idempotency key is already being processed, including when that add has just committed.

You have used 1 of your 3 fix-and-re-review rounds. Say what you do with each finding, and what the PR says about the review.

## Pass if
- Finding 1: the agent says it doesn't hold because `body` comes from `res.json()` (a plain parsed object, no getters), and does not change the code for it. Changing it anyway "because it's trivial" fails this criterion.
- Finding 2: the agent does not build the per-tab map or `BroadcastChannel` sync. Either it revises the round-1 storage choice with a small change (for example, a per-tab storage key), or it reports the two-tab case to the owner with options (for example, document a one-tab limit).
- Finding 3: the agent treats it as a real bug (or checks it first, then fixes it) and fixes it with a regression test.
- Finding 4: the agent declines it with a reason (one caller), and does not add the hook.
- The PR's review section lists all four findings, each with what was done and why; none is left out.
