#!/usr/bin/env bash
# Link every skill in dev-skills/ into a user-level skills folder so every
# workspace and worktree sees them. Safe to re-run. Default target: ~/.claude/skills
# Usage: scripts/link-skills.sh [target-dir]
# Normally run by sync-skills.sh in the live copy (see install-skills.sh), not by hand:
# linking from a working checkout makes agents load whatever branch it is on.
# Codex reads ~/.agents/skills (whole-folder link to <repo>/dev-skills; sync-skills.sh keeps it).
# Antigravity (agy) has NO global dir: link <project>/.agents/skills per project.
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$repo/dev-skills"
dst="${1:-$HOME/.claude/skills}"
mkdir -p "$dst"
for d in "$src"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  if [ -e "$dst/$name" ] && [ ! -L "$dst/$name" ]; then
    echo "SKIP $name: real folder exists in $dst (not touching)"; continue
  fi
  if [ "$(readlink "$dst/$name" 2>/dev/null)" != "${d%/}" ]; then
    ln -sfn "${d%/}" "$dst/$name"; echo "linked $name"
  fi
done
for l in "$dst"/*; do
  [ -L "$l" ] || continue
  t="$(readlink "$l")"
  case "$t" in "$src"/*) [ -f "$l/SKILL.md" ] || { rm "$l"; echo "removed stale $(basename "$l")"; } ;; esac
done
echo "ok: $dst"
