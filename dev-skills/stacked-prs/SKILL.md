---
name: stacked-prs
description: "Use when multiple open PRs share a base or need rebasing."
version: 1.0.0
author: WilsonXY
license: MIT
platforms: [linux]
metadata:
  tags: [git, github, pull-requests, rebase, merge-conflicts, verification]
---

# Stacked PRs — proving merge order before handoff

## When to use
- Several open PRs share the same base branch and the owner needs a safe
  review/merge order.
- A PR must be rebased onto fresh main after an earlier PR of the stack merged.
- A prior session crashed or compacted mid-merge and its "done/clean" claims
  need independent verification.

When several open PRs share a base (or one PR blocks on another's merge), the
per-PR readiness signal lies. Prove the real merge order yourself, in a
throwaway worktree, before telling the owner anything is mergeable.

## The core lie: per-PR `mergeable` flag

GitHub's `mergeable: MERGEABLE` only tests each PR against its base branch. It
cannot see PR-vs-PR conflicts: two PRs that both rewrite the same files can each
read MERGEABLE yet conflict head-on when merged in sequence. Before handing a
stack to the owner for review/merge, run a real sequential merge:

```bash
git worktree add --detach <scratch>/stack-check origin/main
cd <scratch>/stack-check
for B in branch-1 branch-2 branch-3; do
  git merge --no-edit "origin/$B" || { echo "CONFLICT on $B"; git merge --abort; break; }
done
# from the main repo dir afterwards:
git worktree remove --force <scratch>/stack-check
```

Never run this in a dirty main worktree. If the main worktree is mid-merge or
has conflict markers, treat its state as untrusted until reset.

## Rebase gate after a merge lands

When one PR of the stack merges, rebase the next branch before the owner's
review. Work in a fresh throwaway worktree, not the main one:

```bash
git worktree add --detach <scratch>/check origin/main
cd <scratch>/check
git checkout -B <branch> origin/<branch>
git rebase origin/main        # resolve conflicts here
git push --force-with-lease origin <branch>
git worktree remove --force <scratch>/check   # run from the main repo dir
```

Resolve, then run the project's typecheck + full test suite before pushing.
Resolution principle: keep each PR's own semantics — when two PRs moved the
same import/helper to different homes, keep the already-merged PR's home and
adapt the incoming PR to it; drop duplicates of the same symbol.

## Stacked schema-migration PRs
When several unmerged migrations need sequential numbers (e.g. Drizzle journal), branch each PR from the previous PR branch and target that branch as the PR base. Review/test each diff against its parent, and test the top branch against a dev database only (back it up first). After an earlier PR merges, rebase/retarget the next onto updated main and verify again before merging it; per-PR mergeability does not prove a stacked series survives squash merges. Never merge or deploy without the owner's approval.

## Pitfalls (each has cost a silently-broken push at least once)

- **Grep BEFORE add.** After resolving conflicts, `grep -rc '<<<<<<<'` the
  changed files, and only then `git add -A && git rebase --continue` / `git
  commit --amend`. `git add -A` stages conflict markers verbatim and the
  rebase/amend commits them silently — a broken branch that looks pushed-and-done.
- **Write conflict-resolution scripts to a file, never a shell heredoc.** Marker
  lines (`<<<<<<<`) inside a heredoc get mangled by shell quoting; the resolver
  SyntaxErrors while chained continuation commands let the rebase proceed
  unresolved. Put the resolver in a scratch `.py`, run it, check its output,
  then continue the rebase.
- **Typechecking a worktree without node_modules:** symlink the main worktree's
  (`ln -sfn <main>/node_modules <check>/node_modules`) and invoke TypeScript via
  `node <main>/node_modules/typescript/bin/tsc --noEmit`. The `.bin/tsc` shim can
  exit 1 with zero output when run from another worktree — which looks exactly
  like an undebuggable failure. A real typecheck takes seconds; a silent instant
  exit means the tool never ran.
- **After any session crash/compaction mid-merge, re-establish ground truth**
  from `git status` / `gh pr list` / GitHub before continuing. Never trust the
  prior session's "clean / all merged" summary — verify the worktree, the
  branch tips, and open PRs directly.
- **Never hand a dev-server/preview link over while the served worktree is
  dirty or mid-merge.** The page can return 200 on stale build cache while the
  code underneath is broken. Reset the branch to a verified commit and restart
  the server before declaring READY.
