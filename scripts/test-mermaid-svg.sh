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
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
