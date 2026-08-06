# scripts/build_report.py
"""Build seismo-report outputs from a Markdown master.
Order: HTML (always) -> [approval] -> DOCX/PDF/PPTX (explicit flags)."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
CSS = SCRIPTS / "seismo.css"
PREAMBLE = SCRIPTS / "preamble_seismo.tex"
REF_DOCX = SCRIPTS / "reference_seismo.docx"
# Web-style (docked TOC + scrollspy + offline MathJax) assets.
WEB_CSS = SCRIPTS / "report_web.css"
WEB_TOOLBAR = SCRIPTS / "report_web_toolbar.html"
WEB_LIGHTBOX = SCRIPTS / "report_web_lightbox.html"
MJX_BUNDLE = SCRIPTS / "mathjax_tex_mml_svg.js"

def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def _ensure_reference() -> Path:
    if not REF_DOCX.exists():
        from make_reference_docx import build_reference  # type: ignore
        build_reference(REF_DOCX)
    return REF_DOCX

def to_html(md: Path, out: Path) -> Path:
    """Preferred HTML: single self-contained web page with a fixed LEFT docked
    Table of Contents (scrollspy highlights the current section), a floating
    toolbar (Contents / Print-PDF / Full-width / A-/A+ / Top / Reset), click-to-
    zoom lightbox on every figure, light theme, Times New Roman body, and OFFLINE
    MathJax (SVG) with right-aligned \\tag{N} equation numbers.

    IMPORTANT: display equations must be $$ ... \\tag{N}$$ (not \\qquad (N)), and
    the source must avoid autoload-only TeX macros (\\boldsymbol, \\bm, \\color,
    \\cancel) because MathJax autoload fails offline and one failure aborts ALL
    equation rendering. See scripts/finalize_web_html.py and
    templates/html_web_style.md for the full rationale.

    Headings carry their own numbers (e.g. `## 6.2 ...`), so --number-sections is
    intentionally NOT used here (it would double-number)."""
    _run(["pandoc", str(md), "-o", str(out), "--standalone", "--embed-resources",
          "--toc", "--toc-depth=3", f"--mathjax={MJX_BUNDLE}", "-c", str(WEB_CSS),
          f"--include-before-body={WEB_TOOLBAR}",
          f"--include-after-body={WEB_LIGHTBOX}"])
    # Fix MathJax so it renders offline (see finalize_web_html.py docstring).
    sys.path.insert(0, str(SCRIPTS))
    from finalize_web_html import finalize, ensure_bundle  # type: ignore
    finalize(out, ensure_bundle(MJX_BUNDLE))
    return out

def to_html_plain(md: Path, out: Path) -> Path:
    """Fallback: simple standalone HTML (auto-numbered, seismo.css, static math)."""
    _run(["pandoc", str(md), "-o", str(out), "--standalone",
          "--embed-resources", "--toc", "--number-sections", "-c", str(CSS)])
    return out

def to_docx(md: Path, out: Path) -> Path:
    sys.path.insert(0, str(SCRIPTS)); _ensure_reference()
    _run(["pandoc", str(md), "-o", str(out), "--toc", "--number-sections",
          f"--reference-doc={REF_DOCX}"])
    return out

def to_pdf(md: Path, out: Path) -> Path:
    _run(["pandoc", str(md), "-o", str(out), "--pdf-engine=xelatex",
          "--toc", "--number-sections", "-V", "mainfont=Times New Roman",
          "-V", "geometry:margin=1in", "-H", str(PREAMBLE)])
    return out

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("md", type=Path)
    ap.add_argument("--html", action="store_true", help="web-style docked/MathJax HTML (default)")
    ap.add_argument("--html-plain", action="store_true", help="simple auto-numbered HTML")
    ap.add_argument("--docx", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--pptx", action="store_true")
    a = ap.parse_args()
    stem = a.md.with_suffix("")
    if a.html_plain:
        print("HTML:", to_html_plain(a.md, stem.with_suffix(".html")))
    elif a.html or not (a.docx or a.pdf or a.pptx):
        print("HTML:", to_html(a.md, stem.with_suffix(".html")))
    if a.docx: print("DOCX:", to_docx(a.md, stem.with_suffix(".docx")))
    if a.pdf:  print("PDF:", to_pdf(a.md, stem.with_suffix(".pdf")))
    if a.pptx:
        _run(["pandoc", str(a.md), "-o", str(stem.with_suffix(".pptx")),
              "-t", "pptx"])
        print("PPTX:", stem.with_suffix(".pptx"))

if __name__ == "__main__":
    main()
