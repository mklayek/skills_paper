---
name: "ppt-minimal-skill-v5"
description: "DEFAULT skill for making a PowerPoint (replaces ppt-minimal-mkl v4). Use whenever asked for a PPT, PPTX, deck, slides, lecture or teaching presentation. Builds a minimal, white, classroom-ready .pptx teaching deck from any source (PDF incl. scanned chapters, Markdown, HTML, text, Word, a web page) or a topic. Version 5 of ppt-minimal-mkl: v4 house style plus the user's PPT instructions: no equation/figure/page/section numbers or footers, every source equation and figure included with derivations, LHS/RHS equation colors alternating per equation, 22 pt body, subtitles only where a definition starts, source section names as titles with '(continued)', a title font and color per section, archive-first, and tested build scripts. Prefer it over other deck builders unless a Beamer PDF/.tex is wanted (ppt-mkl) or an existing .pptx is restyled (ppt-to-pptx-restyle)."
---

# 📊 ppt-minimal-skill-v5: minimal scientific teaching decks

**⭐ This is the default deck builder** (it replaces `ppt-minimal-mkl` v4). Use it for any "make a PPT" request unless the user wants a Beamer PDF/.tex (`ppt-mkl`) or an existing `.pptx` restyled (`ppt-to-pptx-restyle`).

**Version 5 = `ppt-minimal-mkl` v4 (the base) + the user's PPT instructions** (`reference/PPT_INSTRUCTIONS.md`).
Where v4 and v5 differ, **v5 wins**. The user's words in the current chat always win over both.

Use it when the user asks for a PowerPoint, PPTX, deck, slides or lecture from a source (an attached PDF including scanned book chapters, .md, .html, .txt, .docx, a URL) or a topic to research. The output is a real `.pptx`, with a Markdown copy next to it.

📦 Bundled with this skill:

| Path | What it is |
|---|---|
| `scripts/` | Tested build chain (pptxgenjs + python-pptx + OMML), used for the 341-slide EM Methods deck. Copy it into `temp/<NN>_<name>/build/` |
| `scripts/deck_config.example.json` | Per-deck settings: deck name, source Markdown, source figures, source credit |
| `examples/c1_example.js` | A section file showing every call and item type |
| `examples/apply_titles_example.py` | How source section names were mapped onto slide titles |
| `reference/PPT_INSTRUCTIONS.md` | The user's instructions, verbatim, in a readable table form |

Also read the built-in `pptx` skill's SKILL.md once for pptxgenjs gotchas (hex colors without `#`, `isTextBox: true`, the validate script).

---

## ⭐ V5 rules (override v4)

### 1. 🗄️ Archive first
- **Before changing or regenerating an existing deck, archive the current version**: the PPTX, its MD copy, the instructions file, the section sources and the build scripts, to `<output>/archive/<date>_v<N>/`. Never overwrite an archive.

### 2. 📁 Folders
- If the user names an output folder, the **deck goes at the top of it**, and everything else goes in subfolders of that same folder:
  - `docs/`: the deck's Markdown copy, the instructions file and other documents
  - `figs/`: every figure the deck uses (crops, diagrams, divider patterns)
  - `temp/<NN>_<short_name>/{build,sections,extract}`: generators, section sources, renders, contact sheets
  - `archive/`: earlier versions
- Nothing temporary at the top of the output folder. Only the `.pptx` sits there.

### 3. 🚫 No numbers anywhere on slides
- No **equation numbers** (this replaces v4's sequential numbering rule).
- No **page numbers**, no **footer** of any kind (no slide numbers, dates, source lines).
- No **figure or table numbers** in slide text or captions. Also **crop printed captions and body text out of the figure images** themselves. Check every crop's bottom edge on a strip sheet.
- No **section numbers**, including on divider slides (no "Section 3" line, the divider shows the section name only).
- In-text cross references become plain words ("see the dipole slides"), never "Eq. (12)" or "Figure 7.3".
- Check with `scripts/check_numbers.py Deck.pptx`. A bare value in a data-table cell (a gain of 7.20) is not a section number.

### 4. 🧮 Equations
- **No source equation is left out.** Build an inventory of every display equation (`scripts/eq_inventory.py` → `eqinv.json`) and reference each in a slide as `'§#N'`. `scripts/cover.py` must report **0 missing**.
- **Detailed derivations**: one step per line, each with a short bullet saying what was done ("Take the curl", "Substitute the Lorentz condition", "Let r ≫ λ").
- **Symbols explained directly under each equation** in the ▸ style: symbol in **bold teal Cambria 20 pt**, then a colon and the meaning with units in Cambria 20 pt near-black. Write several symbols on one source line separated by `;`. The generator splits them into separate `▸` runs, so no semicolon reaches the slide.
- Equations are **native, editable PowerPoint equations** (OMML), 22 pt Cambria Math. Source LaTeX goes through `latexomml.py` (pandoc's docx writer → OMML). Hand-written linear `'§ …'` lines go through `omml.py` (v4 rules in §4b below still apply).
- 🎨 **LHS and RHS in different colors, alternating sets on successive equations** (`scripts/eqcolor.py`, called by `inject.py`):

  | Equation | Left-hand side | Right-hand side |
  |---|---|---|
  | 1st, 3rd, 5th … | ⚫ black `000000` | 🔵 deep blue `1E3A8A` |
  | 2nd, 4th, 6th … | 🔴 dark red `991B1B` | 🟢 green `16A34A` |

  The split is at the first relation sign (`= ≈ ≤ ≥ ∝ ≡ ≪ ≫ < >`), row by row in aligned blocks. An equation without a relation takes the LHS color.
- An equation too wide for its box: rewrite it in `eqfix.json` (same id) as stacked fractions or with short helper symbols (p, q, u₁ …) and **define the helpers in a ▸ line**.

### 5. 🖼️ Figures
- **No figure is left behind.** Every source figure is used once. `cover.py` must report **0 unused**.
- Each figure slide gets **enriched bullets**: what is plotted (axes, units, parameters), what the curves show, how to read it or why it matters.
- Image on the right half, text on the left half, aspect ratio kept, no overlap. Caption names the source and the content, never a figure number.

### 6. 🔤 Body text
- **Bullets 22 pt** (fonts still cycle Times New Roman → Comic Sans MS → Bookman Old Style). Symbol lines 20 pt. Equations 22 pt.
- **No subtitle by default.** Pass `''` as the subtitle.
- **Keep a subtitle where it is needed, mainly where a definition starts** ("Definition: the Lorentz condition", "Definitions: in-phase and quadrature"). Case histories may keep a subtitle naming the site. When used, the subtitle keeps v4's style cycle.
- Text never shrinks below 22 pt. It moves to a continuation slide.

### 7. 🏷️ Slide titles
- **Use the source's section names as titles whenever possible**: the subsection name (■) or the lettered part name (●). Drop letters such as "(b)" and turn the book's semicolons into colons. Where no name fits (title slide, summary, numbered field examples, problems), keep a descriptive title.
- **A topic that continues onto the next slide uses the same title plus " (continued)"**, for both automatic splits and hand splits. Never "(cont.)".
- **Copperplate Gothic Bold is the default title font** (title slide, first section, Summary via `SUMMARY()`).
- **Each section gets its own title font and color**, and the color changes when the section changes. Default table (`TF` in `scripts/head.js`), cycling by section index:

  | Section index | Font | Color |
  |---|---|---|
  | 0, 1 (title, introduction), Summary | Copperplate Gothic Bold | navy `0B2A55` |
  | 2 | Copperplate Gothic Light (bold) | red `B91C1C` |
  | 3 | Rockwell | blue `1D4ED8` |
  | 4 | Gill Sans MT | green `15803D` |
  | 5 | Book Antiqua | purple `6D28D9` |
  | 6 | Century | teal `0E7490` |
  | 7 | Garamond (bold) | orange `C2410C` |
  | 8 | Palatino Linotype | navy `0B2A55` |
  | 9 | Trebuchet MS | red `B91C1C` |

  Divider slides use their section's font and color for the section name. Title size auto-fits one line (18 to 28 pt). The ◆ ■ ● level markers stay (Arial, colored by level).

### 8. ✍️ Writing
- 🇺🇸 US English. **No em dashes. No semicolons** in slide text, captions and the MD copy (qa.py checks).
- Spoken-natural, direct sentences.

### 9. 🖥️ Working practice
- ❌ **Never close the user's other PowerPoint files.** Export with `scripts/pp_export.ps1`: it opens only the deck, retries while PowerPoint is busy (RPC_E_CALL_REJECTED), closes only that deck and **never calls Quit**.
- 📝 Always keep a Markdown copy of the deck (`node deck_md.js`, generated from the same section sources).
- 🚀 Never push to GitHub unless asked for that push.

### 10. ✅ Checks before delivery (all must pass)
- `python cover.py`: 0 equations missing, 0 figures unused.
- `python check_numbers.py Deck.pptx`: no equation, figure, table, page or section numbers, no footer fields.
- `python qa.py Deck.pptx`: one Title and one Body per slide, 22 pt bullet cycle, title font per section, no semicolons or em dashes, US English, no raw markup.
- `python measure.py`: no overflow in the linear LibreOffice render.
- `powershell -File pp_export.ps1` then `python eqwidth.py`: in the **real PowerPoint render** nothing runs past the bottom (7.08 in), past the right margin, or from the left half into the image.
- `python sheets.py <first> <last> 4 36`: **look at every slide once** on contact sheets.
- MD copy rebuilt, the previous version archived.

---

## 🔧 Build chain (scripts/)

Run everything from `temp/<NN>_<name>/build/` after `npm install pptxgenjs` (or copy `node_modules`) and writing `deck_config.json` (see the example).

| Step | Command | What it does |
|---|---|---|
| 1 | `python eq_inventory.py` | Every `$$…$$` block of the source Markdown → `eqinv.json` (id, page, section, LaTeX) |
| 2 | `python cover.py` | Coverage report, and `../extract/annotated.md` (source with `[EQ#id]` and `[FIG name]` marks) to write slides from |
| 3 | `python figs_prep.py` | Divider patterns `sec0..sec6.png` + source figures into `<output>/figs`, `sizes.json` |
| 4 | write `../sections/c1_*.js … cN_*.js` | Slides, in order (see `examples/c1_example.js`) |
| 5 | `python calibrate.py` | Pass 1 without splitting on a tall page, measures each Body, writes `scale.json` for the splitter |
| 6 | `./build.sh` | `assemble.sh` → `latexomml.py` → `eqmeta.py` → `node deck.js` → `post.py` → `inject.py` (+ `eqcolor.py`) → `deck_md.js` |
| 7 | checks of §10 | |
| 8 | copy `Deck.pptx` to `<output>/<deck_name>.pptx` | The only file that leaves `temp/` |

Section-file calls: `T(title, subtitle, items)` full width, `S(title, subtitle, items, fig, caption)` half + image, `TB(title, subtitle, items, rows, colW, caption, fontSize)` half + table, `SEC(name, contents)` divider, `SUMMARY()` before the closing slide.
Items: plain string = bullet (`**bold**`, `_{sub}`, `^{sup}` allowed), `'§#N'` = source equation N, `'§ …'` = linear equation (§4b), `'› sym | meaning;  sym | meaning'` = symbol lines.

---

## 📐 Base rules kept from v4 (amended where v5 differs)

### 0. Working files
Every intermediate file lives under `temp/<NN>_<short_name>/` with `sections/`, `extract/`, `build/` (figures in `<output>/figs/`, docs in `<output>/docs/`, see V5 §2). Create the folder first. Keep `temp/` after delivery so revisions are cheap.

### 1. House style
- **Canvas** `LAYOUT_WIDE` 13.333 × 7.5 in, **white** content slides, no bars, stripes or gradients. Only dividers carry a pattern.
- **Exactly two text boxes per content slide**, `Title` (x 0.6, y 0.35, w 12.1, h 0.8) and `Body`, plus an optional image caption. No footer.
- **Level markers** in titles: ◆ red = main topic, title slide and Summary. ■ blue = subsection. ● green = sub-subsection or lettered part. Never a section number in a title.
- **Bold key words** in bullets cycle red `B91C1C`, blue `1D4ED8`, green `15803D`, purple `6D28D9`. Plain text near-black `111827`.
- **Half-and-half rule**: with an image, text left (x 0.6, w 5.9) and image right (x 6.85, y 1.35, w 5.9, h 5.2). Without, full-width Body (x 0.6, y 1.3, w 12.1, h 5.7). A table may take the right half.
- **Captions** Arial 12 pt italic gray `374151` under the image, naming the source (no figure number, V5 §3). `_x` and `_{…}` in captions render as real subscripts.
- **No slide-count limit.** Split, never shrink.

### 2. Section dividers
- A pattern-filled divider before every main section (not before the title slide or Summary). Patterns and colors cycle hexagons/red, stripes/blue, dots/green, waves/purple, triangles/teal, arcs/orange, grid/navy (`figs_prep.py`), with a solid white panel and a 3 pt border in the section color.
- Panel text: the **section name** large in the section's title font and color (V5 §7), and one line listing what the section covers in Verdana bold 18 pt. **No "Section N" line** (V5 §3).

### 3. Detail rule
- Full, informative bullets from the source: definitions, mechanisms, numbers, ranges, units, authors and dates, and the reason behind each point.
- Aim for about 5 bullets beside an image and 6 to 7 on a full-width slide. Avoid a continuation slide with a single short item (merge or move the step to the next slide).
- Cover every section and subsection in order. Add comparison tables, worked examples (marked "illustrative") and the source's problems or case histories.

### 4a. Equation content
- Every equation, plus intermediate derivation steps (V5 §4). Derivation slides full width, beside an image only if they fit.
- If a printed symbol is ambiguous or a misprint, keep the source form and say so in the ▸ line.

### 4b. Writing hand-made equations in linear form (`'§ …'`)
- Unicode symbols directly (∇ ∂ ∑ ∫ ρ σ θ λ π Δ δ ∞ ≈ ≫ → ± × · ′ ″ ℓ √ ² ³ and `−` U+2212).
- `_{…}` subscript, `^{…}` superscript. `∑_{m=1}^{∞}` and `∫_{0}^{2π}` take limits, the body runs to the next `+ − = ≈ , ;` at that level.
- `/` stacks the **adjacent** operands, so write operands without spaces inside: `(Iρ/2π)(1/r)`, `(ρ_{2} − ρ_{1})/(ρ_{2} + ρ_{1})`. Brackets wrapping a whole numerator or denominator are removed when built up. Use `·` to separate a fraction from a following factor.
- Upright words in double quotes: `"or"`, `"Ω·m"`, `"in‑phase (%)"` (use a non-breaking hyphen U+2011 inside words, or they render as "in − phase").
- **No equation number at the end** (V5 §3). One equation per line. A long equation may continue on the next `§` line starting with 4+ spaces or an operator.

### 5. Workflow
1. Say in one sentence what you are building, then start (archive first if a deck exists, V5 §1).
2. Make the folders (V5 §2), copy `scripts/` into `build/`, write `deck_config.json`.
3. Get the source into Markdown with `$$…$$` equations (for scanned books use the Unlimited-OCR pipeline, see the `ocr-unlimited-ocr` memory). Keep raw dumps and renders in `extract/`.
4. Run `eq_inventory.py`, `figs_prep.py`, `cover.py`. Plan the outline from `annotated.md`: title → per main section a divider, then its slides (concepts → definitions and equations with derivations → methods and equipment → procedure → interpretation and examples → practice) → Summary.
5. **Figures**, in order of preference: the user's own files (crop with a 5 % grid, trim whitespace, cut printed captions, check on contact sheets), attached photos, clean matplotlib diagrams (white background, labels ≥ 10 pt, 5.9 × 5.2 in). Never repeat an image.
6. Write the section files, then calibrate, build and run every check in V5 §10. Fix, rebuild, recheck.
7. Deliver: copy the deck to the output folder top, rebuild the MD copy, give a short summary (slide count, structure, where figures came from, anything assumed or unavailable). Mention that equations are native PowerPoint equations (they show as one-line text in Google Slides or LibreOffice).

### 6. Content rules
- Stay faithful to the source: its numbers, names, equations and tables. Credit figures in captions.
- Mark anything not from the source (synthetic diagrams, illustrative values) as such.
- If an image cannot be obtained, say so plainly and use the best alternative.
- US English only unless the user asks otherwise.

---

## 🧩 Implementation notes (lessons from the EM deck)

- **Calibration keys** are `title + '¦' + first item`, because "(continued)" titles repeat. `calibrate.py` reads `keys.json` written by the generator.
- **Built-up equations are taller than the linear text** LibreOffice shows. The real check is the PowerPoint export (`pp_export.ps1` + `eqwidth.py`). Split tall derivations by hand into "(continued)" slides.
- **Bash heredocs mangle backslashes** in JS and regex. Write patch scripts with the Write tool, then run them.
- **Paths with `[` `]`** (e.g. `[UG]_…`) break globbing and PowerShell `Resolve-Path`. Use `glob.escape`, `-LiteralPath` or `$PSScriptRoot`.
- **pandoc OMML** keeps the source LaTeX faithful. Put fixes (wider layouts, helper symbols) in `eqfix.json`, never edit the source.
- **Figure crops from OCR** may include the printed caption. Trim with an `@keep NAME x0,y0,x1,y1` row in the OCR fixes table (or re-crop), and re-run `figs_prep.py`.
