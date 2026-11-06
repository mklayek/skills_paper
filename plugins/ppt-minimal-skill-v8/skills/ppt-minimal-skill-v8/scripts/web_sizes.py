# -*- coding: utf-8 -*-
"""Add the downloaded web images (<output>/figs/web/*) and extra local figures to sizes.json.

Keys are the path below <output>/figs without extension, e.g. 'web/web_C_turam_1', so a section
file uses S(title, '', items, 'web/web_C_turam_1', caption). Run after figs_prep.py.
"""
import glob, io, json, os, sys
from PIL import Image

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "figs"))
sizes = json.load(open(os.path.join(HERE, "sizes.json"), encoding="utf-8"))
n = 0
for f in sorted(glob.glob(os.path.join(glob.escape(FIGS), "web", "*")) + glob.glob(os.path.join(glob.escape(FIGS), "0*_fig_*.png"))):
    if os.path.splitext(f)[1].lower() not in (".png", ".jpg", ".jpeg"):
        continue
    rel = os.path.relpath(f, FIGS).replace("\\", "/")
    key, ext = os.path.splitext(rel)
    w, h = Image.open(f).size
    sizes[key] = [w, h, ext[1:]]
    n += 1
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w", encoding="utf-8"), indent=0)
print(f"✅ {n} web and extra figures added to sizes.json")
