# -*- coding: utf-8 -*-
"""Generate a clean scientific line-drawing for a 'Thank you' end slide.
GPR theme: antenna on the ground, downward rays to a buried target, and the
resulting hyperbolic diffraction with a few curvelet wedges at its apex.
Pure black line art on a transparent background."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

out = sys.argv[1]
LW = 1.6
K = "#111111"

fig, ax = plt.subplots(figsize=(9.0, 4.6), dpi=200)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.set_aspect("equal")

# --- ground surface line with short hatch ticks ---
gy = 4.7
ax.plot([0.6, 11.4], [gy, gy], color=K, lw=LW)
for x in np.linspace(0.8, 11.2, 34):
    ax.plot([x, x - 0.22], [gy, gy - 0.22], color=K, lw=0.7)

# --- GPR antenna box on the surface, with a survey-direction arrow ---
ax.plot([4.7, 6.1, 6.1, 4.7, 4.7], [gy, gy, gy + 0.62, gy + 0.62, gy],
        color=K, lw=LW)
ax.plot([5.05, 5.05, 5.4], [gy + 0.62, gy + 0.95, gy + 0.95], color=K, lw=LW)  # handle
ax.annotate("", xy=(7.1, gy + 0.30), xytext=(6.2, gy + 0.30),
            arrowprops=dict(arrowstyle="->", color=K, lw=LW))

# --- buried target (pipe cross-section) ---
tx, ty = 5.4, 2.55
c = plt.Circle((tx, ty), 0.36, fill=False, color=K, lw=LW)
ax.add_patch(c)
ax.plot([tx], [ty], marker="+", color=K, ms=8, mew=LW)

# --- dashed rays fanning from antenna down to the target ---
for xa in (4.9, 5.4, 5.9):
    ax.plot([xa, tx], [gy, ty + 0.36], color=K, lw=0.9, ls=(0, (4, 3)))

# --- hyperbolic diffraction signature beneath the target ---
xx = np.linspace(-3.0, 3.0, 400)
v = 0.55
yy = ty - np.sqrt((0.30) ** 2 + (v * xx) ** 2) + 0.30
ax.plot(tx + xx, yy, color=K, lw=LW)
# faint second limb pair to suggest the response band
ax.plot(tx + xx, yy - 0.28, color=K, lw=0.7, ls=(0, (2, 3)))

# --- a few curvelet wedges at the apex (oriented ticks along the arc) ---
for a in (-1.4, -0.7, 0.0, 0.7, 1.4):
    xa = tx + a
    ya = ty - np.sqrt((0.30) ** 2 + (v * a) ** 2) + 0.30
    ang = np.arctan2(-(v ** 2) * a, np.sqrt((0.30) ** 2 + (v * a) ** 2) + 1e-6)
    dx, dy = 0.34 * np.cos(ang), 0.34 * np.sin(ang)
    ax.plot([xa - dx, xa + dx], [ya - dy, ya + dy], color=K, lw=1.0)

# --- small B-scan frame to the right, echoing the hyperbola ---
bx0, bx1, by0, by1 = 8.6, 11.2, 1.1, 4.1
ax.plot([bx0, bx1, bx1, bx0, bx0], [by0, by0, by1, by1, by0], color=K, lw=1.1)
bx = np.linspace(-1.15, 1.15, 200)
by = (by1 - 0.5) - np.sqrt(0.06 + (0.85 * bx) ** 2) + 0.25
ax.plot((bx0 + bx1) / 2 + bx, by, color=K, lw=LW)

fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.05)
print("wrote", out)
