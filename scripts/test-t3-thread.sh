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

# T3 Code 0.1.0+ (V2) copies state.sqlite into statev2.sqlite once and writes new threads to V2
# tables; old transcripts stay in the copied legacy tables until T3 imports them.
v2="$tmp/home/.t3/userdata/statev2.sqlite"
mkdir -p "${v2%/*}"
cp "$T3_STATE_DB" "$v2"
new=22222222-2222-3333-4444-555555555555
sqlite3 "$v2" <<SQL
create table orchestration_v2_projection_threads (thread_id text primary key, title text, payload_json text);
create table orchestration_v2_projection_messages (message_id text primary key, thread_id text, role text, streaming integer, created_at text, payload_json text);
insert into orchestration_v2_projection_threads values
  ('$new', 'Add search', '{"branch":"feat/search"}'),
  ('$id', 'Fix login', '{"branch":"fix/login"}');
insert into orchestration_v2_projection_messages values
  ('n1', '$new', 'user', 0, '2026-10-17T01:00:00Z', '{"text":"add search"}'),
  ('n2', '$new', 'assistant', 1, '2026-10-17T01:00:01Z', '{"text":"half a repl"}'),
  ('n3', '$new', 'assistant', 0, '2026-10-17T01:00:02Z', '{"text":"search added"}');
SQL
out="$(env -u T3_STATE_DB HOME="$tmp/home" "$src/t3-thread.sh" "$new" || true)"
check "V2: reads statev2.sqlite by default" grep -q 'Add search (feat/search)' <<<"$out"
check "V2: prints user messages"         grep -q 'add search' <<<"$out"
check "V2: prints assistant messages"    grep -q 'search added' <<<"$out"
check "V2: skips streaming messages"     lacks "half a repl" "$out"
out="$(env -u T3_STATE_DB HOME="$tmp/home" "$src/t3-thread.sh" "$id" || true)"
check "V2: old transcript from legacy tables" grep -q 'please fix login' <<<"$out"
users="$(env -u T3_STATE_DB HOME="$tmp/home" "$src/t3-thread.sh" "$new" --users-only || true)"
check "V2: --users-only keeps user"      grep -q "add search" <<<"$users"
check "V2: --users-only drops assistant" lacks "search added" "$users"
check "T3_STATE_DB beats statev2.sqlite" fails env HOME="$tmp/home" "$src/t3-thread.sh" "$new"
mkdir -p "$tmp/v1/.t3/userdata" && cp "$T3_STATE_DB" "$tmp/v1/.t3/userdata/state.sqlite"
out="$(env -u T3_STATE_DB HOME="$tmp/v1" "$src/t3-thread.sh" "$id" || true)"
check "no statev2.sqlite: falls back to state.sqlite" grep -q 'please fix login' <<<"$out"
echo "$passed passed, $failed failed"
[ "$failed" -eq 0 ]
