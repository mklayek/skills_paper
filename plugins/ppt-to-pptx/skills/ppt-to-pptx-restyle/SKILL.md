---
name: ppt-to-pptx-restyle
description: Use when the user wants to restyle or rebuild an existing PowerPoint (.pptx) into a clean styled deck while keeping the exact content — "restyle this ppt", "mirror this pptx", "same texts and figures, new style", "keep the source text formatting, only change the layout", "convert screenshots of text/equations to real text", "make a proper deck from this old ppt". Produces a slide-for-slide styled PPTX where nothing (text, figures, or tables) is left behind. Two modes: MKL-equation restyle, and faithful source-format-preserving restyle.
---

# ppt-to-pptx-restyle — rebuild an old PPTX into a clean styled deck

## Overview

Turn a messy source `.pptx` into a clean, styled deck that is a **slide-for-slide mirror**:
same text, same figures, same tables — only the layout/styling changes. **Nothing is left
behind.** Text the source baked into **screenshot images** is turned back into real editable
text; genuine diagrams/charts are kept as figures; real PowerPoint tables are carried over as
real tables.

There are **two build modes** — pick the one the user asks for:

| Mode | Text styling | Equations | Use when |
|---|---|---|---|
| **A — MKL restyle** | Re-typeset in the MKL lecture style (Times/Cambria, house colours) | Native OMML via **ppt-mkl** | "make it our lecture style", methods/paper decks, equation-heavy |
| **B — Source-format-preserving** | **Exact source fonts / sizes / word colours** kept; only the textbox/layout changes | Kept as source runs (or re-authored) | "keep the text as in the source, just change the layout / textbox", two-column layout |

**Mode A uses the `ppt-mkl` sub-skill** to build (native equations + Beamer). **Mode B is a
self-contained python-pptx builder** (`build_source_style.py`) — no ppt-mkl, no LaTeX.

## Shared steps (both modes)

1. **Extract** verbatim text + every per-slide image via slide relationships (catches
   grouped/embedded images that a picture-shape walk misses):
   ```bash
   python scripts/extract_pptx.py "<src.pptx>" "<out_dir>"
   # -> <out>/text/all_text.md   and   <out>/figures/slideNN_rMM.<ext>
   ```
   Convert any `.tiff` figures to `.png` (use `os.listdir`, **not** `glob`, if the output path
   contains `[...]` brackets — glob treats them as a character class).

2. **Render the source slides** to PNG so you and the QA agents can see each one exactly:
   ```bash
   soffice --headless --convert-to pdf --outdir <out> "<src.pptx>"
   pdftoppm -png -r 100 -f <first> -l <last> "<out>/<src>.pdf" <out>/srcslides/s
   ```

3. **Map every source slide** before building — for each slide count: editable text boxes +
   chars, tables, and embedded images. This tells you which slides hold text vs
   screenshots vs tables, so nothing is missed:
   ```python
   for sh in slide.shapes:            # recurse GROUPs
       sh.has_text_frame / sh.has_table / shape_type == PICTURE
   ```

---

## Mode A — MKL-equation restyle (native OMML via ppt-mkl)

**REQUIRED SUB-SKILL:** `ppt-mkl` turns a `.deck` into a styled PPTX + Beamer PDF with native
equations. This mode produces the faithful `.deck`.

4A. **Transcribe screenshot text/equations (agents).** Dispatch subagents (≈7 slides each) to
   READ the rendered PNGs and return, per slide, a block in this exact format:
   ```
   === SLIDE n ===
   TITLE: <slide title>
   - <verbatim bullet, exactly as written, no rewording>
   $$ <LaTeX for any displayed equation> $$
   KEEP: <genuine-diagram fig files to keep; montage if several>
   ```
   Transcribe **verbatim** (incl. typos), equations→LaTeX, Greek/symbols as inline math
   (`$\chi$`, `$\mu_0$`), ignore watermark/slide-number/footer. `KEEP:` lists only **genuine
   diagrams** (not the text/equation screenshots — those are now typed). Save to
   `<out>/overrides.txt`.

5A. **Build the `.deck`** → **sanitize** → **build with ppt-mkl**:
   ```bash
   python scripts/build_mirror_deck.py "<src.pptx>" "<out>" <out>/overrides.txt <out>/deck/mirror.deck
   python scripts/sanitize_deck.py <out>/deck/mirror.deck        # LaTeX-safe (see gotchas)
   S=~/.claude/plugins/.../ppt-mkl/scripts
   python "$S/build_styled_slides.py" mirror.deck --out out.pptx --title "…" --author "…" --foot "…"
   python "$S/deck_to_beamer.py"     mirror.deck --out-dir out --name mirror --title "…" …
   ```
   Omit `--title` if you will splice your own full-bleed title slide (otherwise you get **two**
   title slides).

---

## Mode B — Source-format-preserving restyle (the two-column faithful build)

Use when the user says the generated text must look **exactly like the source** (font type,
size, word colour, arrows, highlighters) and only the **textbox / layout** should change. The
canonical layout the user asked for: **body text in one tall-narrow box on the LEFT, figures
on the RIGHT**, with a restyled title bar + rule + footer as chrome.

The whole build is `scripts/build_source_style.py` (python-pptx). Author the per-deck dicts at
the top after inspecting the slides, then run it. It **guarantees nothing is left behind** by
capturing, per source slide: **editable text (copied run-for-run) + tables + every embedded
image.**

### The five content cases (decide per slide from the step-3 map)

1. **Editable text present** → copy the source paragraphs run-for-run into ONE left text box
   (preserves font/size/colour exactly). Figures montaged on the right; full-width if no figure.
2. **Body is a TEXT screenshot** (source has 0 editable text; the words live inside an image) →
   **re-author** the text as real runs matching the screenshot's formatting (colours, italic,
   arrows, red bullets) via the `RICH_BODY` dict. **Do NOT paste the screenshot** — the user
   explicitly rejects text-as-image.
3. **Body is a TABLE screenshot / real table** → rebuild it as a **native table**. If the source
   has a real `graphicFrame` table, deep-copy it and **scale the `<a:gridCol>` widths** to fit
   (otherwise it overflows the slide edge). If the table is only an image, author it natively
   (`build_table10`-style: header fill, zebra rows, red labels where the source is red).
4. **Genuine figure/chart/diagram** (bar chart, current-flow diagram, cross-section) → keep as an
   image. These are NOT "screenshots of text"; a chart cannot go in a text box. Fill the body if
   the slide has no real text; two-column if it has a caption/heading.
5. **Multi-line / long source title** (e.g. a coloured case-study heading stored inside the title
   placeholder with vertical-tab breaks) → push it into the BODY so it is not lost; the title bar
   uses a clean curated one-liner.

### Build + verify

```bash
python build_source_style.py            # writes the pptx into the build folder + copies to deliverable
soffice --headless --convert-to pdf --outdir verify out.pptx
pdftoppm -png -r 110 verify/out.pdf verify/out
```

Then run the **mandatory check-agents** (see below) and iterate until they report **clean**.

---

## The golden rules (Mode B — the user's standing rules)

- **Never leave any text or figure behind.** Every source slide's text (editable **and**
  table **and** screenshot-baked) and every figure must appear in the output. Verify at the end.
- **Body text = one single text box**, exact source formatting (font type, size, word colour,
  arrows, highlighters). Only the textbox/layout is new.
- **Text is never shown as a screenshot.** If the source baked text into an image, re-author it
  as real runs with the same formatting. Screenshots are only for genuine figures/charts/diagrams.
- **Tables are real tables** (native), never an image; scale column widths so they never clip.
- **Two-column layout**: tall-narrow text box left (`vertical > horizontal`), figures right.
  When a slide has no real text, the figure/table fills the body instead.
- **Title bar = clean curated one-liner** (chrome). Source running titles ("Resistivity Method",
  "Hydrogeophysics") are messy/repetitive — do not use them verbatim in the bar; but keep any
  long/coloured multi-line source title as body content.
- **Filter chrome**: drop `MKL`, `Class NN – (Hydro)Geophysics`, slide numbers, empty boxes.
  Watch for near-duplicates (`Class 01 – HydroGeophysics`) that slip a strict regex.
- **Clean control chars** (`\x0b` vertical tab used as a line break in some titles) → space,
  or they render as tofu (`x000B`).
- **First/Thank-you slides**: splice full-bleed image copies of another deck's title/thankyou
  when the user asks ("first and thank-you slide follow <deck>"). Aspect must match (16:9).

## Verification with check-agents (MANDATORY — the user requires this every time)

After **every** build, dispatch **check-agents** (≈10 slides each) that READ the source-slide
PNG and the generated-slide PNG side by side and report, per slide:

```
SLIDE <src> (-> out-MM): OK | ISSUES:
- BLANK: generated body entirely missing?
- Missing text/figure/table vs the original?
- Formatting mismatch (a coloured word / italic / bold / red table row that differs)?
- Layout: cut off, overlapping, unreadable?
```

Tell the agents what is *intentional* (cleaned title bar; dropped MKL/footer/number; a genuine
chart kept as an image) so they only flag real regressions. **Fix every issue and re-run the
check-agents until all ranges report `clean`.** This loop is how the "nothing left behind" rule
is enforced — a python-pptx text walk silently misses tables, embedded images, and title-placeholder
content, so visual QA is the only reliable check.

## Gotchas (learned the hard way)

- **Two extraction methods are complementary.** Picture-shape walks miss embedded/grouped images;
  `slide.part.rels` catches them. A shape-walk also **misses tables and title-placeholder text** —
  always cross-check with the rendered slide and the check-agents.
- **Screenshot text is invisible to extraction** — it is inside an image. In Mode B it must be
  re-authored as runs; in Mode A transcribed to LaTeX. Never leave it as a picture.
- **python-pptx can't see shapes wrapped in `mc:AlternateContent`** (any text box that contains
  OMML math). Such a slide looks "blank" to python-pptx **and to LibreOffice's preview**, but the
  text is present and renders fine in real PowerPoint — confirm by grepping the slide XML, don't
  trust the preview.
- **LibreOffice/Impress drops OMML mixed with text** in its preview (renders blank). Verify
  equations via the slide XML or a LaTeX render, never the Impress raster.
- **Deleting a slide with python-pptx orphans its part** → duplicate `slideN.xml`. Instead
  *replace* a slide's shapes or only *add* slides; move slides via `sldIdLst.insert`.
- **Deep-copied tables** keep their native column widths → overflow. Scale `<a:gridCol w>` by
  `target_width / native_width`. Table styles referenced by GUID may not exist in the new deck
  (renders with a default style — content is fine).
- **`normAutofit`** on the body box lets PowerPoint shrink text that would overflow the narrow
  left column while keeping the authored size where it fits.
- **`[...]` in a path breaks Python `glob`** (character class) — use `os.listdir` or `glob.escape`.
- **`sed -i` / `perl -pi` are unreliable in Git-Bash here** — do in-place edits in Python.
- **LaTeX-unsafe chars (Mode A only, `sanitize_deck.py`)**: Wingdings arrow `U+F0E0`→`$\rightarrow$`,
  Unicode minus `U+2212`→`-`, `~`→`$\sim$`, and all figure paths → forward slashes. Do **not** run
  this sanitizer on a Mode-B deck or on LaTeX-bearing text — its global `\`→`/` corrupts `\frac`.
