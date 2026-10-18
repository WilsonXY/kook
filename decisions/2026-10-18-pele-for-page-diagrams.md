# Pele draws diagrams in HTML pages

**Context.** In T3 thread `07aa2aae-71b7-438c-9bcb-496cfc6b1b68` the owner compared a Mermaid diagram drawn by [Pele](https://pele.run) (Obsidian's MIT renderer, pasted into an inline page as SVG) with the same kind of diagram drawn by T3's built-in mermaid.js in chat, even after recolouring it with an `init` directive. They liked Pele's look and asked for it to be the default wherever we build the page. `html-communicate` said nothing about diagrams, so agents drew SVG by hand.

**Decision.** `html-communicate` tells agents to write diagrams as Mermaid, run the skill's `mermaid-svg.mjs` (stdin to SVG, Pele 1.6.0 pinned and installed into the user cache on first run), paste the SVG inline, and colour it by setting Pele's `--pele-*` CSS variables to the page's or harness's theme variables. `scripts/test-mermaid-svg.sh` checks the helper.

**Why.** Pele runs in plain Node with no browser, its SVG is a few KB, and its colours are CSS variables, so a page stays self-contained and follows the reader's light or dark theme. Pinning the version keeps a young library's layout changes out until we choose them.

**Rejected.**
- *Pele in chat Mermaid blocks.* The reader's app draws those (T3's `ChatMarkdown` runs mermaid.js with a fixed `dark` or `default` theme); only the app can swap its renderer.
- *Load Pele from a CDN in the page.* Breaks "no external assets" and offline viewing.
- *Inline Pele's browser build.* 682 KB, over T3's 512 KB page limit.
- *Changing `show-me` or `teach`.* Both stay unmodified in `vendor/`; extend the rule to them through `profile.md` only if the owner asks.
