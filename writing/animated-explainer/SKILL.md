---
name: animated-explainer
description: "Use when asked to make narrated, animated videos that teach a topic step by step (lecture chapters, slides, a PDF, notes or a concept), one video per chapter, built with Manim and a free local voice."
---

# Animated explainer videos

Turn source material into narrated, animated videos that explain it bottom-up: a concrete example first, then the idea, then the definition, one small visual step per sentence. The kit in `scripts/` does the voice, subtitles, audio levels and automatic layout checks. Your job is the teaching and the checking.

## Setup (once per project)
- **Folders.** Create a project folder with `_source/`, `summaries/` and `_build/`. Copy `scripts/*` and `templates/scene_template.py` into `_build/`.
- **Install:**
  - `pip install torch --index-url https://download.pytorch.org/whl/cpu`
  - then `pip install manim kokoro soundfile pyloudnorm scipy`
  - optional: `edge-tts`; `pymupdf` for PDFs.
- **First run.** Manim's PyAV handles audio, so ffmpeg isn't needed. The first Kokoro run downloads about 330 MB.

## Workflow
1. **Extract the source.**
   - For decks: `export_slides.ps1 -Deck <deck> -OutDir _source/chNN` (Windows with PowerPoint).
   - For PDFs: `export_pdf.py <pdf> _source/chNN`.
   - Look at every slide image, not just the text. Diagrams and tables often exist only in the image.
2. **Write the summary first** (`templates/summary_template.md`). It's one file per chapter in `summaries/`:
   - every source point, tagged `[slide N]`;
   - anything you add, tagged `(explainer)`;
   - list counts kept exact;
   - a storyboard.

   This is the source of truth: the script is written from it and checked against it. It doubles as the user's revision notes.
3. **Pick one running example** for every video, such as an app, a shop or a game the audience knows. Every abstract idea gets shown on it. On screen, mark it as an example, not source content.
4. **Let the user pick the voice.** `voice_samples.py` writes the same passage in each voice. You can't hear audio, so ask, then render a short draft of one section so pace and tone are judged in context. Default: `am_puck`.
5. **Write the narration** following `references/narration.md`, then run the `wilson-humanizer` skill over it. Source definitions and quotes stay word for word.
6. **Build the first video yourself.** It's the reference for the rest.
   - Subclass `VoiceScene`, with one method per section.
   - Each beat is `with self.say(text) as v:`, holding the animations for that sentence, timed with `v.dur`.
   - Build diagrams piece by piece.
   - `self.tag(n)` points at the source slide.
   - Use the kit's helpers (`card`, `info_card`, `phone`, `person`, `numbered_list`, `edge_link`) so every video looks the same.
7. **Layout check before anyone watches.**
   - `EXPLAINER_DRAFT=1 python -m manim render chNN.py ChapterNN --dry_run` takes 1–2 minutes and renders no frames. It lists every issue with its time:
     - objects off the frame;
     - text overlapping or touching text;
     - lines through or grazing text;
     - solid shapes over text;
     - content crowding the section heading.
   - Fix them all. Mark deliberate overlaps (a tap dot on a button, a spell-check squiggle) with `allow_overlap(m)`.
   - Repeat until the list is empty.
8. **Look at every beat.**
   - Render a draft (same command without `--dry_run`), then run `python qa_review.py media/videos/chNN/540p15/ChapterNN.mp4`.
   - `qa/ChapterNN/` gets the issue frames with red boxes, plus `beats_NN.png`: the settled frame at the end of every narration line. Read all of them.
   - The checker only sees geometry. You judge:
     - tiny or cramped text;
     - something sitting too close without touching;
     - a picture that doesn't match its sentence.
   - When a beat shows a defect the checker missed, also tighten the checker, so it stays caught.
9. **Accuracy check.** Compare the `.srt` with the summary:
   - every `[slide N]` point is covered, with list counts matching;
   - nothing contradicts the source;
   - added examples are labelled.
10. **Final render.** Run `python -m manim render chNN.py ChapterNN` (1080p30). Copy the `.mp4` and `.srt` to the project root with readable names, then write a README with the videos, their lengths, the summary files and the re-render commands.
11. **Other chapters.** With the reference video done, a subagent per chapter works well if the user wants parallel work. Give each:
    - the reference script;
    - the kit;
    - its summary;
    - this workflow.

    Then run steps 7–9 on its result yourself. Run one render per folder at a time. Before redoing a stopped subagent's work, check what it already produced.

## Rules
- **Accuracy beats polish.** Never invent a definition, count or claim the source doesn't make. Ask before guessing at a garbled slide.
- **Bottom-up.** Show the example, name the idea, then give the definition. One idea per beat, nothing on screen the narration doesn't mention, and nothing left on screen past its use.
- **Same look in every video:**
  - the kit's palette and font;
  - a section heading per section;
  - the source tag;
  - a recap at the end;
  - the next chapter named.
- **No unchecked video.** Every one goes through steps 7–9.

## Report to the user
Include:
- video paths and lengths;
- where the summaries are;
- what was checked, with results: the layout issue count, the beat pages you read, narration against the summary;
- what wasn't checked;
- how to re-render;
- anything that needs their decision, such as the voice or a slide you couldn't read.

## Files
- `scripts/explainer_kit.py`: style, helpers, voice (Kokoro or edge-tts), audio mastering, subtitles and the layout check. The environment switches are listed at the top.
- `scripts/qa_review.py`: issue frames and beat pages.
- `scripts/narration.py`: dump and apply narration text, for bulk rewrites.
- `scripts/voice_samples.py`: one passage in each voice.
- `scripts/export_slides.ps1` and `scripts/export_pdf.py`: export a deck or PDF to images and text.
- `templates/`: a starter scene and the summary format.
- `references/narration.md`: script style, pronunciation, voice and audio level.
- `references/pitfalls.md`: symptoms, causes and fixes from earlier runs.
