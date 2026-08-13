# Web-style HTML output (docked TOC + offline MathJax)

The preferred HTML deliverable is a **single self-contained web page** that reads like
a documentation site. `scripts/build_report.py to_html` produces it. Assets live in
`scripts/`: `report_web.css`, `report_web_toolbar.html`, `report_web_lightbox.html`,
`mathjax_tex_mml_svg.js`, and `finalize_web_html.py`.

## What the reader gets

- **Left docked Table of Contents** (`nav#TOC`, `position:fixed` on the left), always
  visible and clickable. A **scrollspy** highlights the section currently being read
  and auto-scrolls the dock to keep it in view. Content sits in `<main id="rmain">`
  offset to the right of the dock.
- **Floating top toolbar**: ☰ Contents (toggle the dock), 🖨 Print / PDF, ↔ Full width,
  A− / A+ (font size), ⤒ Top, 🔄 Reset. The `Reset` button restores dock, width, font,
  and closes the zoom viewer.
- **Click-to-zoom lightbox** on every figure (scroll to zoom inside the viewer, Esc to
  close).
- **Light theme only**, Times New Roman body, justified text, descending heading
  hierarchy (chapters > sections > subsections), tables and wide blocks scroll inside
  their own box.
- **Offline MathJax (SVG)** equations with the right-click MathJax Contextual Menu
  (Show Math As -> TeX / MathML, Copy to Clipboard, Accessibility, Zoom) and
  **right-aligned equation numbers**.
- Everything is embedded (images as data URIs, MathJax inline), so the page is one
  portable file. Keep images high resolution; do not downscale by default.

## Build

```
pandoc REPORT.md -o REPORT.html --standalone --embed-resources \
  --toc --toc-depth=3 --mathjax=scripts/mathjax_tex_mml_svg.js \
  -c scripts/report_web.css \
  --include-before-body=scripts/report_web_toolbar.html \
  --include-after-body=scripts/report_web_lightbox.html
python scripts/finalize_web_html.py REPORT.html scripts/mathjax_tex_mml_svg.js
```

`report_web_toolbar.html` opens `<main id="rmain">`; `report_web_lightbox.html` closes
it and carries the toolbar + scrollspy + lightbox JavaScript. Headings carry their own
numbers (`## 6.2 ...`), so do **not** pass `--number-sections` for this style (it would
double-number).

## MathJax gotchas (these cost real debugging time — respect them)

1. **Never rely on pandoc's inlined bundle alone.** `--mathjax --embed-resources`
   inlines MathJax as a raw `<script>` with **no `src`**; MathJax startup cannot locate
   itself and never typesets (equations show as raw `\(...\)`). The finalizer removes
   that inline bundle and re-injects a **config `<script>` + the bundle as a plain
   inline `<script>`** just before `</body>`.
2. **Do not use a `data:` URI for the bundle `src`.** A ~2 MB base64 data URL is
   rejected by the browser as `net::ERR_INVALID_URL` (too long).
3. **Use the SVG bundle** (`tex-mml-svg.js`), not CHTML. SVG output embeds its own glyph
   paths and needs **no external fonts**, so it works fully offline. CHTML fetches web
   fonts from a CDN.
4. **Avoid autoload-only TeX macros.** MathJax autoloads some extensions (e.g.
   `\boldsymbol`, `\bm`, `\color`, `\cancel`) from a relative URL that 404s offline, and
   **one such failure aborts the entire typeset pass** (every equation then shows raw).
   Write the stress tensor as `\sigma` (not `\boldsymbol{\sigma}`), etc. Base + AMS
   macros (`\mathbf`, `\mathit`, `\frac`, `\tfrac`, `\big`, `\Big`, `\nabla`, `\partial`,
   `\int`, `\sum`, greek, `\otimes`, `\simeq`, `\dagger`) are all fine.
5. **Equation numbers**: write `$$ ... \tag{N}$$` (never `\qquad (N)`). With
   `tags:'ams'` MathJax right-aligns `\tag{N}` to the margin. Static MathML (an earlier
   fallback) does not support `\tag`, which is another reason MathJax is used here.

## Verifying (optional but recommended)

MathJax needs a real `http(s)` origin, so serve the file (`python -m http.server`) and
open it; `file://` blocks scripts in some browsers. A quick check that it worked:
`document.querySelectorAll('mjx-container').length` should be > 0 with no TeX-error
`merror` nodes. One bad macro anywhere zeroes the whole count (see gotcha 4).
