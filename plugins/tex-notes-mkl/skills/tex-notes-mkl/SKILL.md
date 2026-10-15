---
name: tex-notes-mkl
description: Build short, simplified two-column LaTeX/PDF lecture notes (11 pt, A4) that explain what a source's equations mean and why they matter, with computed figures, in Jongchan's house style.
---

# tex-notes-mkl: simplified equation-explainer notes (PDF via LaTeX)

Use this skill when the user asks for "notes", "a PDF explaining …", "simplified notes", "explain the significance of these equations and make a PDF", or gives a page limit for notes made from a textbook passage, pasted text, slides or a previous explanation. The output is always a compiled **PDF plus its .tex source**, both sent with SendUserFile.

## 1. House style (the user's words always override)

- **US English** (meter, color, analyze, modeling, gray); keep proper names, book titles and quoted text as printed.
- **Layout:** `article`, **11 pt, A4, two columns**, margins 1.4 cm, column gap 0.6 cm, no page numbers or footer (`\pagestyle{empty}`), `\raggedbottom`.
- **Fonts:** `mathptmx` (Times text and math). `lmodern` is often not installed, so do not use it.
- **Colors:** navy `0B2A55` for the title and section headings, deep blue `1D4ED8` for subsections, deep red `B91C1C` for key phrases (`\key{…}`), green `15803D` for the key-message box.
- **Boxes:** a green `keybox` near the start ("Three messages of the whole section"), and a navy `tcolorbox` at the end ("The whole section in plain words").
- **Tone:** spoken-natural, simplified, intuitive (physical picture first, then the math); short sentences and bullets. The user prefers intuitive, visual explanations and preserving the source's content over adding new material.
- **Page limit:** honor any limit the user gives (e.g. "within 2 pages", "page limit 4"). With no limit, aim for 2–4 pages.

## 2. Structure of the notes

1. **Title block** (spans both columns): topic name, plus a one-line subtitle naming the source (e.g. "after Telford, Geldart & Sheriff, *Applied Geophysics*, Sec. 8.6.3").
2. **The big idea:** one paragraph stating the question the equations answer, then the green `keybox` with 2–4 numbered take-home messages.
3. **One section per equation group, in source order.** Each section has:
   - the equation as a display, with its number;
   - **"Reading the equation"** bullets: what each term or factor *physically* is (e.g. "1 = uniform earth; 4D_w = disturbance from the lower bed; the 4 = 2 × 2 because …");
   - **why it matters / what it is used for**, with one `\key{…}` phrase.
4. **"What the equations tell us":** limiting cases (small or large parameter, special values such as k = ±1), each shown in 1–3 lines of algebra plus its physical meaning.
5. **"Using it on field data" / practical significance:** how the result is used, from crude interpretation through proper methods (e.g. master curves, inversion).
6. **Bridging sections the user asks about** (e.g. "Are these equations used to make master curves?"): add them as their own section, covering how it is made, the physical significance, why it works, the procedure, and modern practice.
7. **Summary table** (`booktabs`, `\footnotesize`/`\small`, `\tabcolsep` 4 pt): columns *Eq.* | *What it is* | *Why it matters*.
8. **Closing "in plain words" box:** one paragraph tying the whole chain together, from physics to measurable quantity to interpretation.

## 3. Equations

- Include **every equation the source gives** in the covered passage, typeset in LaTeX (`amsmath`). Use `multline` or `align` for long ones so the equation number never wraps onto its own line.
- **Numbering:** use the source's numbers **without the chapter prefix**: (8.38) becomes (38), (8.39b) becomes (39b). Use `\tag{…}`. Book section cross-references become plain words ("the method of images"), never "Sec. 8.3.4".
- When a derivation step is short and helps, show it (e.g. the geometric series Σkᵐ = k/(1 − k) and its substitution for each array).
- **Verify algebra numerically** in Python before writing a claim (limits, worked numbers, approximation errors).
- If an OCR'd source is garbled, rebuild the equation from the physics, check it numerically against the limits, and state any constant you could not confirm (e.g. "a similar result (42c) for the double-dipole").

## 4. Figures (computed, not decorative)

- Make 1–3 **matplotlib** figures that are computed from the note's own equations: e.g. curve families against a dimensionless parameter, a recomputed book example, or a "same shape, only shifted" demonstration.
- Style: `font.family='serif'`, `mathtext.fontset='cm'`, figsize about 5.2 × 4 in, dpi 200, deep colors (`#B91C1C`, `#1D4ED8`, `#15803D`, `#6D28D9`), log axes where the physics is scale-free, dotted asymptote lines, legend placed clear of the curves.
- Insert each figure at `\columnwidth`, with a `\footnotesize` caption saying what it shows and which equation produced it.
- Add a small **numbers table** where it builds intuition (e.g. ρa/ρ₁ at a/z = 0.25, 1, 4, 20 for k = ±0.5), followed by a one-line **Lesson**.
- mathtext pitfall: inside an f-string or a plain string, write `r'…\rho…'` so that `\r` does not become a carriage return.

## 5. Preamble template

```latex
\documentclass[11pt,a4paper,twocolumn]{article}
\usepackage[a4paper,margin=1.4cm,columnsep=0.6cm]{geometry}
\usepackage[T1]{fontenc}\usepackage{mathptmx}\usepackage{amsmath,amssymb}
\usepackage{graphicx,booktabs,enumitem,xcolor,titlesec,tcolorbox,array}
\definecolor{navy}{HTML}{0B2A55}\definecolor{deepred}{HTML}{B91C1C}
\definecolor{deepblue}{HTML}{1D4ED8}\definecolor{deepgreen}{HTML}{15803D}
\titleformat{\section}{\large\bfseries\color{navy}}{\thesection}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries\color{deepblue}}{\thesubsection}{0.5em}{}
\titlespacing*{\section}{0pt}{6pt}{2pt}\titlespacing*{\subsection}{0pt}{4pt}{1pt}
\setlist{nosep,leftmargin=1.2em}
\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}
\setlength{\abovedisplayskip}{4pt}\setlength{\belowdisplayskip}{4pt}
\tcbset{colback=navy!4,colframe=navy,boxrule=0.6pt,arc=1pt,left=3pt,right=3pt,top=2pt,bottom=2pt}
\newtcolorbox{keybox}{colback=deepgreen!5,colframe=deepgreen,boxrule=0.6pt,arc=1pt,left=3pt,right=3pt,top=2pt,bottom=2pt}
\newcommand{\key}[1]{\textbf{\color{deepred}#1}}
\pagestyle{empty}\raggedbottom
\begin{document}
\twocolumn[{\begin{center}
{\LARGE\bfseries\color{navy} TITLE}\\[2pt]
{\small Simplified notes --- SUBTITLE (after AUTHOR, \emph{BOOK}, Sec.~X)}
\end{center}\vspace{2pt}}]
% sections ...
\end{document}
```

## 6. Fitting a page limit

Apply these in order until it fits, without dropping the user's content:
1. `\parskip` 2 pt, tighter `\titlespacing`, display skips 3 pt.
2. Figures at 0.65–0.8 `\columnwidth`.
3. Margins down to 1.3 cm and `columnsep` 0.6 cm.
4. Tables at `\footnotesize` with `\tabcolsep` 3–4 pt.
5. Merge restated equations; shorten bullets, but keep every fact.

`flushend` balances the last page but can open large gaps mid-document, so if columns show gaps, remove it and use `\raggedbottom`.

## 7. Workflow

1. Say in one sentence what you are building, then start.
2. Read the source (an attachment or pasted text; for a PDF use `pdftotext`, and read page images for garbled equations). List every equation and its number.
3. Run the numeric checks in Python (limits, sample values, errors), then make the figures.
4. Write the `.tex`, then compile it **twice**: `pdflatex -interaction=nonstopmode notes.tex`.
5. **QA (required):**
   - `grep -E "^!|Overfull" notes.log` must be empty.
   - `pdfinfo notes.pdf | grep Pages` must be within the limit.
   - Render with `pdftoppm -r 55 -png`, paste the pages into one contact sheet, and **look at it**: no wrapped equation numbers, no column gaps, no overlapping legends, figures readable.
   - US-English scan of the `.tex` prose (metre, colour, behaviour, analyse, centre …). siunitx macros such as `\metre` are fine.
6. Deliver the **PDF and the .tex** with SendUserFile, plus a short reply covering:
   - what the notes cover;
   - the computed figures;
   - any constant or step that could not be confirmed from the source;
   - the equation-numbering convention.

   No step-by-step recap.

## 8. Content rules

- Stay faithful to the source: keep its numbers, names, figure references and equations. Mark anything added (worked numbers, computed curves, error estimates, recomputed book examples) as computed or illustrative in the caption or text.
- Explain the **physical significance** of every equation, not just its algebra: what each term represents, why it has its form (powers, factors, signs), its limiting behavior, and how it is used in practice.
- When the user follows up with a conceptual question about the same topic, answer it in chat; if they then ask to include it, add it as a new section and update the summary table and closing box.
