# 📐 Deck rules: EM interpretation, FDEM over a dipping sheet

> 📅 2026-11-05 · deck `EM_Interpretation_FDEM_Dipping_Sheet_Telford_7_7.pptx`
> 📚 Source: Telford, Geldart & Sheriff, *Applied Geophysics*, 7.7.1 Introduction, 7.7.2 General Interpretation Procedure, 7.7.3 Ground Systems: FDEM over Dipping Sheet, parts (a) to (g).
> 🧩 Base skill: `ppt-minimal-skill-v6`, plus the body and title rules of `..\07_EM_equipment_ground_v7\docs\DECK_RULES_EM_equipment_v7.md`.

## ✅ Rules applied

- 🚫 **No title slide and no Thank you slide.** `frame.py` is not run, and the delivered file is `Deck.pptx`.
- ⚫ ~~Body text black, not bold, fonts cycle Times New Roman → Comic Sans MS → Bookman Old Style at 22 pt.~~ Replaced on 2026-11-06, see the body text rules below.
- 🔗 **All content slides use arrow chains.** Each chain starts from the source sentence and is cut at the arrow. Two arrows are the default, and one arrow is used only for a plain fact. `←` appears only where the source gives a cause.
- 🎲 **Title fonts** change at every topic in a seeded random order over six installed fonts, and two topics in a row never share one. Lettered parts are shown as `Section › Part` with the black label.
- 🧮 **Equation colors are dark.** The LHS and RHS colors alternate per equation over four sets:
  - dark red `7F1D1D` / navy `0B2A55`
  - dark green `14532D` / dark purple `4C1D95`
  - dark blue `1E3A8A` / dark red `7F1D1D`
  - dark purple `4C1D95` / dark green `14532D`

  The sets are defined in `temp/01_em_interp/build/eqcolor.py` (`SETS`).

## 🛠️ Build

- 📁 `temp/01_em_interp/build/`: the chain is copied from the v7 equipment deck. Run `python calibrate.py`, then `bash build.sh`, and copy `Deck.pptx` to the top of this folder under the deck name.
- 📄 Source extract: `temp/01_em_interp/extract/src.md`. It covers chapter lines 1236 to 1491, with the (h) figure removed. `fix_tags.py` normalizes `\tag {…}`.
- 🖼️ Figure 7.16 (shootback profiles) is added from the equipment section because part (e) refers to it.

## 🆕 Body text rules (updated 2026-11-06)

> 🗄️ The previous version (deck, docs, sections, build scripts) is archived in `archive/2026-11-06_v1/`.

### 1. 🔹 One bullet per chain
- Each arrow chain is **one bullet paragraph**. When it runs past the line, it wraps under a hanging indent.
- Wrapped rows get **no bullet of their own**. The old v7 rule that cut a chain into one-line bullets is dropped.

### 2. 📐 Body text box sizes (PowerPoint order, Height × Width)

| Slide | Body box | Placement |
|---|---|---|
| 🏷️ Topic start (title box at the top) | **6.53″ H × 13.07″ W** | centered left to right, under the title, flush with the slide bottom |
| ⬛ Same topic continued (black topic label, no title box) | **6.87″ H × 13.04″ W** | centered on the slide |
| 🖼️ Slide with a figure or table | same height, **half the width** | body on the left half, figure on the right half with its caption |

- The text inside the box stays **left-aligned**.

### 3. ⬛ Continued topics keep only the black label
- A slide that continues its topic gets **no title box**, not even "Sub-part (continued)".
- Only the black label with white text, naming the topic, sits at the top left.
- Where a new sub-part starts on a continued slide, its name appears once as a **bold, underlined sub-point** at the top of the body.

### 4. 🧩 Blank space filled (revised 2026-11-06, second pass)
- 🔠 **Body bullets stay at 22 pt**, with 6 pt after each bullet. The earlier 20 to 32 pt fill sizing is dropped.
- ⏩ A slide is filled by **pulling bullets forward from the next slides of the same topic**. The split is greedy, so each slide takes as much as fits and the rest moves on. When the next slide belongs to another topic (or a divider follows), the slide is left as it is.
- 🏷️ When bullets from a new sub-part are pulled in, its name appears first as a bold, underlined `#` heading. A heading never ends a slide.
- 🖼️ A figure or table slide fills its half box the same way, from the text slides after it.
- ✂️ When a run of text slides ends in a tail under half full and a figure slide of the same topic comes next, the tail moves onto that figure slide, ahead of its own bullets.
- 🧮 Equations and symbol lines stay with their lead-in bullet. A slide is cut only in front of a bullet or a heading.
- 🗄️ The previous version (font-size fill) is archived in `archive/2026-11-06_v2/`.

### 5. 🎨 Bullet fonts and color (color revised 2026-11-06, third pass)
- Every bullet draws a font **at random**, seeded so that rebuilds match, from this list:
  - Times New Roman
  - Comic Sans MS
  - Book Antiqua
  - Gabriola
  - Cambria Math
  - Alef
  - Ink Free
  - MV Boli
  - Georgia
- A slide does not need to use all of them. Size factors even out how large they look: Gabriola ×1.3, MV Boli ×0.92, Comic Sans and Georgia ×0.95, Times New Roman ×1.05.
- ⚫ **Body bullet text is black** (`BODY_C` in `head.js`). The earlier per-bullet dark colors are dropped.
- **Two bullets in a row never share a font.** The body text stays regular (not bold).
- 🌈 Equations keep their LHS/RHS colors, arrows stay dark gray, symbol lines stay black, and sub-point headings keep their colored bold underline.
- 🗄️ The colored-bullet version is archived in `archive/2026-11-06_v3/`.

### 6. ✍️ Sub-points
- Sub-points are **bold and underlined**, with no bullet. The bullets that follow use the normal rules above. Example:

  ```
  Transmitter:          <- bold + underlined sub-point
  • Transmitter is …    <- bullet, random font and color
  ```

- In a section file, write a sub-point as `'# Transmitter:'`.

### 7. 🧮 Unchanged
- 🌈 Equation LHS/RHS colors are the same as before (`eqcolor.py`).
- ➡️ Arrows (`→`, `←`) are dark gray, as in v7.
- 🔣 Symbol lines are 18 pt Times New Roman.
- 🖼️ Figure captions are unchanged.

### 🛠️ Build notes
- **`head.js`** implements the rules above:
  - `boxFor` / `figBox` set the boxes
  - `nextStyle` picks the font (the color is fixed black)
  - `greedy` / `emit` / `half` split and fill the slides at 22 pt
  - `T`, `S` and `TB` slides of one topic are pooled until `FLUSH()`
- **`assemble.sh`** calls `FLUSH()` before writing the deck.
- **`fontwidths.py`** now also measures the nine body fonts, including Cambria Math from `cambria.ttc`, face 1.
- **`post.py`** keeps the fill spacing. Equations are detected as **bold** Cambria Math, since Cambria Math is also a body font. `inject.py` uses the same test.
- **`check_fill.py`** reads the PowerPoint PDF export (`pp_export.ps1`) and reports, for each slide, the bullet size and how much of the box is used, flagging `OVER` or `thin`.
