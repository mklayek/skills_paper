# -*- coding: utf-8 -*-
"""Calibrate the slide splitter against a real render.

Pass 1 builds the deck with no splitting (nosplit.flag), renders it with LibreOffice before
equations are injected, and measures where each Body text really ends. The ratio of measured
to estimated height becomes SCALE[title] in scale.json, which deck.js uses on the next build.
Built-up equations are taller than the linear text LibreOffice shows, so each stacked equation
adds its extra height to the measurement.
"""
import io, json, os, subprocess, sys
import pymupdf as fitz
from pptx import Presentation

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
TOP_IN, PT = 1.3, 72.0

open("nosplit.flag", "w").close()
try:
    for cmd in (["bash", "assemble.sh"], ["python", "latexomml.py"], ["python", "eqmeta.py"], ["node", "deck.js"], ["python", "post.py", "Deck.pptx"]):
        subprocess.run(cmd, check=True, capture_output=True)
finally:
    os.remove("nosplit.flag")
subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", "../extract", "Deck.pptx"],
               check=True, capture_output=True)
print("▶️  pass 1 rendered without splitting")

EST = json.load(open("est.json", encoding="utf-8"))
KEYS = json.load(open("keys.json", encoding="utf-8"))
EQM = json.load(open("eqmeta.json", encoding="utf-8"))
EQL = json.load(open("eqlist.json", encoding="utf-8"))
prs = Presentation("Deck.pptx")
doc = fitz.open("../extract/Deck.pdf")
scale, over = {}, []
for i, (sl, pg) in enumerate(zip(prs.slides, doc), 1):
    title = [sh for sh in sl.shapes if sh.name == "Title"][0].text_frame.text
    key = KEYS.get(str(i))
    if key is None:
        continue                                             # divider slides
    half = any(sh.shape_type == 13 or sh.has_table for sh in sl.shapes)
    xmax = 6.6 if half else 12.8
    blocks = [b for b in pg.get_text("blocks") if b[0] < PT * xmax and b[1] > PT * 1.2 ]
    if not blocks:
        continue
    meas = (max(b[3] for b in blocks) / PT - TOP_IN) * PT
    tall = sum(1 for e in EQL.get(str(i), {}).get("eqs", []) if EQM.get(e, [0, False])[1])
    meas += 18 * tall                                        # stacked fractions are taller when built up
    f = max(0.5, min(2.0, meas / EST[key]))
    scale[key] = round(f, 3)
    if meas > 398:
        over.append((i, round(meas / PT + TOP_IN, 2), title[:50]))
json.dump(scale, open("scale.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"✅ scale.json written for {len(scale)} slides; {len(over)} need splitting")
for o in over:
    print("   ", o)
