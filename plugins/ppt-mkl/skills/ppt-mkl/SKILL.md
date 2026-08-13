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
A="Dr. Mrinal Kanti Layek — Geophysics & AI Lab, Department of Energy & Resources Engineering, Chonnam National University, Gwangju, Republic of Korea"

# PPTX (native editable OMML equations)
python3 $S/build_styled_slides.py talk.deck --out /abs/out/talk.pptx \
    --title "…" --subtitle "…" --author "$A" \
    --date "21 July 2026" --foot "short footer label"

# Markdown + Beamer .tex + Beamer PDF (same flags; --md-only for just the .md)
python3 $S/deck_to_beamer.py talk.deck --out-dir /abs/out --name talk \
    --title "…" --subtitle "…" --author "$A" \
    --date "21 July 2026" --foot "short footer label"
```

### Author block (default — do not retype it wrong)

```text
Dr. Mrinal Kanti Layek | Postdoctoral Researcher | 박사후 연구원
Geophysics & AI Lab, Department of Energy & Resources Engineering,
Chonnam National University, Gwangju, Republic of Korea [61186]
지구물리 및 인공지능 연구실, 에너지자원공학과, 전남대학교, 광주광역시, 대한민국 [61186]
```

The `$A` one-liner above is the title-slide form of this block and is the default baked
into `deck_to_beamer.py` (`DEFAULT_AUTHOR`) — omit `--author` and you get it. Madrid's
footline uses the short form `M. K. Layek — CNU` (`--author-short`). Use the Korean lines
when a Korean-language or bilingual deck is requested.

### Beamer theme flags

The Beamer back-end builds on the
**[Madrid](https://deic.uab.cat/~iblanes/beamer_gallery/individual/Madrid-default-default.html)**
theme by default (`Madrid-default-default`): blue frametitle bar, infolines headline, and
Madrid's own footline of *short author | foot label | date + page*.

**Bullets come from the theme, not from us.** In themed mode the body is emitted as real
nested `itemize` environments, so `-` / `--` / `---` render as Madrid's own shaded blue
balls, smaller at each level, with the theme's indentation. Do **not** reintroduce manual
glyphs (`\ding`, black squares) on the Beamer side — that is what the themed path exists to
replace. Themed mode also drops `mathpazo`, so the deck is sans-serif like the gallery, and
sets the class to **11pt**; list spacing is pulled in via `etoolbox` so `[shrink=25]` rarely
has to fire and the body stays legible.

`--beamer-theme none` keeps the old behaviour exactly: 10pt, `mathpazo` serif, hand-built
black-square bullets, inline figures, underlined title over the grey+orange rule.

## Figures get their own slide — BOTH back-ends

A figure sharing a slide with a full set of bullets has to be capped to a fraction of the
text height and comes out unreadably small. **Never do that.** Each `!fig:` is lifted onto
its **own slide** carrying the parent slide's title, with:

- the image as large as the slide allows (~72 % of the height);
- its caption underneath in italic, if the `!fig:` line carries one;
- **one or two lines of description**, condensed from that slide's `!note:` — falling back
  to `!key:` when there is no note.

The bullets stay on the preceding slide. This is the default in **both** the PPTX
(`build_styled_slides.py`) and the themed Beamer build, so the two stay in step: the
GPRTransNet deck is 90 slides in each.

> A deck therefore grows by one slide per figure — 68 → 90 here. That is expected;
> **never shrink a figure to avoid the extra slide.**

`--no-fig-slides` on either script restores inline, bottom-anchored figures (and is implied
by `--beamer-theme none`).

## Filling the text area (Beamer)

A half-empty slide next to a full one reads as a mistake. Before rendering, the themed
Beamer build **packs each frame's text area with content drawn forward from the next
slide**, in two passes:

1. **Whole-slide merge** — while two adjacent slides' bodies together still fit one frame,
   they become one slide.
2. **Bullet pulling** — if a slide is still under `TARGET_FILL`, leading bullet groups are
   lifted off the next slide one at a time until it fills. A group is one level-0 bullet
   plus its sub-bullets, and the donor always keeps at least `MIN_DONOR_GROUPS` of its own.

Pulled content is inserted **above** the `!key:` / `!so:` conclusion, never after it — the
takeaway stays last. Only the donor's **leading run of bullets** is movable, so a bullet is
never torn out from behind an equation or a takeaway it belongs to.

**Titles are rewritten** to name both topics: `PREFIX : topic one · topic two`, or
`PFX-A · PFX-B : …` when the sub-topics differ. A wrapping frametitle would steal back the
body height just gained, so the second topic is shortened word by word to fit one line
(never ending on a dangling `and` / `of` / `the`), prefixes are deduped, and at most two are
ever shown.

- Packing **never crosses a `#` section** — that boundary is the hard stop.
- Reference slides (`!ref:`) are never packed — they keep their fixed ~5-per-slide layout.
- Figures are untouched: each still gets its own frame, and its description is **frozen onto
  the figure** before notes are combined, so two figures on one packed slide keep their own
  `!note:` text.
- `--no-merge-slides` renders every slide exactly as written.

Tuning constants in `deck_to_beamer.py`, all in estimated rendered lines and calibrated
against the actual PDF: `FRAME_LINES` (capacity), `TARGET_FILL` (the point below which a
slide pulls content forward), `MIN_DONOR_GROUPS`, and `TITLE_MAX`.

> Some slides still end under-full — the last slide of a section has nothing it may borrow
> from, and a neighbour that would overflow the frame is left alone. That is correct
> behaviour, not a miss.

## The closing lines get their own markers

`!key:` and `!so:` are conclusions, not more statements, so in themed Beamer they do **not**
take the theme's bullet: `!key:` gets a green ✔ and `!so:` a purple ⇒. That keeps the
takeaway visually separate from the body it summarises.

| Flag | Default | Effect |
|---|---|---|
| `--beamer-theme` | `Madrid` | any beamer theme name; `none` = the old hand-built chrome |
| `--beamer-colortheme` | `default` | beamer color theme |
| `--author-short` | `M. K. Layek — CNU` | left cell of Madrid's footline |
| `--fig-slides` / `--no-fig-slides` | on (both scripts) | one dedicated slide per figure vs. inline |
| `--merge-slides` / `--no-merge-slides` | on when themed | fill the text area by merging slides and pulling bullets forward |

The PPTX back-end is unaffected — it keeps the underlined-title lecture style.

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
`7B2D26` terms · green `2E7D32` checkbox.

Chrome differs by back-end and that is intentional:

| | PPTX | Beamer (themed) |
|---|---|---|
| Title | underlined, grey+orange rule | Madrid blue frametitle bar |
| Bullets | black squares, flush left | Madrid shaded blue balls, nested |
| Body font | Times New Roman | theme sans-serif (no `mathpazo`) |
| Figures | own slide + description | own frame + description |
| `!key:` / `!so:` | no marker | green ✔ / purple ⇒ |
| Under-full slides | left as written | packed from the next slide |
| Footer | date \| label \| page | short author \| label \| date + page |

The **content** palette above is shared and must never drift between the two.

**References** — put every reference on a `!ref:` line, ~5 per slide (they are never
auto-shrunk, so more will overflow). Cite in body text with `@@Author (year)@@`. Follow the
reference slides with a short section stating, point-wise, what each cited work contributed
and where it is used in the deck — grouped by role (foundations, algorithm, theory,
applications), not listed alphabetically.

## House writing rules (apply to every deck, added 2026-07-22)

These project rules govern the prose inside bullets, keys, notes and captions. They sit
on top of the deck grammar above.

**Equations and cross-references**
- Every `$$…$$` keeps its mandatory lead-in bullet ending in a plain connecting phrase and
  a colon (`formulated as below:`, `described as:`, `given by:`, `written as:`,
  `stated as below:`, `defined as below:`). Bold the substance phrase, never the connector.
- Highlight the term the equation defines in a different colour — `**term**` (maroon) in the
  lead-in or symbol bullets, or `==term==` (yellow) for the one key phrase per slide.
- Refer to equations in body text as `Equation (11)` or `Equations (11-12)`, and to tables
  as `Table 1`, `Table 2`. Never "Eq. 11" or "the table above".

**Figures**
- Give every `!fig:` an italic caption after the width using a pipe:
  `!fig: /abs/f.png 60% | Figure 1. One-sentence description.`
  The caption renders italic and centred under the image (PPTX, Beamer and Markdown), and
  always starts with `Figure 1.`, `Figure 2.`, and so on.

**Citations**
- Use real author-year citations, wrapped in `@@…@@`: `@@(Kumar et al., 2023)@@`,
  `@@(Terrasse et al., 2015, 2017; Kumar et al., 2023)@@`, or narrative
  `Following @@Ge et al. (2024)@@, the operator is trained…`.

**Punctuation and tone (crisp, point-wise)**
- Replace em dashes (—) and parenthetical asides. Rephrase, or use commas, "and", "but".
  Keep symbol definitions as short sentences: `$a>0$ is the continuous scale.`
- Avoid semicolons in casual prose. Use periods or conjunctions. Semicolons are allowed only
  inside multi-work citations.
- Remove mid-sentence ellipses.
- Use colons sparingly. The equation lead-in colon is the main sanctioned use.
- Keep each bullet a single crisp point.

**Footer**
- Support building without the date and slide number in the footer when asked
  (centre label only). `build_styled_slides.py` accepts `--no-date` and `--no-page`;
  `deck_to_beamer.py` drops `=DATE=` and `\insertframenumber` under the same flags.

**Bullets and indentation (added 2026-07-22)**
- Every bullet marker is a **solid black square** (`▪`, colour `000000`) on every level,
  in both the PPTX and the Beamer PDF. No green checkbox or red star.
- **Body text starts flush at the left edge of the text box.** Level-0 bullets use
  `marL=0` and no hanging indent, so the first line and every wrapped line begin at the
  leftmost point, with no left gap and no first-line hang. Nested levels get only a small
  left margin, still with no hanging indent.
- The `!key` and `!so` lines are also flush-left with a black-square marker; `!key` stays
  bold black and `!so` stays the purple "Therefore" line.

**Equation slides — describe each term**
- On a slide that carries an equation, add one short `-` bullet per symbol that says in
  plain words what it means (for example `- $D$ is the cluttered B-scan.`). Keep each to a
  single simple clause. This mirrors the `Symbols in (n)` glossary of the methods read-doc.

**End slide — always a graphical Thank-You (added 2026-07-22)**
- Every deck ENDS with a graphical "Thank you" slide, never a bare text slide.
- `build_styled_slides.py` and `deck_to_beamer.py` **auto-append** this slide when the deck
  does not already end with one. No deck edit is required.
- Two bundled assets, in priority order:
  1. `assets/thankyou_slide.png` — a **full-bleed branded Thank-You** image (16:9),
     placed edge-to-edge with no title bar or footer. Use this for a designed closing
     slide with the presenter's name, full affiliation, contact, institution logo, and
     scientific figures. This is preferred when present.
  2. `assets/thankyou_lineart.png` — the fallback, a clean GPR antenna-to-hyperbola line
     drawing shown on a normal content slide with a purple closing line. Regenerate it
     with `scripts/make_thankyou_lineart.py <out.png>`.
- To customise, drop your own 16:9 `assets/thankyou_slide.png` (recommended: name, title,
  affiliation in local script and English, email, institution logo, on-theme figures), or
  end the deck yourself with a slide whose title contains "Thank you".
- The full-bleed image is baked art. Keep the affiliation text in the image correct and
  current, since it is not editable text in the slide.
