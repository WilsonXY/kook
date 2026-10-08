---
skill: html-communicate
from: "#12"
---
## Task
html. I asked you to research whether our team should adopt "Turbo Cache" for CI. Your findings: it cuts CI time from 14 to 6 minutes on our test suite; it needs a paid plan ($20/month); our current test-first rule and required code review are unaffected; two other teams use it without problems; one open bug affects Windows runners, which we don't use. Your recommendation: adopt only its remote cache step, keep everything else in our CI as is, and trial it for two weeks on one repo.

Describe the report page you would build: write out the full text of the first screen exactly as it would appear, then list the remaining sections with one line each.

## Pass if
- The first screen states the recommendation itself (adopt only the remote cache step, two-week trial on one repo) in one plain sentence, separate from the findings.
- The first screen says what stays unchanged (the rest of CI, the test-first rule, required review).
- The report includes one concrete example of how the change would work in practice, end to end.
- No speculative alternatives or "possible later" exception boxes are mixed into the recommended path.
