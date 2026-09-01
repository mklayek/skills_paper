# -*- coding: utf-8 -*-
"""Make a mirror .deck safe for the ppt-mkl Beamer (pdflatex) build.
Usage:  python sanitize_deck.py <deck>
Fixes (python-pptx/PPTX tolerates these; only pdflatex breaks):
  * backslashes in figure paths      -> forward slashes
  * Wingdings arrow  U+F0E0          -> $\\rightarrow$   (renders as tofu otherwise)
  * Unicode minus    U+2212          -> '-'
  * approx tilde     '~'             -> $\\sim$
Greek/symbols in bullets should already be inline math ($\\chi$, $\\theta$, ...) from transcription.
"""
import sys, re
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
t = t.replace("\\", "/")                     # figure paths -> forward slashes
t = t.replace("", r" $\rightarrow$ ")  # Wingdings right arrow
t = t.replace("−", "-")                 # Unicode minus
t = t.replace("~", r"$\sim$")                # approx tilde (no ~ in figure paths)
t = re.sub(r"  +", " ", t)
open(p, "w", encoding="utf-8").write(t)
rest = sorted({hex(ord(c)) for c in t if ord(c) > 127})
print("sanitized", p, "| remaining non-ascii (0x2013/0x2014 en/em dash are safe):", rest)
