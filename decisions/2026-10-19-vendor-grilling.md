# Vendor grilling

**Context.** The owner asked to install Matt Pocock's [grilling](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling) in `vendor/` (T3 thread `3dd7c38e-574b-4d67-974a-2e828fd2a29a`). It has no dependency on Matt's other skills. No observed failure motivated the request; the owner's explicit installation request authorizes this addition.

**Decision.** Copy the skill and `agents/openai.yaml` unchanged, alongside the upstream MIT `LICENSE`, pinned in `SOURCES.md`. Existing bucket linking installs it after merge; no installer or profile changes are needed.

**Why.** The owner wants to stress-test plans, decisions and ideas through rounds of questions. Unlike `handoff` and `teach`, upstream does not disable model invocation: its description also triggers when the owner asks to stress-test their thinking or uses grill phrases. This changes agent behavior and departs from the manual-only rationale in `2026-10-15-vendor-handoff-teach.md`; this addition rests on the owner's explicit request rather than that precedent. Preserve upstream's behavior. The skill calls for sub-agents to investigate facts and waits for shared understanding before acting.

**Verification.** The copied files matched the pin byte for byte, and bucket linking resolved `grilling` correctly in a throwaway directory. No existing skill was rewritten; there was no inbox failure or before/after behavior scenario for this import. The current scenario runner and doctor accept scenarios only for `dev-skills/`; they were left unchanged for this vendor copy.
