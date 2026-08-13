#!/usr/bin/env python3
"""deck_to_beamer.py — deck mini-language -> Markdown, Beamer .tex and Beamer PDF.

Companion to build_styled_slides.py (which renders the same .deck to a styled PPTX).
One source, four artefacts: .deck -> .md + .tex + .pdf (+ .pptx from the other tool),
all carrying the same lecture style:

  * black-square bullets at every level, flush-left body text;
  * display equations keeping the SOURCE's own numbers, printed as a red ---(N);
  * a bold takeaway line and a purple handwriting "Therefore, ..." line;
  * bottom figure with an italic caption, and a graphical Thank-You end slide.

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
from build_styled_slides import RE_DEFN, TOKEN, parse_deck, ensure_thankyou  # noqa: E402

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
\usepackage{mathpazo}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{soul}
\usepackage[normalem]{ulem}
\usepackage{caption}\captionsetup{font={footnotesize,stretch=1.0}}
\usepackage{pifont}

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
def slide_body_tex(sl) -> str:
    lines, item_open = [], False
    MARK = {0: r"\mklsquare", 1: r"\mklsquare", 2: r"\mklsquare"}
    IND = {0: "0pt", 1: "14pt", 2: "26pt"}
    for b in sl.blocks:
        if b.kind == "bullet":
            lv = marker_level(b)
            # flush left, no hanging indent (wrapped lines align at the left margin)
            lines.append(rf"\par\smallskip\noindent\hangindent=0pt\hspace*{{{IND[lv]}}}"
                         rf"{MARK[lv]}~{inline_tex(b.text)}")
            item_open = True
        elif b.kind == "eq":
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
        elif b.kind == "fig" and os.path.exists(b.text):
            cap = (r"\\[0.2ex]{\footnotesize\itshape %s}" % tex_escape(b.tag)) if b.tag else ""
            lines.append(r"\begin{center}\includegraphics[width=%.2f\textwidth,"
                         r"height=0.42\textheight,keepaspectratio]{%s}%s\end{center}"
                         % (min(b.width, 0.95), b.text, cap))
    del item_open
    return "\n".join(lines)


def strip_marks(title: str) -> str:
    return title.replace("**", "").replace("==", "")


def build_tex(slides, args) -> str:
    theme = (getattr(args, "beamer_theme", "") or DEFAULT_THEME).strip()
    ctheme = (getattr(args, "beamer_colortheme", "") or DEFAULT_COLORTHEME).strip()
    plain = theme.lower() in ("", "none", "default")

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

    out = [r"\documentclass[aspectratio=169,10pt]{beamer}", use, pre,
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
        out.append(slide_body_tex(sl))
        if sl.notes:
            out.append(r"\note{" + tex_escape(" ".join(sl.notes)) + "}")
        out.append(r"\end{frame}")
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
