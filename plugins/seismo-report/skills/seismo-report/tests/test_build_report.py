# tests/test_build_report.py
from pathlib import Path
import importlib.util, shutil, subprocess
import pytest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "build_report.py"

def _load():
    spec = importlib.util.spec_from_file_location("br", SCRIPT)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

MD = "2026-08-05\n\n# Demo\n\n**1. Introduction**\n\nThe demo body explains $V_s$.\n"

@pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc required")
def test_html_and_docx(tmp_path):
    mod = _load()
    md = tmp_path / "REPORT.md"; md.write_text(MD, encoding="utf-8")
    html = mod.to_html(md, tmp_path / "REPORT.html")
    assert html.exists() and html.stat().st_size > 0
    docx = mod.to_docx(md, tmp_path / "REPORT.docx")
    assert docx.exists() and docx.stat().st_size > 0
