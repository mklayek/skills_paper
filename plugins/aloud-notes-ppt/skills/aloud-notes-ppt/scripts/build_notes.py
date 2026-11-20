# -*- coding: utf-8 -*-
"""aloud-notes-ppt, step 3: sections/*.md -> master Markdown -> LaTeX (XeLaTeX, Latin Modern) -> PDF, then checks.

Reads <task_folder>/docs/notes_config.json:
  name            output base name (PDF at the top of the task folder, master MD in docs/)
  title, subtitle, author, affiliation (list of lines), year
  range           [first, last] slide numbers covered by the notes, default all slides
  skip            slide numbers with no paragraph (title, section dividers, closing slide)
  parts           {"<first slide of a part>": "<part heading>"}  (the deck's section names)
  fontsize        body size in pt, any value (KOMA class scrartcl), default 13
  title_pt        size of the bold two-line heading (title line + subtitle line), default 15
  write_space_cm  blank space under every slide heading for handwritten notes, default 1.2
  after_space_cm  blank space after each slide block (after the Insight paragraph), default 1.0
  words           [min, max] words per main paragraph, display equations not counted, default [45, 240]
  insight_words   [min, max] words of the optional second paragraph "**Insight:** ..." (default [15, 45])
  max_pages       0 = no limit
  slides_per_page [min, max], [0, 0] = no check
  margin_cm       page margin on all four sides, default 1.0
  math_runs       {"<first slide>": <last slide>} runs of derivation slides summarized in ONE block on the first
                  slide (the later slides of a run are skipped automatically), default none
  math_words      [min, max] words of a mathematics summary block, default [40, 68]
  math_max_lines  most printed lines a mathematics summary may take in the PDF, default 8 (0 = no check)

Checks: one block per content slide, exactly one paragraph per block, word range, no em dash, no semicolon
outside math, 0 missing glyphs, 0 overfull lines, page count and slides per page. Before the build the section
files are checked for control characters (a shell ate a backslash: \b, \t, \r), old font commands (\rm \bf \it,
fatal under KOMA) and broken dark-red significance markup \textcolor[HTML]{8B0000}{...}. Mathematics blocks must
carry "(slides ...)" in the heading, no Insight, no display equation, and fit math_max_lines printed lines.
Layout: A4, two columns, Latin Modern, compact two-line bold navy title, navy part headings, blue slide headings
with a writing gap under them and a gap after each block, no header, page number alone in the bottom-right corner.

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
WMIN, WMAX = C.get("words", [45, 240])
IMIN, IMAX = C.get("insight_words", [15, 45])
MRUNS = {int(k): int(v) for k, v in C.get("math_runs", {}).items()}   # first slide -> last slide of a math run
for a, z in MRUNS.items():
    SKIP |= set(range(a + 1, z + 1))
MWMIN, MWMAX = C.get("math_words", [40, 68])
MLINES = C.get("math_max_lines", 8)
SIG = r"\textcolor[HTML]{8B0000}{"                                    # dark-red significance sentence
slides = json.load(io.open(os.path.join(EXT, "slides.json"), encoding="utf-8"))
LO, HI = C.get("range", [1, 10 ** 6])
content = [s["n"] for s in slides if LO <= s["n"] <= HI and s["n"] not in SKIP]
FS = C.get("fontsize", 13)
TPT, GAP = C.get("title_pt", 15), C.get("write_space_cm", 1.2)
AFTER = C.get("after_space_cm", 1.0)
problems = 0

# ------------------------------------------------------------- collect blocks --
text = ""
for f in sorted(glob.glob(os.path.join(glob.escape(ROOT), "sections", "*.md"))):
    t = io.open(f, encoding="utf-8").read()
    base = os.path.basename(f)
    for m in re.finditer(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", t):
        problems += 1
        print(f"❌ {base}: control character {m.group()!r} near {t[max(0, m.start() - 25):m.start()]!r} "
              "(a shell ate a backslash, fix it with the Edit tool)")
    for m in re.finditer(r"\\(rm|bf|it|tt|sf)\b", t):
        problems += 1
        print(f"❌ {base}: old font command \\{m.group(1)} near {t[max(0, m.start() - 25):m.end() + 10]!r} "
              "(use \\mathrm{...}, \\mathbf{...})")
    k = t.find(SIG)
    while k >= 0:
        i, depth = k + len(SIG), 1
        while i < len(t) and depth:
            depth += {"{": 1, "}": -1}.get(t[i], 0)
            i += 1
        inner = t[k + len(SIG):i - 1]
        if depth or "\n" in inner or "**" in inner:
            problems += 1
            print(f"❌ {base}: broken significance markup near {t[k:k + 70]!r} (unclosed, line break or ** inside)")
        k = t.find(SIG, i)
    text += t.strip() + "\n\n"
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
    if n in MRUNS:                                                    # mathematics summary block
        if not MWMIN <= words <= MWMAX: msg.append(f"math summary {words} words (allowed {MWMIN}-{MWMAX})")
        if "(slides" not in b.split("\n", 1)[0]: msg.append('math heading without "(slides ...)"')
        if ins: msg.append("Insight on a math summary")
        if "$$" in b: msg.append("display equation in a math summary")
    elif not WMIN <= words <= WMAX: msg.append(f"{words} words")
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
n_sig = text.count(SIG)
n_sig_sl = sum(1 for n, b in blocks.items() if n not in MRUNS and SIG in b)
print(f"🔴 {n_sig} dark-red significance sentences on {n_sig_sl} of {len(blocks) - len(MRUNS)} non-math slides"
      + (f", {len(MRUNS)} mathematics summary blocks" if MRUNS else ""))

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
\titleformat{\subsection}{\normalsize\bfseries\color[HTML]{1D4ED8}}{}{0pt}{\Needspace{8\baselineskip}}
\titlespacing*{\section}{0pt}{4pt}{1pt}\titlespacing*{\subsection}{0pt}{AFTERcm}{GAPcm}
\makeatletter
\renewcommand\maketitle{\twocolumn[{\centering
  {\fontsize{TPT}{TLEAD}\selectfont\bfseries\color[HTML]{0B2A55}\@title\\\@subtitle\par}\vspace{3pt}
  {\small\@author\par}\vspace{1pt}{\footnotesize\@date\par}\vspace{3pt}\hrule\vspace{6pt}}]}
\makeatother
\setlength{\parindent}{0pt}\raggedbottom\setlength{\abovedisplayskip}{4pt}\setlength{\belowdisplayskip}{4pt}
\setcounter{secnumdepth}{0}
\setlength{\parskip}{1.5pt}
""".replace("AFTER", str(AFTER)).replace("GAP", str(GAP)).replace("TLEAD", str(round(TPT * 1.18, 1))).replace("TPT", str(TPT))
  + "\n".join(rf"\newunicodechar{{{c}}}{{\ensuremath{{{m}}}}}" for c, m in [
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
                "-V", "documentclass=scrartcl", "-V", "classoption=twocolumn",
                "-V", f"fontsize={FS}pt",
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
try:
    shutil.copy2(os.path.join(BUILD, NAME + ".pdf"), pdf)
except PermissionError:                                               # the PDF is open in a viewer
    problems += 1
    print(f"❌ could not overwrite {pdf}: it is open in a PDF viewer. Close it and run again. "
          "Checking the build copy instead.")
    pdf = os.path.join(BUILD, NAME + ".pdf")

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
if MRUNS and MLINES:                                                  # printed lines of each math summary
    rows = {}
    for pi, pg in enumerate(doc):
        mid = pg.rect.width / 2
        for bl in pg.get_text("dict")["blocks"]:
            for ln in bl.get("lines", []):
                sp = [s for s in ln["spans"] if s["text"].strip()]
                if not sp or (ln["bbox"][1] > pg.rect.height - 40 and "".join(s["text"] for s in sp).strip().isdigit()):
                    continue
                key = (pi, ln["bbox"][0] >= mid - 5, round(ln["bbox"][3]))          # one printed row
                rows.setdefault(key, []).append((ln["bbox"][0], "".join(s["text"] for s in ln["spans"]),
                                                 sp[0]["font"].endswith("Bold")))
    cur, count = None, {}
    for key in sorted(rows):
        parts = sorted(rows[key])
        t, bold = " ".join(p[1] for p in parts).strip(), parts[0][2]
        if bold:
            m = re.match(r"Slide\s*(\d+)", t)
            if m:
                cur = int(m.group(1)) if int(m.group(1)) in MRUNS else None
                if cur: count[cur] = 0
            elif t.startswith("Insight"):
                cur = None
            continue
        if cur is not None:
            count[cur] += 1
    bad = {n: c for n, c in count.items() if c > MLINES}
    print(f"🧮 math summary lines {count}" + (f", ❌ over {MLINES}: {bad}" if bad else f", ✅ all within {MLINES}"))
    problems += len(bad)
print(f"📦 {pdf}")
print("✅ ALL CHECKS PASSED" if not problems else f"❌ {problems} problem(s) above")
