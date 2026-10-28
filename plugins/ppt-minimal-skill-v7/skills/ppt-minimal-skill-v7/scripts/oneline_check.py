# -*- coding: utf-8 -*-
"""v7: no bullet may wrap onto a second line. Checks the real PowerPoint render.

Reads ../extract/Deck_powerpoint.pdf (pp_export.ps1). Every 22 pt body text line must start with a
bullet glyph; a 22 pt line without one is a wrapped bullet. Equations (Cambria Math) and symbol lines
(18 pt) are skipped.  python oneline_check.py
"""
import io, sys
import pymupdf as fitz

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
d = fitz.open("../extract/Deck_powerpoint.pdf"); PT = 72
BUL = ("•", "•")
wraps = []
for i, pg in enumerate(d, 1):
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            sp = [s for s in ln["spans"] if s["text"].strip()]
            if not sp or ln["bbox"][1] < 1.2 * PT: continue
            s0 = sp[0]
            if abs(s0["size"] - 22) > 1.2 or "Math" in s0["font"]: continue
            if any(k in s0["font"] for k in ("Georgia", "Verdana", "Cambria", "Trebuchet", "Tahoma")): continue   # subtitle
            if s0["text"].strip().startswith(BUL): continue
            if any(s["text"].strip().startswith(BUL) for s in ln["spans"][:2]): continue
            wraps.append((i, round(ln["bbox"][1] / PT, 2), "".join(s["text"] for s in sp)[:60]))
# the subtitle line (first body line, underlined, no bullet) is not a wrap: keep only lines that follow a bullet line
print(f"🔍 wrapped bullet lines in the PowerPoint render: {len(wraps)}")
for w in wraps[:40]: print("   ❌", w)
