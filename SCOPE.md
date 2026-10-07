# Scope

Kook is the owner's own set of agent skills. Every skill is maintenance surface, so a change has to earn its place.

## The bar

A change to a skill's behaviour, or a new skill, needs both:

1. **An observed failure.** Something went wrong in a real session: what was asked, what the agent did, what should have happened. Link the thread, PR or issue. "It would be better if…" is not enough.
2. **It fits Kook.** It doesn't repeat a decision in `decisions/`, and it lands in its narrowest home:

| Lesson | Home |
|---|---|
| A mechanical rule (format, a banned name, a missing link) | a check in `scripts/doctor.py`, not prose |
| A fact about one project (port, test login, run command) | that project's `AGENTS.md` or scripts |
| A fact about the owner's tools or this machine | `profile.md` |
| A judgement that will recur in any repo | an edit to one skill in `dev-skills/`, with a scenario in `evals/` that fails before and passes after |
| A decision to do, or not do, something in Kook | a file in `decisions/` |
| A one-off | nowhere |

New skills: first check whether the behaviour composes from existing ones. If it does, it doesn't get a skill.

Exempt from the bar: typo, link and formatting fixes; moves that keep behaviour; checks and tests.

## Inbox

Observed failures wait as GitHub issues labelled `inbox`. The `retro` skill files them, and so can any agent or the owner. Triage regularly: each becomes a PR, a `decisions/` file, or is closed with the reason.

## Buckets

| Folder | Status | Installed for agents |
|---|---|---|
| `dev-skills/` | active, portable, held to `dev-skills/README.md` rules | yes |
| `writing/` | active, the owner's writing and report skills | no |
| `vendor/` | third-party skills kept unmodified; see `SOURCES.md` | no |

Add a bucket (for example `in-progress/` or `frozen/`) only when a skill needs that status.

## Every PR

- Add one line to `CHANGELOG.md`.
- A decision or a rejected idea gets a file in `decisions/`.
- Something taken from another skillset gets a row in `SOURCES.md`.
