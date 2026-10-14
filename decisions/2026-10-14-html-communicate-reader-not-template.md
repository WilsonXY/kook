# html-communicate describes the reader, not a template

**Context.** The owner found Kook's communication skills too strict, leaving the agent no room to fit a page to its content (thread 0745d8d8). A survey of popular skillsets in that thread (Anthropic's skills and authoring guide, superpowers, mattpocock, addyosmani, Vercel, compound-engineering, humanlayer, pstack) found `html-communicate` the outlier: a 25-word "hard rule" per paragraph, an audit of every paragraph over 30 words, a fixed seven-section order, "summary = banner + 3-4 stat tiles", exact font sizes. The others keep exact rules for fragile steps and give goals and defaults for open-ended output. Compound-engineering says "Numeric word or bullet caps are not a length control"; Anthropic's skill-creator calls all-caps rules and "super rigid structures" a yellow flag.

`2026-10-09-borrow-reviews-small-fixes.md` rejected this rewrite until a rule produced a worse page. The new scenario `explainer-fits-its-content` shows one: asked for an onboarding explainer for a new teammate, the old skill put its fixed last section, "What I need from you", on the teammate's page in 6 of 7 runs, and filled the required stat-tile row with counts like "1 click".

**Decision.** `html-communicate` states who the reader is and what the page must do for them (the point on the first screen, visuals over text, terms defined, one path when recommending), gives the findings layout as a default to adapt, and drops numeric caps, the fixed order and exact sizes. Delivery and honesty rules stay exact: private link, 200 check, secret scan, say when the page wasn't rendered. Options are laid out side by side when the reader asked to explore.

**Evidence.** Claude Opus 5.5 as agent and judge (Codex was usage-limited), 3 runs each, old skill then new: `explainer-fits-its-content` 0/3 -> 3/3; `lead-with-recommendation` 3/3 -> 6/6; `no-browser-says-so` 3/3 -> 3/3; `several-pages-reading-order` 3/3 -> 3/3. The first rewrite folded "show it working once" into another bullet and slipped to 2/3 twice on `lead-with-recommendation`; as its own rule it passed 6/6. A line tying each visual to a fact from the task did not change the explainer's rate, so it was left out.

**Rule of thumb for future edits.** Exact rules for fragile or safety steps; for the shape of output, describe the reader and the goal and give a default. Loosening a rule is fine when its scenarios still pass.

**Rejected.** Loosening `wilson-humanizer` in the same change: the owner will test it first.
