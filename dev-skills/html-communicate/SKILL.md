---
name: html-communicate
description: Use when the user says "html" or "report in html".
---

# html-communicate

When the user says "html" / "report in html" / "I want html", they want a **visual, easy-to-scan web page opened by link**, not a markdown file and not an attachment. Dense text hurts their eyes, and reports that assume project knowledge are hard to follow.

## 0. No text walls (hard rule)
Treat any wall of text as a build failure and fix it before handing over:
- **Max 2 lines (~25 words) per paragraph or callout.** Longer: split, make bullets, or fold into a collapsed `<details>` ("Read more").
- **Numbers beat sentences:** counts as big stat tiles, proportions as bars/donuts, comparisons as small charts or tables (inline SVG/CSS, no libraries), steps as numbered cards, status as coloured badges.
- **One idea per card:** bold one-line takeaway, then a visual, then optional collapsed details.
- **Caveats/warnings:** one short line with an icon, detail collapsed beneath. Never a multi-sentence callout up top.
- **Reading comfort:** body 17-18px, line-height ~1.7, max line width ~65ch, generous spacing, muted grey for secondary text, bold only on key words.
- **Executive summary = the answer banner (see Content rules) + 3-4 stat tiles.** Nothing more above the fold.
- **Self-check before delivery:** list every `<p>`/callout/`<li>` over ~30 words in the rendered text and rewrite or collapse each. Render at 390px and desktop; the first screen must be scannable without reading a paragraph.
- Restyling an existing report: change presentation only, keep content and numbers (back up first).

## 1. Content rules
- **Assume the reader knows nothing about the project.** Define every term in plain words at first use; add a small glossary.
- **Lead with the answer, not the investigation.** When the page recommends something, the first screen states the whole recommendation in one plain sentence (what to do, its scope, its limits), apart from the findings. Next to it, say what stays unchanged.
- **Show it working once.** When recommending a change, show one concrete before -> action -> result example using the task's real facts, as step cards when there are several steps. A one-line summary is not an example.
- **One recommended path.** Leave out speculative alternatives and "possible later" ideas unless the owner asked for options. Evidence-backed limits and caveats stay.
- **Order:** answer banner -> what was done (3 lines) -> key numbers as charts with a one-line takeaway each -> the worked example -> findings as cards -> what is NOT known -> "What I need from you".
- Plain-language titles plus one-liners. Never paste raw tool/agent prose, never truncate text mid-word. Heavy detail goes in `<details>`.
- Consequences first, worst first, with real-world likelihood. No recommendation beyond the evidence unless asked.
- Use corrected numbers from reviews; put corrections in a "Corrections" box in the page, not by editing source docs.
- Link raw .md/JSON as "full detail" at the bottom only.
- No secrets, emails or token IDs in the page.

## 2. Technical rules
- **One self-contained file** (inline CSS/JS/SVG, no external assets). Phone-friendly: `viewport` meta, no horizontal overflow at 390px.
- When updating an existing family of reports, reuse its style.
- **Dark mode: true black `#000000` with neutral greys, not blue-tinted.** Keep severity colours (red/amber/green). Save the previous version as `<name>.<variant>-backup.html` before restyling.
- Keep banners honest: update "RUNNING" notices when work finishes; link new pages from older reports.

## 3. Delivery (link, never attachment)
- Serve the folder privately and give the full link. Use the private route the owner's global instructions or the project documents (for example a private HTTPS proxy over a local `python3 -m http.server`).
- One folder per port. Never reuse a port.
- `curl` the link for 200 before reporting; restart the server if it died.
- Several reports: say which to read first and why, then one line per page with its purpose and how it relates to the others (overlaps, adds detail to, or replaces which page).

## 4. Audit before handing over
- Every touched page returns 200.
- Structure check: heading list, `<details>` and chart counts, email/secret scan.
- Grep the page for each specific fact you were asked to include; if one is missing, say so.
- Render at 390px and desktop yourself; do not report "I haven't looked at it".
- **Comprehension check:** from the first screen alone, state the page's answer in one sentence (for a recommendation, with its scope and what stays unchanged). If you can't, rewrite the top of the page.
- Report: link first, 2-3 lines on what is on it, what else changed, what the user must decide. Plain language.

## Pitfalls
- Attaching the file or sending .md when asked for html.
- Jargon-heavy cards copied from agent output.
- Blue-tinted dark theme.
- Stale banner saying a finished stage is still running.
- Port reuse or a dead file server -> 404 / connection refused.
