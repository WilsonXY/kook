#!/usr/bin/env bash
# One-time setup, safe to re-run: clone kook to ~/.local/share/kook (the copy
# agents load skills from; never work in it), point ~/.claude/skills/* and
# ~/.agents/skills into it, and start a systemd user timer that runs
# scripts/sync-skills.sh there every 5 minutes, so merged PRs go live on their own.
# Usage: scripts/install-skills.sh   (from any kook checkout)
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
live="$HOME/.local/share/kook"
[ -d "$live/.git" ] || git clone --quiet --branch main "$(git -C "$repo" remote get-url origin)" "$live"
"$live/scripts/sync-skills.sh"
units="$HOME/.config/systemd/user"
mkdir -p "$units"
install -m644 "$live"/scripts/systemd/kook-skills-sync.{service,timer} "$units/"
systemctl --user daemon-reload
systemctl --user enable --now kook-skills-sync.timer
echo "timer on: merged PRs go live within 5 minutes. Check: $live/scripts/sync-skills.sh --check"
