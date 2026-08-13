#!/usr/bin/env python3
r"""Finalize a pandoc-built web-style seismo-report HTML so MathJax renders
reliably OFFLINE with equation numbers.

Why this exists (hard-won gotchas — do not "simplify" these away):
  * pandoc --mathjax --embed-resources inlines the MathJax bundle as a RAW
    <script>...</script> with NO src. MathJax's startup then cannot locate
    itself and never typesets (equations show as raw \(...\) text).
  * A base64 data: URI in <script src="data:..."> FAILS for the ~2 MB bundle:
    the browser rejects it as net::ERR_INVALID_URL (data URL too long).
  * The reliable offline pattern is: a MathJax CONFIG <script> immediately
    followed by the bundle as a plain inline <script>...</script>, using the
    SVG output bundle (tex-mml-svg.js) which needs NO external font files.
    (The CHTML bundle needs web fonts fetched from a CDN -> not offline.)
  * MathJax AUTOLOADS some TeX extensions (e.g. \boldsymbol) from a relative
    URL that 404s offline, and ONE such failure ABORTS the whole typeset pass
    (every equation then shows raw). Avoid autoload-only macros in the source:
    replace \boldsymbol{\sigma} with \sigma, avoid \color/\cancel/\bm, etc.
  * Equation numbers: write display equations as $$ ... \tag{N}$$ (NOT
    \qquad (N)); with tags:'ams' MathJax right-aligns the number to the margin.

Usage:
    python finalize_web_html.py REPORT.html  [path/to/mathjax_tex_mml_svg.js]
If the bundle path is omitted, uses scripts/mathjax_tex_mml_svg.js next to this
file (downloading it once if missing).
"""
from __future__ import annotations
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_BUNDLE = HERE / "mathjax_tex_mml_svg.js"
CDN = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-svg.js"

CONFIG = ("<script>window.MathJax={"
          "tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],"
          "tags:'ams',processEscapes:true},"
          "options:{ignoreHtmlClass:'no-mathjax'},"
          "svg:{fontCache:'global'},startup:{typeset:true}"
          "};</script>")

INLINE_BUNDLE_RE = re.compile(
    r'<script[^>]*>\(function\(\)\{"use strict";var __webpack_modules__.*?</script>', re.S)


def ensure_bundle(path: Path) -> Path:
    if not path.exists():
        print(f"[finalize] downloading MathJax SVG bundle -> {path}")
        urllib.request.urlretrieve(CDN, path)
    return path


def finalize(html_path: Path, bundle_path: Path) -> None:
    html = html_path.read_text(encoding="utf-8")
    html, n = INLINE_BUNDLE_RE.subn("", html)
    if n != 1:
        print(f"[finalize][warn] removed {n} inline MathJax bundles (expected 1)")
    bundle = bundle_path.read_text(encoding="utf-8").replace("</script>", "<\\/script>")
    inject = CONFIG + "\n<script>" + bundle + "</script>\n"
    html = html.replace("</body>", inject + "</body>", 1)
    html_path.write_text(html, encoding="utf-8")
    mb = html_path.stat().st_size / 1e6
    print(f"[finalize] injected config + inline SVG MathJax into {html_path.name} ({mb:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: finalize_web_html.py REPORT.html [mathjax_tex_mml_svg.js]")
    html = Path(sys.argv[1])
    bundle = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_BUNDLE
    finalize(html, ensure_bundle(bundle))
