---
name: "ppt-minimal-skill-v7"
description: "Use when asked for a PPT, PPTX, deck, slides or teaching/class lecture presentation in which EVERY bullet is an arrow chain (Concept → mechanism → meaning, Effect ← cause), with the user's class title slide (method name, method group, Lecture NN) and Thank you slide, and per-topic title fonts (centered topic start, left continued, oval for key titles, black topic label for sub-topics), or when the user asks for 'v7', 'all arrow slides' or 'class-style deck with arrow chains'."
---

# 📊 ppt-minimal-skill-v7: all-arrow-chain class decks

**Version 7 = `ppt-minimal-skill-v6` with four changes:**
1. 🔗 **Every bullet is an arrow chain.** There are no source-style slides any more.
2. 🎓 **Class title slide first, Thank you slide last.** Both are copied from the user's class deck and stay editable.
3. 🏷️ **Per-topic titles.** Each topic has its own font, dark color, alignment and fill. A gold oval marks very important titles, and a black label names the topic when a sub-topic continues it.
4. 🖼️ **Body text and figures stay exactly as in v6/v5**: 22 pt font cycle, half-and-half layout, native equations, no numbers.

Where v7 and the inherited rules differ, **v7 wins**. The user's words in the current chat always win over all of them.

---

## ⭐ V7 rules

### V7.0 🙋 Ask before building: method name, method group, lecture number
The title slide shows three per-lecture texts. **Unless the user already gave all three in this chat, ask for them with AskUserQuestion before writing `deck_config.json`.** Offer your best reading of the source as the first option:

| Field (`deck_config.json`) | Example | Where it shows |
|---|---|---|
| `method_name` | `IP Method`, `Electromagnetic Methods` | big white title |
| `method_group` | `Electrical Methods` | red-on-yellow line under it |
| `lecture` | `07` (two digits) | "… · Lecture 07" |

- Never take the lecture number from an old deck, a folder name or a slot prefix on your own. A deck for "slot 06" may be lecture 07 this year.
- If the user **explicitly** names where to take the values from or says not to ask ("use the number from the IP deck"), follow that, and state the three values in the delivery summary.
- `Lecture NN` on the title slide is the **one number the no-numbers rule allows**.
- Optional `title_photo`, `title_book` and `title_corner` replace the three title-slide pictures (field photo, textbook cover, corner diagram). Fill them in when the user gives method-specific images. Otherwise the class template pictures stay.

### V7.1 🔗 Every content slide is an arrow-chain slide
- **Every bullet on every content slide is a chain**: the Summary, figure slides, table slides, the lead-in to an equation, a procedure step and a derivation step all count. Equation lines (`§`) and symbol lines (`›`) stay as they are.
- `head.js` **stops the build** on a bullet without `→` or `←`: `Error: v7: every bullet is an arrow chain`. Rewrite that bullet as a chain. Never delete it to get past the error.
- Content that v6 kept in source style becomes a chain like this:

| Passage kind | v7 chain |
|---|---|
| Definition through an equation | `Chargeability → the area under the decay curve, normalized by the voltage during current flow:` then `'§#1'` and the `›` line |
| Derivation step | `Take the curl → of both sides of Faraday's law → the magnetic field appears on the right` |
| Procedure or equipment | `Current electrodes → placed 100 m apart on the line → the transmitter injects a square wave` |
| Figure description | `Horizontal axis → frequency from 0.1 Hz to 1 kHz` and `Falling curve ← electrode polarization decreasing with frequency` |
| List of items | one chain per item, or `Minor sources → normal dielectric and electrokinetic effects, tiny amounts of conducting minerals` |
| History or case study | `Seigel (1959) → overvoltage linear in current at low current density` |
| Naming ("X is called Y") | `Electron exchange at the interface → called overvoltage in physical chemistry` |

### V7.2 🧩 The chain recipe (v6 recipe, middle segment loosened)
`Concept / term  →  original principle or mechanism  →  physical meaning, implication or application`

1. **Segment 1, the concept**: 2 to 6 words, the source's own term. Write it **without** `**…**`, because the renderer bolds it.
2. **Middle segment, the mechanism**: **keep the source's own words**, as much or as little of the sentence as the point needs. A short run of 3 or 4 source words is fine. Trim the sentence, never rephrase its core.
3. **Last segment, the meaning**: a consequence, limitation or application **stated in the source or a direct reading of it**. If the source gives none, write a 2-segment chain. Never invent physics to fill the slot.
4. Keep the source's qualifiers ("in most rocks", "about 10^{−6} cm", "often").
5. **No connectives inside a chain**: drop "because", "so", "since", "therefore" and "which means". The arrow carries that meaning. No semicolons and no em dashes.
6. **Segments are phrases.** Drop a leading "is", "are" or "it is". A segment that brings in a new subject names it. A segment that goes on about the previous segment's subject may start with its verb (`Clay content → does not increase steadily → reaches a maximum and then decreases`).
7. **Size:** at most **4 chains beside an image** and 5 to 6 on a full-width slide. This replaces v4's "about 5 bullets beside an image". Chains wrap more than prose, so the splitter makes "(continued)" slides sooner.
8. **Symbol lines** keep units only where the source gives them. Never invent a unit.
9. **Symbol lines (v7 style)**: directly under the equation, written as one **continuous line** (wrapping onto more lines when long): `ρ_{dc}: apparent resistivity at dc ; FE: frequency effect`, in **Times New Roman 18 pt, black** (symbol bold), no ▸ bullets. Write them as before, `'› ρ_{dc} | apparent resistivity at dc;  FE | frequency effect'`, and the renderer joins the parts with ` ; `. These ` ; ` separators are the one place a semicolon is allowed (qa skips symbol lines).
10. **Never end a bullet with a citation year in parentheses** (`… tabulated by Grover (1962)`): qa reads it as an equation number. Put the citation first: `Grover (1962) → tables for more complicated straight conductors`.

### V7.2b 📏 One line per bullet, Figure captions, no "Definition:" subtitles
- **A bullet never wraps onto a second line.** `head.js` measures each chain with real font widths (`fontwidths.json`, written by `python fontwidths.py` in `build/` before the build) and moves the words that would wrap onto the **next bullet**, a continuation bullet in the same font and segment colors (`lvl="1"` on the paragraph). Write chains as usual. The split is automatic. `python oneline_check.py` (after `pp_export.ps1`) must report **0 wrapped bullet lines** in the real PowerPoint render.
- **Figure captions**: write the caption as `'description | source'`, e.g. `'(a) V(t) compared with V_{c}, (b) integral of V(t) over a time interval | Telford, Geldart and Sheriff, Applied Geophysics'`. It renders as **Figure :** (bold italic) + the description (italic, near-black Arial 12 pt) + `(source)` in a different color and font (Agency FB, orange-brown), placed **directly under the image and left-aligned with it**. Never a figure number. Keep the description short, use (a), (b) for parts. **The description starts with a capital letter** right after **Figure :** (`Figure : After background removal …`, not `Figure : after …`). The renderer capitalizes it automatically (`capFirst()` in `head.js`), and a leading part label such as `(a)` stays lowercase.
- **Never write "Definition:" or "Definitions:" in a subtitle.** Use the name alone (`'The Lorentz condition'`, `'Self-inductance'`). The renderer strips the word if it slips in, and qa fails on it.

### V7.3 ↔️ Arrow direction: the read-aloud test for every arrow
Put "leads to" in place of `→`, or "is caused by" in place of `←`, between the two segments the arrow joins. The sentence must be true according to the source. If it is false, flip the arrow or reorder the segments.

| Arrow | Reads as | First segment is… | ✅ Example |
|---|---|---|---|
| `→` (default) | "leads to / works by / means" | a concept, cause or condition | `Membrane polarization → negative ions accumulate at one end of the zone → current flow is impeded` |
| `←` | "is caused by / comes from" | an **observed effect** the source explains | `IP decay after switch-off ← the ions return to their original positions, taking a finite time` |

- **One direction per bullet** (the build stops on both). Expect `←` in about 1 chain in 4.
- In a `←` chain the segment right after the arrow is the **direct** cause and the root cause comes last. **Each** `←` must pass the test on its own. "Strongest membrane effect ← clay minerals ← pores particularly small" fails, because clay minerals are not caused by small pores. Write `Strongest membrane effect ← clay minerals, in which the pores are particularly small`.
- `←` never introduces a definition, a property, a list or a measured value.
- Two facts that do not cause each other are two 2-segment chains, never one 3-segment chain.

| ❌ Wrong | Why | ✅ Right |
|---|---|---|
| `Background ← cannot be distinguished from electrode polarization ← geological noise` | "background is caused by cannot be distinguished" is false | `Background polarization → cannot be distinguished from electrode polarization → a level of geological noise` |
| `Conduction rate ← depends on the mobility of the ions` | trigger verb repeated after the arrow | `Conduction rate ← the mobility of the ions, the porosity and the degree of saturation` |
| `Electrolytic conduction → is the predominant factor …` | segment starts with a linking verb | `Electrolytic conduction → the predominant factor in most rocks → …` |
| `Large M → strong polarizable content → the IP target` | last segment not in the source | `Integration window → between times t_{1} and t_{2} after switch-off` |

### V7.4 🏷️ Titles: written as plain title strings, styled by `head.js`
**Write titles only through the title string.** Never override `newSlide`, `SEC` or any other `head.js` function in a section file.

A **topic** is the title without its level marker, without " (continued)" and without a " › sub-topic" part.

| You write | Result |
|---|---|
| `'■  Membrane Polarization'` (topic differs from the previous slide) | **topic start**: title **centered**, the next font in the cycle and the next dark color |
| `'■  Membrane Polarization (continued)'` | same topic: **left-aligned**, same font and color |
| `'■  Membrane Polarization › Background Polarization'` on a later slide of that topic | **black label** (white text) at the top left reading "Membrane Polarization", and a left-aligned title "Background Polarization" with the topic's bullet |
| the same `' › '` title on the topic's **first** slide | centered topic title. The sub-topic moves into the subtitle line. **No label**, since a label marks a topic that continues |
| `'★■  Chargeability'` | **gold oval** title, centered, for a very important title (wide oval, long titles shrink to 16 pt to stay on one line) |

- **Fonts cycle per topic**: Copperplate Gothic Bold → Bookman Old Style → MV Boli → Footlight MT Light → Copperplate Gothic Light → Rockwell → Book Antiqua → Californian FB. Two topics in a row never share a font. A divider (`SEC`) uses the font and color of the topic that follows it.
- **Title bullets cycle per topic** too, each with its own color: ◆ red, ■ blue, ● green, ▶ purple, ❖ teal, ✦ orange, ▲ navy, ◉ rose, ➤ dark green, ✿ brown (Segoe UI Symbol, 20 pt). All slides of a topic share its bullet, and two topics in a row never share one. The ◆ ■ ● you write in a title string only switch the bullet on (no marker written = no bullet). The topic decides which glyph and color appear. The oval has no bullet.
- **Dark text colors** cycle per topic: navy, dark red, dark green, dark purple, dark teal, brown, deep blue, dark rose, charcoal.
- **Title boxes**: **no fill for most topics**. Every third topic gets a **light** fill (light yellow, light blue, light green, lavender, pink, sky, peach), kept on all of that topic's slides.
- **Oval (`★`)**: use it for the **few titles the lecture hinges on**: the core mechanism of a section, the key definition, or the main take-home result. **At most one oval per section**, and never on two slides in a row. Not every topic start gets one. `★` may sit on any slide, "(continued)" ones included. The oval is always centered, and qa exempts it from the alignment rule.
- **Black label (`›`)**: only where the **source itself has a sub-heading inside a topic** that runs on from the topic's earlier slides. The label is a separate small box, and the title box still holds the sub-topic.
- "(continued)" is added by the splitter or by you, never "(cont.)".
- **A divider ends the topic.** The slide after `SEC` always starts a topic (centered, next font), even if its name repeats.
- An **intro topic** before the first divider is optional. Add one only when the source has introductory text.
- The Summary is an ordinary topic. `SUMMARY()` is kept only so v6 section files still run.

### V7.5 🎓 Frame slides (`scripts/frame.py`, run by `build.sh`)
- A long method name (e.g. "Electromagnetic Methods") is shrunk from 54 pt so it stays on one line and clear of the photos.
- `frame.py Deck.pptx Final.pptx` copies the class **title slide** to the front and the **Thank you slide** to the end, shape by shape, from `frame_template.pptx`. Pictures, crops, highlights, fonts and colors stay identical, and every text stays an editable text box. It fills `{{METHOD}}`, `{{GROUP}}` and `{{LECTURE}}` from `deck_config.json`, and stops if one is missing.
- **Copy `assets/frame_template.pptx` into `build/`** with the scripts. It was cut from slide 1 and the last slide of `PPT_class_kr\PPT\06_IP_Method_2026.pptx`, a **read-only folder: copy from it, never write to it**. If the class style changes, rebuild the template from a copy of the class deck: `python make_frame_template.py <copy_of_class_deck.pptx> frame_template.pptx`.
- **Deliver `Final.pptx`.** `Deck.pptx` stays content-only, so the slide numbers used by `calibrate.py`, `measure.py`, `eqwidth.py` and `sheets.py` still match.
- Do not write your own title or closing slide in the section files. The first section file starts with the first content topic.

### V7.6 ✅ Checks (run on `Final.pptx`)
`python qa.py Final.pptx` must print **ALL CHECKS PASSED**. On top of the v6 checks it fails on:
- any plain (non-chain) bullet,
- a font, color or title-bullet change inside a topic, two consecutive topics with one font or one title bullet, a topic start that is not centered, a continued title that is not left-aligned, a fill that is not light, or a title color that is not dark,
- a black label on a topic's first slide, or a label that is not white on black,
- a missing title slide or Thank you slide, an unfilled `{{TOKEN}}` or a missing "Lecture NN".

It also prints the topic, font, fill, oval and label counts. Look at the contact sheets of `Final.pptx` too (`pp_export.ps1 Final.pptx`).

### V7.7 🚩 Red flags: stop and fix
| Thought | Reality |
|---|---|
| "This slide is a definition, it stays source style" | v7 has no source slides. Write the lead-in as a chain (V7.1 table). |
| "The lecture number is obviously 06 from the folder" | Ask (V7.0). |
| "I'll patch `newSlide` in the section file to center this title" | Title strings do it (V7.4). Overrides break the topic logic and qa. |
| "Every topic start deserves an oval" | Ovals are for the few key titles only. |
| "This new topic has a sub-heading, so it gets a black label" | A label only marks a topic that **continues**. |
| "I'll copy the Thank you slide from another deck" | `frame.py` with the bundled template. |

**Example section file:** `examples/c1_example_v7.js` covers every title form (start, continued, `›` label, `★` oval) and every chain use (figure slide, equation lead-in, `←`, Summary).

---

# 🔗 Inherited from v6 (amended)

- **Chain rendering** (`head.js` → `chain()`): each segment takes its **own color** from red `B91C1C`, blue `1D4ED8`, green `15803D`, purple `6D28D9`, teal `0E7490` and orange `C2410C`, so the two sides of an arrow always differ. The arrow is bold gray `374151`. **Formats alternate from bullet to bullet**: bold / plain / italic, bold-italic / plain / bold, bold-underline / italic / plain, bold / italic / bold-italic. The concept segment is always bold. `**…**` inside a segment is allowed for one key word. The bullet keeps the 22 pt font cycle (Times New Roman → Comic Sans MS → Bookman Old Style).
- The Markdown copy (`deck_md.js`) bolds the concept segment, keeps the arrows, and adds the title-slide line and the Thank you line.
- The v6 rules on choosing chain vs source slides (V6.1) and the 40 to 60 % mix are **replaced** by V7.1. The source-slide examples in `examples/c1_example_v6.js` are for v6 only.
- `reference/ARROW_NOTES_FORMAT.md` is the user's original "Concept → principle → meaning" note format.

---

# 📐 Inherited from v5 (amended where v7 differs)

**Version 5 = `ppt-minimal-mkl` v4 (the base) + the user's PPT instructions** (`reference/PPT_INSTRUCTIONS.md`).
Where v4 and v5 differ, **v5 wins**.

Use it when the user asks for a PowerPoint, PPTX, deck, slides or lecture from a source (an attached PDF including scanned book chapters, .md, .html, .txt, .docx, a URL) or a topic to research. The output is a real `.pptx`, with a Markdown copy next to it.

📦 Bundled with this skill:

| Path | What it is |
|---|---|
| `scripts/` | Tested build chain (pptxgenjs + python-pptx + OMML), used for the 341-slide EM Methods deck. Copy it into `temp/<NN>_<name>/build/` |
| `scripts/deck_config.example.json` | Per-deck settings: deck name, source Markdown, source figures, source credit |
| `examples/c1_example.js` | A section file showing every call and item type |
| `examples/c1_example_v6.js` | v6 only: source slides and chain slides side by side (v7 has no source slides) |
| `examples/c1_example_v7.js` | **v7: every title form and every chain use** |
| `assets/frame_template.pptx` | **v7: class title slide + Thank you slide** (copy into `build/`) |
| `scripts/frame.py` | **v7: adds the frame slides, `Deck.pptx` → `Final.pptx`** |
| `scripts/make_frame_template.py` | v7: rebuilds the template from a copy of the class deck |
| `scripts/fontwidths.py`, `scripts/oneline_check.py` | v7: one-line bullets, font widths for the splitter and the render check |
| `reference/ARROW_NOTES_FORMAT.md` | The user's "Concept → principle → meaning" note format, the source of the V6 chain recipe |
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
- **v7 exception:** "Lecture NN" on the class title slide (V7.0).
- Check with `scripts/check_numbers.py Final.pptx`. A bare value in a data-table cell (a gain of 7.20) is not a section number.

### 4. 🧮 Equations
- **No source equation is left out.** Build an inventory of every display equation (`scripts/eq_inventory.py` → `eqinv.json`) and reference each in a slide as `'§#N'`. `scripts/cover.py` must report **0 missing**.
- **Detailed derivations**: one step per line, each with a short bullet saying what was done ("Take the curl", "Substitute the Lorentz condition", "Let r ≫ λ").
- **Symbols explained directly under each equation** (**v7**, see V7.2 rule 9): one continuous line `sym: meaning ; sym: meaning` in Times New Roman 18 pt black, symbol bold, no ▸ bullets. Write several symbols on one source line separated by `;`.
- Equations are **native, editable PowerPoint equations** (OMML), 22 pt Cambria Math. Source LaTeX goes through `latexomml.py` (pandoc's docx writer → OMML). Hand-written linear `'§ …'` lines go through `omml.py` (v4 rules in §4b below still apply).
- 🎨 **LHS and RHS in different colors, alternating sets on successive equations** (`scripts/eqcolor.py`, called by `inject.py`):

  | Equation | Left-hand side | Right-hand side |
  |---|---|---|
  | 1st, 3rd, 5th … | ⚫ black `000000` | 🔵 deep blue `1E3A8A` |
  | 2nd, 4th, 6th … | 🔴 dark red `991B1B` | 🟢 green `16A34A` |

  The split is at the first relation sign (`= ≈ ≤ ≥ ∝ ≡ ≪ ≫ < >`), row by row in aligned blocks. An equation without a relation takes the LHS color.
- An equation too wide for its box: rewrite it in `eqfix.json` (same id) as stacked fractions or with short helper symbols (p, q, u₁ …) and **define the helpers in the symbol line**.

### 5. 🖼️ Figures
- **No figure is left behind.** Every source figure is used once. `cover.py` must report **0 unused**.
- Each figure slide gets **enriched bullets**: what is plotted (axes, units, parameters), what the curves show, how to read it or why it matters.
- Image on the right half, text on the left half, aspect ratio kept, no overlap. Caption in the v7 form `'description | source'` → **Figure :** description (source), directly under the image (V7.2b), never a figure number.
- **No border around figures.** Place the image bare: no outline rectangle, frame, or picture border line.

### 6. 🔤 Body text
- **Bullets 22 pt** (fonts still cycle Times New Roman → Comic Sans MS → Bookman Old Style). Symbol lines 18 pt Times New Roman black (v7). Equations 22 pt.
- **No subtitle by default.** Pass `''` as the subtitle.
- **Keep a subtitle where it is needed, mainly where a definition starts**, written as the name alone ("The Lorentz condition", "In-phase and quadrature"), never with "Definition:" (V7.2b). Case histories may keep a subtitle naming the site. When used, the subtitle keeps v4's style cycle.
- Text never shrinks below 22 pt. It moves to a continuation slide.

### 7. 🏷️ Slide titles
- **Use the source's section names as titles whenever possible**: the subsection name (■) or the lettered part name (●). Drop letters such as "(b)" and turn the book's semicolons into colons. Where no name fits (title slide, summary, numbered field examples, problems), keep a descriptive title.
- **A topic that continues onto the next slide uses the same title plus " (continued)"**, for both automatic splits and hand splits. Never "(cont.)".
- **v7:** fonts, colors, alignment, fill, oval and black label follow the **topic** rules of V7.4. The v5 per-section font table no longer applies. The title bullet is chosen per topic (V7.4), not by level.

### 8. ✍️ Writing
- 🇺🇸 US English. **No em dashes. No semicolons** in slide text, captions and the MD copy (qa.py checks).
- Spoken-natural, direct sentences.

### 9. 🖥️ Working practice
- ❌ **Never close the user's other PowerPoint files.** Export with `scripts/pp_export.ps1`: it opens only the deck, retries while PowerPoint is busy (RPC_E_CALL_REJECTED), closes only that deck and **never calls Quit**.
- 📝 Always keep a Markdown copy of the deck (`node deck_md.js`, generated from the same section sources).
- 🚀 Never push to GitHub unless asked for that push.

### 10. ✅ Checks before delivery (all must pass)
- `python cover.py`: 0 equations missing, 0 figures unused.
- `python check_numbers.py Final.pptx`: no equation, figure, table, page or section numbers, no footer fields.
- `python qa.py Final.pptx`: one Title and one Body per slide, 22 pt bullet cycle, v7 topic titles, every bullet a chain, frame slides present, no semicolons or em dashes, US English, no raw markup (V7.6).
- `python measure.py`: no overflow in the linear LibreOffice render.
- `powershell -File pp_export.ps1` then `python eqwidth.py`: in the **real PowerPoint render** nothing runs past the bottom (7.08 in), past the right margin, or from the left half into the image.
- `python oneline_check.py` (after `pp_export.ps1`): **0 wrapped bullet lines** (V7.2b).
- `python sheets.py <first> <last> 4 36`: **look at every slide once** on contact sheets.
- MD copy rebuilt, the previous version archived.
- v7: every chain re-read against the source with the read-aloud test (V7.3), and the title slide and Thank you slide checked on the `Final.pptx` contact sheet.

---

## 🔧 Build chain (scripts/)

Run everything from `temp/<NN>_<name>/build/` after `npm install pptxgenjs` (or copy `node_modules`), copying `assets/frame_template.pptx` next to the scripts and writing `deck_config.json` with the V7.0 fields (see the example).

| Step | Command | What it does |
|---|---|---|
| 1 | `python eq_inventory.py` | Every `$$…$$` block of the source Markdown → `eqinv.json` (id, page, section, LaTeX) |
| 2 | `python cover.py` | Coverage report, and `../extract/annotated.md` (source with `[EQ#id]` and `[FIG name]` marks) to write slides from |
| 3 | `python figs_prep.py` | Divider patterns `sec0..sec6.png` + source figures into `<output>/figs`, `sizes.json` |
| 4 | write `../sections/c1_*.js … cN_*.js` | Slides, in order (see `examples/c1_example.js`) |
| 4b | `python fontwidths.py` | Character widths of the body fonts → `fontwidths.json` for the one-line bullet splitter (V7.2b) |
| 5 | `python calibrate.py` | Pass 1 without splitting on a tall page, measures each Body, writes `scale.json` for the splitter |
| 6 | `./build.sh` | `assemble.sh` → `latexomml.py` → `eqmeta.py` → `node deck.js` → `post.py` → `inject.py` (+ `eqcolor.py`) → `deck_md.js` → `frame.py` (→ `Final.pptx`) |
| 7 | checks of §10 | |
| 8 | copy **`Final.pptx`** to `<output>/<deck_name>.pptx` | The only file that leaves `temp/` |

Section-file calls: `T(title, subtitle, items)` full width, `S(title, subtitle, items, fig, caption)` half + image, `TB(title, subtitle, items, rows, colW, caption, fontSize)` half + table, `SEC(name, contents)` divider. No title or closing slide in the sections (V7.5).
Items: string with `→` or `←` = chain bullet (`_{sub}`, `^{sup}` allowed, a plain bullet stops the build), `'§#N'` = source equation N, `'§ …'` = linear equation (§4b), `'› sym | meaning;  sym | meaning'` = symbol lines.

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
- **Captions** (v7, V7.2b): **Figure :** bold italic + description italic near-black Arial 12 pt + (source) in Agency FB orange-brown, directly under the image, left-aligned with it. `_x` and `_{…}` render as real subscripts.
- **No slide-count limit.** Split, never shrink.

### 2. Section dividers
- A pattern-filled divider before every main section (not before the title slide or Summary). Patterns and colors cycle hexagons/red, stripes/blue, dots/green, waves/purple, triangles/teal, arcs/orange, grid/navy (`figs_prep.py`), with a solid white panel and a 3 pt border in the section color.
- Panel text: the **section name** large in the font and color of the topic that follows it (V7.4), and one line listing what the section covers in Verdana bold 18 pt. **No "Section N" line** (V5 §3).

### 3. Detail rule
- Full, informative bullets from the source: definitions, mechanisms, numbers, ranges, units, authors and dates, and the reason behind each point.
- Aim for about 5 bullets beside an image and 6 to 7 on a full-width slide. Avoid a continuation slide with a single short item (merge or move the step to the next slide).
- Cover every section and subsection in order. Add comparison tables, worked examples (marked "illustrative") and the source's problems or case histories.

### 4a. Equation content
- Every equation, plus intermediate derivation steps (V5 §4). Derivation slides full width, beside an image only if they fit.
- If a printed symbol is ambiguous or a misprint, keep the source form and say so in the symbol line.

### 4b. Writing hand-made equations in linear form (`'§ …'`)
- Unicode symbols directly (∇ ∂ ∑ ∫ ρ σ θ λ π Δ δ ∞ ≈ ≫ → ± × · ′ ″ ℓ √ ² ³ and `−` U+2212).
- `_{…}` subscript, `^{…}` superscript. `∑_{m=1}^{∞}` and `∫_{0}^{2π}` take limits, the body runs to the next `+ − = ≈ , ;` at that level.
- `/` stacks the **adjacent** operands, so write operands without spaces inside: `(Iρ/2π)(1/r)`, `(ρ_{2} − ρ_{1})/(ρ_{2} + ρ_{1})`. Brackets wrapping a whole numerator or denominator are removed when built up. Use `·` to separate a fraction from a following factor.
- Upright words in double quotes: `"or"`, `"Ω·m"`, `"in‑phase (%)"` (use a non-breaking hyphen U+2011 inside words, or they render as "in − phase").
- **No equation number at the end** (V5 §3). One equation per line. A long equation may continue on the next `§` line starting with 4+ spaces or an operator.

### 5. Workflow
1. Ask for the method name, method group and lecture number (V7.0) unless the user gave them. Say in one sentence what you are building, then start (archive first if a deck exists, V5 §1).
2. Make the folders (V5 §2), copy `scripts/` and `assets/frame_template.pptx` into `build/`, write `deck_config.json`.
3. Get the source into Markdown with `$$…$$` equations (for scanned books use the Unlimited-OCR pipeline, see the `ocr-unlimited-ocr` memory). Keep raw dumps and renders in `extract/`.
4. Run `eq_inventory.py`, `figs_prep.py`, `cover.py`. Plan the outline from `annotated.md` (the title slide comes from `frame.py`): per main section a divider, then its slides (concepts → definitions and equations with derivations → methods and equipment → procedure → interpretation and examples → practice) → Summary.
5. **Figures**, in order of preference: the user's own files (crop with a 5 % grid, trim whitespace, cut printed captions, check on contact sheets), attached photos, clean matplotlib diagrams (white background, labels ≥ 10 pt, 5.9 × 5.2 in). Never repeat an image.
6. Write the section files, then calibrate, build and run every check in V5 §10. Fix, rebuild, recheck.
7. Deliver: copy `Final.pptx` to the output folder top under the deck name, rebuild the MD copy, give a short summary (slide count, structure, where figures came from, anything assumed or unavailable). Mention that equations are native PowerPoint equations (they show as one-line text in Google Slides or LibreOffice).

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
