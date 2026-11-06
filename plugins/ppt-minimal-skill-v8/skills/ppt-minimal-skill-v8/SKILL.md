---
name: "ppt-minimal-skill-v8"
description: "Use when asked for any PPT, PPTX, deck, slides, lecture or teaching presentation (the default deck builder), from a PDF, scanned chapter, Markdown, HTML, text, Word file, web page or a topic, and when the user asks for v8, filled slides, continued slides without a repeated title box, or plain black body bullets in mixed fonts."
---

# 📊 ppt-minimal-skill-v8: filled all-arrow-chain class decks

**v8 = `ppt-minimal-skill-v7` + new body-text and slide-layout rules.** The v8 rules were tested on the deck `EM_Interpretation_FDEM_Dipping_Sheet_Telford_7_7.pptx` (39 slides, `qa.py` ALL CHECKS PASSED).

- The inherited text of v7, with v6, v5 and v4 under it, is in **`reference/V7_BASE.md`**. Read it once for:
  - chain writing
  - arrow direction
  - title fonts, oval and label
  - equations
  - figures and captions
  - folders and the no-numbers rule
- **Precedence:** where v8 and the inherited text differ, v8 wins. The user's words in the current chat win over both.
- **Overrides:** the table "What v8 overrides" below lists every inherited rule that v8 replaces.

## ⭐ V8 rules

### V8.1 🔹 One bullet per chain
- Each arrow chain is **one bullet paragraph** that **wraps naturally** under a hanging indent.
- Wrapped rows get **no bullet**.
- Write the full chain as one string. Never cut it into several items yourself.
- Every bullet is still a chain (`→` or `←`, one direction). `head.js` stops the build on a plain bullet.

### V8.2 📐 Body box sizes (PowerPoint order, Height × Width)

| Slide | Body box | Placement |
|---|---|---|
| 🏷️ Topic start (title box at the top) | **6.53″ × 13.07″** | centered left to right, flush with the slide bottom |
| ⬛ Same topic continued (black label only) | **6.87″ × 13.04″** | centered on the slide |
| 🖼️ Either, with a figure or table | same height, **half the width** | body on the left half, figure on the right half with its caption |

- The text inside the box is **left-aligned**.
- These sizes are set by `boxFor()` and `figBox()` in `head.js`. Do not set boxes in section files.

### V8.3 ⬛ Continued slides: black label, no title box
- A slide that continues its topic gets **no Title shape at all**, not even "… (continued)".
- It gets only the **black box with white text** at the top left, naming the topic.
- When a **new sub-part starts** on a continued slide, its name appears once as a bold, underlined sub-point at the top of the body.
- Write titles as in v7 (`'●  Topic › Sub-part'`, `'… (continued)'`). `newSlide()` decides title or label from the topic.

### V8.4 🧩 Fill every slide at 22 pt
- **Body bullets stay at 22 pt** (times the font size factor, V8.5), with 6 pt after each bullet. They never shrink to fit.
- **Pooling:** `T`, `S` and `TB` calls of one topic are pooled and re-split greedily. Each slide takes as many bullets as fit, and the rest move on.
- **Pulling forward:** a half-empty slide therefore pulls bullets from the next slides of the same topic.
- **Topic end:** when the next slide is another topic or a divider, the slide stays as it is. A thin last slide of a topic is correct.
- **"Fill the slides"** means this rule. It is the user's own wording: "fill the slides after getting bullet point from next slide (if same topic) otherwise leave as it is". Never pull bullets across a topic boundary.
- **Cuts:** a slide is cut only in front of a bullet or a `#` heading, so an equation stays with its lead-in and its symbol line. A heading never ends a slide.
- **Figure slides:** a figure or table slide fills its half box the same way.
- **Thin tail before a figure:** when a run of text slides ends in a tail under half full, and the next slide is a figure slide of the same topic, the tail moves onto that figure slide, ahead of its bullets.
- **Write slides as you would split them by hand.** The pool re-splits them. Do not merge or pad sections to fill space.

### V8.5 🎨 Body fonts and color

| Item | Style |
|---|---|
| Bullet text | **black** `000000`, regular (not bold) |
| Bullet font | seeded random pick per bullet from the nine fonts below. **Two bullets in a row never share a font.** |
| Arrows `→` `←` | Cambria Math, dark gray `4B5563` |
| Equations | bold Cambria Math, LHS/RHS colors alternate per equation (`eqcolor.py`) |
| Symbol lines | Times New Roman 18 pt black |
| Sub-point headings | bold, underlined, colored (style cycle) |

| Font | Size factor × 22 pt |
|---|---|
| Times New Roman | 1.05 |
| Comic Sans MS | 0.95 |
| Book Antiqua | 1 |
| Gabriola | 1.3 |
| Cambria Math | 1 |
| Alef | 1 |
| Ink Free | 1 |
| MV Boli | 0.92 |
| Georgia | 0.95 |

- A slide does not need to use all nine fonts.
- The seed is `20261106` (`brnd` in `head.js`). Rebuilds give the same fonts.
- Change the font list or the factors only in `BFONTS`. After that, re-run `fontwidths.py` so the fill estimate stays right.
- **Equation detection:** bold Cambria Math marks an equation. Cambria Math is also a body font, so body bullets must never be bold. `post.py` and `inject.py` rely on this.

### V8.6 ✍️ Sub-points
- A sub-point is **bold and underlined** with no bullet. Write it as an item: `'# Transmitter:'`. The bullets that follow use the normal rules.
- A sub-part name (`'Topic › Sub-part'`) joining the pool becomes such a heading automatically.

### V8.7 🎓 Frame slides are optional
- `deck_config.json` → `"frame": true` adds the class title slide and the Thank you slide (`frame.py`).
  - Deliver `Final.pptx`.
  - Ask for `method_name`, `method_group` and `lecture` first (v7 V7.0).
- `"frame": false` (the tested reference deck) builds no frame slides.
  - Deliver `Deck.pptx`.
  - `deck_md.js` leaves out the title and Thank you lines.
- If the user does not say, ask together with the V7.0 fields.

### V8.8 ✅ Checks before delivery
Run from `build/`. Every check must pass.

| Check | Command | Must show |
|---|---|---|
| coverage | `python cover.py` | 0 equations missing, 0 figures unused |
| numbers | `python check_numbers.py Deck.pptx` (or `Final.pptx`) | no numbers, no footer fields |
| house rules | `python qa.py Deck.pptx` (or `Final.pptx`) | **ALL CHECKS PASSED** |
| real render | `powershell -File pp_export.ps1` then `python check_fill.py` | no `OVER`. Each `thin` must be a topic end or a figure slide before another figure slide |
| equation width | `python eqwidth.py` | no equation past the box |
| look | `python sheets.py 1 <last> 4 36` | look at every slide once |

`qa.py` checks these v8 rules:
- one Title, or one black label and no Title, per slide
- no lvl-1 continuation bullets
- the nine fonts, no repeat on consecutive bullets, 22 pt × factor
- black, non-bold body text
- the V8.2 box sizes
- optional frame slides

## 🔧 Build chain (scripts/, tested)

**Layout:** use the deck task folder layout from CLAUDE.md:
- `sections\` sits at the top of the task folder. The build reads `../../../sections`.
- The build runs in `temp\<NN>_<name>\build\`.
- Copy `scripts/*` and `assets/frame_template.pptx` into `build/`.
- Run `npm install pptxgenjs`.
- Write `deck_config.json`, starting from `deck_config.example.json`.

| Step | Command | Output |
|---|---|---|
| 1 | `python eq_inventory.py` | `eqinv.json` |
| 2 | `python figs_prep.py` | divider patterns, figures, `sizes.json` |
| 3 | `python cover.py` | `../extract/annotated.md` to write slides from |
| 4 | write `sections/c1_*.js … cN_*.js` | see `examples/c1_example_v8.js` |
| 5 | `bash build.sh` | `fontwidths.py` (first run) → `assemble.sh` (adds `FLUSH()`) → `latexomml.py` → `eqmeta.py` → `node deck.js` → `post.py` → `inject.py` → `deck_md.js` → `frame.py` if `"frame": true` |
| 6 | V8.8 checks | |
| 7 | copy `Deck.pptx` or `Final.pptx` to `<task folder>/<deck_name>.pptx` | the only file at the top |

**Section-file calls:**

| Call | Use |
|---|---|
| `T(title, '', items)` | text slide |
| `S(title, '', items, fig, 'description \| source')` | figure slide |
| `TB(title, '', items, rows, colW, caption, fs)` | table slide |
| `SEC(name, contents)` | divider (it also flushes the pool) |

**Items:**

| Item | Meaning |
|---|---|
| a chain string | one bullet |
| `'§#N'` | source equation N |
| `'§ …'` | linear equation |
| `'› sym \| meaning;  sym \| meaning'` | symbol line |
| `'# Heading'` | sub-point |

## 🔁 What v8 overrides in `reference/V7_BASE.md`

| Inherited rule | v8 |
|---|---|
| V7.2b one line per bullet, `oneline_check.py`, lvl-1 continuation bullets | V8.1 one wrapping bullet. `oneline_check.py` is removed |
| `calibrate.py`, `measure.py`, `scale.json` splitter | V8.4 pooled greedy fill from `fontwidths.json`. Checked with `check_fill.py` on the PowerPoint export |
| v4 house style: exactly one `Title` + `Body`, fixed Title/Body positions, half box x 0.6 / 6.85 | V8.2 boxes, V8.3 label-only continued slides |
| Continued title left-aligned with "(continued)" | no title box on continued slides (V8.3) |
| Font cycle Times New Roman → Comic Sans MS → Bookman Old Style | nine random fonts, no repeat in a row (V8.5) |
| Chain segments colored, formats alternating bold/italic | black, regular body text. Arrows gray (V8.5) |
| "Aim for about 5 or 6 to 7 bullets per slide" | fill to the box at 22 pt (V8.4) |
| Frame slides always, deliver `Final.pptx` | optional (V8.7) |

Unchanged from the inherited rules:
- chain recipe and read-aloud test (V7.2, V7.3)
- topic title fonts, oval and title bullets (V7.4)
- no numbers, equations, figures, captions and writing rules (V5 §3 to §8)
- archive first (V5 §1)
- PowerPoint never quit (V5 §9)

## 🚩 Common mistakes

| Mistake | Fix |
|---|---|
| Splitting a long chain into two items so it fits one line | One string per chain. The wrap is the rule (V8.1) |
| Shrinking the font or deleting bullets to fit | 22 pt stays. The pool moves bullets to the next slide (V8.4) |
| Padding a thin topic-end slide with text from the next topic | A topic end may be thin. Leave it (V8.4) |
| Writing a continued slide's title as a new topic to "get a title back" | Continued slides carry the label only. A new topic name starts a new font and color |
| Making a body bullet bold for emphasis | Bold Cambria Math is read as an equation, and `head.js` strips `**…**` from chains. To highlight a key term, put it first in the chain (the concept segment) or give it a `'# Term'` sub-point. If the user wants in-bullet emphasis, ask before changing `head.js` |
| Overriding `newSlide`, `boxFor` or `FLUSH` in a section file | All layout lives in `head.js`. Section files hold content only |
| Running `qa.py Final.pptx` with `"frame": false` | Check `Deck.pptx`. Without a frame there is no `Final.pptx` |
| Trusting the fill estimate without the render | `pp_export.ps1` + `check_fill.py`. Fonts render differently in PowerPoint |
| Path with `[UG]` failing in PowerShell | `Set-Location -LiteralPath` |
| Emoji print error in Python (cp949 console) | `PYTHONIOENCODING=utf-8` |

## 🛑 Red flags: stop and fix

| Thought | Reality |
|---|---|
| "Just this one slide at 20 pt, it's late" | No per-slide size hacks. Rebuild at 22 pt so the pool moves the overflow. On a topic's last slide, tighten the chain wording |
| "fill.json says it fits, skip the export" | The estimate is not the check. Run `pp_export.ps1` + `check_fill.py` every delivery. If PowerPoint cannot run, tell the user the deck is unverified |
| "qa.py fails on one thing only, ship it" | ALL CHECKS PASSED or no delivery |
| "The user wants titles back, so add a Title to continued slides" | Ask first. If they confirm, it is their override of V8.3. Change `newSlide()` in `head.js` and the qa STRUCTURE check together |

**Violating the letter of these rules is violating their spirit.**

## 📦 Bundled files

| Path | What it is |
|---|---|
| `scripts/` | Tested v8 build chain (`head.js` holds all V8 layout logic). `check_fill.py` is new. `qa.py` has the v8 checks |
| `examples/c1_example_v8.js` | Pooled `T`/`S` slides, a `#` sub-point, equation + symbol line |
| `examples/c1_example_v7.js` | Every title form (start, `›` label, `★` oval) and chain use |
| `reference/V7_BASE.md` | Inherited rules (v7 → v6 → v5 → v4) |
| `reference/DECK_RULES_EM_interpretation.md` | The reference deck's rules file, the source of V8 |
| `reference/PPT_INSTRUCTIONS.md`, `reference/ARROW_NOTES_FORMAT.md` | The user's PPT instructions and arrow-note format |
| `assets/frame_template.pptx`, `scripts/frame.py`, `scripts/make_frame_template.py` | Optional class title and Thank you slides |
