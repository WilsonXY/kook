# Agents load skills from a live copy kept on main

**Context.** Installed skills linked into the working checkout, so merged PRs weren't live and branch switches changed what agents loaded (PR #5 sat unloaded).

**Decision.** Agents load from `~/.local/share/kook`. A systemd user timer runs `scripts/sync-skills.sh` every 5 minutes: fast-forward to `origin/main`, relink, refuse if dirty or off main (PR #6).

**Rejected.** A Claude `SessionStart` hook: Claude-only and slows every session. A git worktree: T3 manages worktrees and branches are shared. Known gaps: issue #7.
