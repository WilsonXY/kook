# Personal setup lives in profile.md

**Context.** Reviewer models and Tailscale were written into portable skills. Machine lessons went into one harness's memory only.

**Decision.** `profile.md` holds the owner's tools, models and machine quirks. `sync-skills.sh` links it as `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Portable skills point to "the owner's global instructions" (PR #8). `scripts/doctor.py` fails on model, harness or host names in `dev-skills/`.
