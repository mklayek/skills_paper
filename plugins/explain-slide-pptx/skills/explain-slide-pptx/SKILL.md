---
name: explain-slide-pptx
description: Build editable 16:9 PowerPoint "explain" slides in the png-explain infographic style (navy border, bold title with one accent word, a "What is X?" intro strip, 1 to 4 panels with header pills, definition, figure + credit, native equation box, symbol list, Key points and Example boxes). One slide or a whole set from texts and figures, with a color palette per slide (cycle, list or per-slide; outline or tinted fill; text color). Use when the user asks for slides "like the solenoid slide", "explain slides", an infographic PPTX, or a png-explain style deck as PPTX.
---

# 🧩 explain-slide-pptx: infographic explain slides as native PPTX

Reference look: `assets/reference_solenoid_classic.png` (palette `classic`) and
`assets/reference_rlc_ocean_tint.png` (palette `ocean-tint`). The original hand-built slide is
`assets/reference_solenoid_slide.pptx`.

**Everything is native and editable**: text boxes, rounded boxes, pills and bullets are PowerPoint
shapes, equations are real PowerPoint equations (LaTeX → OMML through pandoc). Only figures are
pictures (photos, plots, a TikZ drawing compiled to PNG). Never paste a rendered image of text or of an equation.

## 🔧 Quick start

```bash
python <skill>/scripts/explain_slides.py <spec.py>          # builds the PPTX (+ Markdown copy)
powershell -NoProfile -ExecutionPolicy Bypass -File <skill>/scripts/export_slides.ps1 <deck.pptx> <out_folder>
```
`explain_slides.py` prints one line per slide with its palette and ends with **✅ no fit warnings**
(exit 0) or a list of `⚠️` fit warnings (exit 2). Then export, look at every PNG, fix, rebuild.
The worked example is `examples/example_spec.py` (two slides, two palettes).

## 📐 Slide anatomy (fixed geometry, 13.333 × 7.5 in)

| Part | Spec key | Notes |
|---|---|---|
| Border | — | rounded frame in the palette `frame` color |
| Title | `title`, `highlight` | Arial bold 28 pt, the `highlight` word in `title_hl` color |
| Subtitle | `subtitle` | gray capitals between two rules, e.g. `What it is · Field · Uses` |
| Intro strip | `intro` | full width: figure │ definition + bullets │ equation box + symbols. Optional |
| Panels | `panels` (1 to 4) | header pill, definition, middle row (figure │ equation + symbols), Key points + Example boxes at the bottom. Below 3.4 in panel width the two boxes stack |

Layout flows top-down from **measured** text heights (Windows Arial / Times metrics). The middle row
gets what is left. If the equation and symbols do not fit beside the figure, the symbols move under
the figure. Anything that still does not fit is reported as a warning: shorten the text, never shrink below the sizes.

## ✍️ The spec file (`DECK`)

```python
DECK = {
    "output": r"...\Deck.pptx",            # final deck (top of the task folder)
    "md": r"...\docs\Deck.md",              # Markdown copy (required by the house rules)
    "work": r"...\temp\build_explain",      # optional: TikZ builds
    "palettes": "cycle",                    # "cycle" | "ocean" | ["classic", "sunset-tint", ...]
    "fill": None,                           # optional deck-wide "outline" | "tint"
    "sizes": {"body": 14, "small": 13, "sym": 13, "eq": 16, "title": 28},
    "slides": [{
        "title": "The Solenoid", "highlight": "Solenoid",
        "subtitle": "What it is · Magnetic field · Uses",
        "palette": "forest",                # optional per-slide override
        "fill": "tint", "text_color": "0B2A55",   # optional per-slide overrides
        "intro": {"head": "What is a solenoid?",
                  "figure": {"image": r"...\figs\coil.png", "credit": "Wikimedia Commons"},
                  "definition": "A **solenoid** is ...",
                  "points": ["...", "..."],
                  "equation": [r"\oint \mathbf{B}\cdot d\mathbf{l}=\mu_0 I_{\mathrm{enc}}", r"\Rightarrow Bl=\mu_0NI"],
                  "symbols": [("$I_{enc}$", "current through the loop"), ("$l$", "length (m)")]},
        "panels": [{"head": "Magnetic field",
                    "definition": "...", "figure": {"image": r"..."} | {"tikz": r"\begin{tikzpicture}...\end{tikzpicture}"},
                    "figure_width": 0.52,
                    "equation": r"B=\mu_0\frac{N}{l}I",      # one LaTeX string or a list (one line each)
                    "symbols": [("$B$", "field inside (T)")],
                    "points": ["...", "..."], "points_title": "Key points",
                    "example": ["...", "..."], "example_title": "Example",
                    "color": None, "example_color": None}],   # optional color overrides (hex)
    }],
}
```

**Text markup** (definitions, bullets, symbols): `**key phrase**` → bold in the panel color,
`$B$` → Times italic math, `_{0}` / `^{2}` → real subscript / superscript (inside or outside `$…$`).
Write Greek and symbols as Unicode (μ, ω, ζ, ∝, ½, π, ×, −). Equations in `equation` are LaTeX.

## 🎨 Palettes (`scripts/palettes.py`)

| Name | Look | Name | Look |
|---|---|---|---|
| `classic` | navy intro, blue / red / green / purple panels | `ocean` | teal / blue / sky / indigo |
| `sunset` | orange / rose / amber / crimson | `forest` | greens and teal |
| `berry` | violet / pink / magenta / indigo | `slate` | slate / teal / rust / blue |
| `<name>-tint` | same colors, boxes filled with a light tint | `classic-navytext` | body text in navy |

- **Switching colors per slide:** `"palettes": "cycle"` walks `CYCLE` (classic → ocean → sunset → forest → berry → slate), a list repeats in order, and `"palette"` on a slide wins.
- **Fill vs outline:** `-tint` palettes, or `"fill": "tint"` on the deck or a slide.
- **Text color:** palette `text`, or `"text_color"` on a slide.
- **New palette:** copy an entry in `PALETTES`. Keep panel colors dark enough for white pill text, and give each panel an Example color that differs from it.

## ✅ QA (required before delivery)

1. The build ends with **✅ no fit warnings**.
2. Export with `export_slides.ps1` and **look at every slide**. Check that no text touches a box edge, the equations sit inside their boxes, the pills are not clipped, and the figures are readable.
3. A Markdown copy exists (`md`).
4. Writing: US English, no em dashes, no semicolons in prose. Credit web images in `credit` only (no licensing notes).

## 🚩 Common mistakes

| Mistake | Fix |
|---|---|
| Rendering equations or text as PNG | equations go in `equation` (LaTeX → native OMML). Text is always a text box |
| Long definitions (4+ lines) | the figure row shrinks. Keep definitions ≤ 3 lines, bullets ≤ 2 lines |
| Four panels with long text | four panels stack their boxes and are narrow. Use 2 or 3 panels, or split into two slides |
| Lowering `body` below 14 to make text fit | shorten the text instead (user rule: body text at least 14 pt) |
| Editing the PPTX by hand, then rebuilding | change the spec and rebuild. The spec is the source |
| Closing the user's PowerPoint files | `export_slides.ps1` closes only its own copy and never calls `Quit` |

## 📦 Files

| Path | What |
|---|---|
| `scripts/explain_slides.py` | generator (spec → PPTX + MD, fit warnings) |
| `scripts/palettes.py` | palettes, `CYCLE`, `tint()` |
| `scripts/export_slides.ps1` | PowerPoint export of every slide to PNG (QA) |
| `examples/example_spec.py` + `examples/figs/` | two-slide worked example (classic + ocean-tint) |
| `examples/example_deck.pptx` / `.md` | its output |
| `assets/reference_*.png`, `assets/reference_solenoid_slide.pptx` | reference renders and the original slide |

Requirements: Windows (fonts in `C:\Windows\Fonts`, PowerPoint for the export), Python with
`python-pptx`, `lxml`, `Pillow`, **pandoc** (equations), pdfLaTeX + poppler only for TikZ figures.
