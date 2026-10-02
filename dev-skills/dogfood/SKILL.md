---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports."
version: 1.0.0
author: Teknium (teknium1)
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [qa, testing, browser, web, dogfood]
---

# Dogfood: Systematic Web Application QA Testing

## Overview

This skill guides you through systematic exploratory QA testing of web applications using a real browser you can drive. You will navigate the application, interact with elements, capture evidence of issues, and produce a structured bug report.

## Prerequisites

- A way to drive and observe a real browser: navigate, read page structure (DOM or accessibility tree), click, type, press keys, scroll, read the JS console, and take screenshots. Any of these work: Playwright/Puppeteer scripts, Chrome DevTools Protocol, a browser MCP server, or your harness's built-in browser tool.
- **No browser access at all?** Say so up front and stop. Do not fake a QA pass from reading code; report "not verified visually" instead. Static checks (HTTP status, fetched HTML, contrast calculations) can be listed as partial evidence only.
- A target URL and testing scope from the user

## Inputs

The user provides:
1. **Target URL** — the entry point for testing
2. **Scope** — what areas/features to focus on (or "full site" for comprehensive testing)
3. **Output directory** (optional) — where to save screenshots and the report (default: `./dogfood-output`)

## Workflow

Follow this 5-phase systematic workflow:

### Phase 1: Plan

1. Create the output directory structure:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   └── report.md          # Final report (generated in Phase 5)
   ```
2. Identify the testing scope based on user input.
3. Build a rough sitemap by planning which pages and features to test:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, etc.)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page:
   Open the page in the browser.

2. **Take a snapshot** to understand the DOM structure:
   Read the page structure (DOM / accessibility tree).

3. **Check the console** for JavaScript errors:
   Read the JS console (clear it first).
   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Take a screenshot** and inspect it for layout problems, broken elements, and accessibility concerns (contrast, focus visibility, tap-target size). If your tooling can label interactive elements on the screenshot, use that to pick click targets.

5. **Test interactive elements** systematically:
   - Click buttons and links
   - Fill forms
   - Test keyboard navigation (Tab, Enter, Escape)
   - Scroll through long content
   - Test form validation with invalid inputs
   - Test empty submissions

6. **After each interaction**, check for:
   - Console errors
   - Visual changes (take another screenshot and compare)
   - Expected vs actual behavior

### Phase 3: Collect Evidence

For every issue found:

1. **Take a screenshot** showing the issue:
   Save the screenshot file path; you will reference it in the report.

2. **Record the details**:
   - URL where the issue occurs
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Console errors (if any)
   - Screenshot path

3. **Classify the issue** using the issue taxonomy (see `references/issue-taxonomy.md`):
   - Severity: Critical / High / Medium / Low
   - Category: Functional / Visual / Accessibility / Console / UX / Content

### Phase 4: Categorize

1. Review all collected issues.
2. De-duplicate — merge issues that are the same bug manifesting in different places.
3. Assign final severity and category to each issue.
4. Sort by severity (Critical first, then High, Medium, Low).
5. Count issues by severity and category for the executive summary.

### Phase 5: Report

Generate the final report using the template at `templates/dogfood-report-template.md`.

The report must include:
1. **Executive summary** with total issue count, breakdown by severity, and testing scope
2. **Per-issue sections** with:
   - Issue number and title
   - Severity and category badges
   - URL where observed
   - Description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshot references (use `MEDIA:<screenshot_path>` for inline images)
   - Console errors if relevant
3. **Summary table** of all issues
4. **Testing notes** — what was tested, what was not, any blockers

Save the report to `{output_dir}/report.md`.

## Tips

- **Always check the JS console after navigating and after significant interactions.** Silent JS errors are among the most valuable findings.
- **Test with both valid and invalid inputs** — form validation bugs are common.
- **Scroll through long pages** — content below the fold may have rendering issues.
- **Test navigation flows** — click through multi-step processes end-to-end.
- **Check responsive behavior** by noting any layout issues visible in screenshots.
- **Don't forget edge cases**: empty states, very long text, special characters, rapid clicking.
- When reporting screenshots to the user, include `MEDIA:<screenshot_path>` so they can see the evidence inline.
