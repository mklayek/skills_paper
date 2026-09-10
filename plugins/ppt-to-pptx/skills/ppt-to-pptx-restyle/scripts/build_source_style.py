# -*- coding: utf-8 -*-
"""Mode-B builder: rebuild a PPTX with SOURCE text formatting preserved (two-column).

This is a COMPLETE WORKED EXAMPLE (the "Resistivity Method" deck). Adapt it per deck —
it is not fully generic. What to customise for a new deck:

  * SRC / BASE / TMP / FIG / OVR / ASSETS / OUT / DELIV  -- paths.
  * SCREENSHOT_BODY  -- source slides that are GENUINE figures/diagrams with little/no
                        text (kept as images). {n: (left_img_or_None, [right_imgs])}.
  * RICH_BODY        -- source slides whose text was baked into a TEXT screenshot; re-author
                        the runs here (text, colour, italic[, bold]) so real editable text
                        with the source formatting is produced. NEVER paste the screenshot.
  * TABLE10_* / build_tableNN  -- native rebuild of any TABLE screenshot.
  * titles/keep come from an overrides.txt (=== SLIDE n === / TITLE: / KEEP:) or inline.

Layout = two columns:
  * LEFT  : one tall-narrow text box, source paragraphs copied run-for-run (exact
            font / size / word colour). Full width if the slide has no figure.
  * RIGHT : figures (montaged) and/or native tables (column-width scaled to fit).
Chrome (frame, title bar + rule, footer) is the restyled wrapper. First/Thank-you slides
are spliced as full-bleed images. After building, ALWAYS run the check-agents (see SKILL.md)
and iterate until every slide reports clean — nothing left behind.
"""
import os, re, copy, math
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

SRC   = r"D:/claudecode/TEACHING/ClassNotesPPT_Geophysics_sem3rd/[Class05] Geophysics_Hydrogophysics.pptx"
BASE  = r"D:/claudecode/TEACHING/PPT_class_kr/[UG]_Geophysics_2026/05_Resistivity_method"
TMP   = os.path.join(BASE, "_05_Resistivity_build")   # build folder now nested inside deliverable
FIG   = os.path.join(TMP, "_build", "figures")
OVR   = os.path.join(TMP, "_build", "overrides.txt")
ASSETS= os.path.join(TMP, "assets")
MON   = os.path.join(TMP, "montage"); os.makedirs(MON, exist_ok=True)
OUT   = os.path.join(TMP, "05_Resistivity_Method_2026.pptx")
DELIV = os.path.join(BASE, "05_Resistivity_Method_2026.pptx")   # final copy lands here

EMU = 914400
def IN(v): return Emu(int(v * EMU))

# geometry (inches) on a 16:9 slide
SW_IN, SH_IN = 13.333, 7.5
FR = (0.16, 0.10, 13.01, 7.28)          # frame border
TITLE_BOX = (0.40, 0.16, 12.53, 0.72)
RULE_Y = 0.98
BODY = (0.46, 1.14, 5.55, 5.75)          # LEFT text column (tall > wide)
IMG_REGION = (6.35, 1.22, 6.42, 5.62)    # RIGHT image column
FOOT_Y = 7.02

C_ORANGE = RGBColor(0xE8, 0x71, 0x1C)
C_GREY   = RGBColor(0x9A, 0x9A, 0x9A)
C_TITLE  = RGBColor(0x1A, 0x1A, 0x1A)

# Source slides whose BODY TEXT is baked into screenshot images (no editable text
# in the source .pptx). We paste the screenshot(s) verbatim so the exact source text
# + formatting is preserved. (body_left_image, [right_diagram_images]).
SCREENSHOT_BODY = {
    # Genuine FIGURES (charts / diagrams), not text -> kept as images.
    9:  ("slide09_r01.png", []),                      # resistivity-of-rocks range chart (figure)
    11: (None, ["slide11_r01.png", "slide11_r02.png", "slide11_r03.png"]),  # current-flow diagrams
    # slide 27: heading "VES for groundwater" already in the title bar; the geoelectric
    # cross-section (r01, which already contains the legend) fills the body. r02 is a
    # redundant legend crop -> dropped (its content is inside r01, nothing lost).
    27: (None, ["slide27_r01.png"]),
}

# Slides whose source text was baked into a screenshot image (no editable text in the
# source). We RE-AUTHOR the text as real runs so it lands in an editable text box with
# the source's formatting (colour / italic / arrow). Each paragraph is a list of
# (text, color, italic) runs; color None = black.
BLUE = RGBColor(0x00, 0x00, 0xFF)
RED_BULLET = RGBColor(0xC0, 0x00, 0x00)
RICH_BODY = {
    7: {"right_img": "slide07_r02.jpeg", "paras": [
        [("Resistivity methods employ an artificial source of current →introduced "
          "into the ground through point electrodes", None, False)],
        [("The procedure is to ", None, False), ("measure potentials", BLUE, False),
         (" at other ", None, False), ("electrodes", BLUE, False),
         (" in the vicinity ", None, False), ("of the current flow", BLUE, False),
         (" - ", None, False), ("current is measured as well", None, True), (".", None, False)],
        [("From this, an ", None, False),
         ("effective or apparent resistivity (ρₐ)", None, True),
         (" of the subsurface.", None, False)],
    ]},
    8: {"right_img": None, "paras": [
        [("In the idealized case of a perfectly uniform conducting half-space the current "
          "flow lines resemble a dipole pattern, and the resistivity determined with a "
          "four-electrode configuration is the ", None, False),
         ("true resistivity (ρ)", None, False, True),
         (" of the half-space.", None, False)],
        [("But in real situations the resistivity is determined by different lithologies and "
          "geological structures and so may be very inhomogeneous. This complexity is not "
          "taken into account when measuring resistivity with a four-electrode method, which "
          "assumes that the ground is uniform", None, False)],
        [("Apparent resistivity", None, False, True),
         (" is defined as the resistivity of an electrically homogeneous "
          "and isotropic half-space that would yield the measured relationship between the "
          "applied current and the potential difference for a particular arrangement and "
          "spacing of electrodes.", None, False)],
    ]},
}

# Natural-waters table (src 10) rebuilt natively. (label, value, label_red, value_red)
TABLE10_HEADER = ("Water type", "ρ (Ωm)")
TABLE10_ROWS = [
    ("Precipitation", "30-1000", True, False),
    ("Surface Waters (ign. rock)", "0.1 – 3 × 10³", False, False),
    ("Surface Waters (sed. rock)", "10 – 100", False, False),
    ("Soil waters", "100", False, False),
    ("Natural waters (ign.)", "0.5-150", False, False),
    ("Natural waters (sed.)", "1-100", False, False),
    ("Sea water", "0.2", True, True),
    ("Saline water 3%", "0.15", False, False),
    ("Drinking water (max salt concentration 0.25%)", ">1.8", True, False),
]

# ---------------------------------------------------------------- overrides
def parse_keep(path):
    keep, cur = {}, None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"=== SLIDE (\d+) ===", line.strip())
        if m:
            cur = int(m.group(1)); keep[cur] = []; continue
        if cur and line.startswith("KEEP:"):
            ks = [x.strip() for x in line[5:].split(",") if x.strip()]
            keep[cur] = [k for k in ks if k.lower() != "none"]
    return keep

def parse_titles(path):
    titles, cur = {}, None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"=== SLIDE (\d+) ===", line.strip())
        if m:
            cur = int(m.group(1)); continue
        if cur and line.startswith("TITLE:"):
            titles[cur] = line[6:].strip()
    return titles

def resolve(files):
    out = []
    for k in files:
        p = os.path.join(FIG, os.path.basename(k))
        if os.path.exists(p):
            out.append(p); continue
        stem = os.path.basename(k).split(".")[0]
        for f in sorted(os.listdir(FIG)):
            if f.startswith(stem + "."):
                out.append(os.path.join(FIG, f)); break
    return out

def montage(paths, out, cols):
    ims = [Image.open(p).convert("RGB") for p in paths]
    n = len(ims); rows = math.ceil(n / cols); H = 380
    ims = [im.resize((max(1, int(im.width * H / im.height)), H)) for im in ims]
    colw = max(im.width for im in ims); gap = 20
    sheet = Image.new("RGB", (cols * colw + gap * (cols + 1), rows * H + gap * (rows + 1)), "white")
    for k, im in enumerate(ims):
        r, c = divmod(k, cols)
        sheet.paste(im, (gap + c * (colw + gap) + (colw - im.width) // 2, gap + r * (H + gap)))
    sheet.save(out); return out

def one_image(n, files):
    files = [f for f in files if os.path.exists(f)]
    if not files:
        return None
    if len(files) == 1:
        return files[0]
    cols = 1 if len(files) == 2 else 2
    return montage(files, os.path.join(MON, f"slide{n:02d}.png"), cols)

# ------------------------------------------------------------- source text
FOOT_RE = re.compile(r"^(MKL|Class\s*\d+\s*[–-]\s*(Hydro)?Geophysics|Hydrogeophysics|INTRODUCTION|\d+)$", re.I)
def is_chrome(t):
    t = (t or "").strip()
    return (not t) or bool(FOOT_RE.match(t))

srcpres = Presentation(SRC)

from pptx.enum.shapes import MSO_SHAPE_TYPE

def title_and_body(n):
    s = srcpres.slides[n - 1]
    title = ""
    title_shape = None
    body, tables = [], []
    def walk(shapes):
        nonlocal title, title_shape
        for sh in shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                walk(sh.shapes); continue
            if sh.has_table:
                tables.append(sh); continue
            if sh.name.startswith("Title"):
                if sh.has_text_frame and sh.text_frame.text.strip():
                    title = sh.text_frame.text.strip(); title_shape = sh
                continue
            if not sh.has_text_frame:
                continue
            if is_chrome(sh.text_frame.text):
                continue
            body.append(sh)
    walk(s.shapes)
    body.sort(key=lambda sh: ((sh.top or 0), (sh.left or 0)))
    # A "title" that is actually multi-line / long is real content (e.g. the green+blue
    # case-study heading) -> keep it in the body so nothing is left behind.
    if title_shape is not None and ("\x0b" in title or "\n" in title or len(title) > 45):
        body.insert(0, title_shape)
    return title, body, tables

_CTRL = re.compile(r"[\x0b\x0c\x1e\x1f]")
def copy_clean(p):
    """Deep-copy a source paragraph, replacing stray control chars (vertical tabs used
    as line breaks in some source titles) with a space so they don't show as tofu."""
    pc = copy.deepcopy(p)
    for t in pc.iter(qn('a:t')):
        if t.text:
            t.text = _CTRL.sub(" ", t.text)
    return pc

def images_for(n):
    pre = f"slide{n:02d}_r"
    fs = sorted(f for f in os.listdir(FIG) if f.startswith(pre))
    return [os.path.join(FIG, f) for f in fs]

def copy_table(slide, src_tbl_shape, x, y, w, h):
    """Deep-copy a source table (graphicFrame) into the new slide, repositioned and
    scaled to fit width (column widths scaled so the table never overflows the slide)."""
    gf = copy.deepcopy(src_tbl_shape._element)
    xfrm = gf.find(qn('p:xfrm'))
    if xfrm is not None:
        off = xfrm.find(qn('a:off')); ext = xfrm.find(qn('a:ext'))
        if off is not None:
            off.set('x', str(int(x * EMU))); off.set('y', str(int(y * EMU)))
        if ext is not None:
            ext.set('cx', str(int(w * EMU))); ext.set('cy', str(int(h * EMU)))
    tbl = gf.find('.//' + qn('a:tbl'))
    if tbl is not None:
        grid = tbl.find(qn('a:tblGrid'))
        cols = grid.findall(qn('a:gridCol'))
        native = sum(int(c.get('w')) for c in cols)
        if native > 0:
            sc = int(w * EMU) / native
            for c in cols:
                c.set('w', str(int(int(c.get('w')) * sc)))
    slide.shapes._spTree.append(gf)

# ------------------------------------------------------------- build deck
out = Presentation()
out.slide_width = IN(SW_IN); out.slide_height = IN(SH_IN)
blank = out.slide_layouts[6]

def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=None):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, IN(x), IN(y), IN(w), IN(h))
    sp.shadow.inherit = False
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(line_w or 0.75)
    return sp

def add_text(slide, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT,
             font="Times New Roman", anchor=MSO_ANCHOR.MIDDLE):
    tb = slide.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(2); tf.margin_top = tf.margin_bottom = Pt(1)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = font
    r.font.color.rgb = color
    return tb

def set_normautofit(tf):
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    for tag in ('a:normAutofit', 'a:spAutoFit', 'a:noAutofit'):
        e = bodyPr.find(qn(tag))
        if e is not None:
            bodyPr.remove(e)
    bodyPr.append(bodyPr.makeelement(qn('a:normAutofit'), {}))

def place_fit(slide, img, region):
    rx, ry, rw, rh = region
    with Image.open(img) as im:
        iw, ih = im.size
    aspect = iw / ih
    w = rw; h = w / aspect
    if h > rh:
        h = rh; w = h * aspect
    slide.shapes.add_picture(img, IN(rx + (rw - w) / 2.0), IN(ry + (rh - h) / 2.0), IN(w), IN(h))

def add_rich_body(slide, region, paras, size):
    x, y, w, h = region
    tb = slide.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Pt(3); tf.margin_right = Pt(3); tf.margin_top = Pt(2)
    first = True
    for para in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(10); p.space_before = Pt(2)
        rb = p.add_run(); rb.text = "▪  "
        rb.font.size = Pt(size * 0.72); rb.font.bold = True
        rb.font.color.rgb = RED_BULLET; rb.font.name = "Arial"
        for run in para:
            txt, color, ital = run[0], run[1], run[2]
            bold = run[3] if len(run) > 3 else False
            r = p.add_run(); r.text = txt
            r.font.size = Pt(size); r.font.name = "Times New Roman"
            r.font.italic = ital; r.font.bold = bold
            if color is not None:
                r.font.color.rgb = color
    set_normautofit(tf)
    return tb

def build_table10(slide):
    from pptx.enum.text import PP_ALIGN as _AL
    rows = len(TABLE10_ROWS) + 1
    gf = slide.shapes.add_table(rows, 2, IN(2.7), IN(1.35), IN(7.9), IN(5.3))
    tbl = gf.table
    tbl.columns[0].width = IN(5.7); tbl.columns[1].width = IN(2.2)
    hdr_fill = RGBColor(0x4F, 0x81, 0xBD); band = RGBColor(0xDC, 0xE6, 0xF1)
    def setcell(c, text, *, bold=False, color=None, white=False, fill=None, align=_AL.LEFT, size=15):
        c.margin_left = Pt(5); c.margin_right = Pt(5); c.margin_top = Pt(1); c.margin_bottom = Pt(1)
        if fill is not None:
            c.fill.solid(); c.fill.fore_color.rgb = fill
        else:
            c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p = c.text_frame.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.bold = bold; r.font.name = "Times New Roman"
        if white:
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        elif color is not None:
            r.font.color.rgb = color
        else:
            r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    setcell(tbl.cell(0, 0), TABLE10_HEADER[0], bold=True, white=True, fill=hdr_fill, size=16)
    setcell(tbl.cell(0, 1), TABLE10_HEADER[1], bold=True, white=True, fill=hdr_fill, align=_AL.CENTER, size=16)
    RED = RGBColor(0xFF, 0x00, 0x00)
    for i, (lab, val, lab_red, val_red) in enumerate(TABLE10_ROWS, start=1):
        f = band if i % 2 else RGBColor(0xFF, 0xFF, 0xFF)
        setcell(tbl.cell(i, 0), lab, color=(RED if lab_red else None), fill=f)
        setcell(tbl.cell(i, 1), val, color=(RED if val_red else None), fill=f, align=_AL.CENTER)

def make_slide(n, title_text, keep):
    s = out.slides.add_slide(blank)
    _, body_shapes, tables = title_and_body(n)
    # chrome: frame
    add_rect(s, *FR, fill=None, line=C_GREY, line_w=0.75)
    # title bar (clean curated header text = chrome; body below stays source-formatted)
    tb = add_text(s, *TITLE_BOX, title_text, 24, C_TITLE, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb.text_frame.paragraphs[0].runs[0].font.underline = True
    set_normautofit(tb.text_frame)
    # double rule under title
    add_rect(s, 0.30, RULE_Y, 12.73, 0.012, fill=C_GREY)
    add_rect(s, 0.30, RULE_Y + 0.03, 12.73, 0.028, fill=C_ORANGE)
    # footer
    add_text(s, 0.45, FOOT_Y, 3.4, 0.30, "September 2026", 11, C_GREY, align=PP_ALIGN.LEFT)
    add_text(s, 4.2, FOOT_Y, 4.9, 0.30, "Class 05 — Resistivity Method", 11, C_GREY, align=PP_ALIGN.CENTER)
    add_text(s, 9.9, FOOT_Y, 3.0, 0.30, str(n - 2), 11, C_GREY, align=PP_ALIGN.RIGHT)

    # ---- re-authored formatted text (source text was a screenshot; now real runs) ----
    if n in RICH_BODY:
        spec = RICH_BODY[n]
        rimg = spec.get("right_img")
        if rimg:
            add_rich_body(s, (0.46, 1.16, 6.15, 5.66), spec["paras"], size=21)
            place_fit(s, resolve([rimg])[0], (6.75, 1.35, 6.05, 5.30))
        else:
            add_rich_body(s, (0.70, 1.20, 11.9, 5.62), spec["paras"], size=24)
        return 0

    # ---- native rebuilt table (src 10 natural-waters), no screenshot ----
    if n == 10:
        build_table10(s)
        return 0

    # ---- screenshot-body slides: genuine figures/diagrams kept as images ----
    if n in SCREENSHOT_BODY:
        left_name, right_names = SCREENSHOT_BODY[n]
        left = resolve([left_name])[0] if left_name else None
        rights = resolve(right_names)
        if left and rights:                       # text-shot LEFT, diagram(s) RIGHT
            place_fit(s, left, (0.46, 1.22, 5.55, 5.58))
            rimg = one_image(n, rights)
            place_fit(s, rimg, (6.30, 1.22, 6.50, 5.58))
        elif left:                                # text-shot fills the body (wide, readable)
            place_fit(s, left, (1.20, 1.22, 10.9, 5.60))
        elif rights:                              # figure-only slide -> montage fills body
            place_fit(s, one_image(n, rights), (0.60, 1.22, 12.1, 5.60))
        return 0

    # ALL embedded images for this slide (nothing left behind), and any tables.
    imgs = images_for(n)
    have_tbl = bool(tables)
    text_len = sum(len(sh.text_frame.text.strip()) for sh in body_shapes)

    # No real body text (content is entirely an image/table) -> fill the body.
    if text_len < 5:
        if imgs:
            place_fit(s, one_image(n, imgs), (0.60, 1.24, 12.1, 5.58))
        if have_tbl:
            copy_table(s, tables[0], 1.60, 1.35, 10.1, 5.30)
        return 0

    # LEFT body: one text box, source paragraphs copied run-for-run (exact formatting)
    bx, by, bw, bh = BODY
    if not imgs and not have_tbl:
        bw = 12.41                        # text-only -> full width
    elif have_tbl and not imgs:
        bw = 3.9                          # narrow text, table takes the rest
    box = s.shapes.add_textbox(IN(bx), IN(by), IN(bw), IN(bh))
    tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Pt(3); tf.margin_right = Pt(3); tf.margin_top = Pt(2)
    dst = tf._txBody
    for p in dst.findall(qn('a:p')):      # drop default empty paragraph
        dst.remove(p)
    ncopied = 0
    for sh in body_shapes:
        for p in sh.text_frame._txBody.findall(qn('a:p')):
            dst.append(copy_clean(p))
            ncopied += 1
    set_normautofit(tf)

    # RIGHT: images (montaged if several)
    if imgs:
        place_fit(s, one_image(n, imgs), IMG_REGION)

    # RIGHT: tables (deep-copied + column-scaled, exact formatting)
    if have_tbl:
        if imgs:
            copy_table(s, tables[0], 4.6, 4.30, 8.2, 2.55)   # below images (rare)
        else:
            copy_table(s, tables[0], 4.55, 1.40, 8.25, 5.25)
    return ncopied

keep = parse_keep(OVR)
titles = parse_titles(OVR)
total = 0
for n in range(4, 35):
    total += make_slide(n, titles.get(n, "Resistivity Method"), keep.get(n, []))

# ---- splice intro title (front) + thank-you (end), full-bleed ----
def fullbleed(img):
    sl = out.slides.add_slide(blank)
    sl.shapes.add_picture(img, 0, 0, out.slide_width, out.slide_height)
    return sl

fullbleed(os.path.join(ASSETS, "intro_thankyou.png"))          # append at end
title_slide = fullbleed(os.path.join(ASSETS, "intro_title.png"))
# move title slide to front
lst = out.slides._sldIdLst
lst.insert(0, lst[-1])

out.save(OUT)
import shutil
shutil.copyfile(OUT, DELIV)
print("saved", OUT, "| content slides 4-34:", 31, "| paragraphs copied:", total,
      "| total slides:", len(out.slides._sldIdLst))
print("copied final ->", DELIV)
