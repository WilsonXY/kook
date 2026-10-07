---
name: github
description: "GitHub via gh CLI: branches, commits, PRs, CI checks."
version: 3.0.0
author: Ben Barclay (benbarclay)
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [github, gh, git, pull-requests, ci, commits]
---

# GitHub

Work the PR lifecycle with the `gh` CLI (REST fallback where noted). Each
workflow lives complete in its reference file: ALWAYS read the matching
reference before starting that workflow; the body below only routes.

## Routing

| Task | Read first |
|---|---|
| Branch, commit, open PR, attach proof, watch CI (merge only if the owner explicitly asks) | `references/pr-workflow.md` |
| A CI check failed: find and fix the cause | `references/ci-troubleshooting.md` |
| Commit message and PR title style | `references/conventional-commits.md` |

Anything else (issues, releases, repo settings, reviewing someone else's PR):
use `gh <command> --help` and the `gh` manual; this skill no longer carries
guides for them.

## Core discipline (applies to every workflow)

- Preflight once per session: `gh auth status`. If it fails, stop and tell
  the owner; do not paste or print tokens to work around it. No `gh` on the
  machine: `references/pr-workflow.md` has `curl` fallbacks using an existing
  `GITHUB_TOKEN`.
- Prefer `gh` over raw REST; drop to `gh api` only for endpoints the
  porcelain lacks.
- Never report CI green without checking `gh pr checks` yourself; never
  claim merged without verifying `state,mergedAt`.
- Read full context before writing: `gh issue view --comments` /
  `gh pr view --comments`: decisions live in threads, not titles.
- Sweep for duplicates before creating anything:
  `gh pr list --search` / `gh issue list --search`.

## Verification

- The workflow's own reference file defines done for that task.
- Cross-cutting: every claim about remote state (CI, merge, release,
  issue state) is backed by a fresh `gh` read, never memory.
