# Pitfalls seen in real runs

| Symptom | Cause | Fix |
|---|---|---|
| Overlapping text, cut-off rows and lines through labels in a "QA'd" video | Contact sheets sampled every 15–25 s at thumbnail size; short-lived defects fall between samples and overlaps are invisible small | The layout check runs after every animation; review the beat pages at full tile size |
| Two lines of text drawn on top of each other | A `VGroup` of texts was never `.arrange()`d | Arrange it; the check reports `text-overlap` |
| Label overlaps a curve it was placed under | `next_to()` used Manim's bounds, which miss how far a Bézier bulges | Place it with `curve_bounds(m)` |
| Diagram lines run through box labels | Lines drawn centre to centre | `edge_link(a, b)` |
| Two "Slide N" tags stacked in the corner | A new tag was added without removing the old one | `self.tag(n)` |
| A moving dot sits on a label at the end of its path | The path passes through the nodes | `self.bring_to_back(dot)` before moving it, or fade it out at the end |
| A row of cards runs off the frame | Widths were added up by hand | The `off-frame` check catches it; shrink the widths or `scale_to_fit_width` |
| `TypeError: 'Text' object is not callable` | A local variable shadows a kit helper (e.g. `ok = T(...)`) | Rename the local |
| `FileNotFoundError` on an `.svg` while rendering | Two renders in the same folder share Manim's text cache | Run one render per folder at a time |
| `-ql` or `-qh` is ignored | The kit fixes the resolution itself | Use `EXPLAINER_DRAFT=1` for previews |
| Subtitle timestamps like `00:00:04,1000` | Milliseconds rounded after splitting | The kit's `_srt_time` rounds first |
| Video sounds quiet next to YouTube | Peak cap without a limiter; mono clips lose 3 dB in a stereo mix | The kit's mastering; measure with pyloudnorm (see `references/narration.md`) |
| "QA" read as "queue, uh" | The acronym was spaced as "Q A" | Write acronyms joined; the kit also joins spaced capitals |
| Narration sounds robotic even with a good voice | Fragments and slogans, one synthesis call per beat | Full sentences, then the `wilson-humanizer` skill |
| Garbled characters in logs on Windows | Console encoding | `PYTHONIOENCODING=utf-8` |
| Python patched from a shell heredoc breaks (`"\n"` became a real newline) | Shell escaping | Write patch scripts to a file, then run them |
| A subagent stopped halfway (rate limit) | Usage limits | Check which outputs already exist before redoing work; re-check its video with the QA loop |
