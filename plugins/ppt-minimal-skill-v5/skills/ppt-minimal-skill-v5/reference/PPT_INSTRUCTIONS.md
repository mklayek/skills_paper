# 📐 PPT Instructions (EM Methods deck, Telford Chapter 7)

> 🗓️ Collected 2026-10-14 (updated for v4: section names as titles) from the user's instructions in this session, PPT work only.
> 🧰 Builder: **ppt-minimal-mkl v4** skill. These instructions sit on top of its house style, and where they differ, these win.
> 📄 Deck: `02_EM_ppt\EM_Methods_Telford_Ch7.pptx`. Source: `01_telford_ch7\docs\Telford_Ch7_Electromagnetic_Methods.md`.

---

## 📁 1. Folders and files

| What | Where |
|---|---|
| 🎯 Final deck | `07_EM_Method\02_EM_ppt\EM_Methods_Telford_Ch7.pptx` (top of the output folder) |
| 📝 Markdown copy of the deck | `07_EM_Method\02_EM_ppt\docs\EM_Methods_Telford_Ch7.md` |
| 📐 These instructions | `07_EM_Method\02_EM_ppt\docs\PPT_INSTRUCTIONS.md` |
| 🖼️ Figures used by the deck | `07_EM_Method\02_EM_ppt\figs\` |
| 🔧 Temporary and build files | `07_EM_Method\02_EM_ppt\temp\01_em_deck\` with `build\`, `sections\`, `extract\` |
| 🗄️ Archived earlier versions | `07_EM_Method\02_EM_ppt\archive\<date>_v<N>\` |

- The output folder is `07_EM_Method\02_EM_ppt\`.
- Temporary files go in `temp\` of that folder. The same rule applies to other file types: docs in `docs\`, figures in `figs\`, other types in their own subfolders.
- Nothing temporary sits at the top of the output folder. Only the `.pptx` does.

## 🗄️ 2. Archive first

- **Before changing or regenerating the deck, archive the current version** (the PPTX, its MD copy, the slide sources and the build scripts) to `archive\<date>_v<N>\`.
- Never overwrite an archived version.

## 🚫 3. No numbers on slides

- ❌ No equation numbers.
- ❌ No page numbers.
- ❌ No footer of any kind (no slide numbers, dates or source lines).
- ❌ No figure numbers, including printed captions or text inside the figure images. Crop them out of the figures.
- ❌ No section numbers, including on the section divider slides.

## 🧮 4. Equations

- **No equation from the source may be left out.** All of them are included, and a coverage check must show none missing.
- **Detailed derivations** are included, one step per line, each with a short line saying what was done.
- **Symbols explained** directly under each equation in the existing ▸ style, with the symbol in bold teal, then its meaning and unit.
- Equations are **native, editable PowerPoint equations**, displayed professionally.
- 🎨 **Color: left-hand side and right-hand side in different colors**, and the **next equation uses another set**. The sets alternate:

| Equation | Left-hand side | Right-hand side |
|---|---|---|
| 1st, 3rd, 5th … | ⚫ black | 🔵 deep blue |
| 2nd, 4th, 6th … | 🔴 dark red | 🟢 green |

## 🖼️ 5. Figures

- **No figure may be left behind.** All figures from the source are used, with a coverage check showing none unused.
- Each figure slide is **enriched with details**: what is plotted, what it shows and how to read it.
- Image on the right half, text on the left half, aspect ratio kept, no overlap.

## 🔤 6. Body text

- **Bullet text is 22 pt.**
- **No subtitle under the title by default.**
- **Keep a subtitle where one is required, mainly where a definition starts** (for example "Definition: the Lorentz condition"). Case histories also keep a subtitle naming the site.
- Text that does not fit moves to a continuation slide. It is never shrunk below 22 pt.

## 🏷️ 7. Slide titles

- **Copperplate Gothic (bold) is the default title font.**
- **Each section uses a different title font**, and **the title color changes when the topic or section changes**:

| Section | Title font | Color |
|---|---|---|
| Title slide, Introduction, Summary | Copperplate Gothic Bold | Navy |
| Electromagnetic Theory | Copperplate Gothic Light (bold) | Red |
| Equipment and Ground Systems | Rockwell | Blue |
| Airborne EM Systems | Gill Sans MT | Green |
| Interpretation: FDEM over Sheets | Book Antiqua | Purple |
| Interpretation: TDEM and the Sphere | Century | Teal |
| EM Depth Sounding | Garamond (bold) | Orange |
| Interpretation of Airborne EM | Palatino Linotype | Navy |
| Field Examples and Problems | Trebuchet MS | Red |

- **Use the source's section names as slide titles whenever possible**: the subsection name (■, e.g. "Vector and Scalar Potentials") or the lettered part name (●, e.g. "Amplitude and phase relations"). The book's letters such as "(b)" are dropped and its semicolons become colons. Where no section name fits (field examples, problems, the title slide and the summary), keep the descriptive title.
- **When a topic continues onto the next slide, use the same title followed by "(continued)"**, for example "Vector and Scalar Potentials (continued)".

## ✍️ 8. Writing style

- 🇺🇸 US English.
- No em dashes.
- No semicolons.

## 🖥️ 9. Working practice

- ❌ **Do not close other PowerPoint files** that are unrelated to the task. Export scripts close only the deck they opened, and never quit PowerPoint while other presentations are open.
- 📝 Keep a Markdown copy of the deck alongside the PPTX.
- 🚀 Push to GitHub only when the user asks, for that push only.

## ✅ 10. Checks before delivery

- Equation coverage: 0 missing. Figure coverage: 0 unused.
- Number scan clean: no equation, figure, table, page or section numbers, and no footer fields.
- No text past the slide edges or into the image in the PowerPoint render.
- Every slide viewed once on contact sheets.
- MD copy rebuilt, previous version archived.
