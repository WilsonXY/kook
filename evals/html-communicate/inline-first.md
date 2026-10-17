---
skill: html-communicate
from: "https://github.com/WilsonXY/kook/issues/36"
---
## Task
html. Compare the three caching options we discussed (in-process LRU, Redis, CDN) in one page. Your harness gives you these tools, and you could also serve the page over a private link:

> `html_preview`: Render an HTML page in T3's headless browser and get back a PNG screenshot, contentHeight, and its console output. Use it to check and iterate on a page before html_render. Width defaults to 728, the reply column; use about 390 to check phones.
>
> `html_render`: Show a finished HTML page inline in this thread, above your final text reply; call it before writing that reply. The reader already sees the page, so the reply should not announce it or restate it. The page sits on the thread's own background, so by default leave html, body, and the outermost element with no background color. This overrides general style preferences such as a fixed black page background.

Say how you deliver the page, what you check before delivering it, and what your reply says.

## Pass if
- The agent delivers the page inline with `html_render`, not by starting a server or sending a link.
- Before rendering, the agent checks the page with `html_preview`, including at about 390px wide.
- The agent leaves the page background to the thread's theme rather than forcing a black background.
- The reply does not repeat what the page shows.
