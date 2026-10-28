# -*- coding: utf-8 -*-
"""v7 one-line bullets: per-character advance widths of the body fonts -> fontwidths.json.

head.js measures every chain bullet with these widths and moves the text that would wrap onto the
next bullet, so no bullet ever runs onto a second line. Widths are in em (fraction of the font size),
for regular / bold / italic / bold-italic of Times New Roman, Comic Sans MS and Bookman Old Style.
Characters of the section files that a font lacks fall back to the font's average width.
    python fontwidths.py          (run once in build/, before assemble.sh)
"""
import glob, io, json, os, sys
from PIL import ImageFont

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
FONTDIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
FILES = {"Times New Roman": ("times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"),
         "Comic Sans MS": ("comic.ttf", "comicbd.ttf", "comici.ttf", "comicz.ttf"),
         "Bookman Old Style": ("BOOKOS.TTF", "BOOKOSB.TTF", "BOOKOSI.TTF", "BOOKOSBI.TTF")}
chars = set(chr(c) for c in range(32, 127))
for f in glob.glob("../sections/c*.js") + glob.glob("../../../sections/c*.js"):
    chars |= set(io.open(f, encoding="utf-8").read())
chars = sorted(c for c in chars if c.isprintable())
out = {}
for face, files in FILES.items():
    for style, fn in zip(("r", "b", "i", "bi"), files):
        path = os.path.join(FONTDIR, fn)
        if not os.path.exists(path):
            print(f"⚠️  {fn} missing, {face} {style} uses Times New Roman widths"); continue
        ft = ImageFont.truetype(path, 1000)
        out[f"{face}|{style}"] = {c: round(ft.getlength(c) / 1000, 4) for c in chars}
json.dump(out, io.open("fontwidths.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"✅ fontwidths.json: {len(out)} font styles x {len(chars)} characters")
