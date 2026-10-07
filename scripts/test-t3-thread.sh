#!/usr/bin/env bash
# Tests for t3-thread.sh against a throwaway T3 state database.
# Usage: scripts/test-t3-thread.sh
set -euo pipefail
src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export T3_STATE_DB="$tmp/state.sqlite"
id=11111111-2222-3333-4444-555555555555
sqlite3 "$T3_STATE_DB" <<SQL
create table projection_threads (thread_id text primary key, title text, branch text, worktree_path text);
create table projection_thread_messages (message_id text primary key, thread_id text, role text, text text, created_at text);
insert into projection_threads values ('$id', 'Fix login', 'fix/login', '/w');
insert into projection_thread_messages values
  ('m1', '$id', 'user', 'please fix login', '2026-10-07T01:00:00Z'),
  ('m2', '$id', 'reasoning', 'secret thoughts', '2026-10-07T01:00:01Z'),
  ('m3', '$id', 'assistant', 'fixed it', '2026-10-07T01:00:02Z'),
  ('m4', 'other', 'user', 'unrelated', '2026-10-07T01:00:03Z');
SQL

passed=0 failed=0
check() { local d="$1"; shift; if "$@"; then passed=$((passed+1)); else failed=$((failed+1)); echo "FAIL: $d"; fi; }
lacks() { ! grep -q -- "$1" <<<"$2"; }
fails() { ! "$@" >/dev/null 2>&1; }
line_of() { grep -n -- "$1" <<<"$2" | cut -d: -f1; }
before() { [ "$(line_of "$1" "$3")" -lt "$(line_of "$2" "$3")" ]; }
out="$("$src/t3-thread.sh" "$id")"
check "prints the title"              grep -q 'Fix login' <<<"$out"
check "prints user messages"          grep -q 'please fix login' <<<"$out"
check "prints assistant messages"     grep -q 'fixed it' <<<"$out"
check "skips reasoning"               lacks "secret thoughts" "$out"
check "skips other threads"           lacks unrelated "$out"
check "user message comes first"      before "please fix login" "fixed it" "$out"
users="$("$src/t3-thread.sh" "$id" --users-only)"
check "--users-only keeps user"       grep -q 'please fix login' <<<"$users"
check "--users-only drops assistant"  lacks "fixed it" "$users"
check "rejects a non-uuid id"         fails "$src/t3-thread.sh" "x' or 1=1 --"
check "rejects an unknown flag"        fails "$src/t3-thread.sh" "$id" --user-only
check "rejects extra arguments"       fails "$src/t3-thread.sh" "$id" --users-only extra
check "unknown id fails"              fails "$src/t3-thread.sh" 99999999-2222-3333-4444-555555555555
check "missing database fails"        fails env T3_STATE_DB=/nonexistent "$src/t3-thread.sh" "$id"
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
