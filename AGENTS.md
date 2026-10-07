# kook

Skills for coding agents. Portable dev skills live in `dev-skills/` (rules in `dev-skills/README.md`).

- Agents load skills from `~/.local/share/kook`, not from your checkout or worktree. A timer fast-forwards it to `origin/main` every 5 minutes, so a merged PR goes live by itself. Never switch branches or edit files there.
- Verify: `scripts/test-sync-skills.sh` and `shellcheck scripts/*.sh`.
- After a PR merges, confirm it is live: `~/.local/share/kook/scripts/sync-skills.sh --check` (or run it without `--check` to sync now).
