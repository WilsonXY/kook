# Vendor handoff and teach

**Context.** The owner asked for Matt Pocock's `handoff` (write a handoff doc for a fresh agent) and `teach` (a multi-session teaching workspace) from [mattpocock/skills](https://github.com/mattpocock/skills) `skills/productivity/`. No observed failure motivated them.

**Decision.** Copy both unmodified into `vendor/`, with upstream `LICENSE` and pins in `SOURCES.md`. Upstream disables model invocation, so neither changes what an agent does unless the owner types `/handoff` or `/teach`.

**Why.** The `SCOPE.md` bar guards changes to agent behaviour. A manual-only vendored skill changes nothing until called, so the owner's request is enough, as with `vendor/show-me`. Edits to either still need the bar; to change one, adapt it into `dev-skills/` or `writing/` instead.
