# The owner merges; docs-only changes are still reviewed

**Context.** Early skills let agents merge their own PRs and skip review for docs-only diffs (PR #2).

**Decision.** Agents never merge, tag, deploy or push to the default branch. Documentation and config changes get the same independent review as code.

**Why.** Merge authority is the owner's main control. Skill and docs changes shape agent behaviour as much as code does.
