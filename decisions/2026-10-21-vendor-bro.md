# Vendor bro

**Context.** The owner asked to install `bro` from poteto's [pstack](https://github.com/cursor/plugins/tree/190d28736eff128ec94f502a22c7fe0c4b56cd37/pstack/skills/bro) into Kook. It restates the agent's last message in plain language, without jargon. No observed failure motivated the request.

**Decision.** Copy `SKILL.md` unchanged into `vendor/bro`, with pstack's MIT `LICENSE`, pinned in `SOURCES.md`. Existing bucket linking installs it after merge.

**Why.** Upstream sets `disable-model-invocation: true`, so it changes nothing until the owner types `/bro`. As with `handoff` and `teach` (`2026-10-15-vendor-handoff-teach.md`), the owner's request is enough for a manual-only vendored skill.
