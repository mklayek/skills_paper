# -*- coding: utf-8 -*-
"""aloud-notes-ppt, step 3: sections/*.md -> master Markdown -> LaTeX (XeLaTeX, Latin Modern) -> PDF, then checks.

Reads <task_folder>/docs/notes_config.json:
  name            output base name (PDF at the top of the task folder, master MD in docs/)
  title, subtitle, author, affiliation (list of lines), year
  skip            slide numbers with no paragraph (title, section dividers, closing slide)
  parts           {"<first slide of a part>": "<part heading>"}  (the deck's section names)
  fontsize        10, 11 or 12 (pt)
  words           [min, max] words per paragraph, display equations not counted
  insight_words   [min, max] words of the optional second paragraph "**Insight:** ..." (default [15, 45])
  max_pages       0 = no limit
  slides_per_page [min, max], [0, 0] = no check
  margin_cm       page margin, default 1.0

Checks: one block per content slide, exactly one paragraph per block, word range, no em dash, no semicolon
outside math, 0 missing glyphs, 0 overfull lines, page count and slides per page.
Layout: A4, two columns, Latin Modern, navy part headings, blue slide headings, no header,
page number alone in the bottom-right corner.

Usage:  python build_notes.py <task_folder>
"""
import glob, io, json, os, re, shutil, subprocess, sys

import pymupdf as fitz

sys.stdout = io.open(1, "w", encoding="utf-8", closefd=False)
if len(sys.argv) != 2:
    sys.exit("usage: python build_notes.py <task_folder>")
ROOT = os.path.abspath(sys.argv[1])
EXT, BUILD, DOCS = (os.path.join(ROOT, "temp", "extract"), os.path.join(ROOT, "temp", "build"),
                    os.path.join(ROOT, "docs"))
os.makedirs(BUILD, exist_ok=True)
C = json.load(io.open(os.path.join(DOCS, "notes_config.json"), encoding="utf-8"))
NAME, SKIP = C["name"], set(C.get("skip", []))
PARTS = {int(k): v for k, v in C.get("parts", {}).items()}
WMIN, WMAX = C.get("words", [85, 140])
IMIN, IMAX = C.get("insight_words", [15, 45])
slides = json.load(io.open(os.path.join(EXT, "slides.json"), encoding="utf-8"))
content = [s["n"] for s in slides if s["n"] not in SKIP]
problems = 0

# ------------------------------------------------------------- collect blocks --
text = ""
for f in sorted(glob.glob(os.path.join(glob.escape(ROOT), "sections", "*.md"))):
    text += io.open(f, encoding="utf-8").read().strip() + "\n\n"
blocks = {int(re.match(r"## Slide (\d+)", b).group(1)): b.strip()
          for b in re.split(r"(?m)^(?=## Slide \d+)", text) if b.startswith("## Slide")}
missing = [n for n in content if n not in blocks]
extra = [n for n in blocks if n not in content]
print(f"🔍 {len(blocks)} slide blocks for {len(content)} content slides"
      + (f", ❌ missing {missing}" if missing else ", ✅ none missing") + (f", ⚠️ not expected {extra}" if extra else ""))
problems += len(missing)
MATH = r"\$\$[\s\S]*?\$\$|\$[^$]*\$"
n_ins = 0
for n, b in sorted(blocks.items()):
    paras = [p for p in b.split("\n\n")[1:] if p.strip()]
    ins = [p for p in paras if p.lstrip().startswith("**Insight:**")]      # optional second paragraph
    main = [p for p in paras if not p.lstrip().startswith("**Insight:**")]
    words = len(re.sub(MATH, "x", " ".join(main)).split())
    body = re.sub(MATH, "", b)
    msg = []
    if len(main) != 1: msg.append(f"{len(main)} paragraphs")
    if not WMIN <= words <= WMAX: msg.append(f"{words} words")
    if len(ins) > 1: msg.append(f"{len(ins)} insights")
    if ins and not paras[-1].lstrip().startswith("**Insight:**"): msg.append("insight not after the paragraph")
    if ins:
        iw = len(re.sub(MATH, "x", ins[0]).split()) - 1
        n_ins += 1
        if not IMIN <= iw <= IMAX: msg.append(f"insight {iw} words")
    if "—" in body: msg.append("em dash")
    if ";" in body: msg.append("semicolon")
    if re.search(r"\*\*(What to say|How to explain|Findings|Significance)", b): msg.append("label")
    if msg:
        problems += 1; print(f"⚠️  slide {n}: " + ", ".join(msg))

print(f"💡 {n_ins} of {len(blocks)} slides carry an Insight paragraph")

# ----------------------------------------------------------------- master MD --
date = "".join(f"  {l}\\\n" for l in C.get("affiliation", [])) + f"  {C.get('year', '')}"
md = ["---", f'title: "{C["title"]}"', f'subtitle: "{C.get("subtitle", "")}"', f'author: "{C.get("author", "")}"',
      "date: |", date, "---", ""]
for n in content:
    if n in PARTS: md += [f"# {PARTS[n]}", ""]
    b = blocks.get(n, f"## Slide {n:02d}\n\n(notes missing)")
    head, rest = b.split("\n", 1)
    md += [head, "", rest.strip(), ""]
mdp = os.path.join(DOCS, NAME + ".md")
io.open(mdp, "w", encoding="utf-8").write("\n".join(md))
print(f"📝 master Markdown: {mdp}")

# ------------------------------------------------------------------ LaTeX --
hdr = os.path.join(BUILD, "header.tex")
io.open(hdr, "w", encoding="utf-8").write(r"""
\usepackage{needspace}
\usepackage{newunicodechar}
\pagestyle{empty}\makeatletter\let\ps@plain\ps@empty\makeatother
\usepackage{eso-pic}\AddToShipoutPictureFG{\AtPageLowerLeft{\put(\LenToUnit{\paperwidth-0.7cm},\LenToUnit{0.45cm}){\makebox[0pt][r]{\normalfont\small\color{black}\thepage}}}}
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries\color[HTML]{0B2A55}}{}{0pt}{}[\titlerule]
\titleformat{\subsection}{\normalsize\bfseries\color[HTML]{1D4ED8}}{}{0pt}{\Needspace{5\baselineskip}}
\titlespacing*{\section}{0pt}{4pt}{1pt}\titlespacing*{\subsection}{0pt}{3pt}{0pt}
\setlength{\parindent}{0pt}\raggedbottom\setlength{\abovedisplayskip}{4pt}\setlength{\belowdisplayskip}{4pt}
\setcounter{secnumdepth}{0}
\setlength{\parskip}{1.5pt}
""" + "\n".join(rf"\newunicodechar{{{c}}}{{\ensuremath{{{m}}}}}" for c, m in [
    # text-mode Greek and relation glyphs only. Never map big operators (integral, partial, sum, infinity,
    # square root): with unicode-math that recurses forever and XeLaTeX hangs.
    ("ρ", r"\rho"), ("σ", r"\sigma"), ("φ", r"\phi"), ("ω", r"\omega"), ("τ", r"\tau"), ("μ", r"\mu"), ("Ω", r"\Omega"),
    ("Δ", r"\Delta"), ("θ", r"\theta"), ("α", r"\alpha"), ("β", r"\beta"), ("γ", r"\gamma"), ("δ", r"\delta"),
    ("ε", r"\varepsilon"), ("λ", r"\lambda"), ("π", r"\pi"), ("≈", r"\approx"), ("≤", r"\leq"), ("≥", r"\geq"),
    ("±", r"\pm"), ("×", r"\times"), ("·", r"\cdot"), ("→", r"\rightarrow"), ("←", r"\leftarrow"), ("∝", r"\propto"),
    ("−", r"-"), ("≫", r"\gg"), ("≪", r"\ll"), ("⁻", r"^{-}"), ("¹", r"^{1}"), ("²", r"^{2}"), ("³", r"^{3}"),
    ("⁴", r"^{4}"), ("⁵", r"^{5}"), ("⁶", r"^{6}"), ("°", r"^{\circ}"), ("′", r"'"), ("∼", r"\sim"), ("ℓ", r"\ell")]) + "\n")
tex = os.path.join(BUILD, NAME + ".tex")
subprocess.run(["pandoc", mdp, "-o", tex, "--standalone", "--pdf-engine=xelatex", "-H", hdr,
                "-V", "documentclass=article", "-V", "classoption=twocolumn", "-V", f"fontsize={C.get('fontsize', 12)}pt",
                "-V", "papersize=a4", "-V", f"geometry:margin={C.get('margin_cm', 1.0)}cm", "-V", "geometry:columnsep=0.5cm",
                "-V", "mainfont=Latin Modern Roman", "-V", "mathfont=Latin Modern Math"], check=True, cwd=DOCS)
for k in (1, 2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", NAME + ".tex"], cwd=BUILD,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    print(f"▶️  xelatex pass {k}: exit {r.returncode}")
log = io.open(os.path.join(BUILD, NAME + ".log"), encoding="utf-8", errors="replace").read()
if r.returncode != 0:
    print(log[-2500:]); sys.exit("❌ XeLaTeX failed")
miss = sorted(set(re.findall(r"Missing character: There is no (.) ", log)))
over = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)[^\n]*lines? (\d+)", log)
print("✅ 0 missing characters" if not miss else f"❌ missing characters: {miss}")
print("✅ 0 overfull lines" if not over else f"❌ overfull lines (pt, tex line): {over}  -> split those display equations")
problems += bool(miss) + len(over)
pdf = os.path.join(ROOT, NAME + ".pdf")
shutil.copy2(os.path.join(BUILD, NAME + ".pdf"), pdf)

# ------------------------------------------------------------- page checks --
doc = fitz.open(pdf)
per = [len(re.findall(r"(?m)^Slide \d+ [·⋅]", pg.get_text())) for pg in doc]   # XeLaTeX renders · as ⋅
print(f"📄 {len(doc)} pages, slides per page {per}")
mp, (smin, smax) = C.get("max_pages", 0), C.get("slides_per_page", [0, 0])
if mp and len(doc) > mp:
    problems += 1; print(f"❌ {len(doc)} pages > max_pages {mp}")
if smax and any(not smin <= p <= smax for p in per):
    problems += 1; print(f"❌ slides per page outside {smin}..{smax}")
    if smin * len(doc) > len(content):
        print(f"⚠️  {len(content)} slides cannot give {smin}+ per page on {len(doc)} pages: change fontsize, margin or words")
print(f"📦 {pdf}")
print("✅ ALL CHECKS PASSED" if not problems else f"❌ {problems} problem(s) above")
