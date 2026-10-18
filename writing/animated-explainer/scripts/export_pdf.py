"""Export a PDF (slides, notes, a paper) to one PNG per page plus its text. Any OS.

    pip install pymupdf
    python export_pdf.py "Lecture 1.pdf" ../_source/ch01

Writes page_01.png, page_02.png, ... and pages.txt ("=== Page N ===" blocks).
"""
import sys
from pathlib import Path

import pymupdf as fitz

src = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_export")
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(src)
blocks = []
for i, page in enumerate(doc, 1):
    zoom = 1600 / page.rect.width  # 1600 px wide, like the slide exporter
    page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(out / f"page_{i:02d}.png")
    blocks.append(f"=== Page {i} ===\n{page.get_text().strip()}\n")
(out / "pages.txt").write_text("\n".join(blocks), encoding="utf-8")
print(f"Exported {len(doc)} pages to {out}")
