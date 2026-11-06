"""Contact sheets of the PowerPoint-exported PDF: sheets.py first last [cols] [dpi]."""
import sys, os, glob
import pymupdf as fitz
from PIL import Image
a, b = int(sys.argv[1]), int(sys.argv[2]); cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 45
d = fitz.open("../extract/Deck_powerpoint.pdf"); b = min(b, len(d))
ims = []
for i in range(a - 1, b):
    pix = d[i].get_pixmap(dpi=dpi); ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
W, H = ims[0].size
sh = Image.new("RGB", (W * cols, H * ((len(ims) + cols - 1) // cols)), "gray")
for k, im in enumerate(ims): sh.paste(im, ((k % cols) * W, (k // cols) * H))
fn = f"../extract/sheets/v2_{a:03d}_{b:03d}.png"; sh.save(fn); print(fn, len(d), "pages")
