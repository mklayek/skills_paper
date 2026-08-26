---
name: note-makingmkl
description: >-
  Turn source study/teaching material (a Word .docx, Markdown, PDF, or scanned pages) into a
  polished, tight, BLACK-AND-WHITE LaTeX -> PDF teaching-notes document: reorganised into a
  clean section/subsection hierarchy, with bounded KEY POINT / NOTE / RESULT / DEFINITION
  boxes, wrapping tables, in-flow figures, page numbers, native equations, and a completeness
  audit against the source. Use this whenever the user wants to MAKE or ORGANISE notes, "note
  making", turn a Word/.docx or messy notes into a clean/printable PDF, build lecture/class/study
  notes, re-typeset a document with proper sections and key-point boxes, or produce a regular
  "tex-to-pdf" style notes document -- even if they don't explicitly say "LaTeX". Prefer this over
  a plain pandoc dump whenever the goal is a well-organised, readable notes PDF (not a report or a
  slide deck).
---

# note-makingmkl — organised LaTeX teaching-notes PDFs

## What this makes
One source document (usually a `.docx`, but also `.md`, a PDF, or scanned pages) becomes a
**clean, information-dense, black-and-white PDF** that reads like a well-typeset set of class
notes: a logical hierarchy of sections and subsections, every point-wise item as a real list,
native equations, wrapping tables, figures next to their text, and important takeaways in
**bounded boxes**. Nothing from the source is lost; low-quality images are improved.

This is deliberately **not** a page-by-page conversion and **not** a slide deck. If the user
wants slides use `ppt-mkl`; if they want a formal report use the report skills. Here the goal is
*organised, readable notes*.

## The style contract (what "good" looks like)
- **Black and white**, plain "regular tex-to-pdf" look — no coloured headings or coloured box
  fills. Content figures may keep their own colours; the *typography* is B&W.
- **Tight and dense** — small margins, compact section spacing, no decorative blank space, no
  half-empty pages.
- **Bounded teaching boxes** (unbreakable) for takeaways: `KEY POINT`, `NOTE`, `RESULT & MEANING`,
  `DEFINITION`, plus a one-line strip.
- **Page numbers** on every page; bold key terms, italic emphasis; every list is a real
  `itemize`/`enumerate`; every table wraps and fills its width; every figure sits near its text.
- All of this is baked into `references/preamble.tex` and `references/authoring_rules.md` — read
  and reuse them, don't reinvent the styling.

## Workflow

Work in a NEW output folder OUTSIDE any read-only/source location (never write into a protected
source folder — read/copy *from* it). A good layout:
```
<out>/  Notes.pdf   CONVERSION_REPORT.md
        build/  main.tex  sec01..secNN.tex  (fragments)
        figs/   (processed + added figures)
        extract/  notes_pandoc.md + media/  (provenance)
```

1. **Extract the source.** `scripts/extract_source.sh <source.docx> <out>/extract` runs pandoc to
   Markdown with media extraction. **Read the whole extracted Markdown** before writing anything —
   you must understand every heading, paragraph, equation, table, list and image.

2. **Inspect the images.** List their pixel dimensions. Decide per image:
   - keep good, clear diagrams as-is (copy into `figs/`);
   - replace low-res equation/sketch crops by **typesetting the math** (or a small TikZ sketch) —
     crisper than a blurry image;
   - re-typeset **scanned/photographed tables**: de-rotate the scan, READ the values, and rebuild
     a clean LaTeX table (keep a cropped copy of the original only if useful);
   - if a better, scientifically-correct figure already exists (e.g. one you made earlier), use it.
   Record every keep/replace decision for the report.

3. **Organise into a hierarchy.** Group the content into a teaching flow: main topic → section →
   subsection → explanation → figure/table/equation → key takeaway. Retain ALL facts; drop only
   URL-citation link dumps and emoji.

4. **Set up the build.** Copy `references/preamble.tex` into `<out>/build/main.tex` (or `\input`
   it). Define `\figpath` (absolute path to `figs/`) and `\runningtitle` before `\begin{document}`.
   Give the document a title and `\input{secNN.tex}` for each section.

5. **Write the LaTeX.** Follow `references/authoring_rules.md` exactly (Unicode→math, verbatim
   equations, wrapping `tabularx` tables, `[H]` in-flow figures/large tables, the box environments).
   For a large source, this parallelises well — see "Multi-agent" below.

6. **Compile & verify.** `pdflatex main.tex` twice. A good build has **0 overfull boxes, no
   undefined references, no missing figures**. Then render pages and check them (see checklist).

7. **Completeness audit.** Compare the PDF against the source: every heading, paragraph fact,
   equation, table, list, keynote and numeric fact must be present. Fix any gaps and recompile.

8. **Report.** Write a short `CONVERSION_REPORT.md` (structure, images kept/replaced, verification
   status). Copy the final PDF to `<out>/Notes.pdf` (or a descriptive name).

## Verification checklist (render the pages and look)
- No **split boxes** (a box with only its title + one line at a page bottom) — the boxes are
  unbreakable, so this shouldn't happen; if a box left a large gap, that's acceptable.
- No **sparse float pages** — a figure/table alone on a page with big empty bands means it floated;
  re-place it with `[H]`.
- No **white gaps inside tables** — text-heavy cells must wrap (raggedright `X` columns); wide
  numeric tables should fill the width.
- Equations render (native, not Unicode text), captions present, page numbers on every page,
  headings/boxes are black-and-white, spacing is tight.

## Multi-agent (Mode A, for large sources)
When the source is long, dispatch **one subagent per section**, in waves (e.g. 5 at a time). Give
each agent: `references/authoring_rules.md`, the exact source line-range for its section, the figure
filenames + captions to use, and the target fragment path. Each returns a `\input`-able `.tex`
fragment (no preamble). Then you assemble under `main.tex`, compile, and fix. This keeps equation
fidelity (agents reuse the source's LaTeX math verbatim) while parallelising the prose. A final
completeness-audit agent comparing source vs fragments is a good last step.

## Common failure modes and fixes (learned the hard way)
- **Big white bands above/below a table or figure** → it's a float on its own page, vertically
  centred. Use `\begin{table}[H]` / `\begin{figure}[H]` to anchor it in the text flow.
- **A box splits across a page** → boxes must be unbreakable (the bundled preamble already removes
  `breakable`). Don't re-add it.
- **Raw θ/α/emoji or `$` showing literally** → convert every Unicode symbol to LaTeX math; keep
  equation numbers as plain `(N)` (or `\tag{}`), not fused into the math.
- **A photographed/rotated table looks bad** → de-rotate, read the numbers, re-typeset as a real
  `longtable`. It also lets you include the *full* table, not just the excerpt.
- **Output looks "too colourful"** → the palette in the preamble maps all colour names to black;
  don't add coloured headings or box fills.

## Bundled resources
- `references/preamble.tex` — the reusable B&W, tight, page-numbered preamble with the four
  bounded box environments. Copy or `\input` it.
- `references/authoring_rules.md` — the per-fragment authoring rules (hand to section subagents).
- `scripts/extract_source.sh` — pandoc extraction (docx → Markdown + media).

## Requirements
`pandoc`, a LaTeX engine (`pdflatex` via TeX Live/MiKTeX), `tcolorbox`, and Python + Pillow for
image inspection/de-rotation. Compile locally; never modify the source/protected folder.
