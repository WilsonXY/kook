"""Shared style, narration and layout-check framework for animated explainer videos.

Every video script does:  from explainer_kit import *
and subclasses VoiceScene. Narration is generated with Kokoro (local, free) or edge-tts, cached in
audio/ next to this file, and synced with animations through `with self.say("..."):`.

    with self.say("Quality means matching what you needed.") as v:
        self.play(Write(title), run_time=v.dur * 0.4)
    # on exit the scene waits until the narration has finished (+ a short pause)

A .srt subtitle file is written next to the rendered video, and a layout report to qa/<Scene>/lint.json.

Environment:
  EXPLAINER_DRAFT=1    960x540 @ 15 fps preview instead of 1920x1080 @ 30
  EXPLAINER_VOICE=..   Kokoro voice (default am_puck); first letter a = American, b = British
  EXPLAINER_TTS=edge   use Microsoft Edge online voices instead of Kokoro
  EXPLAINER_NOLINT=1   skip the layout checks
  EXPLAINER_FONT=..    override the house font
"""
from __future__ import annotations

import asyncio
import hashlib
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path

import av
from manim import *  # noqa: F401,F403

# ----------------------------------------------------------------- config
if os.environ.get("EXPLAINER_DRAFT"):  # fast low-res preview renders
    config.pixel_width, config.pixel_height, config.frame_rate = 960, 540, 15
else:
    config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30

BUILD = Path(__file__).resolve().parent
AUDIO_DIR = BUILD / "audio"
AUDIO_DIR.mkdir(exist_ok=True)
# Narration engine. "kokoro" = free local neural TTS (default); "edge" = the original edge-tts voice.
ENGINE = os.environ.get("EXPLAINER_TTS", "kokoro")
KOKORO_VOICE = os.environ.get("EXPLAINER_VOICE", "am_puck")
KOKORO_SPEED = 0.95
SR = 24_000  # Kokoro's native sample rate (processing happens here)
OUT_SR = 48_000  # clips are saved at the video's audio rate, in stereo
TARGET_LUFS = -15.0  # per clip, before limiting (full videos land near YouTube's -14)
VOICE = "en-US-AndrewNeural"  # edge-tts fallback
RATE = "-4%"

_FONTS = {"win32": ("Segoe UI", "Consolas"), "darwin": ("Helvetica Neue", "Menlo")}
FONT, MONO = _FONTS.get(sys.platform, ("DejaVu Sans", "DejaVu Sans Mono"))
FONT = os.environ.get("EXPLAINER_FONT", FONT)
SOURCE_PREFIX = "Slide"  # source tag text: "<SOURCE_PREFIX> <n>", bottom-right

# ----------------------------------------------------------------- palette
# True black with neutral (untinted) greys: dark mode, no blue cast.
BG = "#000000"
PANEL = "#1C1C1C"
PANEL2 = "#3A3A3A"
INK = "#F5F5F5"      # main text
MUTED = "#A3A3A3"    # secondary text
BLUE = "#38BDF8"
GREEN = "#4ADE80"
RED_ = "#F87171"
YELLOW_ = "#FACC15"
ORANGE_ = "#FB923C"
PURPLE_ = "#C084FC"
PINK_ = "#F472B6"
TEAL_ = "#2DD4BF"
ACCENTS = [BLUE, GREEN, YELLOW_, ORANGE_, PURPLE_, PINK_, TEAL_, RED_]
config.background_color = BG


# ----------------------------------------------------------------- text helpers
def T(text: str, size: float = 36, color=INK, weight=NORMAL, font=FONT, **kw) -> Text:
    """Plain text in the house font."""
    return Text(text, font=font, font_size=size, color=color, weight=weight, **kw)


def M(markup: str, size: float = 36, color=INK, font=FONT, **kw) -> MarkupText:
    """Pango markup text, e.g. M('Quality = <span foreground="#4ADE80">match</span>')."""
    return MarkupText(markup, font=font, font_size=size, color=color, **kw)


def wrap(text: str, width: int = 40) -> str:
    """Hard-wrap a string into lines of <= width characters."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def TW(text: str, width: int = 40, size: float = 32, color=INK, **kw) -> Text:
    """Wrapped, left-aligned paragraph text."""
    return T(wrap(text, width), size=size, color=color, line_spacing=0.9, **kw)


# ----------------------------------------------------------------- shapes
def card(label, color=BLUE, width=3.6, height=1.1, size=30, fill=0.18,
         text_color=INK, corner=0.18, weight=BOLD) -> VGroup:
    """Rounded box with centred label. label may be str or a Mobject."""
    box = RoundedRectangle(corner_radius=corner, width=width, height=height,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=fill)
    txt = T(label, size=size, color=text_color, weight=weight) if isinstance(label, str) else label
    if txt.width > width - 0.3:
        txt.scale_to_fit_width(width - 0.3)
    if txt.height > height - 0.2:
        txt.scale_to_fit_height(height - 0.2)
    txt.move_to(box)
    g = VGroup(box, txt)
    g.box, g.label = box, txt
    return g


def info_card(title, body, color=BLUE, width=5.2, title_size=30, body_size=24,
              body_width=34) -> VGroup:
    """Card with a coloured title and a wrapped body paragraph."""
    t = T(title, size=title_size, color=color, weight=BOLD)
    b = TW(body, width=body_width, size=body_size, color=INK)
    content = VGroup(t, b).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    if content.width > width - 0.4:
        content.scale_to_fit_width(width - 0.4)
    box = RoundedRectangle(corner_radius=0.18, width=width, height=content.height + 0.5,
                           stroke_color=color, stroke_width=3, fill_color=PANEL, fill_opacity=0.95)
    content.move_to(box)
    g = VGroup(box, content)
    g.box, g.title, g.body = box, t, b
    return g


def pill(label, color=BLUE, size=24) -> VGroup:
    txt = T(label, size=size, color=BG, weight=BOLD)
    box = RoundedRectangle(corner_radius=(txt.height + 0.25) / 2, width=txt.width + 0.5,
                           height=txt.height + 0.25, stroke_width=0, fill_color=color, fill_opacity=1)
    txt.move_to(box)
    return VGroup(box, txt)


def person(color=BLUE, scale=1.0, label: str | None = None, label_size=22) -> VGroup:
    """Minimal person icon (head + shoulders)."""
    head = Circle(radius=0.22, fill_color=color, fill_opacity=1, stroke_width=0)
    body = Arc(radius=0.38, start_angle=0, angle=PI, fill_color=color, fill_opacity=1, stroke_width=0)
    body.next_to(head, DOWN, buff=0.06)
    g = VGroup(head, body)
    if label:
        lab = T(label, size=label_size, color=INK)
        lab.next_to(g, DOWN, buff=0.12)
        g.add(lab)
    return g.scale(scale)


def tick(color=GREEN, scale=1.0) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=10)
    m.set_points_as_corners([LEFT * 0.3 + UP * 0.02, DOWN * 0.25 + LEFT * 0.05, RIGHT * 0.35 + UP * 0.35])
    return m.scale(scale)


def cross(color=RED_, scale=1.0) -> VGroup:
    a = Line(UL * 0.25, DR * 0.25, stroke_color=color, stroke_width=10)
    b = Line(UR * 0.25, DL * 0.25, stroke_color=color, stroke_width=10)
    return VGroup(a, b).scale(scale)


def arrow(start, end, color=MUTED, buff=0.1, sw=5, tip=0.22) -> Arrow:
    return Arrow(start, end, buff=buff, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.3, tip_length=tip)


def phone(width=3.0, height=5.6, title="App") -> VGroup:
    """A simple phone mock-up. Returns VGroup with .screen (inner rect) and .header."""
    body = RoundedRectangle(corner_radius=0.35, width=width, height=height,
                            stroke_color=MUTED, stroke_width=4, fill_color="#0A0A0A", fill_opacity=1)
    screen = RoundedRectangle(corner_radius=0.2, width=width - 0.3, height=height - 0.6,
                              stroke_width=0, fill_color=INK, fill_opacity=1)
    header = Rectangle(width=width - 0.3, height=0.55, stroke_width=0, fill_color=ORANGE_, fill_opacity=1)
    header.align_to(screen, UP)
    htxt = T(title, size=24, color=BG, weight=BOLD).move_to(header)
    notch = RoundedRectangle(corner_radius=0.06, width=0.8, height=0.12, stroke_width=0,
                             fill_color=PANEL2, fill_opacity=1).next_to(screen, UP, buff=0.09)
    g = VGroup(body, screen, header, htxt, notch)
    g.body, g.screen, g.header = body, screen, header
    return g


def section_title(text, color=BLUE) -> VGroup:
    """Heading pinned to top-left with an underline bar."""
    t = T(text, size=40, color=INK, weight=BOLD)
    bar = Rectangle(width=t.width, height=0.07, stroke_width=0, fill_color=color, fill_opacity=1)
    bar.next_to(t, DOWN, buff=0.1, aligned_edge=LEFT)
    g = VGroup(t, bar).to_corner(UL, buff=0.5)
    return g


def numbered_list(items, color=BLUE, size=28, width=46, buff=0.28) -> VGroup:
    rows = VGroup()
    for i, it in enumerate(items, 1):
        num = Circle(radius=0.22, fill_color=color, fill_opacity=1, stroke_width=0)
        n = T(str(i), size=22, color=BG, weight=BOLD).move_to(num)
        txt = TW(it, width=width, size=size)
        rows.add(VGroup(VGroup(num, n), txt).arrange(RIGHT, buff=0.3, aligned_edge=UP))
    rows.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return rows


def source_tag(n) -> Text:
    """Small grey reference to the source slide or page, bottom-right."""
    return T(f"{SOURCE_PREFIX} {n}", size=18, color=MUTED).to_corner(DR, buff=0.25)


# ----------------------------------------------------------------- narration
# Scripts spell acronyms letter by letter ("S Q A P") so any engine says them right;
# subtitles show the normal form.
SUB_FIXES = [("I triple E", "IEEE")]


def subtitle_text(text: str) -> str:
    for a, b in SUB_FIXES:
        text = text.replace(a, b)
    return join_letters(text)


def join_letters(text: str) -> str:
    """ "S Q A P" -> "SQAP" (two or more single capitals; a lone "A" stays a word)."""
    return re.sub(r"\b[A-Z](?: [A-Z]\b)+", lambda m: m.group(0).replace(" ", ""), text)


# Words Kokoro gets wrong, given as phonemes in misaki's [word](/phonemes/) syntax. Add per project, e.g.
#   KOKORO_FIXES["ringgit"] = "[ringgit](/ɹˈɪŋɡɪt/)"
# Check what Kokoro will say: KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", model=False)(text)
KOKORO_FIXES: dict[str, str] = {}

_pipes: dict = {}


def _kokoro(text: str, voice: str):
    import numpy as np
    from kokoro import KPipeline

    lang = voice[0]  # 'a' = American, 'b' = British
    if lang not in _pipes:
        _pipes[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
    text = join_letters(text)  # Kokoro reads "QA" well but "Q A" as "queue, a"
    for word, fix in KOKORO_FIXES.items():
        text = re.sub(rf"\b{word}\b", fix, text)
    chunks = [a.numpy() if hasattr(a, "numpy") else a
              for _, _, a in _pipes[lang](text, voice=voice, speed=KOKORO_SPEED, split_pattern=None)]
    return np.concatenate(chunks).astype("float32")


def _limit(a, ceiling=0.89):
    """Fast peak limiter: pull down only the sharp peaks so the voice can sit louder."""
    import numpy as np
    from scipy.ndimage import minimum_filter1d, uniform_filter1d

    need = np.minimum(1.0, ceiling / np.maximum(np.abs(a), 1e-9))
    w = int(0.004 * SR)
    env = uniform_filter1d(minimum_filter1d(need, 4 * w + 1), 2 * w + 1)  # ~4 ms attack/release
    return np.clip(a * env, -ceiling, ceiling)


def _master(a):
    """Trim silence, short fades, normalise loudness, limit peaks.
    Returns 48 kHz stereo, the video's own format, so nothing is converted (or attenuated) when mixing."""
    import numpy as np
    from scipy.signal import resample_poly

    loud = np.flatnonzero(np.abs(a) > 0.01)
    if loud.size:
        a = a[max(0, loud[0] - int(0.03 * SR)): loud[-1] + int(0.08 * SR)]
    fade = min(int(0.01 * SR), len(a) // 4)
    if fade:
        ramp = np.linspace(0, 1, fade, dtype="float32")
        a[:fade] *= ramp
        a[-fade:] *= ramp[::-1]
    try:
        import pyloudnorm as pyln

        a = pyln.normalize.loudness(a, pyln.Meter(SR).integrated_loudness(a), TARGET_LUFS)
    except Exception:  # clip too short to measure: fall back to RMS
        rms = float(np.sqrt(np.mean(a**2))) or 1.0
        a = a * (10 ** (TARGET_LUFS / 20) / rms)
    a = _limit(a)
    a = np.clip(resample_poly(a, OUT_SR // SR, 1), -0.89, 0.89)
    return np.stack([a, a], axis=1).astype("float32")


def _decode_to_wav(src: Path, dest: Path):
    """Decode any audio file to mono float at SR, master it, and save as 16-bit WAV."""
    import numpy as np
    import soundfile as sf

    res = av.AudioResampler(format="flt", layout="mono", rate=SR)
    out = []
    with av.open(str(src)) as c:
        for frame in c.decode(audio=0):
            for f in res.resample(frame):
                out.append(f.to_ndarray().reshape(-1))
    for f in res.resample(None):
        out.append(f.to_ndarray().reshape(-1))
    sf.write(str(dest), _master(np.concatenate(out)), OUT_SR, subtype="PCM_16")


def _tts(text: str) -> Path:
    if ENGINE == "kokoro":
        import soundfile as sf

        key = hashlib.sha1(f"kokoro|{KOKORO_VOICE}|{KOKORO_SPEED}|{KOKORO_FIXES}|{TARGET_LUFS}|lim48|{text}".encode()).hexdigest()[:16]
        wav = AUDIO_DIR / f"{key}.wav"
        if not wav.exists() or wav.stat().st_size == 0:
            sf.write(str(wav), _master(_kokoro(text, KOKORO_VOICE)), OUT_SR, subtype="PCM_16")
        return wav
    key = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:16]
    mp3 = AUDIO_DIR / f"{key}.mp3"
    if not mp3.exists() or mp3.stat().st_size == 0:
        import edge_tts

        async def go():
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(mp3))

        for attempt in range(4):
            try:
                asyncio.run(go())
                break
            except Exception:  # network hiccup: retry
                if attempt == 3:
                    raise
    return mp3


def _duration(path: Path) -> float:
    with av.open(str(path)) as c:
        return c.duration / 1_000_000


def _srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ----------------------------------------------------------------- layout lint
# After every animation, check what is on screen for: objects outside the frame,
# text overlapping or touching text, lines/outlines through text, solid shapes over text and
# content crowding the section heading. Issues go to qa/<Scene>/lint.json; qa_review.py turns
# them into pictures.
# Mark an intentional overlap with `allow_overlap(mobject)`.
import json  # noqa: E402

import numpy as np  # noqa: E402

LINT = not os.environ.get("EXPLAINER_NOLINT")
_T = np.linspace(0, 1, 33)[:, None]
_BEZ = np.hstack([(1 - _T) ** 3, 3 * (1 - _T) ** 2 * _T, 3 * (1 - _T) * _T**2, _T**3])  # (33, 4)


def allow_overlap(*mobs):
    """Tell the layout lint that these mobjects overlap on purpose."""
    for m in mobs:
        m.lint_ok = True
    return mobs[0] if len(mobs) == 1 else mobs


def _is_text(m):
    return isinstance(m, (Text, MarkupText))


def _visible_fill(m):
    return m.get_fill_opacity() > 0.05


def _visible_stroke(m):
    return m.get_stroke_width() > 0 and m.get_stroke_opacity() > 0.05


def _bbox(m):
    pts = np.vstack([f.points for f in m.family_members_with_points()]) if _is_text(m) else m.points
    return pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()


def _samples(m):
    n = len(m.points) // 4 * 4
    if not n:
        return np.empty((0, 2))
    c = m.points[:n].reshape(-1, 4, 3)[:, :, :2]
    return np.einsum("tk,skd->std", _BEZ, c).reshape(-1, 2)


def _label(m, limit=40):
    for f in m.get_family():
        if _is_text(f):
            return "'" + re.sub(r"\s+", " ", getattr(f, "original_text", f.text)).strip()[:limit] + "'"
    return type(m).__name__


def _collect(top, order):
    """Visible text units and shape leaves of `top`, in drawing order (`order` maps id -> draw index)."""
    texts, shapes = [], []

    def walk(m):
        if getattr(m, "lint_ok", False):
            return
        if _is_text(m):
            if any(_visible_fill(g) for g in m.family_members_with_points()):
                texts.append(m)
                order[id(m)] = len(order)
            return
        if isinstance(m, VMobject) and len(m.points) and (_visible_fill(m) or _visible_stroke(m)):
            shapes.append(m)
            order[id(m)] = len(order)
        for sub in m.submobjects:
            walk(sub)

    walk(top)
    return texts, shapes


NEAR = 0.035  # text closer than this to other text counts as touching
NEAR_LINE = 0.08  # outlines are drawn thick, so text needs more room from them
HEAD_GAP = 0.2  # clearance kept around the section heading


def _lint_frame(mobjects, heading=None):
    """Return [(kind, key, desc, [bboxes])] for the current scene state."""
    hw, hh = config.frame_width / 2, config.frame_height / 2
    issues = []
    texts, shapes, owner, order = [], [], {}, {}
    for top in mobjects:
        t, sh = _collect(top, order)
        texts += t
        shapes += sh
        for m in t + sh:
            owner[id(m)] = top
    # 1. off-frame
    for m in texts + shapes:
        x0, x1, y0, y1 = _bbox(m)
        if x0 < -hw - 0.02 or x1 > hw + 0.02 or y0 < -hh - 0.02 or y1 > hh + 0.02:
            top = owner[id(m)]
            over = max(-hw - x0, x1 - hw, -hh - y0, y1 - hh)
            issues.append(("off-frame", ("off", id(top)), f"group with {_label(top)} goes {over:.1f} units past the frame edge",
                           [(x0, x1, y0, y1)]))
    # 2. text over / touching text
    boxes = [_bbox(t) for t in texts]
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = boxes[i], boxes[j]
            ix = min(a[1], b[1]) - max(a[0], b[0])
            iy = min(a[3], b[3]) - max(a[2], b[2])
            if ix > -NEAR and iy > -NEAR:
                verb = "overlaps" if ix > 0.03 and iy > 0.03 else "touches"
                issues.append(("text-overlap", ("tt", id(texts[i]), id(texts[j])),
                               f"{_label(texts[i])} {verb} {_label(texts[j])}", [a, b]))
    # 3. outlines / lines running through (or grazing) text
    stroked = [m for m in shapes if _visible_stroke(m)]
    if stroked and texts:
        samp = [_samples(m) for m in stroked]
        pts = np.vstack(samp)
        own = np.repeat(np.arange(len(stroked)), [len(x) for x in samp])
        for t, (x0, x1, y0, y1) in zip(texts, boxes):
            inside = ((pts[:, 0] > x0 - NEAR_LINE) & (pts[:, 0] < x1 + NEAR_LINE) &
                      (pts[:, 1] > y0 - NEAR_LINE) & (pts[:, 1] < y1 + NEAR_LINE))
            for k in np.unique(own[inside]):
                m = stroked[k]
                issues.append(("line-through-text", ("ls", id(t), id(owner[id(m)])),
                               f"{type(m).__name__} in {_label(owner[id(m)])} crosses or touches text {_label(t)}",
                               [(x0, x1, y0, y1), _bbox(m)]))
    # 4. content crowding the section heading
    if heading is not None and heading in mobjects:
        hp = np.vstack([f.points for f in heading.family_members_with_points()])
        hx0, hx1, hy0, hy1 = hp[:, 0].min(), hp[:, 0].max(), hp[:, 1].min(), hp[:, 1].max()
        for m in texts + shapes:
            top = owner[id(m)]
            if top is heading:
                continue
            x0, x1, y0, y1 = _bbox(m)
            if x0 < hx1 + HEAD_GAP and x1 > hx0 - HEAD_GAP and y0 < hy1 + HEAD_GAP and y1 > hy0 - HEAD_GAP:
                issues.append(("crowds-heading", ("hd", id(top)), f"{_label(top)} is too close to the section heading",
                               [(x0, x1, y0, y1), (hx0, hx1, hy0, hy1)]))
    # 5. solid shapes drawn on top of text
    solid = [m for m in shapes if m.get_fill_opacity() > 0.5]
    for t, (x0, x1, y0, y1) in zip(texts, boxes):
        area = max((x1 - x0) * (y1 - y0), 1e-6)
        for m in solid:
            if order[id(m)] < order[id(t)]:
                continue
            a = _bbox(m)
            ix = min(x1, a[1]) - max(x0, a[0])
            iy = min(y1, a[3]) - max(y0, a[2])
            if ix > 0 and iy > 0 and (ix * iy > 0.1 * area or ix * iy > 0.5 * (a[1] - a[0]) * (a[3] - a[2])):
                issues.append(("covers-text", ("cv", id(t), id(owner[id(m)])),
                               f"{type(m).__name__} in {_label(owner[id(m)])} is drawn over text {_label(t)}",
                               [(x0, x1, y0, y1), a]))
    return issues


def edge_link(a, b, color=MUTED, gap=0.08, **kw) -> Line:
    """Line between the borders of two boxes (not their centres), so it never runs through their labels."""
    ca, cb = a.get_center(), b.get_center()
    d = (cb - ca) / np.linalg.norm(cb - ca)

    def border(m, c, v):
        hw, hh = m.width / 2 + gap, m.height / 2 + gap
        t = min(hw / abs(v[0]) if abs(v[0]) > 1e-9 else np.inf, hh / abs(v[1]) if abs(v[1]) > 1e-9 else np.inf)
        return c + v * t

    return Line(border(a, ca, d), border(b, cb, -d), color=color, **kw)


def curve_bounds(m):
    """(x0, x1, y0, y1) of what is actually drawn. Manim's own bounds can miss how far curves bulge."""
    pts = np.vstack([_samples(f) for f in m.family_members_with_points()])
    return pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()


class _Voice:
    def __init__(self, dur: float):
        self.dur = dur


class VoiceScene(Scene):
    """Scene with `say()` narration blocks and automatic .srt output."""

    PAUSE = 0.35  # gap after each narration line

    def setup(self):
        self._subs: list[tuple[float, float, str]] = []
        self._issues: dict = {}
        self._say_text = ""

    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        if LINT:
            self._lint()

    def _lint(self):
        t = round(self.t_now, 3)
        for kind, key, desc, boxes in _lint_frame(self.mobjects, getattr(self, "_heading", None)):
            rec = self._issues.get(key)
            if rec is None or rec["desc"] != desc:
                self._issues[key] = {"kind": kind, "desc": desc, "start": t, "end": t,
                                     "boxes": [[float(v) for v in b] for b in boxes],
                                     "narration": self._say_text[:90]}
            else:
                rec["end"] = t

    @property
    def t_now(self) -> float:
        return self.renderer.time

    @contextmanager
    def say(self, text: str, pause: float | None = None):
        text = re.sub(r"\s+", " ", text).strip()
        mp3 = _tts(text)
        dur = _duration(mp3)
        start = self.t_now
        self._say_text = text
        self.add_sound(str(mp3))
        yield _Voice(dur)
        elapsed = self.t_now - start
        remaining = dur - elapsed + (self.PAUSE if pause is None else pause)
        if remaining > 0.02:
            self.wait(remaining)
        self._subs.append((start, start + dur, subtitle_text(text)))

    def narrate(self, text: str, *anims, frac: float = 0.6, **play_kw):
        """Shortcut: say `text` while playing `anims` over `frac` of its duration."""
        with self.say(text) as v:
            if anims:
                self.play(*anims, run_time=max(0.5, v.dur * frac), **play_kw)

    # helpers -----------------------------------------------------------
    def tag(self, n):
        """Show the source reference tag, replacing the previous one (never stack two)."""
        old = getattr(self, "_tag", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        self._tag = source_tag(n)
        self.add(self._tag)

    def clear_all(self, run_time=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    def chapter_intro(self, number: int, title: str, subtitle: str, narration: str, kicker="CHAPTER"):
        chip = pill(f"{kicker} {number}", color=BLUE, size=26)
        t = T(title, size=72, weight=BOLD)
        if t.width > 12.4:  # long titles would run off the frame
            t.scale_to_fit_width(12.4)
        s = T(subtitle, size=32, color=MUTED)
        g = VGroup(chip, t, s).arrange(DOWN, buff=0.4)
        with self.say(narration) as v:
            self.play(FadeIn(chip, shift=DOWN * 0.3), run_time=0.6)
            self.play(Write(t), run_time=min(1.6, v.dur * 0.4))
            self.play(FadeIn(s, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(g), run_time=0.6)

    def new_section(self, text: str, narration: str | None = None, color=BLUE) -> VGroup:
        """Clear the screen and pin a new section heading. Returns the heading."""
        self.clear_all()
        h = section_title(text, color=color)
        self._heading = h
        if narration:
            with self.say(narration):
                self.play(FadeIn(h, shift=RIGHT * 0.3), run_time=0.7)
        else:
            self.play(FadeIn(h, shift=RIGHT * 0.3), run_time=0.7)
        return h

    def tear_down(self):
        super().tear_down()
        if LINT:
            self.write_lint()
        try:
            out = Path(self.renderer.file_writer.movie_file_path).with_suffix(".srt")
        except Exception:  # e.g. -s (last frame only) or --dry_run renders have no movie
            return
        lines = []
        for i, (a, b, txt) in enumerate(self._subs, 1):
            lines += [str(i), f"{_srt_time(a)} --> {_srt_time(b)}", wrap(txt, 60), ""]
        out.write_text("\n".join(lines), encoding="utf-8")

    def write_lint(self):
        """Layout issues -> qa/<Scene>/lint.json (also works for --dry_run, which renders no frames)."""
        issues = sorted(self._issues.values(), key=lambda r: r["start"])
        d = BUILD / "qa" / type(self).__name__
        d.mkdir(parents=True, exist_ok=True)
        (d / "lint.json").write_text(json.dumps(
            {"frame": [config.frame_width, config.frame_height], "issues": issues}, indent=1), encoding="utf-8")
        print(f"LAYOUT LINT: {len(issues)} issue(s) -> qa/{type(self).__name__}/lint.json")
        for r in issues:
            print(f"  {r['start']:7.1f}s  {r['kind']:<18} {r['desc']}")
