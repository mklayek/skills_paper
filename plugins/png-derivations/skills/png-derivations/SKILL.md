---
name: png-derivations
description: Use when the user says "png-derivations" or asks for a derivation drawn as a single 16:9 PNG image (one-slide derivation sheet, derivation flow picture) in the numbered-heading textbook style, white background, up to three columns, every equation numbered from (1) in red after a dashed leader.
---

# png-derivations: one 16:9 PNG of a derivation flow

Trigger word: **png-derivations**. The output is one PNG (16:9) that shows a whole derivation as a
continuous flow, like a textbook worked derivation, plus its .tex and an .md copy.

## Style (the user's words always override)
- **16:9 page:** LaTeX `geometry` with `paperwidth=16in, paperheight=9in, hmargin=0.28in, vmargin=0.22in`,
  rendered with `pdftoppm -r 160 -singlefile` to 2560 x 1440 px. **White background**, a thin light-blue
  rounded frame (`7FA7D9`) around the page.
- **Up to 3 columns** (`multicols*{3}`, `columnsep` 0.3 in, light column rule). Use `\columnbreak` so no
  heading is orphaned at a column foot. Must fit on **one page**: check the log says 1 page.
- **Font: as large as fits.** Times (`newtxtext,newtxmath`), body **13.4 pt** (leading 14.9), headings
  **16.5 pt** (the title is fixed at 14 pt, see below). If it overflows, first tighten spacing (`\parskip` 0.6 pt, equation skips
  0.6 to 1 pt, heading skip 2 pt), then shorten connecting prose. Shrink the font only as a last resort.
- **Headings:** "1. Title", "2. Title" … in navy `0B2A55`, bold. **Never write the word "Step"** and
  never say "step" in the text. Just number the parts of the flow.
- **Flow:** short connecting sentences ("Therefore,", "Thus", "Divide by", "Put … into …") between
  the working lines. Show every algebra step, no skipping.
- **Equation numbers: start fresh from (1) and number EVERY displayed line in order** (1), (2), (3) …,
  including working lines and boxed results. Do **not** use the book's numbers such as (10c) or (7.12).
  Each number is **red bold after a red dashed leader**: `H = I/2πρ - - - - - - - - (2)`.
  Cross-references in the text use the new numbers through `\label`/`\ref`, always written as
  **`Eq.(n)`** with no space: `Eq.(\ref{eq:key})` renders "Matching Eq.(2)", "Put Eq.(4) into Eq.(1)".
  Never a bare "(2)" or "Equation (2)" in the prose.
- **Results:** key results in a thin red box (`\fcolorbox{deepred}{white}{...}`), also numbered.
- **Highlights:** key terms in bold blue `1D4ED8`, substitution rules in purple `6D28D9`, checks and
  notes in green `15803D`, reject/keep labels in red/green.
- **Title: always at the top middle of the image**, centered above the columns (not inside column 1),
  in **Copperplate Gothic Light 14 pt** (`C:\Windows\Fonts\COPRGTL.TTF`), **neon green `39FF14` with a
  black text border**. pdflatex cannot load that font, so the script renders the title with PIL
  (`ImageDraw.text(..., fill=(57,255,20), stroke_width≈5% of the font size, stroke_fill=black)` at
  1200 dpi, font size `14*1200/72` px) to `title.png` in the build folder and places it with
  `{\centering\includegraphics[height=<h>in]{title.png}\par}\vspace{2pt}` right before
  `\begin{multicols*}`. Plain words only in the title (no math; write "Ey", "emf").
- A one-line navy source line sits at the top of column 1 (name the source section in words, no book
  equation numbers).

## Macros (copy from the template)
```latex
\newcounter{eqc}
\newcommand{\eqnum}{\refstepcounter{eqc}\textcolor{deepred}{\leaders\hbox to 0.5em{\hss-\hss}\hfill\ \textbf{(\theeqc)}}}
\newcommand{\hd}[2]{\par\vspace{2pt}{\fontsize{16.5}{18.5}\selectfont\color{navy}#1.\ \textbf{#2}}\par\vspace{1pt}}
\newcommand{\ceq}[1]{\par\vspace{0.6pt}\noindent\hspace*{0.6em}$\displaystyle #1$\ \eqnum\par\vspace{0.6pt}}
\newcommand{\eqn}[2]{\par\vspace{1pt}\noindent\hspace*{0.6em}$\displaystyle #1$\ \eqnum\label{eq:#2}\par\vspace{1pt}}
\newcommand{\res}[1]{\par\vspace{1pt}\noindent\hspace*{0.6em}\fcolorbox{deepred}{white}{$\displaystyle #1$}\ \eqnum\par\vspace{1pt}}
```
`\eqn{...}{key}` is a numbered line with a label, cited in the text as `Eq.(\ref{eq:key})`. `\ceq{...}` is a numbered working
line. `\res{...}` is a numbered boxed result. Compile twice so the references resolve.

## Template and placement
- Working template: `D:\claudecode\TEACHING\PPT_class_kr\scripts\76_EM_long_wire_Ey_png_derivations.py`
  (long-wire E_y, 27 numbered equations in 12 parts). Copy it to the next free
  `NN_<Folder>_<name>_png_derivations.py` in the flat `PPT_class_kr\scripts\` folder, replace the TeX body
  and the MD text (keep the MD numbers equal to the PNG numbers), run it, then run
  `03_CodeDocs_build_code_docs.py`.
- Edit the script through a Python file written with the Write tool, not a bash heredoc, because the
  shell can mangle backslashes such as `\a` and `\f` in TeX.
- The PNG sits at the top of the task folder, `.tex` and `.md` in `docs\`, the pdflatex run in
  `temp\build_png\`. Archive an existing PNG before overwriting.

## QA
- Log: 1 page, 0 overfull boxes. Look at the PNG: numbers run (1), (2), (3) … with no gap, no heading at a
  column foot, no clipped equation, numbers aligned at the right edge of each column.
- Title is centered at the top, neon green with a black border, in Copperplate Gothic Light 14 pt.
- Every in-text reference reads `Eq.(n)`: `grep -n "(\\\\ref" script.py` must show only `Eq.(\ref{...})`.
- US English, no em dashes, no semicolons in prose.
