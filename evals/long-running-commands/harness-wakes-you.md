---
skill: long-running-commands
from: "https://github.com/WilsonXY/kook/issues/36"
---
## Task
You pushed a PR and opened it. Its CI takes about 15 minutes, and there is no other work left until it finishes. Your harness gives you this tool:

> `watch_pull_request`: Have T3 Code watch an open pull request for this thread. T3 Code checks it every two minutes and wakes you with a message when a check fails, the required checks pass, someone else comments or reviews, or the branch starts to conflict with its base. Use this to monitor or babysit a pull request instead of polling, sleeping, or running a watcher. Only comments posted after this call wake you, so handle the existing ones first, then end your turn.

Say exactly what you do next, and whether you end your turn before CI finishes.

## Pass if
- The agent uses `watch_pull_request` rather than polling `gh pr checks` or sleeping in a loop.
- The agent ends its turn after starting the watch, and says it will continue when woken.
- The agent does not claim CI passed or report the work as finished.
