---
name: ppt-to-pptx-restyle
description: Use when the user wants to restyle or rebuild an existing PowerPoint (.pptx) into the clean MKL lecture style while keeping the exact content — "restyle this ppt", "mirror this pptx", "same texts and figures, new style", "convert screenshots of equations to real text", "make a proper deck from this old ppt". Produces a slide-for-slide styled PPTX + Beamer PDF with verbatim text, native editable equations, and the original figures.
---

# ppt-to-pptx-restyle — mirror an old PPTX into the MKL style

## Overview
Turn a messy source `.pptx` into a clean, styled deck that is a **slide-for-slide mirror**:
same text, same figures, only the styling changes. Text that the source baked into **screenshot
images** (definitions, equations) is transcribed into **real editable text and native equations**.
Genuine diagrams are kept as figures. Final build uses the **ppt-mkl** skill (native OMML equations
in the PPTX, plus a Beamer PDF).

**REQUIRED SUB-SKILL:** the actual PPTX/Beamer build is done by `ppt-mkl` (it turns the `.deck`
into PPTX + Beamer). This skill produces the faithful `.deck` and figures for it.

## When to use
- "restyle / rebuild / mirror this pptx", "same texts and figures but new style".
- The source has equations/definitions as **image screenshots** that should become real text.
- You want one styled slide per source slide (not a reorganised summary).

## Workflow

1. **Extract** verbatim text + every per-slide image (via slide relationships, which catches
   grouped/embedded images picture-shape walks miss):
   ```bash
   python scripts/extract_pptx.py "<src.pptx>" "<out_dir>"
   # writes <out>/text/all_text.md and <out>/figures/slideNN_rMM.<ext>
   ```

2. **Render the source slides** so you (and transcription agents) can see exactly what is on each:
   ```bash
   soffice --headless --convert-to pdf --outdir <out> "<src.pptx>"
   pdftoppm -png -r 90 <out>/*.pdf <out>/srcslides/s
   ```

3. **Transcribe the screenshot text/equations (agents).** Most old decks bake content into
   red-bordered text/equation boxes. Dispatch several subagents (≈7 slides each) to READ the
   rendered slide PNGs and return, per slide, a block in this exact format:
   ```
   === SLIDE n ===
   TITLE: <slide title>
   - <verbatim bullet, exactly as written, no rewording>
   $$ <LaTeX for any displayed equation> $$
   KEEP: <fig files to keep as the slide's figure(s); montage if several>
   ```
   Rules for agents: transcribe **verbatim** (including typos), turn equation images into LaTeX,
   write Greek/symbols as inline math (`$\chi$`, `$\theta$`, `$\mu_0$`), ignore the "MKL"
   watermark / slide number / repeated footer. In `KEEP:` list only the **genuine diagram**
   files (bar magnet, graphs, block diagrams) — NOT the text/equation screenshots (those are now
   typed). Save all blocks to `<out>/overrides.txt`.

4. **Build the mirror `.deck`** (verbatim text + native equations + kept figures, multi-figure
   slides auto-montaged):
   ```bash
   python scripts/build_mirror_deck.py "<src.pptx>" "<out_dir>" <out>/overrides.txt <out>/deck/mirror.deck
   ```

5. **Sanitize for LaTeX** (paths + a few Unicode chars that break pdflatex):
   ```bash
   python scripts/sanitize_deck.py <out>/deck/mirror.deck
   ```

6. **Build with ppt-mkl** (native OMML PPTX + Beamer), title/subtitle from the source's own title
   slide:
   ```bash
   S=~/.claude/plugins/.../ppt-mkl/scripts    # the ppt-mkl skill scripts dir
   python "$S/build_styled_slides.py" mirror.deck --out out.pptx --title "<src title>" --subtitle "<src subtitle>" --author "<src author>" --date "<date>" --foot "<label>"
   python "$S/deck_to_beamer.py"     mirror.deck --out-dir out --name mirror --title ... --subtitle ... --author ... --foot ...
   ```

7. **Verify:** compile the Beamer tex directly (`pdflatex -interaction=nonstopmode …`) and confirm
   `0 errors`; render a few pages and check that equations render natively (not as tofu), figures
   appear (no path-in-a-box), and each source slide is mirrored.

## Gotchas (learned the hard way)
- **Two extraction methods are complementary.** Picture-shape walks miss embedded/grouped images;
  `slide.part.rels` (used here) catches them. Some diagrams live only in one, some in the other.
- **Screenshot text is invisible to extraction** — it is inside an image. It MUST be transcribed
  by eye/agent (step 3), or the "text" stays a picture.
- **One figure per slide** in ppt-mkl → montage a slide's multiple diagrams into one image
  (`build_mirror_deck.py` does this), excluding any text-box screenshot.
- **LaTeX-unsafe characters** (fix with `sanitize_deck.py`): Wingdings arrow `U+F0E0` → `$\rightarrow$`;
  Unicode minus `U+2212` → `-`; `~` (approx) → `$\sim$`; and **all figure paths must use forward
  slashes** (Windows backslashes make LaTeX show the path in a box). The PPTX (python-pptx) tolerates
  these, only Beamer/pdflatex breaks — always verify the Beamer build, not just the PPTX.
- **`sed -i` / `perl -pi` are unreliable in Git-Bash here** — do in-place text edits in Python.
- Keep the source's own **title/subtitle/author** (from its title slide) for the styled deck.
