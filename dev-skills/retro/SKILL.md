---
name: retro
description: "Look back at a session, find what went wrong, and file each lasting lesson for triage. Use when the owner says retro or asks why a session went badly."
disable-model-invocation: true
---

# Retro

Turn a session's corrections and stumbles into filed, evidence-backed lessons. You report what happened; you don't fix skills here unless the owner asks.

## Steps
1. **Pick the session.** The current one, unless the owner names another (often by pasting its id). For a past session, read its transcript with the method in the owner's global instructions. Work from the transcript, not memory.
2. **Collect signals**, each with a quote or a pointer:
   - the owner corrected, pushed back, or repeated a request
   - the owner was confused ("?", "what does this mean", "same or not?")
   - work was redone, thrown away, or cut down by a reviewer
   - a review finding that a check or a skill should have prevented
   - a stall: waiting, asking permission it already had, a skipped step
   - a fact the agent had to rediscover
3. **Keep only lessons that will recur.** A one-off goes in the report as dropped, with the reason.
4. **Name the narrowest home** for each lesson:

   | Lesson | Home |
   |---|---|
   | A mechanical rule (format, banned name, missing link) | an automated check |
   | A fact about one project | that project's `AGENTS.md` or scripts |
   | A fact about the owner's tools or machine | the owner's global instructions |
   | A judgement that will recur in any repo | an edit to one skill, plus a scenario that would have caught it |
   | A decision to do, or not do, something | a decision record |

5. **File each lesson** where the owner's global instructions name the skill inbox. Search it first; if the lesson is already there, add your evidence to it instead. One item per lesson:
   - **Title:** the failure in one line.
   - **What happened:** a short paraphrase. At most 3 quotes of 20 words each.
   - **Evidence:** session id, timestamps, PR or file links.
   - **Proposed home and change**, and how a test or scenario would show it's fixed.
   - The inbox may be public. Never include secrets, tokens, emails, private code, or details the owner hasn't made public.
6. **Report:** links to what you filed, what you dropped and why.

No inbox configured: put the items in your reply instead.
