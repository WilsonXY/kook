#!/usr/bin/env bash
# Keep the copy of kook that agents load skills from (the "live copy") on
# origin/main, and keep ~/.claude/skills/* and ~/.agents/skills pointing into it.
# Run it from the live copy; scripts/install-skills.sh sets that up plus a
# systemd timer that runs this every 5 minutes. Never switches branches or
# touches local changes: if the live copy is off main or dirty, it stops.
# Usage: scripts/sync-skills.sh          fetch, fast-forward, relink
#        scripts/sync-skills.sh --check  only report drift; exit 1 if any
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
branch=main
claude="$HOME/.claude/skills"
agents="$HOME/.agents/skills"
case "${1:-}" in "" | --check) mode="${1:-sync}" ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac
g() { git -C "$repo" "$@"; }
issues=0
problem() { echo "PROBLEM: $*" >&2; issues=$((issues + 1)); }
origin="$(g remote get-url origin)"
other_kook() { # is link target $1 a skill in some other clone of kook?
  case "$1" in "$repo"/*) return 1 ;; */dev-skills/*) ;; *) return 1 ;; esac
  [ "$(git -C "${1%/dev-skills/*}" remote get-url origin 2>/dev/null)" = "$origin" ]
}

if [ "$mode" = sync ]; then
  exec 9>"$(g rev-parse --absolute-git-dir)/sync-skills.lock"
  flock -w 120 9
fi

cur="$(g branch --show-current)"
[ "$cur" = "$branch" ] || problem "$repo is on '${cur:-detached HEAD}', not $branch"
[ -z "$(g status --porcelain)" ] || problem "$repo has local changes"
if [ "$mode" = sync ] && [ "$issues" -gt 0 ]; then
  echo "not syncing: agents load this copy, so fix it by hand (never work in it)" >&2
  exit 1
fi

g fetch --quiet origin "$branch" || problem "could not fetch origin/$branch"
if [ "$mode" = sync ] && [ "$issues" -eq 0 ]; then
  old="$(g rev-parse --short HEAD)"
  g merge --quiet --ff-only "origin/$branch" || problem "cannot fast-forward to origin/$branch"
  [ "$old" = "$(g rev-parse --short HEAD)" ] || echo "updated $old -> $(g rev-parse --short HEAD)"
  "$repo/scripts/link-skills.sh" "$claude" | grep -v '^ok:' || true
  for l in "$claude"/*; do # links into another checkout that link-skills did not repoint: not on main
    if [ -L "$l" ] && other_kook "$(readlink "$l")"; then rm "$l"; echo "removed $(basename "$l") (not on $branch)"; fi
  done
  if [ -L "$agents" ] || [ ! -e "$agents" ]; then
    mkdir -p "$(dirname "$agents")"
    ln -sfn "$repo/dev-skills" "$agents"
  fi
fi

[ "$(g rev-parse HEAD)" = "$(g rev-parse "origin/$branch")" ] || problem "$repo is not at origin/$branch"
for d in "$repo"/dev-skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  n="$(basename "$d")"
  [ "$(readlink "$claude/$n" 2>/dev/null)" = "${d%/}" ] || problem "$claude/$n does not link to ${d%/}"
done
for l in "$claude"/*; do
  [ -L "$l" ] || continue
  t="$(readlink "$l")"
  case "$t" in "$repo"/dev-skills/*) [ -f "$l/SKILL.md" ] || problem "$l is a dangling link: $t" ;; esac
  ! other_kook "$t" || problem "$l links into another checkout: $t"
done
[ "$(readlink "$agents" 2>/dev/null)" = "$repo/dev-skills" ] || problem "$agents does not link to $repo/dev-skills"

[ "$issues" -eq 0 ] || exit 1
echo "ok: agents load $repo at $(g rev-parse --short HEAD)"
