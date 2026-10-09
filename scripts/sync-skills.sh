#!/usr/bin/env bash
# Keep the copy of kook that agents load skills from (the "live copy") on
# origin/main, and keep ~/.claude/skills/* and ~/.agents/skills/* pointing into it.
# Also links profile.md (the owner's personal setup) as the global instructions
# file of each installed harness, and profile-claude.md as a Claude Code rules
# file, unless that file is the owner's own.
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
buckets=(dev-skills writing vendor) # same list as link-skills.sh
declare -A profiles=( # link -> the file in kook it points to
  ["$HOME/.claude/CLAUDE.md"]=profile.md
  ["$HOME/.codex/AGENTS.md"]=profile.md
  ["$HOME/.claude/rules/kook-profile.md"]=profile-claude.md # Claude Code only
)
case "${1:-}" in "" | --check) mode="${1:-sync}" ;; *) echo "usage: $0 [--check]" >&2; exit 2 ;; esac
g() { git -C "$repo" "$@"; }
issues=0
problem() { echo "PROBLEM: $*" >&2; issues=$((issues + 1)); }
origin="$(g remote get-url origin)"
other_kook() { # is link target $1 a skill (<clone>/<bucket>/<name>) in some other clone of kook?
  local b
  case "$1" in "$repo"/*) return 1 ;; esac
  for b in "${buckets[@]}"; do
    case "$1" in */"$b"/*) [ "$(git -C "${1%/"$b"/*}" remote get-url origin 2>/dev/null)" = "$origin" ] && return 0 ;; esac
  done
  return 1
}
kook_profile() { # is link target $1 the root file $2 (profile.md, ...) of some clone of kook?
  case "$1" in */"$2") ;; *) return 1 ;; esac
  local d="${1%/"$2"}"
  [ "$(git -C "$d" rev-parse --show-toplevel 2>/dev/null)" = "$(cd "$d" 2>/dev/null && pwd -P)" ] &&
    [ "$(git -C "$d" remote get-url origin)" = "$origin" ]
}
link_target() { # where link $1 points, as an absolute path (relative targets resolve from the link's folder)
  local t
  t="$(readlink "$1")" || return 1
  case "$t" in /*) ;; *) t="$(cd "$(dirname "$1")" && pwd -P)/$t" ;; esac # real folder first, then collapse ..
  realpath -ms "$t"
}
wants_profile() { # link $1 to file $2: kook has the file and the harness (~/.claude, ~/.codex) is installed
  local rel="${1#"$HOME"/}"
  [ -f "$repo/$2" ] && [ -d "$HOME/${rel%%/*}" ]
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
  if [ -L "$agents" ]; then rm "$agents"; echo "$agents is now a folder of links"; fi # was one link to dev-skills/
  for dst in "$claude" "$agents"; do
    "$repo/scripts/link-skills.sh" "$dst" | grep -v '^ok:' || true
    for l in "$dst"/*; do # links into another checkout that link-skills did not repoint: not on main
      if [ -L "$l" ] && other_kook "$(readlink "$l")"; then rm "$l"; echo "removed $(basename "$l") (not on $branch)"; fi
    done
  done
  for f in "${!profiles[@]}"; do # never replace the owner's own file or symlink
    s="${profiles[$f]}"
    wants_profile "$f" "$s" || continue
    if { [ ! -e "$f" ] && [ ! -L "$f" ]; } || kook_profile "$(link_target "$f")" "$s"; then
      mkdir -p "$(dirname "$f")" && ln -sfn "$repo/$s" "$f"
    fi
  done
fi

[ "$(g rev-parse HEAD)" = "$(g rev-parse "origin/$branch")" ] || problem "$repo is not at origin/$branch"
[ ! -L "$agents" ] || problem "$agents is one link, not a folder of links"
for dst in "$claude" "$agents"; do
  for b in "${buckets[@]}"; do
    for d in "$repo/$b"/*/; do
      [ -f "$d/SKILL.md" ] || continue
      n="$(basename "$d")"
      [ "$(readlink "$dst/$n" 2>/dev/null)" = "${d%/}" ] || problem "$dst/$n does not link to ${d%/}"
    done
  done
  for l in "$dst"/*; do
    [ -L "$l" ] || continue
    t="$(readlink "$l")"
    case "$t" in "$repo"/*) [ -f "$l/SKILL.md" ] || problem "$l is a dangling link: $t" ;; esac
    ! other_kook "$t" || problem "$l links into another checkout: $t"
  done
done
for f in "${!profiles[@]}"; do
  s="${profiles[$f]}"
  wants_profile "$f" "$s" || continue
  t="$(link_target "$f" 2>/dev/null || true)"
  if [ "$t" = "$repo/$s" ]; then :
  elif [ ! -e "$f" ] && [ ! -L "$f" ]; then problem "$f does not link to $repo/$s"
  elif kook_profile "$t" "$s"; then problem "$f links into another checkout: $t"
  else echo "note: $f is your own file, so $s is not loaded there" >&2
  fi
done

[ "$issues" -eq 0 ] || exit 1
echo "ok: agents load $repo at $(g rev-parse --short HEAD)"
