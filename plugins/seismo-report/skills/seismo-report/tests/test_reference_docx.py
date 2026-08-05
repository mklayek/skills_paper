# tests/test_reference_docx.py
from pathlib import Path
import importlib.util

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "make_reference_docx.py"

def _load():
    spec = importlib.util.spec_from_file_location("mrd", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_reference_docx_styles(tmp_path):
    mod = _load()
    out = mod.build_reference(tmp_path / "reference_seismo.docx")
    assert out.exists()
    doc = Document(str(out))
    normal = doc.styles["Normal"]
    assert normal.font.name == "Times New Roman"
    assert normal.font.size == Pt(12)
    pf = normal.paragraph_format
    assert abs(pf.line_spacing - 1.15) < 1e-6
    assert pf.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY
    assert pf.first_line_indent is not None and pf.first_line_indent > 0
    h1 = doc.styles["Heading 1"]
    assert h1.font.bold is True and h1.font.size == Pt(16)
    h4 = doc.styles["Heading 4"]
    assert not h4.font.bold and h4.font.size == Pt(12)
    h5 = doc.styles["Heading 5"]
    assert h5.font.italic is True
