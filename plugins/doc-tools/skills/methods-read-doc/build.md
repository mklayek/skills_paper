# Build recipe — PDF + DOCX for a methods read-doc

**Strict order: ① MD → ② TEX → ③ PDF → ④ DOCX.** Write and verify the Markdown first, generate the `.tex`
intermediate second, compile the PDF from that `.tex` third, and produce the DOCX fourth. Keep the `.tex`.

Renders the Markdown into a PDF with **rectangular bordered key-term boxes** and **1.15 line spacing**,
and a DOCX with the same boxes and spacing. Robust on machines whose xelatex/lualatex fonts are broken:
uses **pandoc → pdflatex** with explicit Unicode mapping.

## Tools
- `pandoc` (system, or the bundled binary from `pip install pypandoc_binary`; find it with
  `python -c "import pypandoc; print(pypandoc.get_pandoc_path())"`).
- `pdflatex` + TeX Live packages `mdframed`, `setspace`, `newunicodechar`, `graphicx`, `xcolor`, `textcomp` (all standard).
- `pdftoppm` to rasterize schematics / preview pages.

## Filenames and mirroring
- Name: `[Methods_read<NN>]_<YYYYMMDD>_<topic>.md` (also `.pdf`, `.docx`). Get the stamp from `date +%Y%m%d` / `date +%Y%m%d_%H%M%S`.
- Write Markdown to local scratch first (e.g. `/DATA1/mkl/...`), then copy `.md/.pdf/.docx` to the output/NAS folder. Keep figures in a `figures_*` subfolder beside the doc.

## PDF (rectangular boxes + 1.15 spacing + Unicode-safe)
Generate a standalone `.tex`, inject a preamble, then compile twice:

```bash
PB=$(python -c "import pypandoc;print(pypandoc.get_pandoc_path())")   # or: PB=pandoc
"$PB" DOC.md -o DOC.tex --standalone --toc -V geometry:margin=1in

python3 - DOC.tex <<'PY'
import sys,re
p=sys.argv[1]; t=open(p).read()
t=re.sub(r'alt=\{[^{}]*\}\s*,?','',t)          # pandoc 3.x emits \includegraphics[alt=...]; graphicx rejects it
pre=(r"\usepackage{xcolor}""\n"
     r"\usepackage{textcomp}""\n"
     r"\usepackage{graphicx}""\n"
     r"\graphicspath{{/ABS/PATH/TO/DOCDIR/}}""\n"      # so figures_*/x.png resolve
     r"\usepackage[framemethod=default]{mdframed}""\n"
     r"\surroundwithmdframed[linewidth=0.6pt,linecolor=black!55,backgroundcolor=black!4,"
     r"innertopmargin=6pt,innerbottommargin=6pt,innerleftmargin=8pt,innerrightmargin=8pt,"
     r"skipabove=6pt,skipbelow=6pt]{quote}""\n"        # every blockquote -> rectangular box
     r"\usepackage{setspace}\setstretch{1.15}""\n"       # 1.15 line spacing
     r"\usepackage{newunicodechar}""\n")
for ch,rep in [("—","\\textemdash"),("–","\\textendash"),("·","\\textperiodcentered"),
   ("è","\\`e"),("á","\\'a"),("ø","\\o"),("§","\\S"),("°","\\textdegree"),
   ("π","\\ensuremath{\\pi}"),("→","\\ensuremath{\\rightarrow}"),("×","\\ensuremath{\\times}"),
   ("⇒","\\ensuremath{\\Rightarrow}"),("⌈","\\ensuremath{\\lceil}"),("⌉","\\ensuremath{\\rceil}"),
   ("⌊","\\ensuremath{\\lfloor}"),("⌋","\\ensuremath{\\rfloor}"),("≈","\\ensuremath{\\approx}"),
   ("≤","\\ensuremath{\\le}"),("≥","\\ensuremath{\\ge}"),("∼","\\ensuremath{\\sim}"),
   ("∈","\\ensuremath{\\in}"),("∎","\\ensuremath{\\blacksquare}"),("★","")]:
    pre+="\\newunicodechar{%s}{%s}\n"%(ch,rep)
open(p,'w').write(t.replace("\\begin{document}",pre+"\\begin{document}",1))
PY

pdflatex -interaction=nonstopmode -halt-on-error DOC.tex >/dev/null 2>&1
pdflatex -interaction=nonstopmode -halt-on-error DOC.tex   # 2nd pass for TOC
```

Notes:
- The key-term boxes are Markdown blockquotes (`> …`). `\surroundwithmdframed{quote}` turns every blockquote into a rectangular framed box. The only blockquotes in a read-doc are the key-term boxes, so this is exact.
- If a display equation must sit inside a box, every line of that `$$…$$` also starts with `> ` in the Markdown.
- Extend the `newunicodechar` list if pdflatex reports another missing glyph.

## DOCX (bordered boxes + 1.15 spacing)
Build a reference docx once with `make_refbox.py`, then convert:

```bash
python3 make_refbox.py refbox15.docx          # bordered "Block Text" style + 1.15-spaced Normal
"$PB" DOC.md -o DOC.docx --standalone --toc --mathml --reference-doc=refbox15.docx
```
Pandoc renders Markdown blockquotes with the `BlockText` paragraph style; `make_refbox.py` gives that style a
rectangular border + light shading, and sets `Normal` to 1.15 line spacing. Equations render as native Office MathML.

## Optional: red-marked "what changed" variant
Diff at word level against a baseline `.md`, wrap inserted/changed words in `[…]{.new}`/`<span class="new">…</span>`,
protect math/`$…$`/images/URLs from the diff, and color with a Lua filter (`\textcolor[HTML]{CC0000}{…}` for LaTeX,
a "RedText" custom character style for DOCX). Keep math whole so a span never splits a `$…$`.

## Verify
- After stitching multi-agent parts: `grep -c '\\tag{' DOC.md` equals the source's equation count, and no duplicate tags.
- Rasterize a page with a box to confirm the rectangle renders: `pdftoppm -png -r 110 -f <p> -l <p> DOC.pdf pg`.
