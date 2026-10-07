---
name: internship-logbook-writer
description: Helps the user write and format weekly internship logbooks/reports from simple diary notes. Trigger this skill whenever the user mentions writing, generating, or compiling an internship logbook, weekly report, or weekly log from their diary, notes, or weekly activities, even if they don't explicitly name this skill.
---

# Internship Logbook Writer

This skill transforms informal weekly internship notes into a structured, professional logbook in Markdown format.

## Tone & Writing Guidelines
- **Student-Professional Voice**: Write from the perspective of a young university student. The tone should be professional and clear, but casual, direct, and natural. Avoid dry, stiff "AI speak" (e.g., instead of "Acquired hands-on proficiency in utilizing Docker containers for the purposes of local dependency management," write "Set up Docker containers so the team can easily spin up the local development environment").
- **Natural Reading Rhythm**: Vary the sentence lengths. Mix short, direct sentences with slightly longer ones. It should sound natural when read aloud.
- **No Bold Headings/Prefixes in Bullets**: **CRITICAL**: Do NOT use bold headings or label prefixes at the start of bullet points (e.g., do NOT write `* **Database Migration**: Ran postgres migrations...` or `* **Communication**: Attended planning...`). Write simple, straightforward, direct bullet points (e.g., `* Ran postgres migrations and resolved a table locking issue` or `* Attended the sprint planning meeting and updated my task statuses`).
- **Simpler Points**: Keep each point-form bullet simple and to the point.

## Workflow

1. **Extract Key Information**:
   - **Week Number**: Extract the week number (e.g., 3, 4). Fall back to `[WEEK-NUMBER]` if not found.
   - **Dates**: Identify the start and end dates. If missing, use `[DATE-NOT-FOUND]`.
   - **Activities & Objectives**: Extract what the student did and write clear, simple objectives in point-form.
   - **Content**: Synthesize technical and non-technical learnings, experiences, and tasks completed during the week. Do not split this section with bold titles or categories.

2. **Generate the Logbook**:
   - Create a file named `Internship Logbook - Week [number].md` in the workspace root.
   - Follow the structure below.

## Markdown Document Structure

The generated markdown file must follow this exact template:

```markdown
# Internship Logbook

**Week**: [Week Number]
**Start Date**: [Start Date or [DATE-NOT-FOUND]]
**End Date**: [End Date or [DATE-NOT-FOUND]]

## Type(s) & Objective(s) of the Activities
- [Simple, direct objective, e.g., "To learn how logging levels like warning and error are utilized in production code."]
- [Objective 2, e.g., "To prepare release plans and coordinate bug fixes with the QA team."]

## Content
- [Simple, casual but professional bullet point about technical tasks/learnings, e.g., "Learned when to use warn and error logging levels and where to place logs in the codebase."]
- [Simple bullet about non-technical/communication tasks, e.g., "Discussed code review feedback and made the required updates to my branch."]
- [Simple bullet about workflow, e.g., "Learned how to keep my feature branch updated by pulling from master to avoid merge conflicts."]
- [Simple bullet about system architecture/concepts, e.g., "Became more aware of how encryption and decryption are handled during transaction processing."]

[A natural, 1-2 sentence career relevance summary. E.g., "Understanding real-world deployment workflows and database practices helps bridge the gap between classroom theory and industry expectations. These practical engineering habits are exactly what I need to build a career in software development."]
```
