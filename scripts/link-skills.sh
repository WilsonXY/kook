#!/usr/bin/env bash
# Link every skill in kook (dev-skills/, writing/, vendor/) into a user-level
# skills folder so every workspace and worktree sees them. Safe to re-run.
# Default target: ~/.claude/skills
# Usage: scripts/link-skills.sh [target-dir]
# Normally run by sync-skills.sh in the live copy (see install-skills.sh), not by hand:
# linking from a working checkout makes agents load whatever branch it is on.
# sync-skills.sh runs it for ~/.claude/skills and ~/.agents/skills (Codex).
# Antigravity (agy) has NO global dir: link <project>/.agents/skills per project.
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
buckets=(dev-skills writing vendor) # keep in step with SCOPE.md
dst="${1:-$HOME/.claude/skills}"
mkdir -p "$dst"
for b in "${buckets[@]}"; do
  for d in "$repo/$b"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    name="$(basename "$d")"
    if [ -e "$dst/$name" ] && [ ! -L "$dst/$name" ]; then
      echo "SKIP $name: real folder exists in $dst (not touching)"; continue
    fi
    if [ "$(readlink "$dst/$name" 2>/dev/null)" != "${d%/}" ]; then
      ln -sfn "${d%/}" "$dst/$name"; echo "linked $name"
    fi
  done
done
for l in "$dst"/*; do
  [ -L "$l" ] || continue
  t="$(readlink "$l")"
  case "$t" in "$repo"/*) [ -f "$l/SKILL.md" ] || { rm "$l"; echo "removed stale $(basename "$l")"; } ;; esac
done
echo "ok: $dst"
