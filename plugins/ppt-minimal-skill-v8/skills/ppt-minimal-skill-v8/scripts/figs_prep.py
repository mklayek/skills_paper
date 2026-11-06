# -*- coding: utf-8 -*-
"""Section-divider patterns (sec0..sec6) and the chapter figures, with sizes.json for the deck.

Figures come from CFG["source_figs"] (the proofread source crops, optional). Each is copied
as is and its pixel size recorded in sizes.json as [w, h, ext].
"""
import glob, io, json, os, shutil, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
from PIL import Image

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(os.path.dirname(HERE), "..", "..", "figs")   # <output>/figs
os.makedirs(FIGS, exist_ok=True)
CFG = json.load(open(os.path.join(HERE, "deck_config.json"), encoding="utf-8"))
SRC = os.path.normpath(os.path.join(HERE, CFG.get("source_figs", "../figs_src")))

cols = ['#B91C1C', '#1D4ED8', '#15803D', '#6D28D9', '#0E7490', '#C2410C', '#0B2A55']
tint = lambda c, a: tuple(1 - (1 - np.array(matplotlib.colors.to_rgb(c))) * a)
W, H = 13.333, 7.5


def base():
    f = plt.figure(figsize=(W, H)); ax = f.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off'); ax.set_aspect('equal'); return f, ax


def p_hex(ax, c):
    r = 0.45
    for i, x in enumerate(np.arange(0, W + 1, r * 1.5)):
        for y in np.arange(0, H + 1, r * np.sqrt(3)):
            yy = y + (r * np.sqrt(3) / 2 if i % 2 else 0)
            ax.add_patch(RegularPolygon((x, yy), 6, radius=r * 0.95, orientation=np.pi / 6,
                                        fc=tint(c, 0.10 if (i + int(yy * 3)) % 4 else 0.22), ec=tint(c, 0.35), lw=0.8))


def p_diag(ax, c):
    for k in np.arange(-H, W + H, 0.28): ax.plot([k, k + H], [0, H], color=tint(c, 0.22), lw=6)
    for k in np.arange(-H, W + H, 1.4): ax.plot([k, k + H], [0, H], color=tint(c, 0.45), lw=2)


def p_dots(ax, c):
    for x in np.arange(0.2, W, 0.35):
        for y in np.arange(0.2, H, 0.35):
            d = np.hypot(x - W, y) / 15
            ax.add_patch(Circle((x, y), 0.03 + 0.09 * (1 - d) ** 2, fc=tint(c, 0.45), ec='none'))


def p_waves(ax, c):
    x = np.linspace(0, W, 600)
    for i, y0 in enumerate(np.arange(-0.5, H + 0.5, 0.32)):
        ax.plot(x, y0 + 0.18 * np.sin(2 * np.pi * x / 2.4 + i * 0.5), color=tint(c, 0.25 if i % 3 else 0.5), lw=2.2)


def p_tri(ax, c):
    s = 0.8
    for i, y in enumerate(np.arange(0, H + s, s * 0.866)):
        for j, x in enumerate(np.arange(-s, W + s, s / 2)):
            up = (i + j) % 2 == 0; a = 0.08 + 0.22 * ((i * 3 + j * 7) % 5 == 0)
            pts = [(x, y), (x + s / 2, y + s * 0.866), (x + s, y)] if up else \
                  [(x, y + s * 0.866), (x + s / 2, y), (x + s, y + s * 0.866)]
            ax.add_patch(plt.Polygon(pts, fc=tint(c, a), ec=tint(c, 0.3), lw=0.6))


def p_circles(ax, c):
    for r in np.arange(0.4, 16, 0.45):
        ax.add_patch(Circle((W, 0), r, fc='none', ec=tint(c, 0.3 if int(r / 0.45) % 3 else 0.55), lw=2))
    for r in np.arange(0.4, 6, 0.45):
        ax.add_patch(Circle((0, H), r, fc='none', ec=tint(c, 0.25), lw=1.5))


def p_grid(ax, c):
    for x in np.arange(0, W, 0.5): ax.plot([x, x], [0, H], color=tint(c, 0.2), lw=1)
    for y in np.arange(0, H, 0.5): ax.plot([0, W], [y, y], color=tint(c, 0.2), lw=1)
    rng = np.random.default_rng(3)
    for _ in range(40):
        ax.add_patch(plt.Rectangle((rng.integers(0, 26) * 0.5, rng.integers(0, 15) * 0.5), 0.5, 0.5, fc=tint(c, 0.3), ec='none'))


for i, (p, c) in enumerate(zip([p_hex, p_diag, p_dots, p_waves, p_tri, p_circles, p_grid], cols)):
    f, ax = base(); p(ax, c)
    ax.add_patch(plt.Rectangle((0.6, 1.55), 8.4, 4.4, fc='white', ec=c, lw=3, zorder=10))
    f.savefig(os.path.join(FIGS, f'sec{i}.png'), dpi=120, facecolor='white'); plt.close(f)
print("✅ 7 divider patterns")

sizes = {}
for f in sorted(glob.glob(os.path.join(glob.escape(SRC), "fig_*"))):
    name, ext = os.path.splitext(os.path.basename(f))
    shutil.copy(f, os.path.join(FIGS, os.path.basename(f)))
    w, h = Image.open(f).size
    sizes[name] = [w, h, ext[1:]]
json.dump(sizes, open(os.path.join(HERE, "sizes.json"), "w"), indent=0)
print(f"✅ {len(sizes)} chapter figures copied, sizes.json written")
