"""Turn a render into a visual QA report.

    python qa_review.py media/videos/ch01/540p15/Chapter01.mp4

Reads qa/<scene>/lint.json (written by the layout lint) and <video>.srt, then writes to qa/<scene>/:
  report.md        every lint issue with its time and narration line
  issues_NN.png    the frame where each issue starts, offending boxes outlined in red
  beats_NN.png     the settled frame at the end of every narration line, for a quick human pass
"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

video = Path(sys.argv[1])
out = Path(__file__).parent / "qa" / video.stem
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("*.png"):
    old.unlink()
lint = json.loads((out / "lint.json").read_text(encoding="utf-8"))
fw, fh = lint["frame"]
issues = lint["issues"]
srt = video.with_suffix(".srt").read_text(encoding="utf-8")
beats = [(m.group(1), m.group(2)) for m in re.finditer(
    r"\d+:(\d+:\d+,\d+) --> \d+:(\d+:\d+,\d+)", srt)]


def secs(s):
    m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(m) * 60 + int(sec) + int(ms) / 1000


try:
    FONT = ImageFont.truetype("segoeui.ttf", 22)
except OSError:
    FONT = ImageFont.load_default()

container = av.open(str(video))
vs = container.streams.video[0]
fps = float(vs.average_rate)


def frame_at(t):
    container.seek(int(max(0, t - 1) * 1e6), any_frame=False, backward=True)
    last = None
    for f in container.decode(vs):
        if f.time is None:
            continue
        if f.time > t + 0.5 / fps:
            break
        last = f
    return (last or f).to_image().convert("RGB")


def to_px(box, w, h):
    x0, x1, y0, y1 = box
    x0, x1 = max(x0, -fw / 2 + 0.03), min(x1, fw / 2 - 0.03)  # keep off-frame boxes visible at the edge
    y0, y1 = max(y0, -fh / 2 + 0.03), min(y1, fh / 2 - 0.03)
    return ((x0 + fw / 2) / fw * w, (fh / 2 - y1) / fh * h, (x1 + fw / 2) / fw * w, (fh / 2 - y0) / fh * h)


def pages(items, cols, rows, tile_w, name):
    per = cols * rows
    tile_h = tile_w * 9 // 16
    for p in range(0, len(items), per):
        chunk = items[p:p + per]
        sheet = Image.new("RGB", (cols * tile_w, ((len(chunk) + cols - 1) // cols) * (tile_h + 56)), "black")
        d = ImageDraw.Draw(sheet)
        for i, (img, caption) in enumerate(chunk):
            x, y = (i % cols) * tile_w, (i // cols) * (tile_h + 56)
            sheet.paste(img.resize((tile_w, tile_h)), (x, y + 56))
            d.multiline_text((x + 6, y + 2), caption, fill="yellow", font=FONT)
        sheet.save(out / f"{name}_{p // per + 1:02d}.png")


# issues: frame just after the issue appears, with the offending boxes outlined
tiles, lines = [], ["| # | time | kind | problem | narration |", "|---|---|---|---|---|"]
for n, it in enumerate(issues, 1):
    t = it["start"] - 0.5 / fps
    img = frame_at(t)
    d = ImageDraw.Draw(img)
    for b in it["boxes"]:
        d.rectangle(to_px(b, *img.size), outline=(255, 40, 40), width=max(2, img.size[0] // 400))
    tiles.append((img, f"#{n} {t:.1f}-{it['end']:.1f}s {it['kind']}\n{it['desc'][:80]}"))
    lines.append(f"| {n} | {t:.1f}-{it['end']:.1f}s | {it['kind']} | {it['desc']} | {it['narration'][:60]} |")
pages(tiles, 2, 3, 960, "issues")
(out / "report.md").write_text(f"# Layout lint: {video.name}\n\n{len(issues)} issue(s)\n\n" + "\n".join(lines) + "\n",
                               encoding="utf-8")

# beats: the settled frame at the end of each narration line
tiles = [(frame_at(secs(b) - 0.1), f"beat {i + 1}  t={secs(b):.1f}s") for i, (a, b) in enumerate(beats)]
pages(tiles, 3, 4, 640, "beats")
print(f"{len(issues)} issues, {len(beats)} beats -> {out}")
