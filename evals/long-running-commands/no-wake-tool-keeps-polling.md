---
skill: long-running-commands
from: "https://github.com/WilsonXY/kook/issues/36"
---
## Task
You started the project's test suite in the background, writing to `test.log`. It takes about 8 minutes, and there is no other work left until it finishes. Your harness has no tool that wakes you when a job or a PR's checks finish. Say exactly what you do until the suite finishes, and whether you end your turn before it does.

## Pass if
- The agent keeps checking the job (process alive, log tail) in the same turn until it finishes.
- The agent does not end its turn, or send a final message, while the suite is still running.
