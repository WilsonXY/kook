# Animated explainer skill

**Context.** The owner asked for narrated, animated videos explaining university lecture chapters, one video per chapter, in T3 thread `e9325cfd-12ae-40c9-903e-fde3b75a1dd9`. They then asked to turn that thread's process into a reusable skill. Several failures came up along the way:
- Visual QA used contact sheets: one thumbnail every 15–25 s. Videos marked as checked still had text overlaps, a row cut off at the frame edge, lines through labels and stacked slide tags. The owner found three of them by watching.
- The narration sounded robotic. Part of it was the free online voice. The rest was the script: dramatic fragments, slogans and "not X but Y" lines, which a voice synthesised one line at a time reads choppily.
- "Q A" was read as "queue, uh", and finished videos measured about -20 LUFS, around 6 dB below YouTube's -14.

**Decision.** A new `writing/animated-explainer` skill. It holds the workflow and a tested kit:
- **Workflow:** summary as the source of truth, one running example, the voice picked by ear, a humanised script, a reference video before subagents, then a layout check, a beat review and an accuracy check before the final render.
- **Kit:** Manim style and helpers, Kokoro text-to-speech with mastering and subtitles, a layout checker that runs after every animation (and with `--dry_run`, without rendering), a beat-by-beat review sheet, narration bulk edit, voice samples, and deck and PDF exporters.

**Why.**
- **Measured on the thread's chapter 1.** The layout checker found 18 real defects in a video that had passed thumbnail QA, including all three the owner reported. Each fix was confirmed in a re-render with 0 issues left.
- **Tightened from misses.** Reading the beat pages found 4 near-misses that the first checker missed. Its rules were tightened until it caught them.
- **Audio.** The audio changes moved chapter 1 from about -20 to -12.6 LUFS.
- **Doesn't compose from existing skills.** `wilson-humanizer` covers the script's wording only. Nothing in Kook covers video, voice or visual layout. `wilson-humanizer` is used for the narration rather than copied.
- **A writing skill, not a dev skill.** It produces teaching material for the owner. The kit is copied into each video project, so a project keeps working if the skill changes.

**Rejected.**
- **Paid voices (ElevenLabs, OpenAI).** The owner wants a free option. The voice sits behind one function, so it can be swapped.
- **Thumbnail contact sheets as the QA step.** They missed every defect above.
- **Keeping the kit only in the owner's course folder.** It would not be reusable for other topics.
- **Evals.** `evals/` covers `dev-skills/` only (the doctor enforces this). The kit's checks were tested on real renders instead.
