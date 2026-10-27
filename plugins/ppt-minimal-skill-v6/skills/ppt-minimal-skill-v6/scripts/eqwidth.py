"""Half-width slides: flag Body text (equations mostly) that runs past the left half into the image."""
import io, sys
import pymupdf as fitz
from pptx import Presentation
sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
prs = Presentation("Deck.pptx"); d = fitz.open("../extract/Deck_powerpoint.pdf"); PT = 72
bad = []
for i, (sl, pg) in enumerate(zip(prs.slides, d), 1):
    half = any(sh.shape_type == 13 or sh.has_table for sh in sl.shapes)
    if not half: continue
    for b in pg.get_text("blocks"):
        if b[1] > 1.2 * PT and b[0] < 6.5 * PT and b[2] > 6.75 * PT and b[3] < 6.9 * PT:
            bad.append((i, round(b[2] / PT, 2), b[4][:60].replace("\n", " ")))
print(f"🔍 half-width overrun: {len(bad)}")
for x in bad: print("   ❌", x)
# full render: Body text below the slide bottom margin (captions excluded)
low = []
for i, (sl, pg) in enumerate(zip(prs.slides, d), 1):
    half = any(sh.shape_type == 13 or sh.has_table for sh in sl.shapes)
    for b in pg.get_text("blocks"):
        cap = half and b[0] > 6.7 * PT
        if not cap and b[3] > 7.08 * PT:
            low.append((i, round(b[3] / PT, 2), b[4][:50].replace("\n", " ")))
print(f"🔍 below 7.08 in: {len(low)}")
for x in low: print("   ❌", x)

# full-width slides: anything past the right margin
wide = []
for i, (sl, pg) in enumerate(zip(prs.slides, d), 1):
    for b in pg.get_text("blocks"):
        if b[2] > 12.85 * PT and b[1] > 1.2 * PT:
            wide.append((i, round(b[2] / PT, 2), " ".join(b[4][:50].split())))
print(f"🔍 past the right margin: {len(wide)}")
for x in wide: print("   ❌", x)
