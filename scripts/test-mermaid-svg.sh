#!/usr/bin/env bash
# Tests for html-communicate's mermaid-svg.mjs. Installs Pele into a throwaway cache (needs npm and the network).
# Usage: scripts/test-mermaid-svg.sh
set -euo pipefail
script="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/dev-skills/html-communicate/mermaid-svg.mjs"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export XDG_CACHE_HOME="$tmp"

passed=0 failed=0
check() { local d="$1"; shift; if "$@"; then passed=$((passed+1)); else failed=$((failed+1)); echo "FAIL: $d"; fi; }
out="$(printf 'flowchart LR\n  A[Browser] --> B[Gateway]\n' | node "$script")"
check "prints an SVG"                 grep -q '^<svg' <<<"$out"
check "keeps the labels"              grep -q 'Gateway' <<<"$out"
check "colours come from CSS vars"    grep -q 'var(--pele-fg' <<<"$out"
check "installs into the cache"       test -d "$tmp/pele-1.6.0/node_modules/pele"
rejects() { ! node "$script" <<<"$1" >/dev/null 2>&1; }
check "bad Mermaid fails"             rejects 'not a diagram'

# A failed install leaves no cache behind: a fake npm writes half a package, then fails.
mkdir -p "$tmp/bin" "$tmp/broken"
cat > "$tmp/bin/npm" <<'NPM'
#!/bin/sh
mkdir -p "$3/node_modules/pele/dist" && echo "export const" > "$3/node_modules/pele/dist/pele.js"
exit 1
NPM
chmod +x "$tmp/bin/npm"
broken() { PATH="$tmp/bin:$PATH" XDG_CACHE_HOME="$tmp/broken" rejects 'flowchart LR'; }
check "failed install fails"          broken
check "failed install leaves nothing" test -z "$(ls -A "$tmp/broken")"

# Parallel first runs on an empty cache all succeed.
mkdir "$tmp/race"
for i in 1 2 3 4; do (echo 'flowchart LR' | XDG_CACHE_HOME="$tmp/race" node "$script" >"$tmp/race-$i.svg" 2>/dev/null) & done
wait
all_svg() { for f in "$tmp"/race-*.svg; do grep -q '^<svg' "$f" || return 1; done; }
check "parallel first runs succeed"   all_svg
check "parallel runs leave one cache" test "$(ls "$tmp/race")" = pele-1.6.0
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
