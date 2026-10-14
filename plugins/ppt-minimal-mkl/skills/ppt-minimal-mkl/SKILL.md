---
name: "ppt-minimal-mkl"
description: "Superseded by ppt-minimal-skill-v5 (the default). v4 skill for making a PowerPoint. Use whenever asked for a PPT, PPTX, deck, slides, lecture or teaching presentation from any source (PDF incl. scanned chapters, Markdown, HTML, text, Word, a web page) or from a topic to research. Builds a minimal, white, classroom-ready .pptx with level-marked titles, pattern-backed section dividers and native editable PowerPoint equations. Prefer this over other deck builders unless a Beamer PDF/.tex is wanted (ppt-mkl) or an existing .pptx is being restyled (ppt-to-pptx-restyle)."
---

# ppt-minimal-mkl: minimal scientific teaching decks

**Superseded: `ppt-minimal-skill-v5` is now the default deck builder.** Use this v4 skill only when v4 is asked for by name.

Use this skill when the user asks for a PowerPoint / pptx / slides / lecture deck made from a source: an attached PDF (including scanned book chapters), .md, .html, .txt, .docx, a URL, or "search the internet about X". The output is always a real `.pptx` file sent with SendUserFile.

Also read the built-in `pptx` skill's SKILL.md once for the pptxgenjs gotchas (hex colors without #, `isTextBox: true`, validate script, soffice wrapper). This skill adds the house style and workflow on top.

## 0. Working files: everything temporary under `CWD/temp/`

**Every intermediate file this skill produces — Markdown or any other document format, plus every figure used — lives under `CWD/temp/`, never at the top of the working directory.** One numbered folder per deck, named `<NN>_<short_name>` (`01_antenna_deck`, `02_ip_chapter`, …), with fixed sub-subfolders:

```
CWD/
├── <Deck_name>.pptx              <- the ONLY delivered file, at the CWD top
└── temp/
    └── 01_antenna_deck/
        ├── notes.md              <- running source notes (sections, equations, derivation steps)
        ├── outline.md            <- planned slide list with title levels
        ├── sections/             <- per-section .md drafts, and any other temporary .md/.docx/.txt/.html
        ├── figs/                 <- every figure the deck uses: crops, matplotlib diagrams, sec*.png patterns
        ├── extract/              <- pdftotext dumps, pdftoppm page renders, grid overlays, contact sheets
        └── build/                <- build.sh, deck.js, post.py, inject.py, eqmeta.py, omml.py,
                                     sizes.json, eqmeta.json, eqlist.json, QA renders
```

- **Create the folder first**, before reading the source: `mkdir -p temp/<NN>_<short_name>/{sections,figs,extract,build}`. Pick `<NN>` as the next free number in `temp/`.
- **Run the build from `build/`** so the templates' relative paths resolve: figures are `../figs/...`, notes and sections are `../`. The generator writes the `.pptx` into `build/`, then it is **moved to the CWD top** as the final step.
- **Nothing temporary at the CWD root.** No `notes.md`, `sizes.json`, `img/`, page renders, contact sheets or scratch scripts outside `temp/`. The only thing the user sees in the working directory is the finished deck.
- **Keep `temp/` after delivery** — the notes, crops and generator are what make a revision request ("add three slides on 8.6", "redo that figure") cheap. Delete it only if the user asks.
- If the user names an output folder, the deck goes there and `temp/` is created next to it.

## 1. House style (defaults: the user's words always override)

- **Language: always US English.** US spelling (color, center, meter, aluminum, analyze, modeling, labeled, gray, artifact, fiber, program), US punctuation and US number style (1,000.5). Keep proper names, book titles and quoted source text as printed; convert everything else, including captions, table text and subtitles.
- **Canvas:** `LAYOUT_WIDE` (13.333 × 7.5 in), **white background** on every content slide, no dark slides, no decorative bars, stripes or gradients. Only **section divider slides** (§2) carry a pattern.
- **No footer at all.** No slide numbers, dates, source lines, logos or any other text/shape in the footer area of any slide (content or divider). A slide contains only its Title, Body, and, where used, one image/table with its caption.
- **Exactly two text boxes per content slide** (plus an optional image caption):
  1. **Title box**: Arial bold 28 pt, deep navy `0B2A55`, at x 0.6, y 0.35, w 12.1, h 0.8. objectName `Title`. Plain text only (no sub/superscript markup).
  2. **Body box**: holds the subtitle line, bullets, equations and symbol lines. objectName `Body`.
- **Titles carry no numbers — a level bullet instead.** Never put source section numbers (8.1, 8.2.2, 9.3a …) in any title. Start every content-slide title with a colored level marker, then two spaces:
  - **◆ red `B91C1C`** (22 pt) — primary title: a main topic of a section (e.g. "◆ Introduction"), the deck title slide and the Summary.
  - **■ blue `1D4ED8`** (22 pt) — secondary title: a subsection (source level x.y, e.g. "■ Single current electrode at depth").
  - **● green `15803D`** (24 pt) — tertiary title: a sub-subsection or lettered part (source level x.y.z / x.y.za, e.g. "● Schlumberger array over two beds").
  The marker is its own run in the title; the rest of the title stays Arial bold 28 pt navy. Continuation slides keep the marker and add " (cont.)".
- **Subtitle (first paragraph inside the body box):** bold, 22 pt, **underlined**, in a color and font that **change on every slide** (never the same style on two consecutive slides). Cycle:
  - Georgia, red `B91C1C`, single underline (`sng`)
  - Verdana, blue `1D4ED8`, double (`dbl`)
  - Cambria, green `15803D`, heavy (`heavy`)
  - Trebuchet MS, purple `6D28D9`, dashed (`dash`)
  - Georgia italic, teal `0E7490`, wavy (`wavy`)
  - Tahoma, orange `C2410C`, dotted (`dotted`)
  Keep the subtitle plain text (write e.g. "Vc", not `V_{c}`).
- **Bullets:** ~20 pt, fonts **alternate per bullet**: Times New Roman → Comic Sans MS → Bookman Old Style → repeat (equation and symbol lines do not count in the cycle). Plain text in near-black `111827`; **bold key words in deep colors** cycling red `B91C1C`, blue `1D4ED8`, green `15803D`, purple `6D28D9`. Spoken-natural English.
- **Images are optional per slide.** A slide with an image uses the **half-and-half rule**: text on the left half (x 0.6, w 5.9), image on the right half (x 6.85, y 1.35, w 5.9, h 5.2), aspect ratio preserved, never cropped so that content is hidden, never overlapping text. A slide without an image uses a **full-width** body box (x 0.6, y 1.3, w 12.1, h 5.7). A table from the source (or a comparison table built from the text) may take the right half instead of an image.
- **Captions:** Arial 12 pt italic, gray `374151`, under the image, naming the source (e.g. "Telford et al., Applied Geophysics — Fig. 6.3: …"). Figure and table numbers keep the source's numbering.
- **No slide-count limit.** Split content rather than shrinking text: an overflowing slide continues on a full-width "(cont.)" slide.

## 2. Section divider rule (always)

- Put a **section divider slide at the beginning of every main section** of the source (or the deck's own logical sections if the source has none). Not before the title slide or the final summary.
- **Numbering: "Section 1", "Section 2", …** in deck order — never the source's chapter/section number (not "Section 8.3").
- **Design: pattern-filled.** Full-bleed background image with a light, tinted geometric pattern, and a solid white panel (x 0.6–9.0 in, y 1.55–5.95 in) with a 3 pt border in the section color. Each section uses a **different pattern and color**, cycling: hexagons/red `B91C1C`, diagonal stripes/blue `1D4ED8`, graded dots/green `15803D`, waves/purple `6D28D9`, triangles/teal `0E7490`, concentric arcs/orange `C2410C`, grid-with-blocks/navy `0B2A55`.
- **Text on the panel:**
  - "Section 3" — Arial bold 40 pt in the section color.
  - **Section name in large letters** — Georgia bold, deep navy, 54 pt (40 pt if > 20 characters, 34 pt if > 30), in the `Title` box.
  - One line listing what the section covers ("Chargeability · frequency effect · …") — Verdana bold 18 pt in the section color, in the `Body` box.
- No slide number or footer on dividers either.
- The divider counts as a slide for the subtitle-style cycle, so consecutive slides still differ.

Pattern backgrounds (run once from `build/`; writes `../figs/sec0.png` … `../figs/sec6.png` at 13.333×7.5 in):

```python
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
cols=['#B91C1C','#1D4ED8','#15803D','#6D28D9','#0E7490','#C2410C','#0B2A55']
tint=lambda c,a: tuple(1-(1-np.array(matplotlib.colors.to_rgb(c)))*a)
W,H=13.333,7.5
def base():
    f=plt.figure(figsize=(W,H)); ax=f.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis('off'); ax.set_aspect('equal'); return f,ax
def p_hex(ax,c):
    r=0.45
    for i,x in enumerate(np.arange(0,W+1,r*1.5)):
        for y in np.arange(0,H+1,r*np.sqrt(3)):
            yy=y+(r*np.sqrt(3)/2 if i%2 else 0)
            ax.add_patch(RegularPolygon((x,yy),6,radius=r*0.95,orientation=np.pi/6,fc=tint(c,0.10 if (i+int(yy*3))%4 else 0.22),ec=tint(c,0.35),lw=0.8))
def p_diag(ax,c):
    for k in np.arange(-H,W+H,0.28): ax.plot([k,k+H],[0,H],color=tint(c,0.22),lw=6)
    for k in np.arange(-H,W+H,1.4): ax.plot([k,k+H],[0,H],color=tint(c,0.45),lw=2)
def p_dots(ax,c):
    for x in np.arange(0.2,W,0.35):
        for y in np.arange(0.2,H,0.35):
            d=np.hypot(x-W,y)/15; ax.add_patch(Circle((x,y),0.03+0.09*(1-d)**2,fc=tint(c,0.45),ec='none'))
def p_waves(ax,c):
    x=np.linspace(0,W,600)
    for i,y0 in enumerate(np.arange(-0.5,H+0.5,0.32)): ax.plot(x,y0+0.18*np.sin(2*np.pi*x/2.4+i*0.5),color=tint(c,0.25 if i%3 else 0.5),lw=2.2)
def p_tri(ax,c):
    s=0.8
    for i,y in enumerate(np.arange(0,H+s,s*0.866)):
        for j,x in enumerate(np.arange(-s,W+s,s/2)):
            up=(i+j)%2==0; a=0.08+0.22*((i*3+j*7)%5==0)
            pts=[(x,y),(x+s/2,y+s*0.866),(x+s,y)] if up else [(x,y+s*0.866),(x+s/2,y),(x+s,y+s*0.866)]
            ax.add_patch(plt.Polygon(pts,fc=tint(c,a),ec=tint(c,0.3),lw=0.6))
def p_circles(ax,c):
    for r in np.arange(0.4,16,0.45): ax.add_patch(Circle((W,0),r,fc='none',ec=tint(c,0.3 if int(r/0.45)%3 else 0.55),lw=2))
    for r in np.arange(0.4,6,0.45): ax.add_patch(Circle((0,H),r,fc='none',ec=tint(c,0.25),lw=1.5))
def p_grid(ax,c):
    for x in np.arange(0,W,0.5): ax.plot([x,x],[0,H],color=tint(c,0.2),lw=1)
    for y in np.arange(0,H,0.5): ax.plot([0,W],[y,y],color=tint(c,0.2),lw=1)
    rng=np.random.default_rng(3)
    for _ in range(40): ax.add_patch(plt.Rectangle((rng.integers(0,26)*0.5,rng.integers(0,15)*0.5),0.5,0.5,fc=tint(c,0.3),ec='none'))
for i,(p,c) in enumerate(zip([p_hex,p_diag,p_dots,p_waves,p_tri,p_circles,p_grid],cols)):
    f,ax=base(); p(ax,c)
    ax.add_patch(plt.Rectangle((0.6,1.55),8.4,4.4,fc='white',ec=c,lw=3,zorder=10))   # solid white text panel
    f.savefig(f'../figs/sec{i}.png',dpi=120,facecolor='white'); plt.close(f)
```

## 3. Detail rule (default: detailed)

- Write **full, informative bullets** taken closely from the source: definitions, mechanisms, numbers, ranges, units, names/dates of authors, and the reason behind each point. Avoid one-word or headline-only bullets.
- Aim for **5 bullets beside an image** and **6–7 bullets on a full-width slide**; a slide with fewer than 5 bullets should be expanded or merged. A "(cont.)" slide with only one short item should be avoided by trimming or merging.
- Cover **every section and subsection** of the source in order, using the ◆/■/● title level that matches its depth (no section numbers).
- Add teaching slides that help understanding when the source supports them: **comparison tables** (e.g. method A vs B, array choice), **worked numerical examples** that apply the source's equations (mark the numbers "illustrative"), and the source's **practice problems** or case histories.
- When the user asks for "more detail", add slides rather than cramming.

## 4. Equation rule (always apply when the source has equations)

- **Include every equation** from the source, plus the **intermediate derivation steps** (one step per line, with a short plain bullet saying what was done: "Multiply by r² and integrate", "Substitute (3)").
- **Equation numbers are plain sequential numbers (1), (2), (3) …** with the source's letter suffixes kept ((7a), (7b), (29a)). Drop the chapter prefix: source (8.12) → (12), (9.1) → (1). Update every in-text reference the same way ("substituting A in (10)", "Derivation of Eq. (11)"). Book-section cross-references become plain words ("see the vertical-contact slides"), never "Section 8.6.5". Figure and table numbers are not changed.
- **Every equation is a native PowerPoint equation in Professional (built-up) format** — Cambria Math, 20 pt, deep navy `0B2A55`, left-aligned, indented (marL 457200), no bullet, with the equation number at the end of the same line. Stacked fractions, ∑/∫ with limits above/below, real sub/superscripts and auto-sized brackets. The user can click any equation and edit it in PowerPoint's equation editor. This is done by writing each equation in **linear Unicode form** in the generator, then converting it to OMML (§7b).
- **Directly after each equation (the next line or two), explain every symbol** in a **different bullet style** from normal bullets:
  - bullet character **▸**, teal `0E7490`, indented deeper than normal bullets (marL 914400, indent −228600);
  - symbol in **bold teal Cambria 18 pt**, then " — " and its meaning in Cambria 18 pt near-black, with units where known (e.g. "**M** — chargeability (ms)");
  - several short symbols may share one line, separated by ";".
- Put derivation slides full-width; beside an image only if the equation plus symbol lines fit.
- If the source's printed symbol is ambiguous or a misprint, keep the source form and note it in the symbol line.

**Writing equations in linear form (the `'§ …'` items):**
- Unicode symbols directly: ∇ ∂ ∑ ∫ ρ σ θ λ π Δ δ ∞ ≈ ≫ → ⇒ ± × · ′ ″ ℓ √ and `²`, `³`, `−` (U+2212, not hyphen).
- `_{…}` subscript, `^{…}` superscript (e.g. `ρ_{a}`, `(z² + L²/4)^{3/2}`, `k^{m}`); `∑_{m=1}^{∞}` and `∫_{0}^{2π}` give limits; the n-ary body runs to the next `+ − = ≈ , ;` at that level.
- `/` builds a stacked fraction from the **adjacent** operands, so write operands with **no spaces inside**: `(Iρ/2π)(1/r)`, `dV/dr`, `ΔV/Δr`, `(ρ_{2} − ρ_{1})/(ρ_{2} + ρ_{1})`. Brackets that wrap a whole numerator/denominator are removed in the built-up form. Use `·` to separate a fraction from a following factor (`(a/z)³·(2x²/z² − 1)/(…)`).
- Plain (upright) words go in double quotes: `"or"`, `"(using σ = 1/ρ)"`, `"electrode spacing"`, units `"Ω·m"`, `"m"`.
- End the line with the number: `'§ V = (Iρ/2π)(1/r)  "or"  ρ = 2πrV/I   (12)'`. Optional labels at the start are kept upright: `Medium (1):` or `(i)` … `(v)`.
- One equation per line; for two equations on one idea, use two `§` lines. A very long equation may continue on the next `§` line that starts with 4+ spaces or with an operator (`'§     + 2∑_{m=1}^{∞} k^{m}{…}'`); brackets may be left open at a line end and closed on the next line.

## 5. Workflow

1. **Say in one sentence** what you are building, then start. Ask first only if the source is ambiguous and the deck is large.
1. **Make the working folder** `temp/<NN>_<short_name>/{sections,figs,extract,build}` (§0) and put every intermediate file there from here on.
2. **Get the source content into files:**
   - **PDF:** `pdftotext -layout` and plain `pdftotext`; if it is a scan or equations come out garbled, read pages visually with the Read tool (`pages:` ranges) and take the equations from the page images. Render pages with `pdftoppm -r 200 -png` for figure cropping. Write running notes (every section, every equation with its derivation steps) to `temp/<NN>_<name>/notes.md` so long sources survive context limits; keep the raw dumps and page renders in `extract/`.
   - **DOCX:** `markitdown file.docx` or pandoc. **MD/TXT/HTML:** read directly (strip tags for HTML).
   - **Web:** WebSearch + WebFetch; keep the URLs for a Sources slide. The shell usually cannot download web images, so tell the user and use figures from attached files or clean diagrams instead.
3. **Plan the outline:** title → for each main section: divider slide ("Section N"), then its content slides (concepts → definitions/equations with derivations → methods/equipment → procedure → interpretation/examples → practice) → summary. Assign each slide its title level (◆/■/●). Pick which slides deserve an image; the rest are text-only.
4. **Images, in order of preference:**
   1. Figures from the user's own files: overlay a 5 % grid on rendered pages (two pages side by side per image saves views) to pick crop fractions, crop with PIL, trim whitespace, remove running headers and book captions (the slide caption replaces them), and check the crops on a contact sheet before building. Crops and diagrams go to `figs/`, grid overlays and contact sheets to `extract/`. Write `build/sizes.json` ({name:[w,h]}).
   2. Photos the user attached.
   3. Clean matplotlib diagrams (white background, deep colors, labels ≥ 10 pt, figsize 5.9×5.2 in so they fit the right half exactly).

   Never repeat an image on two slides.
5. **Build** (all steps in one `build.sh`):
   1. `python3 eqmeta.py` — equation widths/heights for the slide-splitter (§7b).
   2. `node deck.js` — pptxgenjs (§6); writes `eqlist.json` (which equations are on which slide).
   3. `python3 post.py Deck.pptx` — bullets and spacing (§7a).
   4. `python3 inject.py Deck.pptx` — replaces each equation paragraph with a native PowerPoint equation (§7b).
   5. `mv Deck.pptx ../../../<Deck_name>.pptx` — the finished deck is the only file that leaves `temp/` (§0).
6. **QA (required):**
   - `python /mnt/skills/public/pptx/scripts/office/validate.py Deck.pptx`
   - Programmatic check with python-pptx: every slide has exactly one `Title` and one `Body` and **no other text box except an image caption** (no slide numbers / footers); every content title starts with ◆, ■ or ●; no title contains a section number (regex `^[◆■●]\s+\d`); normal bullets follow the 3-font cycle at 20 pt; the subtitle style differs from the previous slide; no raw markup (`_{`, `^{`, `**`) left; no chapter-prefixed equation numbers like `(8.12)` left in text (outside "Fig."/"Table"); a divider exists before each main section; the number of injected equations equals the number of `§` lines.
   - **US English check:** extract all text (text frames and table cells) with python-pptx and scan with a regex for British forms, e.g. `\b\w+(isation|ised|ising|yse|ysed|our|tre|tres|lled|lling)\b|metre|centre|colour|behaviour|aluminium|artefact|grey|towards|whilst|amongst|programme|fibre|litre`. Whitelist real words (noise, source, four, hour, contour, precise, rise, expertise, promise, filled, controlled, called, drilling, drilled …) and fix every remaining hit in the generator.
   - **Equation check:** LibreOffice cannot display PowerPoint equations (it shows the text twice), so check the math separately: render every `§` line's parsed tree with matplotlib mathtext (build a LaTeX string from the same tree) and look at every equation once — fractions, limits, brackets and exponents must match the source.
   - **Layout check:** render the deck **before** `inject.py` (plain linear equations) with `python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf Deck.pptx`, then `pdftoppm -jpeg -r 50`, paste into 3×4 contact sheets and look at every slide. Also measure the lowest Body word per page with pdfplumber; anything below y 7.0 in overflows. Fix overflow by trimming bullets or letting the splitter move items to a "(cont.)" slide; fix overlaps and clipped crops. Built-up equations are taller than the linear text, so the splitter reserves ~46 pt per stacked equation line.
7. **Deliver** with SendUserFile and a short summary: slide count, structure, where images came from, anything assumed or unavailable. Mention that equations are native PowerPoint equations (they show as one-line text in Google Slides/LibreOffice). No step-by-step recap.

## 6. pptxgenjs template (core helpers)

Items in a body list: plain string = normal bullet; `'§ equation   (n)'` = equation line (linear form, §4); `'› symbol | meaning'` = symbol line (only the first `|` splits; further `|` become " — "). Markup in bullets and symbol lines: `**bold**`, `_{sub}`, `^{sup}`. Titles: `'◆ Main topic'`, `'■ Subsection'`, `'● Sub-subsection'`.

```js
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const IMG = '../figs';                                          // figures live in temp/<NN>_<name>/figs (§0)
const SZ = JSON.parse(fs.readFileSync('sizes.json'));           // {name:[w,h]} for ../figs/*.png
let EQM = {}; try { EQM = JSON.parse(fs.readFileSync('eqmeta.json')); } catch (e) {}   // from eqmeta.py
const EQL = {};                                                  // slide number -> equations (for inject.py)
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE';
const NAVY='0B2A55', INK='111827', MUTED='374151', TEAL='0E7490', EQC='0B2A55';
const LEADS=['B91C1C','1D4ED8','15803D','6D28D9'];
const FONTS=['Times New Roman','Comic Sans MS','Bookman Old Style'];
const SUBS=[{font:'Georgia',color:'B91C1C',u:'sng'},{font:'Verdana',color:'1D4ED8',u:'dbl'},{font:'Cambria',color:'15803D',u:'heavy'},
  {font:'Trebuchet MS',color:'6D28D9',u:'dash'},{font:'Georgia',color:'0E7490',u:'wavy',italic:true},{font:'Tahoma',color:'C2410C',u:'dotted'}];
const HALF={x:0.6,y:1.3,w:5.9,h:5.7}, FULL={x:0.6,y:1.3,w:12.1,h:5.7}, R={x:6.85,y:1.35,w:5.9,h:5.2};
const BC={'◆':'B91C1C','■':'1D4ED8','●':'15803D'};             // title level markers
let n=0;
function newSlide(title){ const s=pres.addSlide(); s.background={color:'FFFFFF'}; n++;
  const tt=BC[title[0]]?[{text:title[0]+'  ',options:{color:BC[title[0]],fontSize:title[0]==='●'?24:22}},{text:title.slice(2)}]:title;
  s.addText(tt,{x:0.6,y:0.35,w:12.1,h:0.8,fontFace:'Arial',fontSize:28,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  return s; }                                                    // NO slide number, NO footer
const SECC=['B91C1C','1D4ED8','15803D','6D28D9','0E7490','C2410C','0B2A55']; let secN=0;
function SEC(name, contents){ const s=pres.addSlide(); n++; const c=SECC[secN%7];
  s.background={path:`${IMG}/sec${secN%7}.png`}; secN++;
  s.addText(`Section ${secN}`,{x:1.0,y:1.85,w:7.6,h:0.9,fontFace:'Arial',fontSize:40,bold:true,color:c,margin:0,isTextBox:true});
  s.addText(name,{x:1.0,y:2.7,w:7.6,h:1.9,fontFace:'Georgia',fontSize:name.length>30?34:(name.length>20?40:54),bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  s.addText([{text:contents,options:{fontFace:'Verdana',fontSize:18,bold:true,color:c}}],{x:1.0,y:4.75,w:7.6,h:1.0,valign:'top',margin:0,isTextBox:true,objectName:'Body'});
  return s; }
function parse(txt, base, lead){ const out=[]; let bold=false, i=0, buf='';
  const push=(t,ex={})=>{ if(!t) return; out.push({text:t,options:{...base,bold:bold||!!base.bold,color:bold?lead:base.color,...ex}}); };
  while(i<txt.length){
    if(txt.startsWith('**',i)){ push(buf); buf=''; bold=!bold; i+=2; continue; }
    if((txt[i]==='_'||txt[i]==='^')&&txt[i+1]==='{'){ push(buf); buf=''; const j=txt.indexOf('}',i);
      push(txt.slice(i+2,j), txt[i]==='_'?{subscript:true}:{superscript:true}); i=j+1; continue; }
    buf+=txt[i]; i++; }
  push(buf); return out; }
function body(s, subtitle, items, box){ const st=SUBS[(n-1)%SUBS.length];
  const arr=[{text:subtitle,options:{fontFace:st.font,fontSize:22,bold:true,italic:!!st.italic,color:st.color,underline:{style:st.u,color:st.color},breakLine:true}}];
  let k=0;
  items.forEach((it,i)=>{ let r;
    if(it.startsWith('§')){ (EQL[n]=EQL[n]||{half:box===HALF,eqs:[]}).eqs.push(it);      // placeholder text; inject.py swaps in the equation
      r=parse(it.slice(1).trim().replace(/"/g,''),{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true},EQC); }
    else if(it.startsWith('›')){ const raw=it.slice(1), p=raw.indexOf('|');
      const sym=raw.slice(0,p).trim(), mean=raw.slice(p+1).trim().replace(/\s*\|\s*/g,' — ');
      r=[...parse(sym,{fontFace:'Cambria',fontSize:18,color:TEAL,bold:true},TEAL), ...parse(' — '+mean,{fontFace:'Cambria',fontSize:18,color:INK},TEAL)]; }
    else { r=parse(it,{fontFace:FONTS[k%3],fontSize:20,color:INK},LEADS[k%4]); k++; }
    if(i<items.length-1) r[r.length-1].options.breakLine=true; arr.push(...r); });
  s.addText(arr,{...box,valign:'top',margin:[4,4,4,4],isTextBox:true,objectName:'Body',fit:'none'}); }
function caption(s,cap,y){ s.addText(cap,{x:R.x,y:y??R.y+R.h+0.08,w:R.w,h:0.45,fontFace:'Arial',fontSize:12,italic:true,color:MUTED,margin:0,valign:'top',isTextBox:true}); }
function img(s,name,cap){ const [pw,ph]=SZ[name]; const sc=Math.min(R.w/pw,R.h/ph); const w=pw*sc,h=ph*sc;
  const x=R.x+(R.w-w)/2, y=R.y+(R.h-h)/2;
  s.addImage({path:`${IMG}/${name}.png`,x,y,w,h,altText:cap||name});
  s.addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{type:'none'},line:{color:'CBD5E1',width:0.75}});
  if(cap) caption(s,cap); }
function table(s,rows,colW,fs=13){ // header row navy, first column blue bold, zebra rows
  const data=rows.map((r,i)=>r.map((c,j)=>({text:c,options:{fontFace:i===0?'Arial':'Times New Roman',fontSize:fs,bold:i===0||j===0,
    color:i===0?'FFFFFF':(j===0?'1D4ED8':INK),fill:{color:i===0?NAVY:(i%2?'FFFFFF':'F1F5F9')},valign:'middle',margin:[2,6,2,6]}})));
  s.addTable(data,{x:R.x,y:R.y,w:R.w,colW,border:{type:'solid',color:'CBD5E1',pt:0.75},autoPage:false}); }
// ---- height estimate (pt) and automatic "(cont.)" split instead of shrinking text ----
const plain=t=>t.replace(/\*\*/g,'').replace(/[_^]\{([^}]*)\}/g,'$1');
function hgt(it,half,k){ const f=half?1:2.15;
  if(it.startsWith('§')){ const m=EQM[it]; if(m){ const L=Math.max(1,Math.ceil(m[0]/(half?34:72))); return L*(m[1]?46:28)+7; } return 34; }
  if(it.startsWith('›')) return Math.max(1,Math.ceil(plain(it).length/(52*f)))*22+3;
  return Math.max(1,Math.ceil(plain(it).length/([45,37,40][k%3]*f)))*24.5+6; }
function fitSplit(sub,items,half){ let h=Math.ceil(sub.length/(half?36:75))*27+8, k=0; const BUD=398;
  for(let i=0;i<items.length;i++){ h+=hgt(items[i],half,k); if(!/^[§›]/.test(items[i])) k++;
    if(h>BUD){ let j=i;                                             // never split a symbol line or an equation continuation from its equation
      while(j>1&&(items[j].startsWith('›')||/^§\s{3,}/.test(items[j])||/^§\s*[+−-]\s/.test(items[j]))) j--;
      if(j>1&&items[j].startsWith('§')&&/:\s*$/.test(items[j-1])) j--; return Math.max(j,1); } }
  return items.length; }
const T=(t,sub,b)=>{ const k=fitSplit(sub,b,false); const s=newSlide(t); body(s,sub,b.slice(0,k),FULL);
  if(k<b.length) T(t.replace(/ \(cont\.\)$/,'')+' (cont.)',sub.replace(/ \(continued\)$/,'')+' (continued)',b.slice(k)); return s; };
const S=(t,sub,b,im,cap)=>{ const k=fitSplit(sub,b,true); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); img(s,im,cap);
  if(k<b.length) T(t+' (cont.)',sub+' (continued)',b.slice(k)); return s; };
const TB=(t,sub,b,rows,colW,cap,fs)=>{ const k=fitSplit(sub,b,true); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); table(s,rows,colW,fs);
  if(cap) caption(s,cap,6.6); if(k<b.length) T(t+' (cont.)',sub+' (continued)',b.slice(k)); return s; };
// ---- usage ----
// SEC('Introduction and Elementary Theory','Ohm’s law · Laplace’s equation · point sources');
// T('■ Single current electrode at the surface','The half-space: current flows into a hemisphere',[
//   'All current flows through a **hemisphere**, so A = −Iρ/2π and:',
//   '§ V = (Iρ/2π)(1/r)  "or"  ρ = 2πrV/I   (12)',
//   '› z | depth (z = 0 at surface);  2πr² | area of a hemisphere',
//   'The equipotentials are **hemispherical** surfaces below ground.']);
pres.writeFile({fileName:'Deck.pptx'}).then(()=>fs.writeFileSync('eqlist.json',JSON.stringify(EQL)));
```

Table cells are plain text (no markup): write "ρa", not `ρ_{a}`.

## 7a. Post-processing (python-pptx): real bullets per paragraph type — `post.py`

pptxgenjs splits runs with stray `<a:pPr>` elements. After `writeFile`, for every shape keep one `<a:pPr>` per paragraph as its first child. In the `Body` shape classify each paragraph (first run's font: `Cambria Math` = equation; `Cambria` 18 pt = symbol line; index 0 = subtitle / divider contents line; otherwise normal), remove existing bullet/spacing children, then add in schema order (lnSpc, spcBef, spcAft, buClr, buFont, buChar/buNone):

- **Subtitle / divider line:** `marL=0`, `indent=0`, `spcAft` 8 pt, `<a:buNone/>`.
- **Equation:** `marL=457200`, `indent=0`, `spcBef` 2 pt, `spcAft` 4 pt, `<a:buNone/>`.
- **Symbol line:** `marL=914400`, `indent=-228600`, `spcAft` 3 pt, `<a:buClr><a:srgbClr val="0E7490"/></a:buClr>`, `<a:buFont typeface="Arial"/>`, `<a:buChar char="▸"/>`.
- **Normal bullet:** `marL=285750`, `indent=-285750`, `spcAft` 6 pt, `<a:buFont typeface="Arial"/>`, `<a:buChar char="•"/>`.
- If the package contains `.jpg` media, make sure `[Content_Types].xml` has `<Default Extension="jpg" ContentType="image/jpeg"/>`, otherwise validate.py fails.

```python
import sys, zipfile, shutil
from pptx import Presentation
from pptx.oxml.ns import qn
from lxml import etree
FN=sys.argv[1]; p=Presentation(FN)
def kind(para,k):
    if k==0: return 'sub'
    r=para.runs[0]
    if r.font.name=='Cambria Math': return 'eq'
    if r.font.name=='Cambria' and r.font.size and r.font.size.pt==18: return 'sym'
    return 'bul'
for sl in p.slides:
    for sh in sl.shapes:
        if not sh.has_text_frame: continue
        for para in sh.text_frame.paragraphs:
            pps=para._p.findall(qn('a:pPr'))
            for e in pps[1:]: para._p.remove(e)
            if pps and para._p.index(pps[0])!=0: para._p.remove(pps[0]); para._p.insert(0,pps[0])
        if sh.name!='Body': continue
        for k,para in enumerate(sh.text_frame.paragraphs):
            t=kind(para,k); pPr=para._p.get_or_add_pPr()
            for tag in ('a:buNone','a:buChar','a:buFont','a:buAutoNum','a:spcAft','a:spcBef','a:buClr','a:buSzPct'):
                for e in pPr.findall(qn(tag)): pPr.remove(e)
            def spc(tag,v):
                e=etree.SubElement(pPr,qn(tag)); etree.SubElement(e,qn('a:spcPts')).set('val',str(v))
            if t=='sub':
                pPr.set('marL','0'); pPr.set('indent','0'); spc('a:spcAft',800); etree.SubElement(pPr,qn('a:buNone'))
            elif t=='eq':
                pPr.set('marL','457200'); pPr.set('indent','0'); spc('a:spcBef',200); spc('a:spcAft',400); etree.SubElement(pPr,qn('a:buNone'))
            elif t=='sym':
                pPr.set('marL','914400'); pPr.set('indent','-228600'); spc('a:spcAft',300)
                c=etree.SubElement(pPr,qn('a:buClr')); etree.SubElement(c,qn('a:srgbClr')).set('val','0E7490')
                etree.SubElement(pPr,qn('a:buFont')).set('typeface','Arial'); etree.SubElement(pPr,qn('a:buChar')).set('char','▸')
            else:
                pPr.set('marL','285750'); pPr.set('indent','-285750'); spc('a:spcAft',600)
                etree.SubElement(pPr,qn('a:buFont')).set('typeface','Arial'); etree.SubElement(pPr,qn('a:buChar')).set('char','•')
            ln=pPr.find(qn('a:lnSpc'))
            if ln is not None: pPr.remove(ln); pPr.insert(0,ln)
p.save(FN)
zin=zipfile.ZipFile(FN); zout=zipfile.ZipFile('tmp.pptx','w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d=zin.read(it.filename)
    if it.filename=='[Content_Types].xml':
        t=d.decode()
        if 'Extension="jpg"' not in t: t=t.replace('<Default ','<Default Extension="jpg" ContentType="image/jpeg"/><Default ',1)
        d=t.encode()
    zout.writestr(it,d)
zout.close(); shutil.move('tmp.pptx',FN)
```

## 7b. Native equations: `omml.py`, `eqmeta.py`, `inject.py`

`omml.py` turns a linear `§` line into OMML (Office Math) following UnicodeMath build-up rules: `/` stacks the adjacent operands, a bracket group that is a whole numerator/denominator loses its brackets, `∑`/`∫` take `_{}`/`^{}` limits and the following term as body, a bracket group grows to fit (`m:d`), letters are math-italic, numbers/operators/quoted words upright. `inject.py` puts each equation into its paragraph as `mc:AlternateContent` (Choice = `a14:m` with `m:oMathPara`, left-justified, equation number inside the math at the end; Fallback = the one-line text for viewers without equation support).

`omml.py`:

```python
"""Convert the deck's linear equation strings (Unicode + _{}/^{} markup) into OMML.
Linear rules follow UnicodeMath build-up: '/' takes the adjacent operands; a bracket group
that is a whole operand loses its brackets; ∑/∫ take limits from _{} ^{} and the next term as body."""
import re
from xml.sax.saxutils import escape

M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

SUPD = {'²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁻': '−', '¹': '1', '⁰': '0', 'ᵐ': 'm'}
SUBD = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4'}
OPS = set('+−=≈→⇒×·,;±<>≫≪≡:~')
FUNCS = ['tan', 'cos', 'sin', 'ln', 'exp']
OPEN = {'(': ')', '[': ']', '{': '}'}


def pre(s):
    """unicode super/subscripts -> markup (outside quotes)."""
    out = []; q = False; i = 0
    while i < len(s):
        c = s[i]
        if c == '"':
            q = not q; out.append(c); i += 1; continue
        if not q and c in SUPD:
            j = i; buf = ''
            while j < len(s) and s[j] in SUPD:
                buf += SUPD[s[j]]; j += 1
            out.append('^{' + buf + '}'); i = j; continue
        if not q and c in SUBD:
            out.append('_{' + SUBD[c] + '}'); i += 1; continue
        out.append(c); i += 1
    return ''.join(out)


def tokenize(s):
    t = []; i = 0
    while i < len(s):
        c = s[i]
        if c == '"':
            j = s.index('"', i + 1); t.append(('text', s[i + 1:j])); i = j + 1; continue
        if c in '_^' and i + 1 < len(s) and s[i + 1] == '{':
            d = 0; j = i + 1
            while True:
                if s[j] == '{': d += 1
                elif s[j] == '}':
                    d -= 1
                    if d == 0: break
                j += 1
            t.append(('sub' if c == '_' else 'sup', s[i + 2:j])); i = j + 1; continue
        if c == ' ':
            j = i
            while j < len(s) and s[j] == ' ': j += 1
            t.append(('sp', j - i)); i = j; continue
        if c in OPEN: t.append(('open', c)); i += 1; continue
        if c in ')]}': t.append(('close', c)); i += 1; continue
        if c == '/': t.append(('slash', c)); i += 1; continue
        if c in '∑∫': t.append(('nary', c)); i += 1; continue
        if c in OPS: t.append(('op', c)); i += 1; continue
        if c.isdigit():
            j = i
            while j < len(s) and (s[j].isdigit() or (s[j] == '.' and j + 1 < len(s) and s[j + 1].isdigit())): j += 1
            t.append(('num', s[i:j])); i = j; continue
        f = next((f for f in FUNCS if s.startswith(f, i) and not (i > 0 and s[i - 1].isalpha())), None)
        if f and (i + len(f) >= len(s) or not s[i + len(f)].isalpha() or s[i + len(f)] in 'θ'):
            t.append(('func', f)); i += len(f); continue
        if c in '′″*' and t and t[-1][0] in ('id',):
            t[-1] = ('id', t[-1][1] + c); i += 1; continue
        if s.startswith('···', i): t.append(('id', '⋯')); i += 3; continue
        t.append(('id', c)); i += 1
    return t


# ---------- tree ----------
class Atom:
    def __init__(self, kind, val):
        self.kind, self.val, self.sub, self.sup = kind, val, None, None


def parse(tokens, pos=0, close=None, noscript_frac=False):
    items = []
    while pos < len(tokens):
        k, v = tokens[pos]
        if k == 'close':
            if close is None:
                items.append(Atom('cl', v)); pos += 1; continue
            return items, pos + 1
        if k == 'open':
            p0 = pos
            inner, pos = parse(tokens, pos + 1, OPEN[v], noscript_frac)
            a = Atom('group', inner); a.br = v
            a.open_only = not (pos - 1 < len(tokens) and tokens[pos - 1][0] == 'close' and pos - 1 > p0 and _closes(tokens, p0, pos - 1))
            items.append(a); continue
        if k in ('sub', 'sup') and items and isinstance(items[-1], Atom):
            sc, _ = parse(tokenize(v), 0, None, True)
            if k == 'sub': items[-1].sub = sc
            else: items[-1].sup = sc
            pos += 1; continue
        if k in ('id', 'num', 'func', 'text', 'nary'):
            items.append(Atom(k, v)); pos += 1; continue
        items.append((k, v)); pos += 1
    return items, pos


def _closes(tokens, a, b):
    d = 0
    for k, v in tokens[a:b + 1]:
        if k == 'open': d += 1
        elif k == 'close': d -= 1
    return d == 0


def is_atom(x):
    return isinstance(x, Atom)


def build(items, frac=True):
    """fractions and n-ary bodies on a flat item list (recursively)."""
    for x in items:
        if is_atom(x):
            if x.kind == 'group': x.val = build(x.val, frac)
            for sc in ('sub', 'sup'):
                if getattr(x, sc) is not None: setattr(x, sc, build(getattr(x, sc), False))
    if frac:
        while any(not is_atom(x) and x[0] == 'slash' for x in items):
            i = next(i for i, x in enumerate(items) if not is_atom(x) and x[0] == 'slash')
            a = i
            while a - 1 >= 0 and is_atom(items[a - 1]) and items[a - 1].kind not in ('nary', 'cl'): a -= 1
            b = i + 1
            while b < len(items) and is_atom(items[b]) and items[b].kind not in ('nary', 'cl'): b += 1
            num, den = items[a:i], items[i + 1:b]
            f = Atom('frac', (strip(num), strip(den)))
            items = items[:a] + [f] + items[b:]
    else:
        items = [('op', '/') if (not is_atom(x) and x[0] == 'slash') else x for x in items]
    out = nary_pass(items)
    # a group that holds a single fraction (no scripts) drops its brackets
    res = []
    for x in out:
        if is_atom(x) and x.kind == 'group' and x.sub is None and x.sup is None and len(x.val) == 1 and is_atom(x.val[0]) and x.val[0].kind == 'frac':
            res.append(x.val[0])
        else:
            res.append(x)
    return res


def nary_pass(items):
    out = []; i = 0
    while i < len(items):
        x = items[i]
        if is_atom(x) and x.kind == 'nary' and not hasattr(x, 'body'):
            j = i + 1
            while j < len(items) and not is_atom(items[j]) and items[j][0] == 'sp': j += 1
            k = j
            while k < len(items) and not (not is_atom(items[k]) and items[k][0] == 'op' and items[k][1] in '+−=≈,;→'):
                k += 1
            body = items[j:k]
            while body and not is_atom(body[-1]) and body[-1][0] == 'sp': body.pop()
            x.body = nary_pass(body)
            out.append(x); i = k; continue
        out.append(x); i += 1
    return out


def strip(ops):
    if len(ops) == 1 and is_atom(ops[0]) and ops[0].kind == 'group' and ops[0].sub is None and ops[0].sup is None:
        return ops[0].val
    return ops


# ---------- OMML ----------
class Style:
    def __init__(self, target, sz=2200, color='0B2A55'):
        self.target, self.sz, self.color = target, sz, color

    def rpr(self, italic=True):
        if self.target == 'pptx':
            return (f'<a:rPr lang="en-US" sz="{self.sz}" b="0" i="{1 if italic else 0}"><a:solidFill><a:srgbClr val="{self.color}"/></a:solidFill>'
                    f'<a:latin typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/>'
                    f'<a:cs typeface="Cambria Math" panose="02040503050406030204" pitchFamily="18" charset="0"/></a:rPr>')
        return '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'

    def ctrl(self):
        return f'<m:ctrlPr>{self.rpr()}</m:ctrlPr>'


def run(txt, st, plain=False):
    mr = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ''
    return f'<m:r>{mr}{st.rpr(not plain)}<m:t xml:space="preserve">{escape(txt)}</m:t></m:r>'


def emit(items, st):
    out = []
    prev_atom = False
    for x in items:
        if not is_atom(x):
            k, v = x
            if k == 'sp':
                if v >= 2: out.append(run(' ' * (1 if v < 6 else 2), st, True))
                elif prev_atom: out.append(run(' ', st, True))
                continue
            if k == 'op':
                out.append(run(v, st, True)); prev_atom = False; continue
            out.append(run(v, st, True)); prev_atom = False; continue
        out.append(atom(x, st)); prev_atom = True
    return ''.join(out)


def base(x, st):
    if x.kind == 'id':
        return run(x.val, st)
    if x.kind == 'num':
        return run(x.val, st, True)
    if x.kind in ('func', 'cl'):
        return run(x.val, st, True)
    if x.kind == 'text':
        return run(x.val, st, True)
    if x.kind == 'group':
        b = x.br; e = '' if getattr(x, 'open_only', False) else OPEN[b]
        return (f'<m:d><m:dPr><m:begChr m:val="{escape(b)}"/><m:endChr m:val="{escape(e)}"/>{st.ctrl()}</m:dPr>'
                f'<m:e>{emit(x.val, st)}</m:e></m:d>')
    if x.kind == 'frac':
        n, d = x.val
        return f'<m:f><m:fPr>{st.ctrl()}</m:fPr><m:num>{emit(n, st)}</m:num><m:den>{emit(d, st)}</m:den></m:f>'
    if x.kind == 'nary':
        lim = 'undOvr' if x.val == '∑' else 'subSup'
        hide = ('<m:subHide m:val="1"/>' if x.sub is None else '') + ('<m:supHide m:val="1"/>' if x.sup is None else '')
        sub = emit(x.sub, st) if x.sub else ''
        sup = emit(x.sup, st) if x.sup else ''
        body = emit(getattr(x, 'body', []) or [], st)
        return (f'<m:nary><m:naryPr><m:chr m:val="{x.val}"/><m:limLoc m:val="{lim}"/>{hide}{st.ctrl()}</m:naryPr>'
                f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>')
    raise ValueError(x.kind)


def atom(x, st):
    if x.kind == 'nary':
        return base(x, st)
    b = base(x, st)
    if x.sub is not None and x.sup is not None:
        return f'<m:sSubSup><m:sSubSupPr>{st.ctrl()}</m:sSubSupPr><m:e>{b}</m:e><m:sub>{emit(x.sub, st)}</m:sub><m:sup>{emit(x.sup, st)}</m:sup></m:sSubSup>'
    if x.sub is not None:
        return f'<m:sSub><m:sSubPr>{st.ctrl()}</m:sSubPr><m:e>{b}</m:e><m:sub>{emit(x.sub, st)}</m:sub></m:sSub>'
    if x.sup is not None:
        return f'<m:sSup><m:sSupPr>{st.ctrl()}</m:sSupPr><m:e>{b}</m:e><m:sup>{emit(x.sup, st)}</m:sup></m:sSup>'
    return b


LABEL = re.compile(r'^(Medium \(\d\):|\((?:i|ii|iii|iv|v)\))\s+')
EQNO = re.compile(r'\s+\((\d+[a-e]?(?:,\s*[a-e])?)\)\s*$')


def split_line(raw):
    """raw '§ ...' item -> (label, math, eqno)"""
    s = raw[1:].strip()
    label = None; eqno = None
    m = EQNO.search(s)
    if m: eqno = m.group(1); s = s[:m.start()]
    m = LABEL.match(s)
    if m: label = m.group(1); s = s[m.end():]
    return label, s.rstrip(), eqno


def to_omml(math, st, label=None, eqno=None, para=False):
    toks = tokenize(pre(math))
    items, _ = parse(toks)
    items = build(items)
    lead = ''
    if math.startswith('    '):
        lead = run('  ', st, True)
    lab = run(label + ' ', st, True) if label else ''
    num = run('  (' + eqno + ')', st, True) if eqno else ''
    body = f'<m:oMath>{lab}{lead}{emit(items, st)}{num}</m:oMath>'
    if para:
        return (f'<m:oMathPara xmlns:m="{M}"><m:oMathParaPr><m:jc m:val="left"/></m:oMathParaPr>' + body + '</m:oMathPara>')
    return body.replace('<m:oMath>', f'<m:oMath xmlns:m="{M}">', 1)


def width(math):
    """rough displayed width in characters after build-up (fractions stack)."""
    items = build(parse(tokenize(pre(math)))[0])
    def w(xs):
        t = 0
        for x in xs:
            if not is_atom(x):
                t += (1.6 if x[0] == 'op' else (1.5 if x[0] == 'sp' and x[1] >= 2 else 0.3 if x[0] == 'sp' else 1)); continue
            t += wa(x)
        return t
    def wa(x):
        if x.kind in ('id', 'num', 'func', 'text', 'cl'): b = len(x.val)
        elif x.kind == 'group': b = w(x.val) + 2
        elif x.kind == 'frac': b = max(w(x.val[0]), w(x.val[1])) + 0.6
        elif x.kind == 'nary': b = 1.6 + w(getattr(x, 'body', []) or [])
        s = max(w(x.sub) if x.sub else 0, w(x.sup) if x.sup else 0) * 0.65
        return b + s
    def tall(xs):
        for x in xs:
            if is_atom(x):
                if x.kind == 'frac': return True
                if x.kind == 'nary' and (x.sub or x.sup): return True
                if x.kind == 'group' and tall(x.val): return True
                if x.kind == 'nary' and tall(getattr(x, 'body', []) or []): return True
        return False
    return w(items), tall(items)
```

`eqmeta.py` (run before `node deck.js`; list the generator's file names):

```python
import re, json, omml
src=''.join(open(f).read() for f in ['deck.js'])
meta={}
for raw in re.findall(r"'(§[^']*)'",src):
    label,math,eqno=omml.split_line(raw)
    w,tall=omml.width(math)
    meta[raw]=[round(w+(len(label)+2 if label else 0)+(len(eqno)+4 if eqno else 0),1), tall]
json.dump(meta,open('eqmeta.json','w'),ensure_ascii=False)
```

`inject.py` (run after `post.py`):

```python
import json, sys
from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn
import omml
FN=sys.argv[1]; EQL=json.load(open('eqlist.json')); p=Presentation(FN)
A='http://schemas.openxmlformats.org/drawingml/2006/main'
MC='http://schemas.openxmlformats.org/markup-compatibility/2006'
A14='http://schemas.microsoft.com/office/drawing/2010/main'
st=omml.Style('pptx', sz=2000, color='0B2A55'); done=0
for i,sl in enumerate(p.slides,1):
    info=EQL.get(str(i))
    if not info: continue
    body=[sh for sh in sl.shapes if sh.name=='Body'][0]
    paras=[pa for k,pa in enumerate(body.text_frame.paragraphs) if k>0 and pa.runs and pa.runs[0].font.name=='Cambria Math']
    assert len(paras)==len(info['eqs']),(i,len(paras),len(info['eqs']))
    for pa,raw in zip(paras,info['eqs']):
        label,math,eqno=omml.split_line(raw); p_=pa._p
        runs=[r for r in p_ if r.tag in (qn('a:r'),qn('a:br'))]
        fbtxt=''.join(''.join(r.itertext()) for r in runs if r.tag==qn('a:r')).strip()
        for r in runs: p_.remove(r)
        if eqno and fbtxt.endswith(f'({eqno})'): fbtxt=fbtxt[:-len(f'({eqno})')].rstrip()
        if label and fbtxt.startswith(label): fbtxt=fbtxt[len(label):].lstrip()
        fbline=((label+'  ') if label else '')+' '.join(fbtxt.split())+(('   ('+eqno+')') if eqno else '')
        xml=(f'<mc:AlternateContent xmlns:mc="{MC}" xmlns:a="{A}"><mc:Choice xmlns:a14="{A14}" Requires="a14"><a14:m>'
             + omml.to_omml(math,st,label,eqno,True).replace('<m:oMathPara xmlns:m=',f'<m:oMathPara xmlns:a="{A}" xmlns:m=')
             + f'</a14:m></mc:Choice><mc:Fallback><a:r><a:rPr lang="en-US" sz="1800"><a:solidFill><a:srgbClr val="0B2A55"/></a:solidFill>'
             f'<a:latin typeface="Cambria Math"/></a:rPr><a:t>{omml.escape(fbline)}</a:t></a:r></mc:Fallback></mc:AlternateContent>')
        endp=p_.find(qn('a:endParaRPr')); el=etree.fromstring(xml)
        (endp.addprevious(el) if endp is not None else p_.append(el)); done+=1
p.save(FN); print('equations',done)
```

## 8. Content rules

- Stay faithful to the source. Keep its numbers, names, equations, tables and figure numbers, and credit figures in captions. Only equation numbers are renumbered (chapter prefix dropped, §4).
- Mark anything not from the source (synthetic diagrams, illustrative values, worked examples) as such in the subtitle or caption.
- If a requested image cannot be obtained (blocked site, no figure in the source), say so plainly and use the best available alternative rather than silently skipping it.
- **Every working file stays in `temp/<NN>_<name>/`** (§0) — notes, section drafts, figures, page renders, generator scripts. The working directory gets the finished `.pptx` and nothing else.
- US English only unless the user asks otherwise.