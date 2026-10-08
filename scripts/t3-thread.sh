#!/usr/bin/env bash
# Print a T3 Code thread's user and assistant messages (no reasoning), oldest first,
# read-only from T3's state database. Used by the retro skill to read past sessions.
# Usage: scripts/t3-thread.sh <thread-id> [--users-only]
set -euo pipefail
db="${T3_STATE_DB:-$HOME/.t3/userdata/state.sqlite}"
id="${1:-}"
[[ "$id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || { echo "usage: $0 <thread-uuid> [--users-only]" >&2; exit 2; }
case "$#:${2:-}" in
  1:) roles="'user','assistant'" ;;
  2:--users-only) roles="'user'" ;;
  *) echo "usage: $0 <thread-uuid> [--users-only]" >&2; exit 2 ;;
esac
[ -f "$db" ] || { echo "no T3 database at $db" >&2; exit 1; }
q() { sqlite3 -readonly "$db" "$1"; }
title="$(q "select '# '||title||' ('||coalesce(branch,'-')||')' from projection_threads where thread_id='$id';")"
[ -n "$title" ] || { echo "no thread $id in $db" >&2; exit 1; }
echo "$title"
q "select char(10)||'## '||role||' · '||substr(created_at,1,16)||char(10)||text from projection_thread_messages where thread_id='$id' and role in ($roles) order by created_at;"
