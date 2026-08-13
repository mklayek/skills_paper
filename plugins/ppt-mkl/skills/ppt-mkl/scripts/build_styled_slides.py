#!/usr/bin/env python3
"""build_styled_slides.py — deck mini-language -> styled research-presentation PPTX.

Renders the "lecture" slide style used for the cganac_v2_r1 methodology talk:

  * underlined bold serif title with a red key phrase, over a double (grey+orange) rule;
  * green checkbox bullets, red star sub-bullets, small dot sub-sub-bullets;
  * native, editable PowerPoint equations (OMML via pandoc) with a red `---(N)`
    equation tag placed on the same line, preserving the source numbering;
  * a bold takeaway line and a purple handwriting "Therefore, ..." line;
  * bottom-anchored figure, thin page frame, and a date / label / page-number footer;
  * the source's discussion paragraph as the speaker note.

INPUT — strict line-prefix mini-language (see DECK_SPEC.md):

    # Section title            section divider slide
    == PREFIX : Title with **red** phrase
    - level-0 bullet           --  level-1 bullet        --- level-2 bullet
    $$ latex $$ (7)            display equation numbered (7)
    !key: bold takeaway        !so: purple therefore-line
    !fig: /abs/f.png 60%       !note: speaker note
    Inline: $math$  **maroon bold**  ==yellow highlight==

USAGE:
    python3 build_styled_slides.py deck.deck --out /abs/out.pptx \
        --title "..." --subtitle "..." --author "..." --date "21 July 2026" \
        --foot "Methodological Evolution"

Author: Mrinal Kanti Layek - Geophysics & AI Lab, Chonnam National University.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

# --------------------------------------------------------------------------- #
# Style constants
# --------------------------------------------------------------------------- #
SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)

C_TITLE = "000000"      # title black
C_RED = "C00000"        # title key phrase / stars / equation tags
C_TERM = "7B2D26"       # maroon key terms in body
C_CHECK = "2E7D32"      # green checkbox
C_TEXT = "000000"
C_SO = "6A0DAD"         # purple "therefore" line
C_FOOT = "808080"
C_RULE_ORANGE = "E8722C"
C_RULE_GREY = "404040"
C_FRAME = "BFBFBF"
C_REF = "1F3864"        # dark blue — references and inline citations

F_TITLE = "Times New Roman"
F_BODY = "Times New Roman"   # all prose: title, bullets, footer
F_HAND = "Segoe Script"        # reserved for the purple "Therefore, ..." line
F_SYM = "Segoe UI Symbol"
F_MATH = "Cambria Math"
F_REF = "Comic Sans MS"        # references / citations

# geometry (inches)
M_L, M_R = 0.30, 0.30
TITLE_TOP, TITLE_H = 0.14, 0.72
RULE_Y = 0.95
BODY_TOP = 1.08
FOOT_RULE_Y = 6.96
FOOT_Y = 7.00
BODY_BOT = 6.88

SZ = {0: 20.0, 1: 18.0, 2: 16.0}   # pt per bullet level
SZ_EQ = 20.0
SZ_KEY = 20.0
SZ_SO = 19.0
SZ_REF = 20.0                  # references are fixed at 20 pt, never auto-shrunk
MIN_SCALE = 0.62

NSMAP = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
NSDECL = " ".join(f'xmlns:{k}="{v}"' for k, v in NSMAP.items())
A = NSMAP["a"]
P = NSMAP["p"]
MC = NSMAP["mc"]

EMU_IN = 914400


def emu(inches: float) -> int:
    return int(round(inches * EMU_IN))


# --------------------------------------------------------------------------- #
# 1. Parse the deck mini-language
# --------------------------------------------------------------------------- #
@dataclass
class Block:
    kind: str                     # bullet | eq | key | so | fig
    text: str = ""
    level: int = 0
    tag: str = ""                 # equation number, e.g. "7"
    width: float = 0.55           # figure width fraction


@dataclass
class Slide:
    title: str = ""
    blocks: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    section: bool = False


RE_EQ = re.compile(r"^\$\$(?P<tex>.*?)\$\$\s*(?:\((?P<tag>[0-9]+[a-z]?)\))?\s*$")
RE_FIG = re.compile(r"^!fig:\s*(?P<path>\S.*?)\s+(?P<w>[0-9.]+)%\s*(?:\|\s*(?P<cap>.+?))?\s*$")


def parse_deck(path: str) -> list[Slide]:
    slides: list[Slide] = []
    cur: Slide | None = None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n").rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            slides.append(Slide(title=line[2:].strip(), section=True))
            cur = None
            continue
        if line.startswith("== "):
            cur = Slide(title=line[3:].strip())
            slides.append(cur)
            continue
        if cur is None:                     # stray content before any slide
            cur = Slide(title="")
            slides.append(cur)
        s = line.strip()
        m = RE_EQ.match(s)
        if m:
            cur.blocks.append(Block("eq", m.group("tex").strip(), tag=m.group("tag") or ""))
            continue
        m = RE_FIG.match(s)
        if m:
            cur.blocks.append(Block("fig", m.group("path").strip(),
                                    width=float(m.group("w")) / 100.0,
                                    tag=(m.group("cap") or "").strip()))
            continue
        if s.startswith("!key:"):
            cur.blocks.append(Block("key", s[5:].strip()))
            continue
        if s.startswith("!ref:"):
            cur.blocks.append(Block("ref", s[5:].strip()))
            continue
        if s.startswith("!so:"):
            cur.blocks.append(Block("so", s[4:].strip()))
            continue
        if s.startswith("!note:"):
            cur.notes.append(s[6:].strip())
            continue
        m = re.match(r"^(-{1,3})\s+(.*)$", s)
        if m:
            cur.blocks.append(Block("bullet", m.group(2).strip(), level=len(m.group(1)) - 1))
            continue
        # bare continuation text -> level-0 bullet without a marker
        cur.blocks.append(Block("bullet", s, level=0))
    return slides


# --------------------------------------------------------------------------- #
# 2. LaTeX -> OMML (one batched pandoc run)
# --------------------------------------------------------------------------- #
RE_MATH = re.compile(r"\$(?P<tex>[^$]+?)\$")
# a bullet that starts with maths and then explains it, e.g. "$a>0$ — continuous scale"
RE_DEFN = re.compile(r"^\s*\$[^$]+\$.{0,40}?(?:—|--)")


def find_pandoc() -> str:
    p = shutil.which("pandoc")
    if p:
        return p
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except Exception:
        sys.exit("ERROR: pandoc not found (pip install pypandoc_binary).")


def clean_tex(tex: str) -> str:
    tex = tex.replace("\\tag{", "\\ignoretag{")
    tex = re.sub(r"\\ignoretag\{[^}]*\}", "", tex)
    tex = re.sub(r"\\boxed\s*\{", "{", tex)
    tex = tex.replace("\\!", "").replace("\\;", "\\ ").replace("\\,", "\\ ")
    return tex.strip()


def collect_math(slides: list[Slide]) -> list[str]:
    """Every distinct LaTeX string in the deck, in first-seen order."""
    seen: dict[str, None] = {}
    for sl in slides:
        for t in (sl.title,):
            for m in RE_MATH.finditer(t):
                seen.setdefault(clean_tex(m.group("tex")), None)
        for b in sl.blocks:
            if b.kind == "eq":
                seen.setdefault(clean_tex(b.text), None)
            elif b.kind in ("bullet", "key", "so"):
                for m in RE_MATH.finditer(b.text):
                    seen.setdefault(clean_tex(m.group("tex")), None)
    return [k for k in seen if k]


def build_omml_map(tex_list: list[str]) -> dict[str, str]:
    """Convert every LaTeX snippet to an <m:oMath> XML string via one pandoc call."""
    if not tex_list:
        return {}
    pandoc = find_pandoc()
    tmp = tempfile.mkdtemp(prefix="omml_")
    md = os.path.join(tmp, "m.md")
    with open(md, "w", encoding="utf-8") as f:
        for i, tex in enumerate(tex_list):
            f.write(f"## MK{i}MK\n\n$${tex}$$\n\n")
    out = os.path.join(tmp, "m.pptx")
    r = subprocess.run([pandoc, md, "-o", out, "--slide-level=2"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        print("  WARN: pandoc math pass failed:", (r.stderr or "")[-400:])
        return {}
    mapping: dict[str, str] = {}
    with zipfile.ZipFile(out) as z:
        for name in z.namelist():
            if not (name.startswith("ppt/slides/slide") and name.endswith(".xml")):
                continue
            xml = z.read(name).decode("utf-8")
            mk = re.search(r"MK(\d+)MK", xml)
            if not mk:
                continue
            idx = int(mk.group(1))
            om = re.search(r"<m:oMath[ >].*?</m:oMath>", xml, re.S)
            if om:
                mapping[tex_list[idx]] = om.group(0)
    shutil.rmtree(tmp, ignore_errors=True)
    missing = [t for t in tex_list if t not in mapping]
    if missing:
        print(f"  WARN: {len(missing)} equations did not convert; first: {missing[0][:70]}")
    return mapping


def omml_run(omml: str, size_pt: float) -> str:
    """Wrap a stored <m:oMath> as an inline a14:m run at the requested size."""
    body = omml
    if not body.startswith("<m:oMath "):
        body = body.replace("<m:oMath>", f'<m:oMath xmlns:m="{NSMAP["m"]}">', 1)
    # size the maths by stamping a:rPr sz onto every m:r that lacks one
    # Mirror what PowerPoint itself writes: <m:r>[<m:rPr>]<a:rPr sz><a:latin Cambria Math/>
    sz = int(round(size_pt * 100))
    arpr = (f'<a:rPr sz="{sz}"><a:latin typeface="Cambria Math"'
            ' panose="02040503050406030204" pitchFamily="18" charset="0"/></a:rPr>')
    body = re.sub(r"<m:r>(?!<m:rPr)", f"<m:r>{arpr}", body)
    body = re.sub(r"(</m:rPr>)(?!<a:rPr)", f"\\1{arpr}", body)
    return f'<a14:m xmlns:a14="{NSMAP["a14"]}">{body}</a14:m>'


# --------------------------------------------------------------------------- #
# 3. Rich-text runs
# --------------------------------------------------------------------------- #
def math_width(tex: str) -> float:
    """Approximate the RENDERED width of a LaTeX snippet, in character units.

    Counting raw LaTeX characters badly overestimates: "\\Delta r\\sim 2^{-j}" is 20
    source characters but draws about 6. Each control sequence renders as roughly one
    glyph, and braces/scripts/spacing macros draw nothing, so strip them first. The
    body-text line estimator depends on this, and so therefore does the vertical
    placement of every equation-number box.
    """
    t = re.sub(r"\\(?:left|right|big|Big|bigg|Bigg|displaystyle|limits)\b", "", tex)
    t = re.sub(r"\\(?:quad|qquad)\b", "  ", t)
    t = re.sub(r"\\[,;!:> ]", "", t)
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\operatorname\{([^}]*)\}", r"\1", t)
    t = re.sub(r"\\[A-Za-z]+", "M", t)          # one glyph per control sequence
    t = re.sub(r"[{}$&\\]", "", t)
    t = re.sub(r"[_^]", "", t)
    return len(t) * 1.15


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# Some renderers let an <a:highlight> leak into the following paragraphs. When a slide
# uses a yellow highlight at all, every other run on that slide is given an explicit
# white highlight, which is invisible on the white page and stops the inheritance.
_HL_RESET = [False]


def rpr(size_pt: float, *, bold=False, color=C_TEXT, italic=False, font=F_BODY,
        highlight: str | None = None, underline=False, sym: str | None = None) -> str:
    if highlight is None and _HL_RESET[0]:
        highlight = "FFFFFF"
    a = [f'lang="en-US" sz="{int(round(size_pt * 100))}"', 'dirty="0"']
    if bold:
        a.append('b="1"')
    if italic:
        a.append('i="1"')
    if underline:
        a.append('u="sng"')
    inner = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
    if highlight:
        inner += f'<a:highlight><a:srgbClr val="{highlight}"/></a:highlight>'
    inner += f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/>'
    if sym:                     # a:sym must follow a:latin/a:ea/a:cs in the schema
        inner += f'<a:sym typeface="{sym}"/>'
    return f'<a:rPr {" ".join(a)}>{inner}</a:rPr>'


def text_run(txt: str, size_pt: float, **kw) -> str:
    if not txt:
        return ""
    return f"<a:r>{rpr(size_pt, **kw)}<a:t>{esc(txt)}</a:t></a:r>"


TOKEN = re.compile(r"(\$[^$]+?\$|\*\*.+?\*\*|==.+?==|@@.+?@@|\*[^*\n]+?\*)")


def rich_runs(text: str, size_pt: float, omml: dict[str, str],
              base_color=C_TEXT, base_bold=False, font=F_BODY, italic=False) -> tuple[str, float]:
    """Render one line into PPTX runs; returns (xml, estimated display length)."""
    out, est = [], 0.0
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("$") and part.endswith("$") and len(part) > 2:
            tex = clean_tex(part[1:-1])
            if tex in omml:
                out.append(omml_run(omml[tex], size_pt))
                est += max(2.0, math_width(tex))
            else:
                out.append(text_run(part[1:-1], size_pt, color=base_color,
                                    bold=base_bold, italic=True, font=F_MATH))
                est += math_width(tex)
        elif part.startswith("**") and part.endswith("**"):
            s = part[2:-2]
            out.append(text_run(s, size_pt, bold=True, color=C_TERM, font=font))
            est += len(s)
        elif part.startswith("==") and part.endswith("=="):
            s = part[2:-2]
            out.append(text_run(s, size_pt, bold=True, color=C_RED,
                                highlight="FFFF00", font=font))
            est += len(s)
        elif part.startswith("@@") and part.endswith("@@"):
            s = part[2:-2]                       # inline citation, same look as !ref:
            out.append(text_run(s, size_pt, color=C_REF, italic=True, font=F_REF))
            est += len(s) * 1.08
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            s_ = part[1:-1]
            out.append(text_run(s_, size_pt, color=base_color, bold=base_bold,
                                font=font, italic=True))
            est += len(s_)
        else:
            out.append(text_run(part, size_pt, color=base_color, bold=base_bold,
                                font=font, italic=italic))
            est += len(part)
    return "".join(out), est


# --------------------------------------------------------------------------- #
# 4. Paragraph builders
# --------------------------------------------------------------------------- #
IND = {0: (0.0, 0.0), 1: (0.30, 0.0), 2: (0.60, 0.0)}   # (marL, hanging) inches
# Body text starts flush at the LEFT edge of the text box: marL=0 and hanging=0 for
# level-0, so first line and wrapped lines both begin at the leftmost point (no gap,
# no hanging indent). Nested levels get a small left margin but still no hanging.
# Markers are ordinary TEXT characters in the run, not PowerPoint list bullets
# (every paragraph carries <a:buNone/>). That way the user can select a line, copy it,
# and the symbol travels with the text. Plain Unicode is used rather than Wingdings
# private-use code points, which paste as broken glyphs outside PowerPoint.
MARK = {0: ("\u25AA  ", "000000", F_SYM),    # solid black square, level-0 statements
        1: ("\u25AA  ", "000000", F_SYM),    # solid black square, term / symbol definitions
        2: ("\u25AA  ", "000000", F_SYM)}    # solid black square, third level


def para(pPr: str, runs: str) -> str:
    return f"<a:p>{pPr}{runs}</a:p>"


def build_paragraphs(blocks, omml: dict[str, str], scale: float) -> tuple[str, float, list]:
    """Return (paragraph XML, estimated height, equation-tag anchors).

    Everything — bullets AND equations — goes into ONE body text box. The anchors
    are (tag, y_offset, line_height) triples telling the caller where each numbered
    equation lands, so only the red ---(N) can be placed as a small separate box at
    the right margin, level with its equation.
    """
    xml, height, anchors = [], 0.0, []
    body_w = 13.333 - M_L - M_R - 0.30
    for b in blocks:
        if b.kind == "fig":
            continue
        if b.kind == "bullet":
            level = b.level
            if level == 0 and RE_DEFN.match(b.text):
                level = 1               # "$x$ — meaning." is a definition, not a claim
            size = SZ[level] * scale
            marL, hang = IND[level]
            mark, mcol, mfont = MARK[level]
            pPr = (f'<a:pPr marL="{emu(marL)}" indent="{emu(-hang)}" lvl="0">'
                   f'<a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
                   f'<a:spcBef><a:spcPts val="{int(520 * scale)}"/></a:spcBef>'
                   f'<a:buNone/></a:pPr>')
            runs = text_run(mark, size * 1.04, color=mcol, bold=True, font=mfont)
            body, est = rich_runs(b.text, size, omml)
            xml.append(para(pPr, runs + body))
            avail = body_w - marL
            cpl = max(12.0, avail / (size * 0.0060))
            height += math.ceil((est + 3) / cpl) * (size * 1.30 / 72.0) + 0.05
        elif b.kind == "eq":
            size = SZ_EQ * scale
            tex = clean_tex(b.text)
            body_eq = (omml_run(omml[tex], size) if tex in omml
                       else text_run(b.text, size, italic=True, font=F_MATH))
            # A numbered equation owns its own text box; the red ---(N) sits in a
            # SEPARATE box at the right margin, so reserve that strip with marR and
            # centre the maths in what is left.
            marR = emu(1.55) if b.tag else 0
            pPr = (f'<a:pPr algn="ctr" marL="0" marR="{marR}" indent="0">'
                   f'<a:spcBef><a:spcPts val="{int(420 * scale)}"/></a:spcBef>'
                   '<a:buNone/></a:pPr>')
            runs = body_eq
            xml.append(para(pPr, runs))
            est = math_width(tex) + 8
            cpl = max(12.0, body_w / (size * 0.0072))
            eq_h = math.ceil(est / cpl) * (size * 1.70 / 72.0) + 0.12
            if b.tag:
                anchors.append((b.tag, height, eq_h))
            height += eq_h
        elif b.kind == "key":
            size = SZ_KEY * scale
            pPr = ('<a:pPr marL="0" indent="0">'
                   f'<a:spcBef><a:spcPts val="{int(420 * scale)}"/></a:spcBef>'
                   '<a:buNone/></a:pPr>')
            runs = text_run("▪  ", size, bold=True, color="000000", font=F_SYM)
            body, est = rich_runs(b.text, size, omml, base_bold=True)
            xml.append(para(pPr, runs + body))
            cpl = max(12.0, body_w / (size * 0.0063))
            height += math.ceil((est + 3) / cpl) * (size * 1.30 / 72.0) + 0.06
        elif b.kind == "ref":
            # References keep their own size no matter how full the slide is: the
            # auto-shrink deliberately does not touch them.
            size = SZ_REF
            pPr = ('<a:pPr marL="0" indent="0">'
                   f'<a:spcBef><a:spcPts val="360"/></a:spcBef>'
                   '<a:buNone/></a:pPr>')
            body, est = rich_runs(b.text, size, omml, base_color=C_REF,
                                  font=F_REF, italic=True)
            xml.append(para(pPr, body))
            cpl = max(12.0, body_w / (size * 0.0076))
            height += math.ceil(est / cpl) * (size * 1.34 / 72.0) + 0.07
        elif b.kind == "so":
            size = SZ_SO * scale
            pPr = ('<a:pPr marL="0" indent="0">'
                   f'<a:spcBef><a:spcPts val="{int(420 * scale)}"/></a:spcBef>'
                   '<a:buNone/></a:pPr>')
            runs = text_run("▪  ", size, bold=True, color=C_SO, font=F_SYM)
            body, est = rich_runs(b.text, size, omml, base_color=C_SO, font=F_HAND)
            xml.append(para(pPr, runs + body))
            cpl = max(12.0, body_w / (size * 0.0080))
            height += math.ceil((est + 3) / cpl) * (size * 1.34 / 72.0) + 0.06
    return "".join(xml), height, anchors


CONNECTORS = ("expressed as below", "formulated as below", "described as",
              "written as", "given by", "stated as below", "defined as below",
              "as follows", "reads")


def lint_pretext(slides) -> int:
    """Check the equation-pretext rule on every display equation.

    A display equation must be introduced by a statement that says what it establishes,
    ending in a PLAIN connector plus a colon, with the substantive phrase — what the
    equation makes explicit — in bold. Bolding the connector instead puts the emphasis on
    "given by:" rather than on the physics, which is the mistake this catches.
    """
    n = 0

    def warn(tag, msg, title):
        print(f'  WARN: equation ({tag or "-"}) {msg}  [slide: {title[:52]}]')

    for sl in slides:
        prev = None
        for b in sl.blocks:
            if b.kind == "eq":
                raw = (prev.text.rstrip() if prev is not None and prev.kind == "bullet" else "")
                txt = re.sub(r"[*_`\s]+$", "", raw)
                bolds = re.findall(r"\*\*(.+?)\*\*", raw)
                connector_bolded = any(
                    c in bb.lower() for bb in bolds for c in CONNECTORS)
                substantive = [bb for bb in bolds
                               if not any(c in bb.lower() for c in CONNECTORS)]
                if not txt.endswith(":"):
                    n += 1; warn(b.tag, "has no lead-in", sl.title)
                elif not any(c in txt.lower() for c in CONNECTORS):
                    n += 1; warn(b.tag, "lead-in has no connecting phrase", sl.title)
                elif connector_bolded:
                    n += 1; warn(b.tag, "connector is bolded (bold the substance instead)",
                                 sl.title)
                elif not substantive:
                    n += 1; warn(b.tag, "lead-in has no bold phrase naming what the "
                                        "equation establishes", sl.title)
            prev = b
    return n


# --------------------------------------------------------------------------- #
# 5. Slide assembly
# --------------------------------------------------------------------------- #
def set_txbody(shape, paragraphs_xml: str, *, anchor="t", autofit=True) -> bool:
    """Replace a textbox's paragraphs with raw XML. Returns True if it holds maths."""
    sp = shape._element
    tx = sp.find(f"{{{P}}}txBody")
    for child in list(tx):
        if child.tag in (f"{{{A}}}p",):
            tx.remove(child)
    bodyPr = tx.find(f"{{{A}}}bodyPr")
    bodyPr.set("wrap", "square")
    bodyPr.set("anchor", anchor)
    bodyPr.set("lIns", "0"); bodyPr.set("rIns", "0")
    bodyPr.set("tIns", "0"); bodyPr.set("bIns", "0")
    for ch in list(bodyPr):
        bodyPr.remove(ch)
    if autofit:
        etree.SubElement(bodyPr, f"{{{A}}}normAutofit")
    frag = etree.fromstring(f"<root {NSDECL}>{paragraphs_xml}</root>".encode("utf-8"))
    for child in frag:
        tx.append(child)
    return "a14:m" in paragraphs_xml or "}m" in paragraphs_xml


def wrap_alternate_content(shape) -> None:
    """Wrap a maths-bearing <p:sp> in mc:AlternateContent/mc:Choice (as pandoc does)."""
    # Built from a literal XML string, not SubElement: `Requires="a14"` names a namespace
    # PREFIX, so xmlns:a14 must be declared on mc:Choice itself. Letting lxml invent the
    # prefixes (ns0:Choice with no a14 in scope) produces a file PowerPoint rejects.
    sp = shape._element
    parent = sp.getparent()
    idx = parent.index(sp)
    sp_xml = etree.tostring(sp, encoding="unicode")
    wrapper = (f"<mc:AlternateContent {NSDECL}>"
               f'<mc:Choice xmlns:a14="{NSMAP["a14"]}" Requires="a14">{sp_xml}</mc:Choice>'
               "</mc:AlternateContent>")
    alt = etree.fromstring(wrapper.encode("utf-8"))
    parent.remove(sp)
    parent.insert(idx, alt)


def add_line(slide, y: float, color: str, width_pt: float,
             x0: float = M_L, x1: float = 13.333 - M_R):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, emu(x0), emu(y),
                                emu(x1 - x0), emu(width_pt / 72.0))
    ln.fill.solid()
    ln.fill.fore_color.rgb = RGBColor.from_string(color)
    ln.line.fill.background()
    ln.shadow.inherit = False
    return ln


def add_frame(slide):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, emu(0.16), emu(0.10),
                               emu(13.333 - 0.32), emu(7.5 - 0.22))
    r.fill.background()
    r.line.color.rgb = RGBColor.from_string(C_FRAME)
    r.line.width = Pt(0.75)
    r.shadow.inherit = False
    return r


_FOOTER_OPTS = {"no_date": False, "no_page": False}


def add_footer(slide, date_s: str, foot: str, page: int):
    y, h = FOOT_Y, 0.30
    slots = [(13.333 / 2 - 2.5, 5.0, foot, PP_ALIGN.CENTER)]
    if not _FOOTER_OPTS["no_date"]:
        slots.insert(0, (M_L + 0.15, 3.0, date_s, PP_ALIGN.LEFT))
    if not _FOOTER_OPTS["no_page"]:
        slots.append((13.333 - M_R - 3.15, 3.0, str(page), PP_ALIGN.RIGHT))
    for x, w, txt, align in slots:
        tb = slide.shapes.add_textbox(emu(x), emu(y), emu(w), emu(h))
        tf = tb.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = align
        run = p.add_run()
        run.text = txt
        run.font.size = Pt(11)
        run.font.name = F_BODY
        run.font.color.rgb = RGBColor.from_string(C_FOOT)


def title_paragraph(title: str, omml: dict[str, str], size_pt: float) -> str:
    pPr = ('<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/>'
           '<a:lnSpc><a:spcPct val="92000"/></a:lnSpc></a:pPr>')
    runs, _ = rich_runs_title(title, size_pt, omml)
    return para(pPr, runs)


def rich_runs_title(text: str, size_pt: float, omml: dict[str, str]) -> tuple[str, float]:
    out, est = [], 0.0
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            s = part[2:-2]
            out.append(text_run(s, size_pt, bold=True, color=C_RED,
                                font=F_TITLE, underline=True))
            est += len(s)
        elif part.startswith("$") and part.endswith("$") and len(part) > 2:
            s = part[1:-1]
            out.append(text_run(s, size_pt, bold=True, color=C_TITLE,
                                font=F_TITLE, italic=True, underline=True))
            est += len(s)
        elif part.startswith("==") and part.endswith("=="):
            s = part[2:-2]
            out.append(text_run(s, size_pt, bold=True, color=C_RED,
                                font=F_TITLE, underline=True))
            est += len(s)
        else:
            part = part.replace("*", "")
            out.append(text_run(part, size_pt, bold=True, color=C_TITLE,
                                font=F_TITLE, underline=True))
            est += len(part)
    return "".join(out), est


def build_content_slide(prs, sl: Slide, omml: dict[str, str], date_s: str,
                        foot: str, page: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])   # blank
    add_frame(slide)

    # --- title ------------------------------------------------------------- #
    _HL_RESET[0] = False
    plain_len = len(re.sub(r"[*=$]", "", sl.title))
    t_size = 30.0 if plain_len <= 52 else (26.0 if plain_len <= 66 else 23.0)
    tb = slide.shapes.add_textbox(emu(M_L + 0.10), emu(TITLE_TOP),
                                  emu(13.333 - M_L - M_R - 0.20), emu(TITLE_H))
    set_txbody(tb, title_paragraph(sl.title, omml, t_size), anchor="ctr")

    add_line(slide, RULE_Y, C_RULE_GREY, 0.9)
    add_line(slide, RULE_Y + 0.035, C_RULE_ORANGE, 2.4)

    # --- body first: it decides how much room is left for the figure ------- #
    figs = [b for b in sl.blocks if b.kind == "fig" and os.path.exists(b.text)]
    for b in sl.blocks:
        if b.kind == "fig" and not os.path.exists(b.text):
            print(f"  WARN: missing figure {b.text}")

    usable_w = 13.333 - M_L - M_R - 0.40
    fig_cap = figs[0].tag if figs else ""
    cap_h = 0.32 if fig_cap else 0.0
    fig_h = 0.0
    if figs:
        from PIL import Image
        with Image.open(figs[0].text) as im:
            iw, ih = im.size
        want_h = min(4.35 - cap_h, usable_w * figs[0].width * ih / iw)
        options = [want_h, want_h * 0.86, want_h * 0.72, max(1.75, want_h * 0.58)]
    else:
        options = [0.0]

    _HL_RESET[0] = any("==" in b.text for b in sl.blocks
                       if b.kind in ("bullet", "key", "so"))
    for fh in options:                      # give the figure its space, then fit the body
        avail = (FOOT_RULE_Y - 0.14 - fh - cap_h) - BODY_TOP
        scale = 1.0
        xml, hgt, anchors = build_paragraphs(sl.blocks, omml, scale)
        while hgt > avail and scale > MIN_SCALE:
            scale = max(MIN_SCALE, scale - 0.04)
            xml, hgt, anchors = build_paragraphs(sl.blocks, omml, scale)
        fig_h = fh
        if hgt <= avail:
            break

    if figs:
        h = fig_h
        w = min(usable_w, h * iw / ih)
        h = w * ih / iw
        img_bottom = FOOT_RULE_Y - 0.12 - cap_h
        slide.shapes.add_picture(figs[0].text, emu((13.333 - w) / 2.0),
                                 emu(img_bottom - h), emu(w), emu(h))
        if fig_cap:                         # italic caption centred under the image
            cb = slide.shapes.add_textbox(emu(M_L + 0.16), emu(img_bottom + 0.02),
                                          emu(13.333 - M_L - M_R - 0.32), emu(cap_h))
            cb.text_frame.word_wrap = True
            set_txbody(cb,
                       para('<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/></a:pPr>',
                            rich_runs(fig_cap, 13.5, omml, italic=True)[0]),
                       anchor="t", autofit=False)

    box_x, box_w = M_L + 0.16, 13.333 - M_L - M_R - 0.32

    # ONE body text box: every bullet and every equation flows inside it.
    bb = slide.shapes.add_textbox(emu(box_x), emu(BODY_TOP), emu(box_w),
                                  emu(max(0.6, avail)))
    if set_txbody(bb, xml, anchor="t"):
        wrap_alternate_content(bb)

    # Only the equation number is a separate box, pinned to the right margin at the
    # vertical position its equation flows to.
    tw = 1.30 * max(scale, 0.78)
    for tag, y_off, line_h in anchors:
        tb2 = slide.shapes.add_textbox(emu(box_x + box_w - tw),
                                       emu(BODY_TOP + y_off), emu(tw),
                                       emu(max(line_h, 0.34)))
        set_txbody(tb2,
                   para('<a:pPr algn="r" marL="0" indent="0"><a:buNone/></a:pPr>',
                        text_run(f"---({tag})", SZ_EQ * scale, bold=True,
                                 color=C_RED)),
                   anchor="ctr", autofit=False)

    add_line(slide, FOOT_RULE_Y, C_FRAME, 0.75)
    add_footer(slide, date_s, foot, page)

    if sl.notes:
        slide.notes_slide.notes_text_frame.text = " ".join(sl.notes)


def build_section_slide(prs, sl: Slide, date_s: str, foot: str, page: int) -> None:
    _HL_RESET[0] = False
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_frame(slide)
    add_line(slide, 3.05, C_RULE_GREY, 0.9)
    add_line(slide, 3.085, C_RULE_ORANGE, 2.4)
    tb = slide.shapes.add_textbox(emu(1.0), emu(3.25), emu(11.333), emu(1.4))
    pPr = '<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/></a:pPr>'
    runs = text_run(sl.title, 34, bold=True, color=C_TITLE, font=F_TITLE)
    set_txbody(tb, para(pPr, runs), anchor="ctr")
    add_line(slide, 4.75, C_RULE_ORANGE, 2.4)
    add_line(slide, 4.785, C_RULE_GREY, 0.9)
    add_line(slide, FOOT_RULE_Y, C_FRAME, 0.75)
    add_footer(slide, date_s, foot, page)


def build_title_slide(prs, title: str, subtitle: str, author: str, date_s: str,
                      foot: str) -> None:
    _HL_RESET[0] = False
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_frame(slide)
    add_line(slide, 2.28, C_RULE_GREY, 0.9)
    add_line(slide, 2.315, C_RULE_ORANGE, 2.6)
    tb = slide.shapes.add_textbox(emu(0.9), emu(2.55), emu(11.533), emu(1.9))
    pPr = ('<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/>'
           '<a:lnSpc><a:spcPct val="96000"/></a:lnSpc></a:pPr>')
    set_txbody(tb, para(pPr, text_run(title, 36, bold=True, color=C_TITLE,
                                      font=F_TITLE, underline=False)), anchor="ctr")
    add_line(slide, 4.62, C_RULE_ORANGE, 2.6)
    add_line(slide, 4.655, C_RULE_GREY, 0.9)
    if subtitle:
        sb = slide.shapes.add_textbox(emu(1.2), emu(4.85), emu(10.933), emu(0.7))
        set_txbody(sb, para('<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/></a:pPr>',
                            text_run(subtitle, 20, color=C_TERM, italic=True)), anchor="ctr")
    ab = slide.shapes.add_textbox(emu(1.2), emu(5.6), emu(10.933), emu(1.0))
    lines = "".join(
        para('<a:pPr algn="ctr" marL="0" indent="0"><a:buNone/></a:pPr>',
             text_run(t, 16, color=C_FOOT))
        for t in (author, date_s) if t)
    set_txbody(ab, lines, anchor="ctr")
    add_footer(slide, date_s, foot, 1)


def _asset(name: str) -> str:
    return os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", name)
    ).replace("\\", "/")


# A full-bleed designed slide is preferred; the line-art content slide is the fallback.
THANKYOU_SLIDE = _asset("thankyou_slide.png")     # full-bleed branded Thank-You image
THANKYOU_ASSET = _asset("thankyou_lineart.png")   # fallback line-drawing


def ensure_thankyou(slides: "list[Slide]") -> None:
    """Every deck ends with a graphical 'Thank you' slide. When the deck does not
    already end with one, append it: a full-bleed branded image if bundled,
    otherwise a content slide carrying the scientific line-drawing."""
    if any("thank" in (s.title or "").lower() for s in slides):
        return
    s = Slide(title="Recap : **Thank you**")
    if os.path.exists(THANKYOU_SLIDE):
        s.fullbleed_img = THANKYOU_SLIDE          # rendered edge-to-edge, no title/footer
    else:
        if os.path.exists(THANKYOU_ASSET):
            s.blocks.append(Block("fig", THANKYOU_ASSET, width=0.58))
        s.blocks.append(Block("so", "Thank you for your attention. "
                                    "Questions and discussion are welcome."))
    slides.append(s)


def build_fullbleed_slide(prs, img_path: str) -> None:
    """A single image covering the whole slide, with no title bar or footer."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(img_path, 0, 0, SLIDE_W, SLIDE_H)


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="deck mini-language → styled PPTX")
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--foot", default="")
    ap.add_argument("--no-date", action="store_true", help="omit the date from the footer")
    ap.add_argument("--no-page", action="store_true", help="omit the page number from the footer")
    args = ap.parse_args()
    _FOOTER_OPTS["no_date"] = args.no_date
    _FOOTER_OPTS["no_page"] = args.no_page

    slides = parse_deck(args.input)
    ensure_thankyou(slides)
    print(f"build_styled_slides: {args.input}")
    print(f"  parsed slides       : {len(slides)}")

    n_warn = lint_pretext(slides)
    if n_warn:
        print(f"  equation-pretext warnings: {n_warn}")

    tex_list = collect_math(slides)
    print(f"  distinct equations  : {len(tex_list)}")
    omml = build_omml_map(tex_list)
    print(f"  converted to OMML   : {len(omml)}")

    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H
    page = 1
    if args.title:
        build_title_slide(prs, args.title, args.subtitle, args.author, args.date, args.foot)
        page += 1
    for sl in slides:
        if getattr(sl, "fullbleed_img", None):
            build_fullbleed_slide(prs, sl.fullbleed_img)
        elif sl.section:
            build_section_slide(prs, sl, args.date, args.foot, page)
        else:
            build_content_slide(prs, sl, omml, args.date, args.foot, page)
        page += 1
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    prs.save(args.out)

    with zipfile.ZipFile(args.out) as z:
        n_omml = sum(z.read(n).decode("utf-8", "ignore").count("<m:oMath")
                     for n in z.namelist()
                     if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
    print(f"  PPTX                : {args.out}")
    print(f"  slides={page - 1}  OMML equations={n_omml}")


if __name__ == "__main__":
    main()
