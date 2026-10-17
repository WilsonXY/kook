# Owner profile

Personal setup for every agent session on this machine. Skills in `dev-skills/` stay portable and point here for anything specific to this owner, these tools or this machine. `scripts/sync-skills.sh` links this file as `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Claude Code also loads `profile-claude.md`, which Codex never sees.

## Coding style
On every coding task, load the `ponytail` skill at full intensity next to `full-cycle`, without waiting to be asked. Ponytail shortens the code, never the workflow: tests, review and the PR still happen.

## Reviewer routing
Used by `requesting-code-review` when the task names no reviewer. Unless the exception below applies, try in order:
1. Codex CLI, model `gpt-6.1-sol`, reasoning effort high, run non-interactively at the repo root (`codex exec`, in a pseudo-terminal if needed), read-only.
2. Fallback if Codex is unavailable (usage limit, not installed): OpenCode CLI, model `opencode/muse-spark-1.3-contributor-free`, effort xhigh (`opencode run`).

Exception: when `gpt-6.1-sol` implemented the change (wrote the diff, itself or as a delegated child), use this route instead, each in a fresh read-only context:
1. Claude Code CLI, model `claude-opus-5-5`, effort high (`claude -p --model claude-opus-5-5 --effort high --permission-mode plan`).
2. Fallback if Claude is unavailable or usage-limited: Codex CLI, model `gpt-6-astra`, reasoning effort high (`codex exec`, read-only).

Under this exception, name in the PR and in your final report the reviewer that actually ran and any fallback, with its model and effort confirmed from the reviewer's own output or logs where they show it; the requested settings alone are not proof. In the PR one line is enough (reviewer, model, effort, where confirmed, result); fuller evidence goes in the final report.

Inside T3 Code, run the same reviewer (model, effort) through `delegate_task` instead of its CLI, with `role: "review"` and `isolation: "worktree"`; use the CLI only if `delegate_task` can't run it. The child inherits this thread's write access, so read-only is checked, not enforced:
- Commit first: the worktree gets committed code only. Tell the child not to edit, commit, push or post to GitHub.
- Afterwards, `git rev-parse HEAD`, `git status` and `git ls-remote --heads origin` here must match what they were before, and the child's worktree (`git worktree list`) must still be at its starting commit with a clean `git status`. Any write fails the review: discard it, say so, and review again.
- Model and effort proof is the child's own session log (`~/.codex/sessions/`, or `~/.claude/projects/<worktree>/`).

## T3 Code
Inside T3 Code 0.1.0+, where T3's own instructions or tools cover the same job as a skill, follow T3. Its PR watch (`watch_pull_request`) and the wake-up when an async task finishes count as waiting for `long-running-commands` and `full-cycle`. For `html-communicate`, show the page with `html_render`, after checking it with `html_preview` at 390px and 728px, before any Tailscale link.

## Sharing reports and previews
Private links go over Tailscale: if `tailscale status` works, run `tailscale serve --bg --https=<port> http://127.0.0.1:<port>` over a local `python3 -m http.server <port> --bind 127.0.0.1 --directory <folder>`. Without `--bind` it listens on every interface, so the LAN can read it too. The folder holds only pages meant to be read: everything in it can be browsed.

## Session history
- Pasted UUIDs are usually T3 Code thread ids. Read one with `~/.local/share/kook/scripts/t3-thread.sh <thread-id>` (add `--users-only` for just the owner's messages).

## Skill inbox
Lessons about skills and agent setup (from `retro` or noticed mid-task) go to GitHub issues on `WilsonXY/kook` with the label `inbox`: `gh issue create -R WilsonXY/kook --label inbox`. The repo is public: paraphrase, cite thread ids, and leave out secrets and private details.

## This machine
- `/tmp` is a small RAM disk that is often nearly full. For large downloads or builds, set `TMPDIR` to a folder under `$HOME`.
- Kook skills load from `~/.local/share/kook`, a copy a timer keeps on `origin/main`. Never work in it; work in `~/projects/kook` or a worktree.
