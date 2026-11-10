"""explain-slide-pptx: infographic "explain" slides (png-explain style) as native, editable PPTX.

Usage:  python explain_slides.py <spec.py>          (the spec file defines DECK, see SKILL.md)

Every slide: border, bold title with one highlighted word, gray subtitle between rules, an optional
full-width intro strip, then 1 to 4 panels (header pill, definition, figure + credit, equation box,
symbol list, Key points and Example boxes). Text, boxes and pills are native shapes, equations are
native PowerPoint equations (LaTeX -> OMML through pandoc), only figures are images.
Colors come from palettes.py, cycling per slide or set per slide. Text heights are measured with the
Windows fonts, the layout flows top-down, and any box that would overflow is reported.
"""
import importlib.util, io, os, re, shutil, subprocess, sys, tempfile, zipfile

from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import palettes

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
SANS, MATHF = "Arial", "Times New Roman"
FONTS = r"C:\Windows\Fonts"
SIZES = {"title": 28, "subtitle": 12, "head": 14, "intro_head": 15, "body": 14, "small": 13, "sym": 13,
         "eq": 16, "pill_small": 11.5, "credit": 8.5}
SW, SH = 13.333, 7.5
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WARN = []


# ------------------------------------------------------------------ measuring --
_fonts = {}


def font(bold=False, italic=False, math=False, size=14):
    name = ("timesi.ttf" if math else "arialbd.ttf" if bold else "arial.ttf")
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONTS, name), max(1, round(size * 10)))
    return _fonts[key]


def plain(t):
    """Markup -> plain text (for measuring and Markdown)."""
    t = re.sub(r"[_^]\{([^}]*)\}", r"\1", t)
    return t.replace("**", "").replace("$", "")


def text_width(t, size, bold=False):
    """Width in inches of a plain string (font rendered at 10x for precision)."""
    return font(bold, size=size).getlength(t) / 10 / 72


def lines_of(t, size, width, bold=False):
    words, n, cur = plain(t).split(), 1, ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, size, bold) > width and cur:
            n, cur = n + 1, w
        else:
            cur = trial
    return n


def height_of(paras, size, width, space_after=2):
    """Height (in) of a list of paragraphs at size pt in a box of width (in), 1.2 line spacing."""
    lines = sum(lines_of(p, size, width) for p in paras)
    return lines * size * 1.2 / 72 + len(paras) * space_after / 72 + 0.06


# ------------------------------------------------------------------- equations --
def latex_to_omml(latexes, size_pt, color):
    """List of LaTeX strings -> list of <m:oMath> xml strings (pandoc docx writer)."""
    tmp = tempfile.mkdtemp(prefix="explain_eq_")
    md = "\n\n".join(f"EQMARK{i}\n\n$${l}$$" for i, l in enumerate(latexes)) + "\n"
    io.open(os.path.join(tmp, "e.md"), "w", encoding="utf-8").write(md)
    subprocess.run(["pandoc", "e.md", "-f", "markdown", "-o", "e.docx"], cwd=tmp, check=True)
    doc = etree.fromstring(zipfile.ZipFile(os.path.join(tmp, "e.docx")).read("word/document.xml"))
    shutil.rmtree(tmp, ignore_errors=True)
    out, cur = {}, None
    for p in doc.iter(f"{{{W_NS}}}p"):
        txt = "".join(p.itertext()).strip()
        oms = p.findall(f".//{{{M_NS}}}oMath")
        if not oms and txt.startswith("EQMARK"):
            cur = int(txt[6:]); continue
        if oms and cur is not None:
            om = oms[0]
            for wr in list(om.iter(f"{{{W_NS}}}rPr")):
                wr.getparent().remove(wr)
            for r in om.iter(f"{{{M_NS}}}r"):
                sty = r.find(f"{{{M_NS}}}rPr/{{{M_NS}}}sty")
                v = sty.get(f"{{{M_NS}}}val") if sty is not None else "i"
                t = r.find(f"{{{M_NS}}}t")
                r.insert(list(r).index(t), _arpr(size_pt, color, v in ("i", "bi"), v in ("b", "bi")))
            for c in om.iter(f"{{{M_NS}}}ctrlPr"):
                for k in list(c):
                    c.remove(k)
                c.append(_arpr(size_pt, color, True, False))
            out[cur] = re.sub(r' xmlns:\w+="[^"]+"', "", etree.tostring(om, encoding="unicode"))
            cur = None
    missing = [latexes[i] for i in range(len(latexes)) if i not in out]
    if missing:
        WARN.append(f"pandoc could not convert: {missing}")
    return [out.get(i) for i in range(len(latexes))]


def _arpr(size_pt, color, italic, bold):
    return etree.fromstring(
        f'<a:rPr xmlns:a="{A_NS}" lang="en-US" sz="{int(size_pt * 100)}" b="{int(bold)}" i="{int(italic)}">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Cambria Math"/></a:rPr>')


def eq_height(latexes, size_pt):
    h = sum((0.47 if re.search(r"\\frac|\\dfrac|\\sum|\\int|\\sqrt", l) else 0.32) for l in latexes)
    return h * size_pt / 16 + 0.14


# --------------------------------------------------------------------- shapes --
class Painter:
    def __init__(self, slide, pal, sizes, label):
        self.s, self.pal, self.z, self.label = slide, pal, sizes, label

    def rgb(self, h):
        return RGBColor.from_string(h)

    def box(self, x, y, w, h, color, lw=1.3, radius=0.06, fill=None):
        sh = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.adjustments[0] = radius
        sh.fill.solid(); sh.fill.fore_color.rgb = self.rgb(fill or "FFFFFF")
        sh.line.color.rgb = self.rgb(color); sh.line.width = Pt(lw); sh.shadow.inherit = False
        return sh

    def boxfill(self, color):
        return palettes.tint(color) if self.pal["fill"] == "tint" else "FFFFFF"

    def pill(self, cx, cy, text, color, size, icon=None, left=None, max_w=None):
        label = (icon + "  " if icon else "") + text.upper()
        w = text_width(text.upper(), size, True) + (0.3 if icon else 0) + 0.32
        if max_w and w > max_w:
            if text_width(text.upper(), size, True) + (0.3 if icon else 0) > max_w:
                WARN.append(f"{self.label}: pill '{text}' wider than its box, use a shorter title")
            w = max_w
        x = left if left is not None else cx - w / 2
        h = 0.30 * size / 13
        sh = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(cy - h / 2), Inches(w), Inches(h))
        sh.adjustments[0] = 0.18
        sh.fill.solid(); sh.fill.fore_color.rgb = self.rgb(color); sh.line.fill.background(); sh.shadow.inherit = False
        tf = sh.text_frame; tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = False
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        if icon:
            r = p.add_run(); r.text = icon + "  "; r.font.name = "Segoe UI Symbol"; r.font.size = Pt(size - 1)
            r.font.color.rgb = self.rgb("FFFFFF")
        r = p.add_run(); r.text = text.upper(); r.font.name = SANS; r.font.bold = True; r.font.size = Pt(size)
        r.font.color.rgb = self.rgb("FFFFFF")

    def textbox(self, x, y, w, h, anchor=MSO_ANCHOR.TOP):
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(0.03); tf.margin_top = tf.margin_bottom = Inches(0.02)
        return tf

    def rich(self, p, text, size, hl, align=None):
        """**key phrase** -> bold in hl color, $math$ -> Times italic, _{sub} ^{sup} anywhere."""
        if align is not None:
            p.alignment = align
        for seg in re.split(r"(\*\*.+?\*\*|\$.+?\$)", text):
            if not seg:
                continue
            kind = "kw" if seg.startswith("**") else "math" if seg.startswith("$") else "plain"
            body = seg[2:-2] if kind == "kw" else seg[1:-1] if kind == "math" else seg
            for part in re.split(r"([_^]\{[^}]*\})", body):
                if not part:
                    continue
                r = p.add_run()
                script = part[:2] in ("_{", "^{")
                txt = part[2:-1] if script else part
                r.text = txt
                r.font.size = Pt(size)
                word_script = script and len(txt) > 2          # e.g. _{enc}, _{eff}: upright sans
                r.font.name = MATHF if kind == "math" and not word_script else SANS
                r.font.italic = kind == "math" and not word_script
                r.font.bold = kind == "kw"
                r.font.color.rgb = self.rgb(hl if kind == "kw" else self.pal["text"])
                if script:
                    r._r.get_or_add_rPr().set("baseline", "-25000" if part[0] == "_" else "30000")

    def bullets(self, tf, items, size, color, first=True):
        for i, t in enumerate(items):
            p = tf.paragraphs[0] if first and i == 0 else tf.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(int(Inches(0.2)))); pPr.set("indent", str(int(-Inches(0.17))))
            buClr = pPr.makeelement(qn("a:buClr"), {})
            buClr.append(buClr.makeelement(qn("a:srgbClr"), {"val": color})); pPr.append(buClr)
            pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": SANS}))
            pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "•"}))
            p.space_after = Pt(2)
            self.rich(p, t, size, color)

    def picture(self, path, x, y, w, h, credit=None):
        iw, ih = Image.open(path).size
        ch = 0.2 if credit else 0
        sc = min(w / iw, (h - ch) / ih)
        pw, ph = iw * sc, ih * sc
        px, py = x + (w - pw) / 2, y + (h - ch - ph) / 2
        self.s.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))
        if credit:
            p = self.textbox(x, py + ph, w, 0.2).paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = credit; r.font.size = Pt(self.z["credit"]); r.font.italic = True
            r.font.name = SANS; r.font.color.rgb = self.rgb(self.pal["subtitle"])

    def symbols(self, rows, x, y, w, color):
        tf = self.textbox(x, y, w, 0.3 * len(rows))
        for i, (a, b) in enumerate(rows):
            self.rich(tf.paragraphs[0] if i == 0 else tf.add_paragraph(), a + " : " + b, self.z["sym"], color)

    def equation(self, omml_lines, x, y, w, h, color):
        self.box(x, y, w, h, color, lw=1.0, radius=0.08, fill=self.boxfill(color))
        tf = self.textbox(x + 0.04, y + 0.03, w - 0.08, h - 0.06, anchor=MSO_ANCHOR.MIDDLE)
        body = tf._txBody
        for p in list(body.findall(qn("a:p"))):
            body.remove(p)
        for om in omml_lines:
            body.append(etree.fromstring(
                f'<a:p xmlns:a="{A_NS}"><a:pPr algn="ctr"/><mc:AlternateContent '
                f'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
                f'<mc:Choice xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" Requires="a14">'
                f'<a14:m><m:oMathPara xmlns:m="{M_NS}"><m:oMathParaPr><m:jc m:val="centerGroup"/></m:oMathParaPr>'
                f'{om}</m:oMathPara></a14:m></mc:Choice><mc:Fallback><a:r><a:rPr lang="en-US"/><a:t>[equation]</a:t>'
                f'</a:r></mc:Fallback></mc:AlternateContent></a:p>'))

    def small_box(self, x, y, w, h, color, icon, title, items):
        self.box(x, y, w, h, color, lw=0.9, radius=0.07, fill=self.boxfill(color))
        self.pill(0, y + 0.2, title, color, self.z["pill_small"], icon=icon, left=x + 0.1, max_w=w - 0.2)
        self.bullets(self.textbox(x + 0.08, y + 0.36, w - 0.14, h - 0.4), items, self.z["small"], color)


# ---------------------------------------------------------------------- figures --
def figure_path(fig, work):
    """{"image": path} or {"tikz": code}; TikZ is compiled to PNG in the work folder."""
    if "image" in fig:
        return fig["image"]
    name = "tikz_%08x" % (abs(hash(fig["tikz"])) & 0xFFFFFFFF)
    tex = (r"\documentclass[border=3pt]{standalone}\usepackage{amsmath,tikz}"
           r"\usetikzlibrary{arrows.meta,decorations.pathreplacing,calc}\usepackage[T1]{fontenc}"
           r"\usepackage[scaled=0.96]{helvet}\begin{document}\fontsize{14}{16}\selectfont" + fig["tikz"] + r"\end{document}")
    io.open(os.path.join(work, name + ".tex"), "w", encoding="utf-8").write(tex)
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", name + ".tex"], cwd=work, capture_output=True,
                       text=True, errors="replace")
    if r.returncode:
        sys.exit(f"❌ TikZ figure failed:\n{r.stdout[-1500:]}")
    subprocess.run(["pdftoppm", "-r", "400", "-png", "-singlefile", name + ".pdf", name], cwd=work, check=True)
    return os.path.join(work, name + ".png")


# ------------------------------------------------------------------------ slide --
ICON_KEY, ICON_BULB = "\U0001F511", "\U0001F4A1"


def build_slide(prs, sd, pal, z, work, idx):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    P = Painter(sl, pal, z, f"slide {idx}")
    P.box(0.1, 0.1, SW - 0.2, SH - 0.2, pal["frame"], lw=2.6, radius=0.015).name = "Page border"
    # title + subtitle
    p = P.textbox(0.5, 0.33, SW - 1.0, 0.55).paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    t, hl = sd["title"], sd.get("highlight", "")
    parts = t.split(hl, 1) if hl and hl in t else [t]
    for i, seg in enumerate([parts[0], hl, parts[1]] if len(parts) == 2 else parts):
        if not seg:
            continue
        r = p.add_run(); r.text = seg; r.font.name = SANS; r.font.bold = True; r.font.size = Pt(z["title"])
        r.font.color.rgb = P.rgb(pal["title_hl"] if (len(parts) == 2 and i == 1) else pal["text"])
    if sd.get("subtitle"):
        p = P.textbox(1.0, 0.83, SW - 2.0, 0.3).paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = "———————   " + sd["subtitle"].upper() + "   ———————"
        r.font.name = SANS; r.font.size = Pt(z["subtitle"]); r.font.color.rgb = P.rgb(pal["subtitle"])
    top = 1.33
    if sd.get("intro"):
        top = intro(P, sd["intro"], top, z, work) + 0.25
    panels = sd.get("panels", [])
    if panels:
        n = len(panels); gap = 0.26; pw = (SW - 0.54 - gap * (n - 1)) / n
        for k, pn in enumerate(panels):
            panel(P, pn, 0.27 + k * (pw + gap), top, pw, SH - 0.22 - top, k, z, work)


def intro(P, it, y0, z, work):
    c = it.get("color") or P.pal["intro"]
    has_fig, has_eq = bool(it.get("figure")), bool(it.get("equation"))
    wf = 2.6 if has_fig else 0
    we = 3.5 if has_eq else 0
    x0, W = 0.27, SW - 0.54
    tw = W - 0.26 - (wf + 0.12 if has_fig else 0) - (we + 0.2 if has_eq else 0)
    paras = [it["definition"]] + it.get("points", [])
    th = height_of(paras, z["body"], tw - 0.25)
    eqs = it.get("equation") or []
    eqs = [eqs] if isinstance(eqs, str) else eqs
    eh = eq_height(eqs, z["eq"]) if has_eq else 0
    sh = len(it.get("symbols", [])) * z["sym"] * 1.25 / 72
    h0 = max(th, eh + 0.1 + sh, 1.2 if has_fig else 0) + 0.38
    P.box(x0, y0, W, h0, c, radius=0.05, fill=P.boxfill(c))
    x = x0 + 0.13
    if has_fig:
        P.picture(figure_path(it["figure"], work), x, y0 + 0.25, wf, h0 - 0.35, it["figure"].get("credit"))
        x += wf + 0.12
    tf = P.textbox(x, y0 + 0.22, tw, h0 - 0.25)
    P.rich(tf.paragraphs[0], it["definition"], z["body"], c); tf.paragraphs[0].space_after = Pt(4)
    P.bullets(tf, it.get("points", []), z["body"], c, first=False)
    if has_eq:
        ex = x0 + W - we - 0.13
        P.equation(latex_to_omml(eqs, z["eq"], P.pal["text"]), ex, y0 + 0.25, we, eh, c)
        P.symbols(it.get("symbols", []), ex - 0.05, y0 + 0.3 + eh, we + 0.1, c)
    P.pill(x0 + W / 2, y0, it.get("head", ""), c, z["intro_head"])
    return y0 + h0


def panel(P, pn, x, y, pw, ph, k, z, work):
    c = pn.get("color") or P.pal["panels"][k % len(P.pal["panels"])]
    exc = pn.get("example_color") or P.pal["examples"][k % len(P.pal["examples"])]
    P.box(x, y, pw, ph, c, radius=0.04, fill=P.boxfill(c) if P.pal["fill"] == "tint" else None)
    iw = pw - 0.24
    dh = height_of([pn["definition"]], z["body"], iw - 0.06, 0)
    P.rich(P.textbox(x + 0.12, y + 0.2, iw, dh).paragraphs[0], pn["definition"], z["body"], c)
    # bottom boxes: height from the longer list
    stacked = pw < 3.4
    bw = iw if stacked else (iw - 0.12) / 2
    kh = height_of(pn.get("points", []), z["small"], bw - 0.4) + 0.42
    xh = height_of(pn.get("example", []), z["small"], bw - 0.4) + 0.42 if pn.get("example") else 0
    bh = max(kh, xh)
    boxes_h = (kh + xh + 0.1) if stacked else bh
    by = y + ph - 0.1 - boxes_h
    if pn.get("points"):
        P.small_box(x + 0.12, by, bw, kh if stacked else bh, c, ICON_KEY, pn.get("points_title", "Key points"), pn["points"])
    if pn.get("example"):
        ex, ey = (x + 0.12, by + kh + 0.1) if stacked else (x + 0.24 + bw, by)
        P.small_box(ex, ey, bw, xh if stacked else bh, exc, ICON_BULB, pn.get("example_title", "Example"), pn["example"])
    # middle row: figure | equation + symbols
    my = y + 0.2 + dh + 0.08
    mh = by - 0.1 - my
    eqs = pn.get("equation") or []
    eqs = [eqs] if isinstance(eqs, str) else eqs
    eh = eq_height(eqs, z["eq"]) if eqs else 0
    rows = pn.get("symbols", [])
    frac = pn.get("figure_width", 0.52) if pn.get("figure") else 0
    ew = iw * (1 - frac) - (0.1 if frac else 0)
    sh = height_of([a + " : " + b for a, b in rows], z["sym"], ew, 0) if rows else 0
    need = eh + (0.08 + sh if rows else 0)
    sym_left = bool(rows and frac and need > mh)        # no room beside: symbols go under the figure
    if sym_left:
        sh = height_of([a + " : " + b for a, b in rows], z["sym"], iw * frac, 0)
        need = eh
    if need > mh + 0.02 or (sym_left and sh + 0.6 > mh):
        WARN.append(f"{P.label} panel '{pn['head']}': equation/symbols do not fit ({mh:.2f} in free), shorten the text")
    if mh < 0.6:
        WARN.append(f"{P.label} panel '{pn['head']}': only {mh:.2f} in left for the figure, shorten the text")
    if pn.get("figure"):
        fh = mh - (sh + 0.04 if sym_left else 0)
        P.picture(figure_path(pn["figure"], work), x + 0.12, my, iw * frac, fh, pn["figure"].get("credit"))
        if sym_left:
            P.symbols(rows, x + 0.1, my + fh + 0.02, iw * frac, c)
    ex = x + 0.12 + iw * frac + (0.1 if frac else 0)
    ey = my + max(0, (mh - need) / 2)
    if eqs:
        P.equation(latex_to_omml(eqs, z["eq"], P.pal["text"]), ex, ey, ew, eh, c)
    if rows and not sym_left:
        P.symbols(rows, ex - 0.05, ey + eh + 0.06, ew + 0.1, c)
    P.pill(x + pw / 2, y, pn["head"], c, z["head"])


# ---------------------------------------------------------------------- deck --
def resolve_palettes(deck):
    choice = deck.get("palettes", "cycle")
    seq = palettes.CYCLE if choice == "cycle" else ([choice] if isinstance(choice, str) else list(choice))
    out = []
    for i, sd in enumerate(deck["slides"]):
        name = sd.get("palette") or seq[i % len(seq)]
        pal = palettes.get(name)
        if sd.get("fill") or deck.get("fill"):
            pal["fill"] = sd.get("fill") or deck.get("fill")
        if sd.get("text_color"):
            pal["text"] = sd["text_color"]
        out.append((name, pal))
    return out


def write_md(deck, pals, path):
    md = []
    for (name, _), sd in zip(pals, deck["slides"]):
        md += [f"# {sd['title']}", "", f"_{sd.get('subtitle', '')}_  (palette: {name})", ""]
        blocks = ([sd["intro"]] if sd.get("intro") else []) + sd.get("panels", [])
        for b in blocks:
            md += [f"## {b.get('head', '')}", "", plain(b["definition"]), ""]
            md += [f"- {plain(t)}" for t in b.get("points", [])]
            eqs = b.get("equation") or []
            for e in ([eqs] if isinstance(eqs, str) else eqs):
                md += ["", f"$${e}$$"]
            md += [f"- {plain(a)}: {plain(s)}" for a, s in b.get("symbols", [])]
            if b.get("example"):
                md += ["", f"**{b.get('example_title', 'Example')}**", ""] + [f"- {plain(t)}" for t in b["example"]]
            fig = b.get("figure") or {}
            if fig.get("image"):
                rel = os.path.relpath(fig["image"], os.path.dirname(path)).replace("\\", "/")
                md += ["", f"![{os.path.basename(fig['image'])}]({rel})  _{fig.get('credit', '')}_"]
            md += [""]
        md += ["---", ""]
    io.open(path, "w", encoding="utf-8").write("\n".join(md))


def build(deck):
    z = dict(SIZES); z.update(deck.get("sizes", {}))
    out = deck["output"]
    work = deck.get("work") or os.path.join(os.path.dirname(out), "temp", "build_explain_slides")
    os.makedirs(work, exist_ok=True)
    pals = resolve_palettes(deck)
    print(f"▶️  Building {len(deck['slides'])} explain slide(s) -> {out}")
    prs = Presentation(); prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
    for i, ((name, pal), sd) in enumerate(zip(pals, deck["slides"]), 1):
        print(f"🎨 slide {i}: '{sd['title']}' with palette '{name}' ({pal['fill']})")
        build_slide(prs, sd, pal, z, work, i)
    prs.save(out)
    print(f"✅ PPTX: {out}")
    if deck.get("md"):
        os.makedirs(os.path.dirname(deck["md"]), exist_ok=True)
        write_md(deck, pals, deck["md"]); print(f"📝 Markdown copy: {deck['md']}")
    for w in WARN:
        print("⚠️  " + w)
    print("✅ no fit warnings" if not WARN else f"⚠️  {len(WARN)} fit warning(s): shorten text or use fewer panels")
    return 0 if not WARN else 2


def load_spec(path):
    spec = importlib.util.spec_from_file_location("explain_spec", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.DECK


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python explain_slides.py <spec.py>")
    sys.exit(build(load_spec(sys.argv[1])))
