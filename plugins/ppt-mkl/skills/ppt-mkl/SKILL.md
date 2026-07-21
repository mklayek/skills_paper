---
name: ppt-mkl
description: Use when asked to build a research presentation, slide deck, PPTX, or Beamer PDF from a paper section, methods document, or report — especially in the MKL lecture style with underlined titles, checkbox bullets, numbered equations and figure slides.
---

# ppt-mkl — MKL lecture-style slide decks

## Overview

One plain-text source (`.deck`) renders to **four** artefacts that all look the same:
**PPTX** (native editable equations), **Beamer PDF**, **.tex**, and **.md**.

**Core principle: never hand-build slides with python-pptx and never fake maths with
Unicode.** Equations must be native Office-Math (OMML) so they stay editable and print
correctly. The scripts here do that via pandoc; writing your own builder loses it.

## When to Use

- "make slides / a deck / a PPTX / a presentation" from a methods, paper or report section
- "same style as the CCT→DCT→LCCF deck", "lecture style", "like our other decks"
- a Beamer PDF or `.tex` is wanted alongside (or instead of) the PPTX
- **Not** for: a document/report PDF (use the `md_pipeline` read-doc tools instead)

## Workflow

1. **Read the source** section fully before writing any slide.
2. **Write a `.deck` file** in the mini-language — read `DECK_SPEC.md` (in this skill
   directory) for the complete syntax and the authoring rules. For a long source,
   dispatch one subagent per section, each handed `DECK_SPEC.md` and a line range.
3. **Build** both back-ends (commands below).
4. **Verify** — render the PPTX to PDF and look at several slides.

## Quick Reference — the deck language

| Line | Renders as |
|---|---|
| `# Section title` | section-divider slide |
| `== CCT : Topic with **red** phrase` | new slide + underlined title |
| `- text` | ☑ green checkbox statement |
| `-- text` / `--- text` | ✪ red star / ▪ sub-levels |
| `$$ latex $$ (7)` | centred equation + red `---(7)` in its own right-margin box |
| `!key:` / `!so:` | bold takeaway / purple Segoe Script "Therefore…" |
| `!fig: /abs/f.png 55%` | bottom-anchored figure |
| `!ref: Author (year). Title. Journal…` | reference entry — dark blue italic Comic Sans, fixed 20 pt |
| `!note:` | speaker note |

Inline: `$math$` · `**maroon term**` · `==yellow highlight==` · `@@Author (year)@@` citation

A bullet that **opens with maths** (`$a>0$ — continuous scale`) is auto-detected as a
term definition and gets the ✪ star; a bullet opening with prose keeps the ☑.

## Equation pretext — REQUIRED

**Every `$$…$$` is immediately preceded by a `-` statement saying what the equation
establishes, ending in a PLAIN connecting phrase and a colon.** Emphasis goes on the
substance, never on the connector — bold the phrase naming what the equation makes
explicit, defines, estimates or bounds. That phrase renders dark brown.

```
- Writing the atom directly in the frequency plane at integer scale $j$, in polar
  coordinates $(r,\vartheta)$, makes the **discrete construction explicit**, given by:
$$ \tilde U_{j,\ell}(\omega)=\tilde W_j(\omega)\,\tilde V_{j,\ell}(\omega) $$ (18)
```

| | |
|---|---|
| ✅ | `…makes the **discrete construction explicit**, given by:` |
| ❌ | `…makes the discrete construction explicit, **given by:**` — connector bolded, substance plain |
| ❌ | `**Given by:**` — no description at all |

Connectors, always **plain** and ending in `:` — vary them so the deck does not read
mechanically, and pick the one that fits the sentence grammatically:
`given by:` · `expressed as below:` · `formulated as below:` · `described as:` ·
`written as:` · `stated as below:` · `defined as below:`

- Exactly **one** bold phrase per lead-in, 2–5 words: **term count**, **exact
  reconstruction**, **anisotropic dilation matrix**, **tight-frame property**.
- Never drop an equation after a bullet ending in a full stop; never open a slide with an
  equation that has no lead-in.
- `==yellow==` is a different marker — do not use it for this.
- `build_styled_slides.py` warns on a missing lead-in, a missing connector, a **bolded
  connector**, and a lead-in with no bold phrase. A clean build has zero warnings.

## Build commands

```bash
S=~/.claude/skills/ppt-mkl/scripts
A="Mrinal Kanti Layek — Geophysics & AI Lab, Chonnam National University"

# PPTX (native editable OMML equations)
python3 $S/build_styled_slides.py talk.deck --out /abs/out/talk.pptx \
    --title "…" --subtitle "…" --author "$A" \
    --date "21 July 2026" --foot "short footer label"

# Markdown + Beamer .tex + Beamer PDF (same flags; --md-only for just the .md)
python3 $S/deck_to_beamer.py talk.deck --out-dir /abs/out --name talk \
    --title "…" --subtitle "…" --author "$A" \
    --date "21 July 2026" --foot "short footer label"
```

Author and affiliation are always the `$A` line above unless told otherwise.

**Output conventions**
- Name every artefact `YYYYMMDD_HHMMSS_<topic>_slides` — one stem, five extensions.
- Build into local `/DATA1/mkl/<project>_slides_build/` first, then copy to the NAS.
- **Ship the `.deck` beside the outputs** (`…_source.deck`) — it is the editable source;
  without it the deck can only be revised by hand in PowerPoint.
- Never overwrite an existing deck: new timestamp = new file.

**Requirements** — `python-pptx`, `lxml`, `pillow`, `pandoc` (or `pypandoc_binary`),
`pdflatex`. `deck_to_beamer.py` imports `build_styled_slides.py`, so **keep the two
scripts in the same directory**; copying just one breaks the Beamer path.

## Verification (required before reporting done)

```bash
soffice --headless --convert-to pdf --outdir . out.pptx && pdftoppm -png -r 80 out.pdf s
```

Then **read several rendered slides**, and check the equation count is non-zero:

```bash
python3 -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); \
print('OMML equations:', sum(z.read(n).decode('utf8','ignore').count('<m:oMath') \
for n in z.namelist() if n.startswith('ppt/slides/slide')))" out.pptx
```

## Common Mistakes

| Mistake | Consequence / fix |
|---|---|
| Building slides directly with python-pptx | Maths becomes Unicode text (`2j ψ(2jx − k)`), not editable, no fractions or integrals. Use the scripts. |
| Inventing equation numbers | Numbers must be the source's own `\tag{N}`. Copy them exactly, including `21b`, `30a`. |
| Titling a slide after its equation | Titles are topics ("DCT : The **digital coefficient** and its wrapping"), never "Equation (21)". |
| Trusting the LibreOffice preview for maths | Impress drops OMML that is mixed with text and ignores math font size. Layout is checkable there; equations are not. |
| Wingdings / private-use glyphs for bullets | Paste as broken characters outside PowerPoint. Plain Unicode ☑ ✪ ▪ only. |
| Overfilling a slide | ≤6 statements, ≤2 equations, ≤1 figure. Split into two slides with distinct topical titles. |

## Style contract (do not drift)

Times New Roman prose · Cambria Math equations · Segoe Script only for the purple
"Therefore…" line · **Comic Sans MS italic dark blue `1F3864` at a fixed 20 pt for every
reference and inline citation** · red `C00000` key phrases and equation tags · maroon
`7B2D26` terms · green `2E7D32` checkbox · grey+orange rule under the title ·
footer = date | label | page.

**References** — put every reference on a `!ref:` line, ~5 per slide (they are never
auto-shrunk, so more will overflow). Cite in body text with `@@Author (year)@@`. Follow the
reference slides with a short section stating, point-wise, what each cited work contributed
and where it is used in the deck — grouped by role (foundations, algorithm, theory,
applications), not listed alphabetically.
