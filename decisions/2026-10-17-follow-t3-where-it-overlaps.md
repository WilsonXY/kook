# Inside T3 Code, T3's own tools win, except for reviews

**Context.** T3 Code 0.1.0 adds an orchestration section to every agent's system prompt, and tools that overlap kook's skills (#36). `watch_pull_request` and async `delegate_task` wake the agent and tell it to end the turn, while `long-running-commands` said "nothing will wake you" and `full-cycle` polled `gh pr checks`. `html_preview` and `html_render` show a page inline in the thread, while `html-communicate` delivered only by Tailscale link. T3 also tells agents to run review rounds through `delegate_task`.

**Decision.** The owner asked that kook respect T3: inside T3, follow T3 where it covers the same job.
- `long-running-commands` and `full-cycle`: a harness tool that wakes you counts as waiting. Without one, the old rule stands.
- `html-communicate`: inline first, a link only when the harness can't show the page or the user asks for one; a harness preview screenshot counts as viewing the page.
- Reviews stay on the CLI route in `profile.md`, because `delegate_task` children inherit write access and T3 says a narrower mode "is not a read-only switch". Revisit in #38. Superseded by `2026-10-18-t3-reviews-in-worktree.md`.

**Why here.** The skills say it portably ("a harness tool that wakes you", "if your harness can show the page"), because `dev-skills/` may not name a harness or its tools. `profile.md` names T3 and its tools, which are the owner's setup.

**Rejected.**
- Only a `profile.md` line: the skills would still say "never end your turn" and "deliver by link", which contradicts the profile in every T3 session.
- Allowing `delegate_task` reviews with plan mode and worktree isolation: untested for Codex children. That's #38.

**Rollback.** Revert the PR. Agents then poll and serve links again inside T3, which still works, just more slowly.
