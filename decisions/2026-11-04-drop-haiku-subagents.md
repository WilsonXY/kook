# Drop the Haiku subagent rule

**Context.** `profile-claude.md` asked Claude Code to fan out five or more independent items to subagents, every one on Haiku at high effort (`2026-10-10-claude-subagents.md`). The owner found it unnecessary and of no use in daily work. It also overrode skills that pick their own subagent models, such as pstack's `how`, which wants Opus for its explainers.

**Decision.** Remove the whole Subagents section. Claude Code falls back to its default: spawn when the owner asks or a skill says to, on the model the skill names.

**Why.** The October trial showed the rule made sessions spawn, but the Haiku spend came on top of the main agent's cost and its context did not shrink. With no daily benefit, it is surface to maintain and a conflict with vendored skills.
