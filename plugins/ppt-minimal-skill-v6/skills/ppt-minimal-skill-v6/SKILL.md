---
name: "ppt-minimal-skill-v6"
description: "Use when asked for a PPT, PPTX, deck, slides or teaching presentation whose body text should mix source-style bullets with arrow-chain bullets (Concept → mechanism → meaning, or Effect ← cause), colored and formatted differently on each side of the arrows, or when the user asks for 'v6', 'arrow style slides' or 'concept arrow bullets'. Same house style as ppt-minimal-skill-v5 (white minimal classroom .pptx from a PDF, scanned chapter, Markdown, Word, web page or topic). Includes the class title slide and Thank you slide and per-topic title fonts like v7, with v6's mixed body text."
---

# 📊 ppt-minimal-skill-v6: minimal teaching decks with arrow-chain slides

**Version 6 = `ppt-minimal-skill-v5` (everything below the V6 section, unchanged) + arrow-chain slides.**
The look of the deck is exactly v5. Only the body text changes: some slides keep source-style bullets and others become arrow chains. Where v5 and v6 differ, **v6 wins**. The user's words in the current chat always win over both.

---

## ⭐ V6 rules: two kinds of content slide

### V6.1 🧭 Every content slide is ONE kind, chosen per slide
- **Source slide**: v5 bullets, full sentences close to the source wording, no arrows.
- **Chain slide**: every bullet is an arrow chain (V6.2). Equation lines (`§`) and symbol lines (`›`) may sit on either kind, unchanged.
- A slide never mixes the two bullet kinds. One plain lead-in sentence before an equation is the only exception.

Pick the kind from what the **source passage for that slide** does:

| The passage… | Slide kind |
|---|---|
| states cause and effect, a condition and its result, a property and what it implies, a mechanism and its consequence, or a dependence ("X depends on Y", "X is largest when Y") | **Chain** |
| is a title, introduction, history or narrative | Source |
| defines a quantity through an equation, or derives one (step bullets such as "Take the curl") | Source |
| lists procedure steps, equipment, survey layout, or describes a figure (axes, curves, how to read it) | Source |
| is a case history or worked example | Source |
| is the Summary | Chain if the points are mechanisms and consequences, else Source |

- Aim for a **mix**: roughly 40 to 60 % chain slides among content slides. If a long topic runs over several slides, the mechanism slides become chains and the definition/derivation slides stay source style.
- Plan the kind of each slide in the outline before writing (`// kind: chain` or `// kind: source` comment above each call).

### V6.2 🔗 The arrow-chain bullet recipe
A chain bullet is **2 or 3 segments** (1 or 2 arrows), one idea per bullet:

`**Concept / term**  →  original principle or mechanism  →  physical meaning, implication or application`

1. **Segment 1, the concept**: 2 to 6 words, the source's own term ("Membrane polarization", "Warburg impedance", "Pore-fluid salinity").
2. **Middle segment, the mechanism**: **keep part of the original source sentence verbatim**, a run of 6 or more consecutive source words wherever the source sentence allows. Trim the start or end of the sentence, never rephrase its core.
3. **Last segment, the meaning**: a consequence, limitation or application **stated in the source or a direct reading of it**. If the source gives no consequence, use a 2-segment chain. Never invent physics to fill the slot.
4. Keep the source's qualifiers ("in most rocks", "at low frequencies", "about 10^{−6} cm", "often").
5. **No connectives inside a chain**: drop "because", "so", "since", "therefore", "which means". The arrow carries that meaning.
6. **No semicolons, no em dashes** (v5 §8 still applies).

### V6.3 ↔️ Arrow direction: decide per bullet
Read each arrow aloud. Pick the direction whose reading is true:

| Arrow | Reads as | Use when the bullet's first segment is… | Example |
|---|---|---|---|
| `→` (default) | "leads to / works by / means" | a concept, cause or condition | `**Membrane polarization** → negative ions accumulate at one end of the zone and leave the other → current flow is impeded` |
| `←` | "is caused by / comes from / is largest when" | an **observed effect or measured result** that the source explains by a cause | `**IP decay after switch-off** ← the ions return to their original positions ← taking a finite time to do so` |

- **One direction per bullet.** Never `→` and `←` in the same bullet (the build stops with an error).
- **Read-aloud test, for every arrow:** put "leads to" in place of `→`, or "is caused by" in place of `←`, between the two segments it joins. The sentence must be true according to the source. If it is false, flip the arrow or reorder the segments.
- In a `←` chain the **first segment names the effect with its direction** ("Weaker membrane effect", "Largest overvoltage", "Residual voltage"). The source's trigger verb ("depends on", "decreases with", "is most pronounced in", "is largest when") is absorbed into that first segment and is **never repeated** at the start of the next segment.
- `←` never introduces a definition, a property, a list or a measured value.
- Expect `←` in a minority of chains (about 1 in 4).

| ❌ Wrong | Why | ✅ Right |
|---|---|---|
| `Disseminated mineral ← the surface area … is then maximized` | reads "disseminated mineral is caused by maximal surface area", which is false | `**Disseminated mineral** → the surface area available for the interface is then maximized → overvoltage effect is largest` |
| `Conduction rate ← depends on the mobility of the ions …` | trigger verb repeated after the arrow | `**Conduction rate** ← the mobility of the ions, the porosity and the degree of saturation` |
| `Membrane polarization ← most pronounced in the presence of clay minerals` | a property, not a cause | `**Strongest membrane polarization** ← clay minerals ← pores particularly small` |
| `Real IP spectra ← c between 0.25 and 0.35` | a measured value, not a cause | `**Measured IP spectra** → c between 0.25 and 0.35 for most rocks → the simple Warburg form only approximates real behavior` |
| `Electrolytic conduction → is the predominant …` | segment starts with a linking verb | `**Electrolytic conduction** → predominant conduction mechanism in most rocks → …` |

- **Segments are phrases.** Drop a leading "is", "are" or "it is" from a middle or last segment. Keep the rest of the source words. Every segment names its own subject (not "← often positive in the direction of flow" but "← streaming potentials often positive in the direction of fluid flow").
- **Order of causes in a `←` chain:** the segment right after the arrow is the **direct** cause, the root cause comes last. `Much weaker anomaly ← no electrical continuity across the water table ← a disseminated or isolated body`.
- **Two facts that do not cause each other are not a 3-segment chain.** `Background potentials → usually less than 100 mV → arise from streaming …` fails the test. Write two 2-segment chains (`**Background potentials** → usually less than 100 mV` and `**Background potentials** → arise from streaming of fluids …`) or keep that slide source style.

### V6.4 🎨 How chains render (automatic, `scripts/head.js` → `chain()`)
- Any bullet containing `→` or `←` renders as a chain. Each segment takes its **own color** from red `B91C1C`, blue `1D4ED8`, green `15803D`, purple `6D28D9`, teal `0E7490`, orange `C2410C`, so the two sides of every arrow always differ. The arrow is bold gray `374151`.
- **Formats alternate from bullet to bullet**: bold / plain / italic, bold-italic / plain / bold, bold-underline / italic / plain, bold / italic / bold-italic. The concept segment is always bold.
- The bullet keeps v5's 22 pt font cycle (Times New Roman → Comic Sans MS → Bookman Old Style). Do not add `**…**` around whole segments. The renderer formats them. `**…**` inside a segment is allowed for one key word.
- The Markdown copy (`deck_md.js`) bolds the concept segment and keeps the arrows.

### V6.5 ✅ Extra checks
- `python qa.py Deck.pptx` now also reports **ARROW CHAINS**: fails on a bullet with both directions or the same color on both sides of an arrow, and prints the chain/source slide counts plus a NOTE for mixed slides or an all-one-style deck.
- Before building, re-read every chain against the source: each middle segment keeps source words, each last segment is supported by the source, no connectives.

**Example section file:** `examples/c1_example_v6.js` (induced-polarization slides showing source and chain slides, `→` and `←`).

---

## ⭐ V6 frame, titles and captions (ported from v7 on 2026-10-28)

Everything outside the body text box follows v7: the class title slide and Thank you slide, the per-topic title system, the Figure caption style and the equation symbol lines. **The body bullets stay v6**: source and chain slides mixed (V6.1), 22 pt body font cycle.

### V6.6 🙋 Ask before building: method name, method group, lecture number
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

### V6.7 🏷️ Titles: written as plain title strings, styled by `head.js`
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
- **Black label (`›`), required for lettered sub-parts**: when a source section has sub-headings inside it ((a) General, (b) Biot–Savart law, (c) …), write the section as **one topic** and every later sub-part slide as `'■  Section name › Sub-part name'`, **not** as a separate `●` topic. Each such slide gets the small **black box with white text** at the top left naming the section (in the topic's font), and the sub-part as a left-aligned title below it. Its continuation slides keep the label: `'■  Section name › Sub-part name (continued)'`. On the section's own first slide the `›` part moves into the subtitle (a label only marks a topic that continues). Example:
  ```
  T('■  Description of EM Fields','',[…]);                                        // topic start, centered
  S('■  Description of EM Fields › Biot–Savart Law','',[…],'fig_7_01','… | …');    // black label + sub-part title
  T('■  Description of EM Fields › Biot–Savart Law (continued)','',[…]);          // label kept
  ```
- "(continued)" is added by the splitter or by you, never "(cont.)".
- **A divider ends the topic.** The slide after `SEC` always starts a topic (centered, next font), even if its name repeats.
- An **intro topic** before the first divider is optional. Add one only when the source has introductory text.
- The Summary is an ordinary topic. `SUMMARY()` is kept only so v6 section files still run.

### V6.8 🎓 Frame slides (`scripts/frame.py`, run by `build.sh`)
- A long method name (e.g. "Electromagnetic Methods") is shrunk from 54 pt so it stays on one line and clear of the photos.
- `frame.py Deck.pptx Final.pptx` copies the class **title slide** to the front and the **Thank you slide** to the end, shape by shape, from `frame_template.pptx`. Pictures, crops, highlights, fonts and colors stay identical, and every text stays an editable text box. It fills `{{METHOD}}`, `{{GROUP}}` and `{{LECTURE}}` from `deck_config.json`, and stops if one is missing.
- **Copy `assets/frame_template.pptx` into `build/`** with the scripts. It was cut from slide 1 and the last slide of `PPT_class_kr\PPT\06_IP_Method_2026.pptx`, a **read-only folder: copy from it, never write to it**. If the class style changes, rebuild the template from a copy of the class deck: `python make_frame_template.py <copy_of_class_deck.pptx> frame_template.pptx`.
- **Deliver `Final.pptx`.** `Deck.pptx` stays content-only, so the slide numbers used by `calibrate.py`, `measure.py`, `eqwidth.py` and `sheets.py` still match.
- Do not write your own title or closing slide in the section files. The first section file starts with the first content topic.

### V6.9 🖼️ Figure captions
- **Figure captions**: write the caption as `'description | source'`, e.g. `'(a) V(t) compared with V_{c}, (b) integral of V(t) over a time interval | Telford, Geldart and Sheriff, Applied Geophysics'`. It renders as **Figure :** (bold italic) + the description (italic, near-black Arial 12 pt) + `(source)` in a different color and font (Agency FB, orange-brown), placed **directly under the image and left-aligned with it**. Never a figure number. Keep the description short, use (a), (b) for parts. **The description starts with a capital letter** right after **Figure :** (`Figure : After background removal …`, not `Figure : after …`). The renderer capitalizes it automatically (`capFirst()` in `head.js`), and a leading part label such as `(a)` stays lowercase.

### V6.9b 🔣 Equation symbol lines
- Directly under the equation, one **continuous line** (wrapping onto more lines when long): `ρ_{dc}: apparent resistivity at dc ; FE: frequency effect`, in **Times New Roman 18 pt, black** (symbol bold), no ▸ bullets. Write them as before, `'› ρ_{dc} | apparent resistivity at dc;  FE | frequency effect'`. The ` ; ` separators are the one place a semicolon is allowed (qa skips symbol lines).

### V6.10 ✅ Extra checks (run on `Final.pptx`)
- `python qa.py Final.pptx` also fails on a font, color or title-bullet change inside a topic, two consecutive topics with one font or title bullet, a topic start that is not centered, a continued title that is not left-aligned, a fill that is not light, a title color that is not dark, a black label on a topic's first slide, and a missing title or Thank you slide or unfilled `{{TOKEN}}`.

---

# 📐 Inherited from v5 (amended where V6.6 to V6.10 differ)

**Version 5 = `ppt-minimal-mkl` v4 (the base) + the user's PPT instructions** (`reference/PPT_INSTRUCTIONS.md`).
Where v4 and v5 differ, **v5 wins**.

Use it when the user asks for a PowerPoint, PPTX, deck, slides or lecture from a source (an attached PDF including scanned book chapters, .md, .html, .txt, .docx, a URL) or a topic to research. The output is a real `.pptx`, with a Markdown copy next to it.

📦 Bundled with this skill:

| Path | What it is |
|---|---|
| `scripts/` | Tested build chain (pptxgenjs + python-pptx + OMML), used for the 341-slide EM Methods deck. Copy it into `temp/<NN>_<name>/build/` |
| `scripts/deck_config.example.json` | Per-deck settings: deck name, source Markdown, source figures, source credit |
| `examples/c1_example.js` | A section file showing every call and item type |
| `examples/c1_example_v6.js` | v6: source slides and arrow-chain slides (`→` and `←`) side by side |
| `reference/ARROW_NOTES_FORMAT.md` | The user's "Concept → principle → meaning" note format, the source of the V6 chain recipe |
| `examples/apply_titles_example.py` | How source section names were mapped onto slide titles |
| `reference/PPT_INSTRUCTIONS.md` | The user's instructions, verbatim, in a readable table form |
| `assets/frame_template.pptx`, `scripts/frame.py` | Class title slide + Thank you slide, `Deck.pptx` → `Final.pptx` (V6.8) |
| `scripts/make_frame_template.py` | Rebuilds the frame template from a copy of the class deck |

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
- **Exception:** "Lecture NN" on the class title slide (V6.6).
- Check with `scripts/check_numbers.py Final.pptx`. A bare value in a data-table cell (a gain of 7.20) is not a section number.

### 4. 🧮 Equations
- **No source equation is left out.** Build an inventory of every display equation (`scripts/eq_inventory.py` → `eqinv.json`) and reference each in a slide as `'§#N'`. `scripts/cover.py` must report **0 missing**.
- **Detailed derivations**: one step per line, each with a short bullet saying what was done ("Take the curl", "Substitute the Lorentz condition", "Let r ≫ λ").
- **Symbols explained directly under each equation** as one continuous line `sym: meaning ; sym: meaning`, Times New Roman 18 pt black, symbol bold, no ▸ bullets (V6.9b). Write several symbols on one source line separated by `;`.
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
- Image on the right half, text on the left half, aspect ratio kept, no overlap. Caption in the form `'description | source'` → **Figure :** description (source), directly under the image (V6.9), never a figure number.
- **No border around figures.** Place the image bare: no outline rectangle, frame, or picture border line.

### 6. 🔤 Body text
- **Bullets 22 pt** (fonts still cycle Times New Roman → Comic Sans MS → Bookman Old Style). Symbol lines 18 pt Times New Roman black (V6.9b). Equations 22 pt.
- **No subtitle by default.** Pass `''` as the subtitle.
- **Keep a subtitle where it is needed, mainly where a definition starts** ("Definition: the Lorentz condition", "Definitions: in-phase and quadrature"). Case histories may keep a subtitle naming the site. When used, the subtitle keeps v4's style cycle.
- Text never shrinks below 22 pt. It moves to a continuation slide.

### 7. 🏷️ Slide titles
- **Use the source's section names as titles whenever possible**: the subsection name (■) or the lettered part name (●). Drop letters such as "(b)" and turn the book's semicolons into colons. Where no name fits (title slide, summary, numbered field examples, problems), keep a descriptive title.
- **A topic that continues onto the next slide uses the same title plus " (continued)"**, for both automatic splits and hand splits. Never "(cont.)".
- **Titles follow V6.7** (per-topic font, dark color, title bullet, centered start, left continued, light or no fill, gold oval `★`, black topic label `›`). The v5 per-section font table no longer applies.

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
- `python qa.py Final.pptx`: one Title and one Body per slide, 22 pt bullet cycle, topic titles (V6.7), frame slides (V6.8), no semicolons or em dashes, US English, no raw markup.
- `python measure.py`: no overflow in the linear LibreOffice render.
- `powershell -File pp_export.ps1` then `python eqwidth.py`: in the **real PowerPoint render** nothing runs past the bottom (7.08 in), past the right margin, or from the left half into the image.
- `python sheets.py <first> <last> 4 36`: **look at every slide once** on contact sheets.
- MD copy rebuilt, the previous version archived.
- v6: the ARROW CHAINS block of `qa.py` passes and every chain was re-read against the source (V6.5).

---

## 🔧 Build chain (scripts/)

Run everything from `temp/<NN>_<name>/build/` after `npm install pptxgenjs` (or copy `node_modules`), copying `assets/frame_template.pptx` next to the scripts and writing `deck_config.json` with the V6.6 fields (see the example).

| Step | Command | What it does |
|---|---|---|
| 1 | `python eq_inventory.py` | Every `$$…$$` block of the source Markdown → `eqinv.json` (id, page, section, LaTeX) |
| 2 | `python cover.py` | Coverage report, and `../extract/annotated.md` (source with `[EQ#id]` and `[FIG name]` marks) to write slides from |
| 3 | `python figs_prep.py` | Divider patterns `sec0..sec6.png` + source figures into `<output>/figs`, `sizes.json` |
| 4 | write `../sections/c1_*.js … cN_*.js` | Slides, in order (see `examples/c1_example.js`) |
| 5 | `python calibrate.py` | Pass 1 without splitting on a tall page, measures each Body, writes `scale.json` for the splitter |
| 6 | `./build.sh` | `assemble.sh` → `latexomml.py` → `eqmeta.py` → `node deck.js` → `post.py` → `inject.py` (+ `eqcolor.py`) → `deck_md.js` → `frame.py` (→ `Final.pptx`) |
| 7 | checks of §10 | |
| 8 | copy **`Final.pptx`** to `<output>/<deck_name>.pptx` | The only file that leaves `temp/` |

Section-file calls: `T(title, subtitle, items)` full width, `S(title, subtitle, items, fig, caption)` half + image, `TB(title, subtitle, items, rows, colW, caption, fontSize)` half + table, `SEC(name, contents)` divider. No title or closing slide in the sections, `frame.py` adds both (V6.8).
Items: plain string = bullet (`**bold**`, `_{sub}`, `^{sup}` allowed), `'§#N'` = source equation N, `'§ …'` = linear equation (§4b), `'› sym | meaning;  sym | meaning'` = symbol lines.

---

## 📐 Base rules kept from v4 (amended where v5 differs)

### 0. Working files
Every intermediate file lives under `temp/<NN>_<short_name>/` with `sections/`, `extract/`, `build/` (figures in `<output>/figs/`, docs in `<output>/docs/`, see V5 §2). Create the folder first. Keep `temp/` after delivery so revisions are cheap.

### 1. House style
- **Canvas** `LAYOUT_WIDE` 13.333 × 7.5 in, **white** content slides, no bars, stripes or gradients. Only dividers carry a pattern.
- **Exactly two text boxes per content slide**, `Title` (x 0.6, y 0.35, w 12.1, h 0.8) and `Body`, plus an optional image caption. No footer.
- **Level markers** in titles: write ◆, ■ or ● to switch the title bullet on. Its glyph and color are chosen per topic (V6.7). Never a section number in a title.
- **Bold key words** in bullets cycle red `B91C1C`, blue `1D4ED8`, green `15803D`, purple `6D28D9`. Plain text near-black `111827`.
- **Half-and-half rule**: with an image, text left (x 0.6, w 5.9) and image right (x 6.85, y 1.35, w 5.9, h 5.2). Without, full-width Body (x 0.6, y 1.3, w 12.1, h 5.7). A table may take the right half.
- **Captions** (V6.9): **Figure :** bold italic + description italic near-black Arial 12 pt + (source) in Agency FB orange-brown, directly under the image and left-aligned with it. `_x` and `_{…}` render as real subscripts.
- **No slide-count limit.** Split, never shrink.

### 2. Section dividers
- A pattern-filled divider before every main section (not before the title slide or Summary). Patterns and colors cycle hexagons/red, stripes/blue, dots/green, waves/purple, triangles/teal, arcs/orange, grid/navy (`figs_prep.py`), with a solid white panel and a 3 pt border in the section color.
- Panel text: the **section name** large in the font and color of the topic that follows it (V6.7), and one line listing what the section covers in Verdana bold 18 pt. **No "Section N" line** (V5 §3).

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
1. Ask for the method name, method group and lecture number (V6.6) unless the user gave them. Say in one sentence what you are building, then start (archive first if a deck exists, V5 §1).
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
