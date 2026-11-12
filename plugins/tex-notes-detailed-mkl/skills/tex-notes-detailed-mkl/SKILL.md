---
name: tex-notes-detailed-mkl
description: Detailed two-column, colored scientific notes (LaTeX -> PDF) with computed figures, TikZ diagrams, full derivations and discussion, no page limit. Use when the user asks for "detailed notes", "scientific notes with figures", "notes in the detailed style", or wants an existing short note expanded into a full study/reference document. Abbreviations are expanded only at first use (acronym package); references go on a separate final page.
---

# tex-notes-detailed-mkl: detailed two-column scientific notes (PDF via LaTeX)

The detailed sibling of `tex-notes-mkl`. Where `tex-notes-mkl` keeps notes short and
page-limited, this skill writes a **full reference document**: physics first, then the
math with every term explained, then the nuances, worked numbers and computed figures.
**There is no page limit** unless the user gives one.

## 1. House style

- **Language:** US English (meter, color, modeling, analyze); proper names and quotes as printed.
- **Layout:** `article`, 11 pt, A4, **two columns**, margins 1.4 cm, column gap 0.6 cm,
  `\pagestyle{plain}` (page numbers at the bottom center), `\raggedbottom`.
  Sections flow on in the columns; do not force a new page or a full-width
  `\twocolumn[...]` header except for the title block and the final references page.
  Wide multi-panel figures are redrawn at one-column size rather than spanning both columns.
- **Font:** Latin Modern (`\usepackage[T1]{fontenc}` + `\usepackage{lmodern}`), as the
  project rule for every TeX PDF.
- **Colors:**
  | name | hex | used for |
  |---|---|---|
  | navy | `0B2A55` | title, section headings, plain-words box |
  | deepblue | `1D4ED8` | subsections, "physics" boxes |
  | deepred | `B91C1C` | `\key{...}` phrases |
  | deepgreen | `15803D` | key-message box, worked examples |
  | violet | `6D28D9` | nuance boxes |
  | amber | `B7791F` | "My work" / application boxes |
- **Boxes (tcolorbox):**
  - `keybox` (green): "Three messages" near the start;
  - `nuance` (violet): pitfalls, caveats, alternative meanings;
  - `worked` (green, titled): a worked numerical example with the numbers computed in Python;
  - `mybox{title}` (amber, titled): applications / own work;
  - final navy `tcolorbox`: "The whole story in plain words".
- **Tone:** spoken-natural but complete. Physical picture first, then equations, then
  "Reading it", then nuances. Short paragraphs and bullets, but do not cut content.

## 2. Abbreviations: full form only at first use

- Use the **`acronym`** package (`\usepackage{acronym}`). Define every abbreviation once,
  without printing a list, with `\acrodef` right after `\begin{document}` (do NOT wrap
  `\acro` in a `\setbox`/group: the definitions are then local and vanish):
  ```latex
  \acrodef{GPR}{ground-penetrating radar}
  \acrodef{CRIM}{complex refractive index model}
  ```
  Compile three times (the package uses the `.aux` file); the log must have no
  "Acronym ... is not defined".
- In the text write `\ac{GPR}`: first use prints "ground-penetrating radar (GPR)", every
  later use prints "GPR". Plural: `\acp{}`. Start of sentence: `\Ac{}`.
- **Headings, figure captions, TikZ nodes and tables use `\acs{}`** (short form only), so
  they never consume or show the first expansion. The first `\ac{}` in body text expands.
- Verify after the build: search the PDF text (`pdftotext`) for each full form; it must
  appear exactly once (except where the words are used naturally in prose).
- Expand only abbreviations whose full form is certain. Brand or software names
  (GSSI, MALA, SPECFEM) and network names without an official expansion stay as written.

## 3. Structure

1. Title block across both columns: topic, one-line subtitle.
2. **The big picture** + green `keybox` with 3-4 messages.
3. One section per topic, each with:
   - physical picture (1 paragraph);
   - equation(s) with numbers, then **"Reading it"** bullets (each term, signs, powers,
     limits);
   - **worked numbers** (computed in Python, marked "computed");
   - a **nuance** box where the topic has pitfalls;
   - an amber **application / my work** paragraph when relevant;
   - figures: computed (matplotlib) or TikZ, at `\columnwidth`, numbered `\small` caption
     (`\figcap`, see Section 4b), text inside at least 10 pt (Section 5).
4. Bridging / discussion sections the user asks for (definitions, terms unpacked,
   project ideas, question-and-answer points).
5. **Summary table** (`booktabs`, `\footnotesize`): Eq. | What it is | Why it matters.
6. **Plain-words box.**
7. **References on a separate final page** (`\clearpage` before the reference list),
   numbered [1], [2] ... in order of the list, cited as [n] in the text.

## 4. Equations

- `amsmath`; long ones in `multline`/`gather` so the number never wraps.
- Manual numbers with `\tag{}`. When adding equations to an existing note, use
  lettered tags (`3b`, `3c`) so earlier cross-references stay valid.
- Check every claim numerically in Python before writing it (limits, examples, errors).

## 4b. Cross-references: Eq., Table, Fig.

- **Equations:** always `Eq.~(15)` in the text, never a bare `(15)`; several: `Eqs.~(21)--(24)`,
  `Eqs.~(3), (3b) and (8)`. Write "the misfit in Eq.~(15)", "from Eq.~(17)", "Eq.~(46) says".
  This also holds in captions, tables, TikZ labels and `\text{}` inside equations.
  The `\tag{}` numbers themselves and the "Eq." column of the summary table stay bare.
- **Tables:** numbered `Table~1`, caption above the table, referenced as `Table~\ref{tab:x}`.
- **Figures:** numbered `Fig.~1`, caption below, referenced as `Fig.~\ref{fig:x}`, panels
  as `Fig.~\ref{fig:x}(b)` or `Figs.~3(a)--(b)`. Never "the figure", "the table", "panel b".
- In the two-column layout (no floats), use counters and caption macros:
  ```latex
  \newcounter{figno}\newcounter{tabno}
  \newcommand{\figcap}[2]{\refstepcounter{figno}\label{#1}{\small\textbf{Fig.~\thefigno.} #2}}
  \newcommand{\tabcap}[2]{\refstepcounter{tabno}\label{#1}{\small\textbf{Table~\thetabno.} #2}\par\smallskip}
  ```
  Captions at `\small` (10 pt). Wrap each figure + caption, and each table caption +
  table, in `\begin{minipage}{\columnwidth}` so a caption never lands in the next column.
- When converting an existing note, rewrite the references with a script (collect all
  `\tag{}` values, match groups joined by `--`, `,`, `and`, `or`, `through`; skip the
  summary table, references list and false hits such as "soil (1) and target (2)"), then
  proofread the result for awkward phrasing.

## 5. Figures

- matplotlib: `font.family='serif'`, `mathtext.fontset='cm'`, dpi 200,
  colors `#B91C1C #1D4ED8 #15803D #6D28D9 #B7791F`, legends clear of curves.
- **All text in figures, graphs and flow charts is at least 10 pt as printed** (body text,
  equations and headings keep their normal sizes):
  - matplotlib: draw at the **printed size**: `figsize` width = the printed width
    (3.45 in for one column of this layout, the minipage width for wider figures),
    `font.size` 10, every `fontsize=` at least 10. Then include at `\columnwidth`
    (scale about 1), so 10 pt in the script stays about 10 pt on the page. Never
    shrink a wide figure into a column.
  - Use `layout="constrained"` and put legends **outside** the axes
    (`fig.legend(loc="outside lower center", ncol=2)`) when they would cover curves;
    use short legend labels and shorter panel titles; stack two-panel plots vertically.
  - TikZ: `\small` (10 pt in an 11 pt document) or larger for every node and label,
    never `\scriptsize`/`\tiny`; widen `text width`/spacing so labels do not overlap.
  - Raster diagrams with small text that cannot be regenerated (screenshots, exported
    slides): redraw them as TikZ, cropping image panels out of the original if needed.
  - Check the size: a PNG's printed width = pixels / dpi; the scale factor is
    printed width / figure width, and text size x scale must be at least 10 pt.
- Each figure is computed from the note's equations, or is a TikZ diagram of a workflow.
  Captions say what is shown and which equation made it; invented parameters are labeled
  "illustrative".
- Keep figure scripts next to the `.tex` (and a copy in `docs\`).

## 6. Workflow

1. Archive the previous PDF + `.tex` (`archive\<date>_<name>_r<N>\`) before changing.
2. Collect content; list abbreviations with their certain full forms.
3. Python checks, then figures.
4. Write the `.tex`; compile **twice** with `pdflatex -interaction=nonstopmode`.
5. QA: `grep -E "^!|Overfull" *.log` empty; render pages (`pdftoppm -r 60`) and look:
   no wrapped equation numbers, no label overlaps in TikZ, legends readable, references
   alone on the last page; first-use check of abbreviations; no bare `(n)` equation
   references left; every figure and table numbered, caption in the same column;
   figure text at least 10 pt.
6. Copy the PDF to its final place (if locked by a viewer, say so and keep the built copy).
7. Reply briefly: what was added, figures, any unverified item.
