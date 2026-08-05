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

def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)

def _ensure_reference() -> Path:
    if not REF_DOCX.exists():
        from make_reference_docx import build_reference  # type: ignore
        build_reference(REF_DOCX)
    return REF_DOCX

def to_html(md: Path, out: Path) -> Path:
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
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--docx", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--pptx", action="store_true")
    a = ap.parse_args()
    stem = a.md.with_suffix("")
    if a.html or not (a.docx or a.pdf or a.pptx):
        print("HTML:", to_html(a.md, stem.with_suffix(".html")))
    if a.docx: print("DOCX:", to_docx(a.md, stem.with_suffix(".docx")))
    if a.pdf:  print("PDF:", to_pdf(a.md, stem.with_suffix(".pdf")))
    if a.pptx:
        _run(["pandoc", str(a.md), "-o", str(stem.with_suffix(".pptx")),
              "-t", "pptx"])
        print("PPTX:", stem.with_suffix(".pptx"))

if __name__ == "__main__":
    main()
