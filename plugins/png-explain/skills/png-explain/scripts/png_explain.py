"""png-explain: build one 16:9 explainer PNG (infographic style) from a Python content spec.

Layout: bordered white page, bold black title with one highlighted word, gray subtitle between rules,
2 or 3 side-by-side panels (colored outline + header pill), each with a definition, a figure (TikZ,
a Python-made PNG or a downloaded image with credit), a boxed equation with its symbol list, and two
small boxes (key points and example) with icons, then an optional full-width comparison table.

Usage (from a spec script):
    import sys; sys.path.insert(0, r"D:\\claudecode\\TEACHING\\.claude\\skills\\png-explain\\scripts")
    from png_explain import build
    build(SPEC, out=r"...\\figs\\07_Name.png", docs=r"...\\docs", work=r"...\\temp\\build_png_explain_name")

The spec format is documented in ../SKILL.md and shown in ../examples/spec_self_mutual_induction.py.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

COLORS = {"blue": "1D4ED8", "red": "B91C1C", "green": "15803D", "purple": "6D28D9",
          "orange": "C2410C", "teal": "0E7490", "navy": "0B2A55", "rose": "BE185D"}
EXAMPLE_COLORS = ["green", "orange", "purple"]
DPI = 160                                      # 16 in x 9 in -> 2560 x 1440 px

PREAMBLE = r"""\documentclass{article}
\usepackage[paperwidth=16in,paperheight=9in,margin=0.32in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[scaled=0.96]{helvet}\renewcommand{\familydefault}{\sfdefault}
\usepackage[table]{xcolor}
\usepackage{amsmath,amssymb,graphicx,array,tabularx,enumitem,adjustbox}
\usepackage[most]{tcolorbox}
\usepackage{fontawesome5}
\usepackage{tikz}\usepackage[siunitx,american]{circuitikz}
\usetikzlibrary{arrows.meta,decorations.markings,calc}
\pagestyle{empty}\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}
\definecolor{ink}{HTML}{111111}\definecolor{subgray}{HTML}{4B5563}\definecolor{rulegray}{HTML}{D1D5DB}
\definecolor{pageframe}{HTML}{0B2A55}
@COLORDEFS@
\color{ink}\hyphenpenalty=10000\exhyphenpenalty=10000
\colorlet{pc}{blue}
\newcommand{\kw}[1]{\textcolor{pc}{\textbf{#1}}}
\newcommand{\hl}[1]{\textcolor{red}{#1}}
\newcommand{\pill}[3]{\tikz[baseline=(p.base)]\node[fill=#1,text=white,rounded corners=3pt,inner xsep=7pt,inner ysep=3pt,font=\bfseries\fontsize{12.5}{14}\selectfont](p){#2\ \MakeUppercase{#3}};}
\setlist[itemize]{leftmargin=1.05em,itemsep=2pt,topsep=1pt,parsep=0pt,label=\textcolor{pc}{\textbullet}}
\tcbset{panel/.style={enhanced,halign=left,colback=white,colframe=#1,boxrule=1.3pt,arc=6pt,
  left=9pt,right=9pt,top=13pt,bottom=7pt,fonttitle=\bfseries\fontsize{16}{18}\selectfont,coltitle=white,
  attach boxed title to top center={yshift=-3.2mm},
  boxed title style={colback=#1,colframe=#1,arc=4pt,boxrule=0pt,left=10pt,right=10pt,top=2pt,bottom=2pt}},
  small/.style={enhanced,halign=left,colback=white,colframe=#1,boxrule=0.9pt,arc=4pt,left=6pt,right=6pt,top=4pt,bottom=4pt}}
\begin{document}
\begin{tikzpicture}[remember picture,overlay]
\draw[pageframe,line width=2.6pt,rounded corners=4pt] ([shift={(0.13in,-0.13in)}]current page.north west) rectangle ([shift={(-0.13in,0.13in)}]current page.south east);
\end{tikzpicture}%
"""


def _figure(fig, work, height, font_pt):
    """TeX for one panel figure: TikZ code, or an image file (copied into the build folder) with credit.
    TikZ is only shrunk to fit (never enlarged), so draw it at about the figure slot size (~10 cm wide)."""
    if not fig:
        return ""
    if "tikz" in fig:
        return (r"{\fontsize{%s}{%s}\selectfont\begin{adjustbox}{max width=\linewidth,max height=%.2fin,center}"
                % (font_pt, font_pt + 2, height) + fig["tikz"] + r"\end{adjustbox}}")
    src = Path(fig["image"])
    dst = work / f"img_{src.stem}{src.suffix}"
    shutil.copy2(src, dst)
    tex = r"{\centering\includegraphics[width=\linewidth,height=%.2fin,keepaspectratio]{%s}\par}" % (height, dst.name)
    if fig.get("credit"):
        tex += r"{\centering\fontsize{9}{10.5}\selectfont\color{subgray}\itshape %s\par}" % fig["credit"]
    return tex


def _items(lst):
    if isinstance(lst, str):
        return lst
    return r"\begin{itemize}" + "".join(r"\item " + x for x in lst) + r"\end{itemize}"


def _panel(i, p, s, work):
    col = p["color"]
    exc = p.get("example_color", EXAMPLE_COLORS[i % len(EXAMPLE_COLORS)])
    body = s["body_pt"]
    sym_rows = r"\\[1pt]".join(r"$%s$ & : & %s" % (a, b) for a, b in p.get("symbols", []))
    eq = ""
    if p.get("equation"):
        eq = (r"\begin{tcolorbox}[small=" + col + r",halign=center,top=6pt,bottom=6pt]"
              r"{\fontsize{%s}{%s}\selectfont$\displaystyle %s$}\end{tcolorbox}" % (s["eq_pt"], s["eq_pt"] + 4, p["equation"]))
        if sym_rows:
            eq += (r"\par\vspace{4pt}{\fontsize{%s}{%s}\selectfont\begin{tabular}{@{}r@{\ }c@{\ }>{\raggedright\arraybackslash}p{0.70\linewidth}@{}}%s\end{tabular}\par}"
                   % (body - 1, body + 2, sym_rows))
    fig = _figure(p.get("figure"), work, s["fig_h"], body - 1)
    frac = p.get("figure_width", 0.56)
    mid = (r"\begin{minipage}[c]{%.2f\linewidth}%s\end{minipage}\hfill\begin{minipage}[c]{%.2f\linewidth}%s\end{minipage}"
           % (frac, fig, 0.97 - frac, eq)) if fig else eq
    boxes = ""
    pts, ex = p.get("points"), p.get("example")
    if pts or ex:
        def small(c, icon, title, content, grp):
            return (r"\begin{tcolorbox}[small=%s,equal height group=%s]\pill{%s}{%s}{%s}\par\vspace{4pt}"
                    r"{\fontsize{%s}{%s}\selectfont %s}\end{tcolorbox}" % (c, grp, c, icon, title, body - 0.5, body + 2, _items(content)))
        grp = f"sub{i}"
        left = small(col, r"\faKey", p.get("points_title", "Key points"), pts, grp) if pts else ""
        right = (r"{\colorlet{pc}{%s}" % exc + small(exc, r"\faLightbulb[regular]", p.get("example_title", "Example"), ex, grp) + "}") if ex else ""
        if left and right:
            boxes = (r"\begin{minipage}[t]{0.49\linewidth}%s\end{minipage}\hfill\begin{minipage}[t]{0.49\linewidth}%s\end{minipage}"
                     % (left, right))
        else:
            boxes = left or right
    return (r"{\colorlet{pc}{%s}\begin{tcolorbox}[panel=%s,title=\MakeUppercase{%s},equal height group=panels]"
            r"{\fontsize{%s}{%s}\selectfont %s\par}\vspace{6pt}%s\par\vspace{7pt}%s\end{tcolorbox}}"
            % (col, col, p["head"], body, body + 3.5, p["definition"], mid, boxes))


def _table(t, panels, s):
    n = len(t["rows"][0]) - 1
    head = " & ".join(r"\textcolor{%s}{\textbf{%s}}" % (panels[k]["color"], panels[k]["head"]) for k in range(n))
    rows = r"\\\arrayrulecolor{rulegray}\hline ".join(" & ".join([r"\textbf{%s}" % r[0]] + list(r[1:])) for r in t["rows"])
    spec = r"@{}>{\raggedright\arraybackslash}p{%.1fin}" % t.get("label_w", 2.4) + r"*{%d}{>{\centering\arraybackslash}X}@{}" % n
    return (r"\begin{tcolorbox}[panel=navy,title=\MakeUppercase{%s},top=12pt,bottom=4pt]"
            r"{\fontsize{%s}{%s}\selectfont\renewcommand{\arraystretch}{1.25}\begin{tabularx}{\linewidth}{%s}"
            r" & %s\\\arrayrulecolor{rulegray}\hline %s\\\end{tabularx}}\end{tcolorbox}"
            % (t["head"], s["body_pt"], s["body_pt"] + 3, spec, head, rows))


def tex_of(spec, work, shrink=(0.0, 0.0)):
    """shrink = (figure height cut in inches, body size cut in pt), used by the auto-fit loop."""
    s = {"body_pt": 14, "eq_pt": 21, "fig_h": 2.45, "title_pt": 34}
    s.update(spec.get("sizes", {}))
    s["fig_h"] -= shrink[0]
    s["body_pt"] -= shrink[1]
    colordefs = "\n".join(r"\definecolor{%s}{HTML}{%s}" % kv for kv in COLORS.items())
    out = [PREAMBLE.replace("@COLORDEFS@", colordefs)]
    out.append(r"{\centering\fontsize{%s}{%s}\selectfont\bfseries %s\par}\vspace{4pt}"
               % (s["title_pt"], s["title_pt"] + 4, spec["title"]))
    if spec.get("subtitle"):
        rule = r"\tikz[baseline=-0.6ex]\draw[subgray,line width=0.8pt](0,0)--(1.6in,0);"
        out.append(r"{\centering%s\ \ {\fontsize{14}{16}\selectfont\color{subgray}\MakeUppercase{%s}}\ \ %s\par}\vspace{10pt}"
                   % (rule, spec["subtitle"], rule))
    panels = spec["panels"]
    w = (1 - 0.018 * (len(panels) - 1)) / len(panels)
    out.append(r"\hfill".join(r"\begin{minipage}[t]{%.3f\linewidth}%s\end{minipage}" % (w, _panel(i, p, s, work))
                              for i, p in enumerate(panels)))
    if spec.get("table"):
        out.append(r"\par\vspace{10pt}" + _table(spec["table"], panels, s))
    out.append(r"\end{document}")
    return "\n".join(out)


def _md_text(t):
    t = re.sub(r"\\(kw|hl|textbf)\{([^{}]*)\}", r"**\2**", t)
    return t.replace(r"\&", "&").replace("~", " ").replace(r"\,", " ")


def md_of(spec):
    L = [f"# {_md_text(spec['title'])}", ""]
    if spec.get("subtitle"):
        L += [f"_{spec['subtitle']}_", ""]
    for p in spec["panels"]:
        L += [f"## {p['head']}", "", _md_text(p["definition"]), ""]
        fig = p.get("figure") or {}
        if fig.get("image"):
            L += [f"![{p['head']}]({Path(fig['image']).name})" + (f"  \n_{fig['credit']}_" if fig.get("credit") else ""), ""]
        elif fig.get("tikz"):
            L += ["_(figure drawn with TikZ on the PNG)_", ""]
        if p.get("equation"):
            L += [f"$$ {p['equation']} $$", ""]
            L += [f"- ${a}$ : {_md_text(b)}" for a, b in p.get("symbols", [])] + [""]
        for key, default in (("points", "Key points"), ("example", "Example")):
            v = p.get(key)
            if v:
                L += [f"**{p.get(key + '_title', default)}**", ""]
                L += ([f"- {_md_text(x)}" for x in v] if isinstance(v, list) else [_md_text(v)]) + [""]
    t = spec.get("table")
    if t:
        n = len(t["rows"][0]) - 1
        L += [f"## {t['head']}", "", "| | " + " | ".join(p["head"] for p in spec["panels"][:n]) + " |",
              "|---|" + "---|" * n]
        L += ["| " + " | ".join(_md_text(c) for c in r) + " |" for r in t["rows"]] + [""]
    return "\n".join(L)


def build(spec, out, docs, work, archive=None):
    """Render SPEC to the PNG `out`, write .tex/.md to `docs`, compile in `work`.
    An existing PNG is first copied to `archive` (default: <out>/../../archive/previous_<name>)."""
    out, docs, work = Path(out), Path(docs), Path(work)
    name = out.stem
    print(f"▶️ png-explain: {name}")
    for d in (out.parent, docs, work):
        d.mkdir(parents=True, exist_ok=True)
    if out.exists():
        arch = Path(archive) if archive else out.parent.parent / "archive" / f"previous_{name}"
        arch.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, arch / out.name)
        print(f"🗄️ Archived the previous PNG to {arch}")
    # auto-fit: shrink the figures first, then the body text, until the page fits on one sheet
    for shrink in ((0, 0), (0.2, 0), (0.35, 0.5), (0.5, 1.0), (0.6, 1.5)):
        (work / "explain.tex").write_text(tex_of(spec, work, shrink), encoding="utf-8")
        print(f"🔧 Compiling with pdflatex (figure -{shrink[0]} in, body -{shrink[1]} pt)…")
        for _ in (1, 2):
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "explain.tex"],
                               cwd=work, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode:
                print("❌ pdflatex failed:\n" + r.stdout[-2500:])
                return 1
        log = (work / "explain.log").read_text(encoding="utf-8", errors="replace")
        pages = re.search(r"Output written on .*?\((\d+) page", log)
        npages = int(pages.group(1)) if pages else -1
        print(f"🔍 Pages: {npages} (must be 1), overfull boxes: {log.count('Overfull')}")
        if npages == 1:
            break
        print("⚠️  Overflow, shrinking and retrying")
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-singlefile", "-f", "1", "-l", "1",
                    "explain.pdf", "explain"], cwd=work, check=True)
    shutil.copy2(work / "explain.png", out)
    shutil.copy2(work / "explain.tex", docs / f"{name}.tex")
    (docs / f"{name}.md").write_text(md_of(spec), encoding="utf-8")
    print(f"📦 TeX and Markdown copies in {docs}")
    print(f"✅ Final PNG: {out}")
    return 0 if npages == 1 else 2
