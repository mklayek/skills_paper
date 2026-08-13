#!/usr/bin/env python3
"""deck_to_beamer.py — deck mini-language -> Markdown, Beamer .tex and Beamer PDF.

Companion to build_styled_slides.py (which renders the same .deck to a styled PPTX).
One source, four artefacts: .deck -> .md + .tex + .pdf (+ .pptx from the other tool),
all carrying the same lecture style:

  * display equations keeping the SOURCE's own numbers, printed as a red ---(N);
  * a bold takeaway line and a purple handwriting "Therefore, ..." line;
  * bottom figure with an italic caption, and a graphical Thank-You end slide.

Bullets differ by back-end on purpose. The PPTX keeps black squares; the Beamer body is
emitted as real nested itemize, so the theme's own bullets apply (Madrid: shaded blue
balls, smaller at each level). Themed mode also skips mathpazo (sans-serif, like the
beamer gallery) and sets 11pt; --beamer-theme none restores 10pt serif black squares.

Figures are NOT shrunk to share a slide with the bullets. In themed mode every !fig: gets
its own frame under the same title at ~72% of the slide height, with its caption and one
or two lines of description drawn from that slide's !note: (or !key:). Use
--no-fig-slides to keep them inline.

The Beamer back-end uses the **Madrid** theme by default (Madrid-default-default,
https://deic.uab.cat/~iblanes/beamer_gallery/individual/Madrid-default-default.html):
a blue frametitle bar, an infolines headline carrying the section name, and Madrid's
own footline reading short author | foot label | date + page. Pass --beamer-theme none
to restore the hand-built chrome (underlined title over a grey+orange rule, plain
footline). The PPTX back-end is unaffected and keeps the underlined-title style.

Compiles with pdflatex only (never lualatex/xelatex — they render blank on this box).

USAGE:
    python3 deck_to_beamer.py talk.deck --out-dir /abs/dir --name talk \
        --title "..." --subtitle "..." --author "..." \
        --date "21 July 2026" --foot "Methodological Evolution"
    python3 deck_to_beamer.py talk.deck --beamer-theme none   # pre-Madrid chrome
    python3 deck_to_beamer.py talk.deck --md-only             # just the Markdown

Author: Dr. Mrinal Kanti Layek - Geophysics & AI Lab, Department of Energy &
Resources Engineering, Chonnam National University, Gwangju, Republic of Korea.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_styled_slides import (RE_DEFN, TOKEN, parse_deck, ensure_thankyou,  # noqa: E402
                                 figure_description)

# --------------------------------------------------------------------------- #
# Shared style constants (kept in step with build_styled_slides.py)
# --------------------------------------------------------------------------- #
C_RED, C_TERM, C_CHECK, C_SO = "C00000", "7B2D26", "2E7D32", "6A0DAD"
C_REF = "1F3864"   # dark blue references / citations

# Beamer theme. Madrid-default-default is the house default:
#   https://deic.uab.cat/~iblanes/beamer_gallery/individual/Madrid-default-default.html
# Madrid brings an infolines headline (section name) and its own footline
# (short author | short title | short date + page). Pass --beamer-theme none to
# fall back to the hand-built underlined title rule and plain footline.
DEFAULT_THEME = "Madrid"
DEFAULT_COLORTHEME = "default"

# Default author block — override with --author on any build.
DEFAULT_AUTHOR = ("Dr. Mrinal Kanti Layek — Geophysics & AI Lab, "
                  "Department of Energy & Resources Engineering, "
                  "Chonnam National University, Gwangju, Republic of Korea")
DEFAULT_AUTHOR_SHORT = "M. K. Layek — CNU"

PREAMBLE = r"""
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{soul}
\usepackage[normalem]{ulem}
\usepackage{caption}\captionsetup{font={footnotesize,stretch=1.0}}
\usepackage{pifont}
\usepackage{etoolbox}

% Dense research decks: keep the theme's own bullet glyphs but pull the vertical
% spacing in, so [shrink] has far less work to do and the body stays legible.
\AtBeginEnvironment{itemize}{%
  \setlength{\itemsep}{0.35ex}\setlength{\parskip}{0pt}%
  \setlength{\parsep}{0pt}\setlength{\topsep}{0.35ex}}
\setlength{\leftmargini}{1.6em}
\setlength{\leftmarginii}{1.4em}
\setlength{\leftmarginiii}{1.2em}

\definecolor{mklred}{HTML}=RED=
\definecolor{mklterm}{HTML}=TERM=
\definecolor{mklcheck}{HTML}=CHECK=
\definecolor{mklso}{HTML}=SO=
\definecolor{mklref}{HTML}=REF=
\definecolor{mklrule}{HTML}=E8722C=

% marker glyphs: a solid black square is the bullet on every level
\newcommand{\mklsquare}{{\color{black}\ding{110}}}
\newcommand{\mklcheckbox}{\mklsquare}
\newcommand{\mklstar}{\mklsquare}
\newcommand{\mkldot}{\mklsquare}
\newcommand{\mklterm}[1]{{\color{mklterm}\bfseries #1}}
\newcommand{\mklhl}[1]{{\color{mklred}\bfseries\sethlcolor{yellow}\hl{#1}}}
\newcommand{\mklkey}[1]{\par\medskip\textbf{#1}}
\newcommand{\mklso}[1]{\par\smallskip{\color{mklso}\itshape #1}}
% references / citations: dark blue italic, 20 pt (kept at size, never shrunk)
\newcommand{\mklref}[1]{\par\smallskip\noindent\hangindent=1.4em{\color{mklref}\itshape\fontsize{11}{13}\selectfont #1}}
\newcommand{\mklcite}[1]{{\color{mklref}\itshape #1}}
% the equation number, printed flush right on the equation's own line
\newcommand{\mkltag}[1]{{\color{mklred}\bfseries -{}-{}-(#1)}}

\setbeamertemplate{navigation symbols}{}
"""

# Chrome for --beamer-theme none: the original hand-built title rule and footline.
# A named theme (Madrid by default) supplies its own frametitle bar and footline,
# so these overrides are emitted ONLY when no theme is in play.
PREAMBLE_PLAIN_CHROME = r"""
\usepackage{mathpazo}
\setbeamercolor{frametitle}{fg=black}
\setbeamerfont{frametitle}{series=\bfseries,size=\large}
\setbeamertemplate{frametitle}{%
  \vskip0.6ex\centering\usebeamerfont{frametitle}\uline{\insertframetitle}\par
  \vskip0.4ex{\color{black}\rule{\textwidth}{0.4pt}}\par\vskip-0.9ex
  {\color{mklrule}\rule{\textwidth}{1.6pt}}\par\vskip0.4ex}
\makeatletter
\setbeamertemplate{footline}{%
  \leavevmode\hbox{\begin{beamercolorbox}[wd=\paperwidth,ht=2.6ex,dp=1.3ex,%
    leftskip=1.2em,rightskip=1.2em]{palette quaternary}%
    {\footnotesize\color{gray}=DATE=\hfill =FOOT=\hfill =PAGE=}%
  \end{beamercolorbox}}}
\makeatother
"""


# --------------------------------------------------------------------------- #
# Inline formatting
# --------------------------------------------------------------------------- #
def tex_escape(s: str) -> str:
    """Escape LaTeX specials in PROSE only (never inside $...$)."""
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return s


def inline_tex(text: str) -> str:
    """deck inline markup -> LaTeX. Maths passes through untouched."""
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("$") and part.endswith("$") and len(part) > 2:
            out.append(part)                                  # verbatim maths
        elif part.startswith("**") and part.endswith("**"):
            out.append(r"\mklterm{" + tex_escape(part[2:-2]) + "}")
        elif part.startswith("==") and part.endswith("=="):
            out.append(r"\mklhl{" + tex_escape(part[2:-2]) + "}")
        elif part.startswith("@@") and part.endswith("@@"):
            out.append(r"\mklcite{" + tex_escape(part[2:-2]) + "}")
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(r"\emph{" + tex_escape(part[1:-1]) + "}")
        else:
            out.append(tex_escape(part))
    return "".join(out)


def inline_md(text: str) -> str:
    """deck inline markup -> Markdown (highlight becomes bold; citations italic)."""
    text = re.sub(r"==(.+?)==", r"**\1**", text)
    return re.sub(r"@@(.+?)@@", r"*\1*", text)


def marker_level(b) -> int:
    """Same rule as the PPTX build: a bullet that opens with maths is a definition."""
    return 1 if (b.level == 0 and RE_DEFN.match(b.text)) else b.level


# --------------------------------------------------------------------------- #
# Emitters
# --------------------------------------------------------------------------- #
def figure_frames_tex(sl, title: str) -> list:
    """One dedicated frame per figure: large image + caption + short description.

    Figures compete badly with a full slide of bullets — capped to a fraction of
    the text height they come out unreadably small. Giving each figure its own
    frame lets it run to ~72% of the slide height, with its caption underneath
    and one or two lines of description from the slide's !note:.
    """
    figs = [b for b in sl.blocks if b.kind == "fig" and os.path.exists(b.text)]
    if not figs:
        return []
    desc = figure_description(sl)      # shared with the PPTX back-end

    frames = []
    for b in figs:
        body = [r"\begin{frame}{" + tex_escape(title) + "}",
                r"\vfill\begin{center}",
                r"\includegraphics[width=0.92\textwidth,height=0.72\textheight,"
                r"keepaspectratio]{%s}" % b.text]
        if b.tag:
            body.append(r"\\[0.6ex]{\footnotesize\itshape " + tex_escape(b.tag) + "}")
        body.append(r"\end{center}")
        if desc:
            body.append(r"\vfill{\footnotesize " + inline_tex(desc) + r"}\vfill")
        else:
            body.append(r"\vfill")
        body.append(r"\end{frame}")
        frames.append("\n".join(body))
    return frames


def slide_body_tex(sl, themed: bool = True, skip_figs: bool = False) -> str:
    """Emit one slide's body.

    themed=True  -> real nested itemize, so the beamer theme's own bullets apply
                    (Madrid: shaded blue balls, smaller at each level).
    themed=False -> the hand-built flush-left black squares of the plain chrome.
    skip_figs    -> omit !fig: blocks (they get their own frame instead).
    """
    lines = []
    depth = 0                      # how many itemize environments are open

    def close_lists(to: int = 0):
        nonlocal depth
        while depth > to:
            lines.append(r"\end{itemize}")
            depth -= 1

    def open_lists(to: int):
        nonlocal depth
        while depth < to:
            lines.append(r"\begin{itemize}")
            depth += 1

    MARK = {0: r"\mklsquare", 1: r"\mklsquare", 2: r"\mklsquare"}
    IND = {0: "0pt", 1: "14pt", 2: "26pt"}
    for b in sl.blocks:
        if b.kind == "bullet":
            lv = marker_level(b)
            if themed:
                # levels are 0-based in the deck, nesting depth is 1-based
                want = lv + 1
                if want < depth:
                    close_lists(want)
                open_lists(want)
                lines.append(r"\item " + inline_tex(b.text))
            else:
                # flush left, no hanging indent (wrapped lines align at the left margin)
                lines.append(rf"\par\smallskip\noindent\hangindent=0pt\hspace*{{{IND[lv]}}}"
                             rf"{MARK[lv]}~{inline_tex(b.text)}")
            continue
        # anything that is not a bullet ends the current list nesting
        close_lists(0)
        if b.kind == "eq":
            tag = rf"\mkltag{{{b.tag}}}" if b.tag else ""
            if b.tag:
                # \makebox at full line width gives the \hfill glue something to
                # stretch against, so the maths centres and the tag sits flush right
                lines.append(r"\par\vspace{0.5ex}\noindent\makebox[\linewidth]{"
                             r"\hfill$\displaystyle " + b.text + r"$\hfill " + tag
                             + r"}\vspace{0.3ex}")
            else:
                lines.append(r"\par\vspace{0.5ex}\begin{center}$\displaystyle "
                             + b.text + r"$\end{center}\vspace{0.3ex}")
        elif b.kind == "key":
            lines.append(r"\mklkey{" + inline_tex(b.text) + "}")
        elif b.kind == "ref":
            lines.append(r"\mklref{" + inline_tex(b.text) + "}")
        elif b.kind == "so":
            lines.append(r"\mklso{" + inline_tex(b.text) + "}")
        elif b.kind == "fig" and not skip_figs and os.path.exists(b.text):
            cap = (r"\\[0.2ex]{\footnotesize\itshape %s}" % tex_escape(b.tag)) if b.tag else ""
            lines.append(r"\begin{center}\includegraphics[width=%.2f\textwidth,"
                         r"height=0.42\textheight,keepaspectratio]{%s}%s\end{center}"
                         % (min(b.width, 0.95), b.text, cap))
    close_lists(0)
    return "\n".join(lines)


def strip_marks(title: str) -> str:
    return title.replace("**", "").replace("==", "")


def build_tex(slides, args) -> str:
    theme = (getattr(args, "beamer_theme", "") or DEFAULT_THEME).strip()
    ctheme = (getattr(args, "beamer_colortheme", "") or DEFAULT_COLORTHEME).strip()
    plain = theme.lower() in ("", "none", "default")
    # Dedicated figure frames: on by default for a named theme, off for the plain
    # chrome so legacy decks re-render exactly as before. --no-fig-slides overrides.
    fig_slides = getattr(args, "fig_slides", None)
    if fig_slides is None:
        fig_slides = not plain

    body = PREAMBLE + (PREAMBLE_PLAIN_CHROME if plain else "")
    pre = (body.replace("=RED=", "{" + C_RED + "}")
                   .replace("=TERM=", "{" + C_TERM + "}")
                   .replace("=CHECK=", "{" + C_CHECK + "}")
                   .replace("=SO=", "{" + C_SO + "}")
                   .replace("=REF=", "{" + C_REF + "}")
                   .replace("=E8722C=", "{E8722C}")
                   .replace("=DATE=", "" if args.no_date else tex_escape(args.date))
                   .replace("=PAGE=", "" if args.no_page else r"\insertframenumber")
                   .replace("=FOOT=", tex_escape(args.foot)))
    use = (r"\usetheme{default}\usecolortheme{default}" if plain
           else rf"\usetheme{{{theme}}}\usecolortheme{{{ctheme}}}\usefonttheme{{default}}")

    # Short forms drive a named theme's footline: author | foot label | date + page.
    a_short = tex_escape(getattr(args, "author_short", "") or DEFAULT_AUTHOR_SHORT)
    t_short = tex_escape(args.foot or args.title)
    d_short = "" if args.no_date else tex_escape(args.date)

    # A named theme gets 11pt (matches the beamer gallery's density); the plain
    # chrome keeps 10pt so older decks re-render identically.
    docclass = (r"\documentclass[aspectratio=169,10pt]{beamer}" if plain
                else r"\documentclass[aspectratio=169,11pt]{beamer}")
    out = [docclass, use, pre,
           r"\title[" + t_short + "]{" + tex_escape(args.title) + "}",
           r"\subtitle{" + tex_escape(args.subtitle) + "}",
           r"\author[" + a_short + "]{" + tex_escape(args.author) + "}",
           r"\date[" + d_short + "]{" + tex_escape(args.date) + "}",
           r"\begin{document}", r"{\setbeamertemplate{footline}{}\frame{\titlepage}}"]
    for sl in slides:
        fb = getattr(sl, "fullbleed_img", None)
        if fb and os.path.exists(fb):
            out.append(r"{\setbeamertemplate{footline}{}\begin{frame}[plain]"
                       r"\centering\makebox[\paperwidth][c]{\includegraphics"
                       r"[width=\paperwidth,height=\paperheight,keepaspectratio]{"
                       + fb + r"}}\end{frame}}")
            continue
        if sl.section:
            out.append(r"\section{" + tex_escape(sl.title) + "}")
            out.append(r"\begin{frame}[plain]\vfill\centering{\Large\bfseries "
                       + tex_escape(sl.title) + r"}\vfill\end{frame}")
            continue
        title = strip_marks(sl.title)
        out.append(r"\begin{frame}[shrink=25]{" + tex_escape(title) + "}")
        out.append(slide_body_tex(sl, themed=not plain, skip_figs=fig_slides))
        if sl.notes:
            out.append(r"\note{" + tex_escape(" ".join(sl.notes)) + "}")
        out.append(r"\end{frame}")
        if fig_slides:
            out.extend(figure_frames_tex(sl, title))
    out.append(r"\end{document}")
    return "\n".join(out)


def build_md(slides, args) -> str:
    out = [f"# {args.title}", ""]
    if args.subtitle:
        out += [f"*{args.subtitle}*", ""]
    out += [f"**Author:** {args.author}", f"**Date:** {args.date}", "", "---", ""]
    for sl in slides:
        if sl.section:
            out += [f"## {sl.title}", ""]
            continue
        out += [f"### {strip_marks(sl.title)}", ""]
        for b in sl.blocks:
            if b.kind == "bullet":
                out.append("  " * marker_level(b) + f"- {inline_md(b.text)}")
            elif b.kind == "eq":
                tag = f" \\tag{{{b.tag}}}" if b.tag else ""
                out += ["", "$$", b.text + tag, "$$", ""]
            elif b.kind == "key":
                out += ["", f"**{inline_md(b.text)}**"]
            elif b.kind == "ref":
                out.append(f"- *{inline_md(b.text)}*")
            elif b.kind == "so":
                out += ["", f"> {inline_md(b.text)}"]
            elif b.kind == "fig":
                out += ["", f"![]({b.text}){{width={int(b.width * 100)}%}}", ""]
                if b.tag:
                    out += [f"*{b.tag}*", ""]
        if sl.notes:
            out += ["", f"*Note: {' '.join(sl.notes)}*"]
        out += ["", "---", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="deck → Markdown + Beamer tex/PDF")
    ap.add_argument("input")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--name", default=None)
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", default=DEFAULT_AUTHOR)
    ap.add_argument("--author-short", default=DEFAULT_AUTHOR_SHORT,
                    help="short author for a themed footline")
    ap.add_argument("--date", default="")
    ap.add_argument("--foot", default="")
    ap.add_argument("--beamer-theme", default=DEFAULT_THEME,
                    help="beamer theme (default: Madrid; 'none' = hand-built chrome)")
    ap.add_argument("--beamer-colortheme", default=DEFAULT_COLORTHEME,
                    help="beamer color theme (default: default)")
    ap.add_argument("--fig-slides", dest="fig_slides", action="store_true", default=None,
                    help="give every figure its own frame (default with a named theme)")
    ap.add_argument("--no-fig-slides", dest="fig_slides", action="store_false",
                    help="keep figures inline under the bullets")
    ap.add_argument("--no-date", action="store_true", help="omit the date from the footline")
    ap.add_argument("--no-page", action="store_true", help="omit the frame number from the footline")
    ap.add_argument("--md-only", action="store_true")
    args = ap.parse_args()

    src = os.path.abspath(args.input)
    out_dir = os.path.abspath(args.out_dir or os.path.dirname(src))
    name = args.name or os.path.splitext(os.path.basename(src))[0]
    os.makedirs(out_dir, exist_ok=True)

    slides = parse_deck(src)
    ensure_thankyou(slides)
    print(f"deck_to_beamer: {src}\n  slides: {len(slides)}")

    md_path = os.path.join(out_dir, name + ".md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(build_md(slides, args))
    print(f"  MD     : {md_path}")
    if args.md_only:
        return

    tex_path = os.path.join(out_dir, name + "_beamer.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(build_tex(slides, args))
    print(f"  TEX    : {tex_path}")

    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        print("  PDF    : SKIPPED (pdflatex not found)")
        return
    env = dict(os.environ, PATH="/usr/bin:" + os.environ.get("PATH", ""))
    for _ in range(2):
        subprocess.run([pdflatex, "-interaction=nonstopmode",
                        "-output-directory", out_dir, tex_path],
                       env=env, capture_output=True, text=True)
    pdf = os.path.splitext(tex_path)[0] + ".pdf"
    for ext in (".aux", ".log", ".nav", ".snm", ".toc", ".out", ".vrb"):
        f = os.path.splitext(tex_path)[0] + ext
        if os.path.exists(f):
            os.remove(f)
    print(f"  PDF    : {pdf}" if os.path.exists(pdf) else "  PDF    : FAILED (see .log)")


if __name__ == "__main__":
    main()
