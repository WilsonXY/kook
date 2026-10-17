#!/usr/bin/env bash
# Print a T3 Code thread's user and assistant messages (no reasoning), oldest first,
# read-only from T3's state database. Used by the retro skill to read past sessions.
# T3 Code 0.1.0+ (V2) writes to statev2.sqlite; older versions to state.sqlite.
# Usage: scripts/t3-thread.sh <thread-id> [--users-only]
set -euo pipefail
db="${T3_STATE_DB:-$HOME/.t3/userdata/statev2.sqlite}"
[ -n "${T3_STATE_DB:-}" ] || [ -f "$db" ] || db="$HOME/.t3/userdata/state.sqlite"
id="${1:-}"
[[ "$id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || { echo "usage: $0 <thread-uuid> [--users-only]" >&2; exit 2; }
case "$#:${2:-}" in
  1:) roles="'user','assistant'" ;;
  2:--users-only) roles="'user'" ;;
  *) echo "usage: $0 <thread-uuid> [--users-only]" >&2; exit 2 ;;
esac
[ -f "$db" ] || { echo "no T3 database at $db" >&2; exit 1; }
q() { sqlite3 -readonly "$db" "$1"; }
has() { [ -n "$(q "select 1 from sqlite_master where name='$1';")" ]; }
fmt="char(10)||'## '||role||' · '||substr(created_at,1,16)||char(10)"
title="" msgs=""
if has orchestration_v2_projection_threads; then
  title="$(q "select '# '||title||' ('||coalesce(json_extract(payload_json,'\$.branch'),'-')||')' from orchestration_v2_projection_threads where thread_id='$id';")"
  msgs="$(q "select $fmt||json_extract(payload_json,'\$.text') from orchestration_v2_projection_messages where thread_id='$id' and streaming=0 and role in ($roles) order by created_at, message_id;")"
fi
# Threads from before V2 keep their transcript in the legacy tables until T3 imports it.
if has projection_threads; then
  [ -n "$title" ] || title="$(q "select '# '||title||' ('||coalesce(branch,'-')||')' from projection_threads where thread_id='$id';")"
  [ -n "$msgs" ] || msgs="$(q "select $fmt||text from projection_thread_messages where thread_id='$id' and role in ($roles) order by created_at;")"
fi
[ -n "$title" ] || { echo "no thread $id in $db" >&2; exit 1; }
echo "$title"
[ -z "$msgs" ] || echo "$msgs"
