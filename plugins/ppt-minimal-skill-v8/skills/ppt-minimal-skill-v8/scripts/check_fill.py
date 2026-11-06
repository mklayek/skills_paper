"""Report how far each slide's Body text reaches in the PowerPoint export (fill and overflow check)."""
import io, json, sys
import pymupdf as fitz
from pptx import Presentation
sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
prs = Presentation("Deck.pptx"); doc = fitz.open("../extract/Deck_powerpoint.pdf")
fill = json.load(open("fill.json", encoding="utf-8"))
for i, (sl, pg) in enumerate(zip(prs.slides, doc), 1):
    b = [sh for sh in sl.shapes if sh.name == "Body"]
    if not b or str(i) not in fill: continue
    b = b[0]; x0, y0 = b.left / 914400 * 72, b.top / 914400 * 72
    x1, y1 = x0 + b.width / 914400 * 72, y0 + b.height / 914400 * 72
    bl = [k for k in pg.get_text("blocks") if k[0] >= x0 - 2 and k[2] <= x1 + 30 and k[1] >= y0 - 2]
    low = max((k[3] for k in bl), default=y0)
    used = (low - y0) / (y1 - y0)
    f = fill[str(i)]
    flag = "OVER" if low > y1 else ("thin" if used < 0.8 else "")
    print(f"{i:3d} size {f['s']:2d} est {f['est']:3d}/{f['use']} used {used:5.0%} {flag}")
