# Owner profile

Personal setup for every agent session on this machine. Skills in `dev-skills/` stay portable and point here for anything specific to this owner, these tools or this machine. `scripts/sync-skills.sh` links this file as `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`.

## Reviewer routing
Used by `requesting-code-review` when the task names no reviewer. Try in order:
1. Codex CLI, model `gpt-6.1-sol`, reasoning effort high, run non-interactively at the repo root (`codex exec`, in a pseudo-terminal if needed), read-only.
2. Fallback if Codex is unavailable (usage limit, not installed): OpenCode CLI, model `opencode/muse-spark-1.3-contributor-free`, effort xhigh (`opencode run`).

## Sharing reports and previews
Private links go over Tailscale: if `tailscale status` works, run `tailscale serve --bg --https=<port> http://127.0.0.1:<port>` over a local `python3 -m http.server`.

## This machine
- `/tmp` is a small RAM disk that is often nearly full. For large downloads or builds, set `TMPDIR` to a folder under `$HOME`.
- Kook skills load from `~/.local/share/kook`, a copy a timer keeps on `origin/main`. Never work in it; work in `~/projects/kook` or a worktree.
