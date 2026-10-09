#!/usr/bin/env bash
# Tests for sync-skills.sh, run against a throwaway origin and a fake $HOME.
# Usage: scripts/test-sync-skills.sh
set -euo pipefail
src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp/home" GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
mkdir -p "$HOME"
live="$HOME/.local/share/kook"
claude="$HOME/.claude/skills"
agents="$HOME/.agents/skills"

passed=0 failed=0
expect_ok()   { local d="$1"; shift; if "$@" >"$tmp/out" 2>&1; then passed=$((passed+1)); else failed=$((failed+1)); echo "FAIL (expected success): $d"; sed 's/^/  | /' "$tmp/out"; fi; }
expect_fail() { local d="$1"; shift; if "$@" >"$tmp/out" 2>&1; then failed=$((failed+1)); echo "FAIL (expected failure): $d"; sed 's/^/  | /' "$tmp/out"; else passed=$((passed+1)); fi; }
links_to()    { [ "$(readlink "$1")" = "$2" ]; }
sync()        { "$live/scripts/sync-skills.sh" "$@"; }
add_skill()   { local b="${2:-dev-skills}"; mkdir -p "$tmp/dev/$b/$1"; printf -- '---\nname: %s\n---\n' "$1" >"$tmp/dev/$b/$1/SKILL.md"; }
push()        { git -C "$tmp/dev" add -A; git -C "$tmp/dev" commit -qm "$1"; git -C "$tmp/dev" push -q origin HEAD:main; }

git init -q --bare -b main "$tmp/origin.git"
git init -q "$tmp/dev"
git -C "$tmp/dev" remote add origin "$tmp/origin.git"
cp -r "$src" "$tmp/dev/scripts"
add_skill alpha
push init
mkdir "$tmp/bin"
printf '#!/bin/sh\necho "$*" >>"%s/systemctl.log"\n' "$tmp" >"$tmp/bin/systemctl"
chmod +x "$tmp/bin/systemctl"

expect_ok   "install clones the live copy and syncs" env PATH="$tmp/bin:$PATH" "$tmp/dev/scripts/install-skills.sh"
expect_ok   "install enables the timer"             grep -qx -- "--user enable --now kook-skills-sync.timer" "$tmp/systemctl.log"
expect_ok   "install copies the units"              test -f "$HOME/.config/systemd/user/kook-skills-sync.service"
expect_ok   "install is safe to re-run"             env PATH="$tmp/bin:$PATH" "$tmp/dev/scripts/install-skills.sh"
expect_ok   "sync succeeds"                         sync
expect_ok   "claude link points into live copy"     links_to "$claude/alpha" "$live/dev-skills/alpha"
expect_ok   "agents link points into live copy"     links_to "$agents/alpha" "$live/dev-skills/alpha"
expect_ok   "agents skills dir is a real folder"     test -d "$agents" -a ! -L "$agents"
expect_ok   "check passes after sync"               sync --check

rm -r "$agents"; ln -s "$live/dev-skills" "$agents"
expect_fail "check reports the old whole-folder link" sync --check
expect_ok   "sync replaces it"                      sync
expect_ok   "  with a real folder"                  test -d "$agents" -a ! -L "$agents"
expect_ok   "  of skill links"                      links_to "$agents/alpha" "$live/dev-skills/alpha"
expect_ok   "  and the live copy stays clean"       test -z "$(git -C "$live" status --porcelain)"

add_skill prose writing; add_skill borrowed vendor; push "add writing and vendor skills"
expect_ok   "sync with every bucket"                sync
expect_ok   "writing skill linked for claude"       links_to "$claude/prose" "$live/writing/prose"
expect_ok   "vendor skill linked for claude"        links_to "$claude/borrowed" "$live/vendor/borrowed"
expect_ok   "writing skill linked for agents"       links_to "$agents/prose" "$live/writing/prose"
expect_ok   "vendor skill linked for agents"        links_to "$agents/borrowed" "$live/vendor/borrowed"
expect_ok   "check passes with every bucket"        sync --check
rm "$agents/prose"
expect_fail "check reports a missing agents link"   sync --check
ln -sfn "$tmp/dev/writing/prose" "$claude/prose"
expect_fail "check reports a writing link into another checkout" sync --check
expect_ok   "sync repoints it"                      sync
expect_ok   "  to the live copy"                    links_to "$claude/prose" "$live/writing/prose"
expect_ok   "  and relinks the agents one"          links_to "$agents/prose" "$live/writing/prose"
mkdir -p "$agents/own"; touch "$agents/own/SKILL.md"
expect_ok   "own skill in the agents dir: sync succeeds" sync
expect_ok   "  and keeps it"                        test -f "$agents/own/SKILL.md"
expect_ok   "  and check passes"                    sync --check
rm -r "$tmp/dev/vendor/borrowed"; push "remove borrowed"
expect_ok   "sync after a vendor skill is deleted"  sync
expect_fail "its claude link is removed"            test -L "$claude/borrowed"
expect_fail "its agents link is removed"            test -L "$agents/borrowed"

printf '# profile\n' >"$tmp/dev/profile.md"; push "add profile"
expect_ok   "sync with a profile"                   sync
expect_ok   "claude reads the profile"              links_to "$HOME/.claude/CLAUDE.md" "$live/profile.md"
expect_fail "no ~/.codex: nothing created there"    test -e "$HOME/.codex"
mkdir "$HOME/.codex"
expect_fail "check reports a missing profile link"  sync --check
expect_ok   "sync links it"                         sync
expect_ok   "codex reads the profile"               links_to "$HOME/.codex/AGENTS.md" "$live/profile.md"
expect_ok   "check passes with profile links"       sync --check
rm "$HOME/.codex/AGENTS.md"; echo mine >"$HOME/.codex/AGENTS.md"
expect_ok   "own AGENTS.md: sync still succeeds"    sync
expect_ok   "own AGENTS.md is untouched"            grep -qx mine "$HOME/.codex/AGENTS.md"
expect_ok   "own AGENTS.md: check passes"           sync --check
rm "$HOME/.codex/AGENTS.md"; ln -s "$tmp/mine.md" "$HOME/.codex/AGENTS.md"
expect_ok   "own symlink: sync still succeeds"      sync
expect_ok   "own symlink is untouched"              links_to "$HOME/.codex/AGENTS.md" "$tmp/mine.md"
rm "$HOME/.codex/AGENTS.md"; ln -s "$tmp/dev/profile.md" "$HOME/.codex/AGENTS.md"
expect_fail "check reports a profile link into another checkout" sync --check
expect_ok   "sync repoints it"                      sync
expect_ok   "profile link back on the live copy"    links_to "$HOME/.codex/AGENTS.md" "$live/profile.md"
mkdir -p "$tmp/dev/private"; echo mine >"$tmp/dev/private/profile.md"
rm "$HOME/.codex/AGENTS.md"; ln -s "$tmp/dev/private/profile.md" "$HOME/.codex/AGENTS.md"
expect_ok   "own profile.md inside a kook checkout: sync succeeds" sync
expect_ok   "  and leaves that symlink alone"       links_to "$HOME/.codex/AGENTS.md" "$tmp/dev/private/profile.md"
rm "$HOME/.codex/AGENTS.md"; ln -s ../../dev/profile.md "$HOME/.codex/AGENTS.md"
expect_fail "check reports a relative link into another checkout" sync --check
expect_ok   "sync repoints it"                      sync
expect_ok   "  to the live copy"                    links_to "$HOME/.codex/AGENTS.md" "$live/profile.md"
rm "$HOME/.codex/AGENTS.md"; ln -s ../.local/share/kook/profile.md "$HOME/.codex/AGENTS.md"
expect_ok   "a relative link to the live profile is fine" sync --check
mv "$HOME/.codex" "$tmp/codex-real"; ln -s "$tmp/codex-real" "$HOME/.codex"
rm "$HOME/.codex/AGENTS.md"; ln -s ../dev/profile.md "$HOME/.codex/AGENTS.md"
expect_fail "symlinked ~/.codex: relative link into another checkout is reported" sync --check
expect_ok   "sync repoints it"                      sync
expect_ok   "  to the live copy"                    links_to "$HOME/.codex/AGENTS.md" "$live/profile.md"
rm "$HOME/.codex"; mv "$tmp/codex-real" "$HOME/.codex"
rm -r "$tmp/dev/private"

add_skill beta; push "add beta"
expect_fail "check reports live copy behind origin" sync --check
expect_ok   "sync fast-forwards"                    sync
expect_ok   "new skill is linked"                   links_to "$claude/beta" "$live/dev-skills/beta"

rm -r "$tmp/dev/dev-skills/alpha"; push "remove alpha"
expect_ok   "sync after a skill is deleted"         sync
expect_fail "deleted skill's link is removed"       test -L "$claude/alpha"

ln -sfn "$tmp/dev/dev-skills/beta" "$claude/beta"
expect_fail "check reports link into another checkout" sync --check
expect_ok   "sync repoints it"                      sync
expect_ok   "link is back on the live copy"         links_to "$claude/beta" "$live/dev-skills/beta"

add_skill unmerged
ln -sfn "$tmp/dev/dev-skills/unmerged" "$claude/unmerged"
expect_fail "check reports a link to another checkout's unmerged skill" sync --check
expect_ok   "sync removes it"                       sync
expect_fail "unmerged skill's link is gone"         test -L "$claude/unmerged"
expect_ok   "the other checkout is untouched"       test -f "$tmp/dev/dev-skills/unmerged/SKILL.md"
rm -r "$tmp/dev/dev-skills/unmerged"

mkdir -p "$tmp/other/dev-skills/theirs"; touch "$tmp/other/dev-skills/theirs/SKILL.md"
ln -s "$tmp/other/dev-skills/theirs" "$claude/theirs"
expect_ok   "link into a non-kook dev-skills is not a problem" sync --check
expect_ok   "sync leaves it alone"                  sync
expect_ok   "non-kook link kept"                    links_to "$claude/theirs" "$tmp/other/dev-skills/theirs"

ln -s "$live/dev-skills/ghost" "$claude/ghost"
expect_fail "check reports a dangling link into the live copy" sync --check
expect_ok   "sync removes the dangling link"        sync
expect_fail "dangling link is gone"                 test -L "$claude/ghost"

add_skill husk; touch "$tmp/dev/dev-skills/husk/notes.md"; push "add husk"
expect_ok   "sync links husk"                       sync
rm "$tmp/dev/dev-skills/husk/SKILL.md"; push "husk loses SKILL.md"
expect_ok   "sync after SKILL.md removed, folder kept" sync
expect_fail "its link is removed"                   test -L "$claude/husk"

git -C "$live" switch -q -c feature
add_skill gamma; push "add gamma"
expect_fail "sync refuses when live copy is off main" sync
expect_fail "check reports live copy off main"      sync --check
expect_ok   "branch left alone"                     test "$(git -C "$live" branch --show-current)" = feature
expect_fail "nothing linked while refused"          test -e "$claude/gamma"
git -C "$live" switch -q main

touch "$live/stray"
expect_fail "sync refuses when live copy is dirty"  sync
expect_fail "check reports dirty live copy"         sync --check
rm "$live/stray"
expect_ok   "sync recovers once clean"              sync
expect_ok   "skill added meanwhile is linked"       links_to "$claude/gamma" "$live/dev-skills/gamma"


expect_fail "unknown argument is rejected"          sync --bogus

echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
