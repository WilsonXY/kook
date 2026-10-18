"""Template for one explainer video. Copy to chNN.py next to explainer_kit.py, rename the class, replace the content.

    EXPLAINER_DRAFT=1 python -m manim render ch01.py Chapter01 --dry_run   # layout check only, no frames
    EXPLAINER_DRAFT=1 python -m manim render ch01.py Chapter01             # 540p draft
    python -m manim render ch01.py Chapter01                                # 1080p final

Patterns to keep:
- One method per section; construct() lists them in order.
- One `with self.say(...)` block per beat. Its animations show what that sentence says, timed with v.dur.
- Concrete before abstract: show the example, then name the idea, then give the definition.
- self.tag(n) points at the source slide/page; it replaces the previous tag.
- Running-example content gets a small "(example, not from the source)" note.
"""
from explainer_kit import *  # noqa: F401,F403


class Chapter01(VoiceScene):
    def construct(self):
        self.intro()
        self.what_is_quality()
        self.recap()

    def intro(self):
        self.chapter_intro(1, "Software Quality", "What it is, and why it matters",
                           "This is chapter one, Software Quality. Before any definitions, let's start "
                           "with something you already know.")

    def what_is_quality(self):
        self.new_section("1. What is quality?", "So, first up. What is quality?")
        need = info_card("What you needed", "Large pizza, hot, in 30 minutes", BLUE, width=4.6)
        got = info_card("What you got", "Small pizza, cold, 90 minutes late", RED_, width=4.6)
        VGroup(need, got).arrange(RIGHT, buff=2.2).shift(UP * 0.3)
        with self.say("Say you order a pizza. You need a large one, it has to be hot, and it should arrive "
                      "within thirty minutes.") as v:
            self.play(FadeIn(need, shift=UP * 0.2), run_time=v.dur * 0.4)
        with self.say("What actually shows up is a small pizza, cold, an hour and a half late.") as v:
            self.play(FadeIn(got, shift=UP * 0.2), run_time=v.dur * 0.4)

        gap = edge_link(need, got, color=YELLOW_, stroke_width=6)  # border to border, never through text
        gap_l = T("the gap", size=26, color=YELLOW_).next_to(gap, UP, buff=0.2)
        with self.say("There's a big gap between what you needed and what you got.") as v:
            self.play(Create(gap), FadeIn(gap_l), run_time=v.dur * 0.5)

        rule = card("Quality = how closely what you get matches what you need", GREEN, width=11, height=0.9, size=28)
        rule.to_edge(DOWN, buff=0.8)
        with self.say("That's basically the whole idea. Quality is how closely what you get matches what you need.") as v:
            self.play(FadeIn(rule, shift=UP * 0.2), run_time=v.dur * 0.4)
        self.tag(3)
        note = T("(example, not from the source)", size=18, color=MUTED).to_corner(DL, buff=0.25)
        self.add(note)
        self.wait(0.5)

    def recap(self):
        self.new_section("Recap", "Let's recap.", color=GREEN)
        lst = numbered_list(["Quality = what you get matches what you need",
                             "A big gap means low quality"], color=GREEN, size=28, width=60)
        lst.next_to(self._heading, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        with self.say("Quality is about closing the gap between what you get and what you need.") as v:
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in lst], lag_ratio=0.5), run_time=v.dur * 0.8)
        self.wait(0.5)
