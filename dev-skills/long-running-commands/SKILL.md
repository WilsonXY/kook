---
name: long-running-commands
description: "Use when a test, build or other command takes over a minute."
version: 1.0.0
author: WilsonXY
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [tests, builds, background-jobs, waiting, turn-discipline]
---

# Long-running commands

## The rule

**Never end your turn while you are waiting on a command you started.** Ending a turn
usually means you stop acting; nothing will wake you when the job finishes, so the work
silently stalls and an observer (a human or an orchestrating agent) cannot tell
"finished" from "stuck waiting".

## Procedure

1. **Start the job** so it cannot block or be killed with your shell: run it in the
   background (or with your harness's background-process option) and send output to a
   log file. Note the process id and the log path.
2. **Keep working or keep checking.** If other useful work exists, do it. Otherwise poll
   the job every 30-60 seconds (check the process is alive, read the tail of the log) in
   the same turn. Do not write "waiting for X" as a final message.
3. **Finish only when the result is in.** Read the exit status and the relevant part of the
   log. Passed: continue to the next step. Failed: investigate, fix, rerun.
4. **Report the outcome, not the wait.** Final messages state what ran, the result, and
   what happens next. "Waiting for the test run" is never a final message.

## Pitfalls

- **Foreground commands that exceed the harness time limit** get killed. Background them
  instead of retrying the same foreground call.
- **Do not run several heavy jobs at once** (test suites, builds) on small machines; run
  one at a time, as the project's rules say.
- **A silent log is not proof of progress or of failure.** Check the process is still
  alive before concluding either; look for a stuck prompt or a hung child process.
- **If the job is hopelessly long** (many minutes beyond what you can sensibly poll), say
  so plainly in your report and give the exact command to check on it, rather than ending
  the turn as if the work were complete.
- **Never claim success from a partial run.** If you stopped a run early, say which part
  was not run.

## Verification

- The final message contains a result (pass/fail with numbers), not a wait.
- No background process you started is still running unless you say so and why.
