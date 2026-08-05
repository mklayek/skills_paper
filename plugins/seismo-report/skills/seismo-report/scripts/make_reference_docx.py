# scripts/make_reference_docx.py
"""Build reference_seismo.docx encoding the seismo-report DOCX styles.
Body: Times New Roman 12pt, 1.15 spacing, first-line indent 0.5in, justified,
Korean via Malgun Gothic (eastAsia). Headings per formatting_spec.md."""
from __future__ import annotations
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

BODY_FONT = "Times New Roman"
EA_FONT = "Malgun Gothic"

def _set_eastasia(style, font_name: str) -> None:
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), font_name)

def _body(style) -> None:
    style.font.name = BODY_FONT
    style.font.size = Pt(12)
    _set_eastasia(style, EA_FONT)
    pf = style.paragraph_format
    pf.line_spacing = 1.15
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = Inches(0.5)
    pf.space_after = Pt(6)

def _heading(doc, name: str, size: int, bold: bool, italic: bool) -> None:
    st = doc.styles[name]
    st.font.name = BODY_FONT
    _set_eastasia(st, EA_FONT)
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.italic = italic
    st.paragraph_format.space_before = Pt(10)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.first_line_indent = Inches(0)

def build_reference(out_path) -> Path:
    out_path = Path(out_path)
    doc = Document()
    for name in ("Normal", "Body Text", "First Paragraph"):
        if name in [s.name for s in doc.styles]:
            _body(doc.styles[name])
    # Heading hierarchy from formatting_spec.md.
    _heading(doc, "Heading 1", 16, True, False)
    _heading(doc, "Heading 2", 14, True, False)
    _heading(doc, "Heading 3", 13, True, False)
    _heading(doc, "Heading 4", 12, False, False)
    _heading(doc, "Heading 5", 12, False, True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    return out_path

if __name__ == "__main__":
    p = build_reference(Path(__file__).with_name("reference_seismo.docx"))
    print(f"wrote {p}")
