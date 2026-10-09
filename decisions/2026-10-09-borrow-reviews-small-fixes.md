# Skill comparisons: take the fixes, not the redesigns

**Context.** Three threads compared Kook skills with popular ones and proposed changes: a rewrite of `html-communicate` (thread 80813318), `light`/`rewrite`/`audit` modes for `wilson-humanizer` (23a73360), and an adapted show-me skill wired into `html-communicate`, the GitHub PR guide and `full-cycle` (db48e657). None started from a failure in a real session.

**Decision.** Keep only the fixes for rules that are wrong as written, plus show-me unchanged in `vendor/`:
- `profile.md`: the report server binds to `127.0.0.1` and serves a folder of reports only. `python3 -m http.server` listens on every interface by default, so the LAN could read reports meant for Tailscale.
- `html-communicate`: backups stay outside the served folder; if the agent can't render the page, it says so instead of implying it looked. The old line ("do not report 'I haven't looked at it'") read as "hide a skipped check"; the new one says what to do instead. The scenario `no-browser-says-so` passed 2/3 both before and after, so this is a clarification, not a measured fix.
- `wilson-humanizer`: specifics come from the draft, the notes or a source, never invented; an unsupported quantifier is flagged, not softened. In graded work, a made-up place or an unsourced "many" is worse than plain wording.
- `vendor/show-me`: HumanLayer's skill, unmodified and manual only (upstream disables model invocation). Not installed; to use it, tell the agent to follow `~/.local/share/kook/vendor/show-me/SKILL.md`.

**Why.** `SCOPE.md` asks for an observed failure before a behaviour change, and none of these has one. The owner chose to land them anyway: they remove a privacy leak and rules that invite false statements, and each failure would be costly before it was observed. This is not a general exemption; the redesigns below still wait for evidence. The redesigns are "it would be better if".

**Rejected.**
- Rewriting `html-communicate` to loosen the no-text-wall rules, stat tiles and section order. The one real failure with this skill (#12) was a report that was too vague, not too strict. Reopen with a failure where a rule produced a worse page.
- Humanizer modes. Asking for "light edit only" or "just audit" already does it.
- A Kook `show-me` skill with hooks in `html-communicate`, the PR guide and `full-cycle`. It composes from asking for a diagram, and it repeats the shape of the rejected p3 plan (`2026-10-06-p3-adopt-selectively.md`). Reopen if threads show repeated "I don't understand" outside HTML reports.
