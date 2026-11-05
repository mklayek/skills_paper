---
name: png-explain
description: Build one 16:9 explainer PNG in infographic style (white page with border, bold black title, 2 or 3 side-by-side concept panels with header pills, a definition, a schematic, a boxed equation with symbol list, Key points and Example boxes with icons, and a comparison table). Use when the user says "png-explain", or asks for an infographic, a concept comparison sheet, or an explainer image like examples/reference_style.png (e.g. "self vs mutual induction as one image", "compare X and Y in one PNG").
---

# png-explain: one 16:9 infographic-style explainer PNG

Trigger word: **png-explain**. The output is one PNG (16:9, 2560 × 1440 px) that explains two or three
related concepts side by side, plus its `.tex` and an `.md` copy. The layout follows
`examples/reference_style.png` (the user's reference) with the user's modifications below.
A finished example is `examples/self_mutual_induction_explain.png`, made by
`examples/spec_self_mutual_induction.py`.

## Style (the user's words always override)

| Rule | What it means |
|---|---|
| **Background always white** | Page, panels, boxes and table are all white. No tinted fills, no gradients. Color appears only in outlines, header pills and highlighted words |
| **Mostly black** | Body text, equations, symbol lists and table cells are black (`111111`). Color is used **only to highlight**: key phrases (`\kw{...}`), the one accent word in the title (`\hl{...}`), panel outlines and pills, arrows and field lines in figures |
| **Border** | A navy (`0B2A55`) 2.6 pt rounded frame around the whole page (drawn by the generator) |
| **16:9** | `16 in × 9 in` page, rendered at 160 dpi to 2560 × 1440 px |
| **Proper bullets** | Real `itemize` lists with a colored bullet and a hanging indent. One idea per bullet, short sentences, no run-on lists |
| **Figures** | Images downloaded from the web, or generated with **TikZ / circuitikz** or **Python (matplotlib)**. Never hand-drawn placeholders |
| **Text size** | As large as fits. Defaults: title 34 pt bold, body 14 pt, equations 21 pt, Helvetica (sans). The generator shrinks the figures first, then the body, only if the page overflows |
| **Writing** | US English. No em dashes, no semicolons in prose |

Panel colors come from a fixed set: `blue`, `red`, `green`, `purple`, `orange`, `teal`, `navy`, `rose`.
Use `blue` and `red` for two panels, and add `green` for a third.

## Layout (built by `scripts/png_explain.py`)

1. **Title** centered, bold black, one word or symbol in red through `\hl{...}` (e.g. `Self Induction \hl{\&} Mutual Induction`).
2. **Subtitle** in gray capitals between two thin rules (e.g. `Electromagnetism · Inductance`).
3. **2 or 3 panels** side by side, all the same height. Each panel has:
   - a colored outline with the panel name in a **header pill** at the top center;
   - a **definition** sentence (black, key phrase in the panel color with `\kw{...}`);
   - a row with the **figure** on the left (`figure_width`, default 0.56 of the panel) and, on the right, the **equation box** (white, colored outline) with the **symbol list** under it;
   - two small boxes side by side: **Key points** (key icon, panel color) and **Example** (light-bulb icon, green / orange / purple), each with real bullets.
4. **Comparison table** across the full width (optional), navy pill title, a header row naming each panel in its color, black cells, thin gray rules.

## The content spec

Each image is described by one Python file holding `SPEC` (raw strings, so LaTeX needs no escaping):

```python
SPEC = {
    "title": r"Self Induction \hl{\&} Mutual Induction",
    "subtitle": "Electromagnetism · Inductance",
    "sizes": {"body_pt": 14, "eq_pt": 21, "fig_h": 2.45, "title_pt": 34},   # optional
    "panels": [
        {
            "head": "Self induction", "color": "blue",
            "definition": r"... induces an emf in the \kw{same coil}.",
            "figure": {"tikz": r"\begin{circuitikz} ... \end{circuitikz}"},
            #   or    {"image": r"...\figs\web_coil.jpg", "credit": "Source name"}
            "figure_width": 0.56,                                            # optional
            "equation": r"e=-L\,\frac{dI}{dt}",
            "symbols": [("e", "induced emf (V)"), ("L", "self inductance (H)"), ("dI/dt", "rate of change of current (A/s)")],
            "points": ["Also called the \\kw{back emf}.", "..."],            # Key points bullets
            "example": ["...", "..."],                                       # Example bullets (or one string)
            # optional: "points_title", "example_title", "example_color"
        },
        {...},
    ],
    "table": {"head": "Self induction vs mutual induction",
              "rows": [("Coils", "One coil", "Two coils"), ...]},            # one value per panel
}
```

- Symbols are written in math mode. Use the inline form `dI/dt` in symbol lists, because stacked fractions come out tiny there.
- Use `\kw{...}` for one or two key phrases per panel. Do not color whole sentences.
- Keep definitions to 2 lines and bullets to 1 or 2 lines each.

## Figures

1. **TikZ / circuitikz** (preferred for circuits, coils, field lines, vectors): put the whole `tikzpicture` or `circuitikz` environment in `"tikz"`. Draw it at about the slot size (10 to 11 cm wide, use `scale=1.3` to `1.4`). The generator only **shrinks** a figure to fit, never enlarges it. Nodes use the body font automatically, so do not add `\small`. Black lines, a colored arrow for current (red), dashed blue for field lines.
2. **Python (matplotlib)**: write the figure script first, save a PNG (white background, `dpi=300`, labels ≥ 11 pt, deep colors), then pass it as `{"image": path}`.
3. **Downloaded images** (photos of equipment and the like): save them into the task's `figs\` folder and pass them with `"credit"`. The credit appears as a small gray caption under the image. **Never write licensing or permission notes**: these images are for class use, and the credit line is enough.

## Workflow

1. **Content first.** Collect the user's text (or the source). If the user asks for a detailed Markdown first, write it in `docs\<name>.md`, then build the spec from it. Otherwise the generator writes the `.md` copy from the spec.
2. **Write the spec script.** For `PPT_class_kr` work it goes in the flat `PPT_class_kr\scripts\` folder as `NN_<Folder>_<name>_png_explain.py` (next free number), starting with
   ```python
   import sys; sys.path.insert(0, r"D:\claudecode\TEACHING\.claude\skills\png-explain\scripts")
   from png_explain import build
   ```
   and ending with
   ```python
   if __name__ == "__main__":
       sys.exit(build(SPEC, out=r"...\figs\NN_<Name>.png", docs=r"...\docs", work=r"...\temp\build_png_explain_<name>"))
   ```
   Elsewhere, put the spec next to the task (not at the project root).
3. **Make the figures** (TikZ inside the spec, or Python / downloaded PNGs in `figs\`).
4. **Run** the spec script. `build()`:
   - archives an existing PNG to `<out>\..\..\archive\previous_<name>\`;
   - compiles twice with pdflatex and checks the page count, shrinking the figures and then the body until the page fits;
   - writes the PNG, `docs\<name>.tex` and `docs\<name>.md`.

   It returns 0 when the page fits.
5. For `PPT_class_kr`, refresh the code docs: `python D:/claudecode/TEACHING/PPT_class_kr/scripts/03_CodeDocs_build_code_docs.py`.
6. **Edit spec scripts with the Write / Edit tools or a Python file**, never with a bash heredoc. The shell mangles TeX backslashes (`\f`, `\t`, `\v`).

## File placement

- The final PNG goes where the user says (usually the topic `figs\` folder), named with the next free `NN_` prefix.
- `.tex` and `.md` go in the task's `docs\`, and the pdflatex run goes in `temp\build_png_explain_<name>\`.
- Archive before overwriting: the generator does this for the PNG, and you archive the spec script yourself.

## QA (required)

- The log line says **Pages: 1** and **overfull boxes: 0**. Report any auto-fit shrink the run printed.
- **Look at the PNG**. Check that:
  - the background is white everywhere;
  - text is black and color only highlights;
  - the panels are the same height and the pills are not clipped;
  - figure labels are readable (≥ about 11 pt in the image) and nothing overlaps;
  - the table fits inside the border.
- US English, no em dashes, no semicolons in prose.

## Requirements

MiKTeX/TeX Live with `tcolorbox` (most), `fontawesome5`, `circuitikz`, `helvet`, `tabularx`, `adjustbox`, and
`xcolor` with `table`. `pdftoppm` (poppler) is needed to rasterize.
