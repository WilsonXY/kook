---
skill: html-communicate
from: "decisions/2026-10-18-pele-for-page-diagrams.md"
---
## Task
html. Show me how a login request moves through our web app: browser -> API gateway -> auth service -> Postgres, and where the session token gets created. Your harness can show pages inline (`html_preview`, `html_render`), and the page should follow the harness's theme colours, which it injects as CSS variables such as `--background`, `--foreground`, `--card`, `--border` and `--accent`.

Say how you make the diagram and how it gets onto the page.

## Pass if
- The agent writes the flow as Mermaid and turns it into an SVG with the skill's Pele helper script (`mermaid-svg.mjs`), then pastes that SVG into the page.
- The agent does not load mermaid.js or Pele from a CDN, and does not leave a raw Mermaid block for the reader's app to draw.
- The agent colours the diagram by setting Pele's CSS variables (such as `--pele-fg` or `--pele-accent`) to the harness's theme variables.
