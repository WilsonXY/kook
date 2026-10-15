---
name: html-communicate
description: Use when the user says "html" or "report in html".
---

# html-communicate

"html" means the user wants a page they open by link and take in at a glance, not a markdown file or an attachment. Dense text tires their eyes, and pages that assume project knowledge lose them. Everything below serves that reader; the layout is your call.

## Write for a reader who knows nothing about the project
- **Lead with the point.** From the first screen alone, the reader should be able to say what the page tells them. For a recommendation, that means the whole recommendation in one plain sentence (what to do, its scope, its limits), apart from the findings, with what stays unchanged next to it.
- **Show more than you tell.** Numbers as stat tiles or small charts, steps as numbered cards, comparisons as tables, status as coloured badges, code as its shape (pseudocode, a call tree, a file tree or a diff, with real names).
- **Show it working once.** When recommending a change, walk through one concrete case with the task's real facts: before -> action -> result, as step cards when there are several steps. A one-line summary or a restated headline number is not an example.
- **Pick the smallest view that makes the point.** Keep only what the reader needs for their question, and say each thing once: a summary, tiles, a diagram and steps that repeat one another are one view too many. Skip preamble and notes on your own process. Short plain paragraphs; depth goes in collapsed `<details>`. Define each term the reader didn't use, where it first appears.
- **Shape the page to its content.** For findings or a recommendation, a good default is: answer -> what was done -> key numbers -> worked example -> findings, worst consequence first -> what is not known -> what you need from the reader. An explainer, comparison or status page wants its own shape. Drop sections with nothing to say.
- **One path when you recommend.** Leave out speculative alternatives and "possible later" ideas, and don't recommend beyond the evidence. When the reader asked for options or to explore, lay the options out side by side instead. Evidence-backed limits and caveats stay either way.
- Use corrected numbers from reviews and say on the page what was corrected, without editing the source docs. Never paste raw agent output or truncate text mid-word. Link raw .md/JSON as "full detail" at the bottom.
- No secrets, emails or token IDs on the page.

## Build
- One self-contained file (inline CSS/JS/SVG, no external assets), readable on a phone: `viewport` meta, no horizontal scroll at 390px.
- Comfortable to read: large body text, generous line height, lines around 65 characters. Dark mode is true black with neutral greys, not blue-tinted; keep red/amber/green for severity. Reuse the style of an existing family of reports.
- Restyling a page: keep its content and numbers, and save the old version outside the served folder, because anything in it can be browsed.
- Keep banners honest: update "RUNNING" notices when work finishes; link new pages from older ones.

## Deliver by link, never attachment
- Serve the folder privately and give the full link, using the route the owner's global instructions or the project document (for example a private HTTPS proxy over a local `python3 -m http.server`). One folder per port; never reuse a port.
- Before reporting: `curl` every touched page for 200 (restart the server if it died), scan the pages for secrets and emails, and check each fact you were asked to include is there; say so if one is missing.
- View the page at 390px and desktop. If you can't render it (no browser tool), say so in the report; never imply you looked.
- Report: link first, then 2-3 plain lines on what's on it, what else changed and what the user must decide. Several pages: say which to read first and why, then one line per page with its purpose and how it relates to the others (overlaps, adds detail to, or replaces which page).
