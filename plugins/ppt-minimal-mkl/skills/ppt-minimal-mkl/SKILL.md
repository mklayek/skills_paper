---
name: "ppt-minimal-mkl"
description: "Build a minimal, white, classroom-ready .pptx teaching deck from any source (PDF, Markdown, HTML, text, Word, web pages or a topic to research), in Jongchan's house style."
---

# ppt-minimal-mkl: minimal scientific teaching decks

Use this skill when the user asks for a PowerPoint / pptx / slides / lecture deck made from a source: an attached PDF (including scanned book chapters), .md, .html, .txt, .docx, a URL, or "search the internet about X". The output is always a real `.pptx` file sent with SendUserFile.

Also read the built-in `pptx` skill's SKILL.md once for the pptxgenjs gotchas (hex colors without #, `isTextBox: true`, validate script, soffice wrapper). This skill adds the house style and workflow on top.

## 1. House style (defaults: the user's words always override)

- **Language: always US English.** US spelling (color, center, meter, aluminum, analyze, modeling, labeled, gray, artifact, fiber, program), US punctuation and US number style (1,000.5). Keep proper names, book titles and quoted source text as printed; convert everything else, including captions, table text and subtitles.
- **Canvas:** `LAYOUT_WIDE` (13.333 × 7.5 in), **white background** on every content slide, no dark slides, no decorative bars, stripes or gradients. Only **section divider slides** (§2) carry a pattern.
- **Exactly two text boxes per content slide:**
  1. **Title box**: Arial bold 28 pt, deep navy `0B2A55`, at x 0.6, y 0.35, w 12.1, h 0.8. objectName `Title`. Plain text only (no sub/superscript markup).
  2. **Body box**: holds the subtitle line, bullets, equations and symbol lines. objectName `Body`.
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
- **Captions:** Arial 12 pt italic, gray `374151`, under the image, naming the source (e.g. "Telford et al., Applied Geophysics — Fig. 6.3: …").
- **Slide number:** Arial 11 pt, bottom right, on every slide including dividers.
- **No slide-count limit.** Split content rather than shrinking text.

## 2. Section divider rule (always)

- Put a **section divider slide at the beginning of every main section** of the source (e.g. 9.1, 9.2 …; or the deck's own logical sections if the source has none). Not before the title slide or the final summary.
- **Design: pattern-filled.** Full-bleed background image with a light, tinted geometric pattern, and a solid white panel (x 0.6–9.0 in, y 1.55–5.95 in) with a 3 pt border in the section color. Each section uses a **different pattern and color**, cycling: hexagons/red `B91C1C`, diagonal stripes/blue `1D4ED8`, graded dots/green `15803D`, waves/purple `6D28D9`, triangles/teal `0E7490`, concentric arcs/orange `C2410C`, grid-with-blocks/navy `0B2A55`.
- **Text on the panel:**
  - "Section 9.3" (section number) — Arial bold 40 pt in the section color.
  - **Section name in large letters** — Georgia bold, deep navy, 54 pt (44 pt if > 22 characters, 38 pt if > 34), in the `Title` box.
  - One line listing what the section covers ("Chargeability · frequency effect · …") — Verdana bold 18 pt in the section color, in the `Body` box.
- The divider counts as a slide for the subtitle-style cycle, so consecutive slides still differ.

Pattern backgrounds (run once; writes img/sec0.png … img/sec6.png at 13.333×7.5 in):

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
    f.savefig(f'img/sec{i}.png',dpi=120,facecolor='white'); plt.close(f)
```

## 3. Detail rule (default: detailed)

- Write **full, informative bullets** taken closely from the source: definitions, mechanisms, numbers, ranges, units, names/dates of authors, and the reason behind each point. Avoid one-word or headline-only bullets.
- Aim for **5 bullets beside an image** and **6–7 bullets on a full-width slide**; a slide with fewer than 5 bullets should be expanded or merged.
- Cover **every section and subsection** of the source in order, with its section number in the slide title where useful (e.g. "9.3.2 Time domain …").
- Add teaching slides that help understanding when the source supports them: **comparison tables** (e.g. method A vs B, array choice), **worked numerical examples** that apply the source's equations (mark the numbers "illustrative"), and the source's **practice problems** or case histories.
- When the user asks for "more detail", add slides rather than cramming.

## 4. Equation rule (always apply when the source has equations)

- **Include every equation** from the source, with its **equation number** (e.g. `(9.1)`) at the end of the line.
- An equation gets its **own line**, not a bullet: Cambria Math, 22 pt, bold, deep navy `0B2A55`, indented, no bullet, a little space above and below.
- **Directly after each equation (the next line or two), explain every symbol** in a **different bullet style** from normal bullets:
  - bullet character **▸**, teal `0E7490`, indented deeper than normal bullets (marL 914400, indent −228600);
  - symbol in **bold teal Cambria 18 pt**, then " — " and its meaning in Cambria 18 pt near-black, with units where known (e.g. "**M** — chargeability (ms)");
  - several short symbols may share one line, separated by ";".
- Use real sub/superscripts (markup `_{dc}`, `^{5}` → pptx `subscript`/`superscript`) in equations and symbol lines.
- Put the equation slide full-width if the equation plus symbol lines would not fit beside an image; long derivations may span two lines.
- If the source's printed symbol is ambiguous or a misprint, keep the source form and note it in the symbol line.

## 5. Workflow

1. **Say in one sentence** what you are building, then start. Ask first only if the source is ambiguous and the deck is large.
2. **Get the source content into files:**
   - **PDF:** `pdftotext -layout` and plain `pdftotext`; if it is a scan or equations come out garbled, read pages visually with the Read tool (`pages:` ranges) and take the equations from the page images. Render pages with `pdftoppm -r 200 -png` for figure cropping.
   - **DOCX:** `markitdown file.docx` or pandoc. **MD/TXT/HTML:** read directly (strip tags for HTML).
   - **Web:** WebSearch + WebFetch; keep the URLs for a Sources slide. The shell usually cannot download web images, so tell the user and use figures from attached files or clean diagrams instead.
3. **Plan the outline:** title → for each main section: divider slide, then its content slides (concepts → definitions/equations → methods/equipment → procedure → interpretation/examples → practice) → pros and limits → summary. Pick which slides deserve an image; the rest are text-only.
4. **Images, in order of preference:**
   1. Figures from the user's own files: overlay a 5 % grid on rendered pages to pick crop fractions, crop with PIL, trim whitespace, remove running headers and book captions (the slide caption replaces them), and check the crops on a contact sheet before building.
   2. Photos the user attached.
   3. Clean matplotlib diagrams (white background, deep colors, labels ≥ 10 pt, figsize 5.9×5.2 in so they fit the right half exactly).

   Never repeat an image on two slides.
5. **Build** with pptxgenjs (template below), then **post-process** paragraphs with python-pptx (below).
6. **QA (required):**
   - `python /mnt/skills/public/pptx/scripts/office/validate.py deck.pptx`
   - Programmatic check: every slide has one `Title` and one `Body`; normal bullets follow the 3-font cycle at 20 pt; the subtitle style differs from the previous slide; no raw markup (`_{`, `^{`, `**`) left in any text; a divider exists before each main section.
   - **US English check:** extract all text (text frames and table cells) with python-pptx and scan with a regex for British forms, e.g. `\b\w+(isation|ised|ising|yse|ysed|our|tre|tres|lled|lling)\b|metre|centre|colour|behaviour|aluminium|artefact|grey|towards|whilst|amongst|programme|fibre|litre`. Whitelist real words (noise, source, four, hour, contour, precise, rise, expertise, promise, filled, controlled, called, drilling …) and fix every remaining hit in the generator.
   - Render: `python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf deck.pptx`, then `pdftoppm -jpeg -r 60`, paste into 3×4 contact sheets and look at every slide. Fix overflow (text past the bottom or out of the divider panel), overlaps and clipped crops. Re-render only changed slides.
7. **Deliver** with SendUserFile and a short summary: slide count, structure, where images came from, anything assumed or unavailable. No step-by-step recap.

## 6. pptxgenjs template (core helpers)

Items in a body list: plain string = normal bullet; `'§ equation (n.n)'` = equation line; `'› symbol | meaning'` = symbol line (only the first `|` splits; further `|` become " — "). Markup: `**bold**`, `_{sub}`, `^{sup}`.

```js
const pptxgen = require('pptxgenjs'); const fs = require('fs');
const SZ = JSON.parse(fs.readFileSync('sizes.json')); // {name:[w,h]} written by python for img/*.png
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE';
const NAVY='0B2A55', INK='111827', MUTED='374151', TEAL='0E7490', EQC='0B2A55';
const LEADS=['B91C1C','1D4ED8','15803D','6D28D9'];
const FONTS=['Times New Roman','Comic Sans MS','Bookman Old Style'];
const SUBS=[{font:'Georgia',color:'B91C1C',u:'sng'},{font:'Verdana',color:'1D4ED8',u:'dbl'},{font:'Cambria',color:'15803D',u:'heavy'},
  {font:'Trebuchet MS',color:'6D28D9',u:'dash'},{font:'Georgia',color:'0E7490',u:'wavy',italic:true},{font:'Tahoma',color:'C2410C',u:'dotted'}];
const HALF={x:0.6,y:1.3,w:5.9,h:5.7}, FULL={x:0.6,y:1.3,w:12.1,h:5.7}, R={x:6.85,y:1.35,w:5.9,h:5.2};
let n=0;
function newSlide(title){ const s=pres.addSlide(); s.background={color:'FFFFFF'}; n++;
  s.addText(title,{x:0.6,y:0.35,w:12.1,h:0.8,fontFace:'Arial',fontSize:28,bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  s.addText(String(n),{x:12.2,y:7.0,w:0.6,h:0.3,fontFace:'Arial',fontSize:11,color:MUTED,align:'right',margin:0,isTextBox:true});
  return s; }
// section divider (pattern backgrounds from §2)
const SECC=['B91C1C','1D4ED8','15803D','6D28D9','0E7490','C2410C','0B2A55']; let secN=0;
function SEC(num, name, contents){ const s=pres.addSlide(); n++; const c=SECC[secN%7];
  s.background={path:`img/sec${secN%7}.png`}; secN++;
  s.addText(num,{x:1.0,y:1.85,w:7.6,h:0.9,fontFace:'Arial',fontSize:40,bold:true,color:c,margin:0,isTextBox:true});
  s.addText(name,{x:1.0,y:2.7,w:7.6,h:1.9,fontFace:'Georgia',fontSize:name.length>34?38:(name.length>22?44:54),bold:true,color:NAVY,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  s.addText([{text:contents,options:{fontFace:'Verdana',fontSize:18,bold:true,color:c}}],{x:1.0,y:4.75,w:7.6,h:1.0,valign:'top',margin:0,isTextBox:true,objectName:'Body'});
  s.addText(String(n),{x:12.2,y:7.0,w:0.6,h:0.3,fontFace:'Arial',fontSize:11,color:MUTED,align:'right',margin:0,isTextBox:true});
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
    if(it.startsWith('§')) r=parse(it.slice(1).trim(),{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true},EQC);
    else if(it.startsWith('›')){ const raw=it.slice(1), p=raw.indexOf('|');
      const sym=raw.slice(0,p).trim(), mean=raw.slice(p+1).trim().replace(/\s*\|\s*/g,' — ');
      r=[...parse(sym,{fontFace:'Cambria',fontSize:18,color:TEAL,bold:true},TEAL), ...parse(' — '+mean,{fontFace:'Cambria',fontSize:18,color:INK},TEAL)]; }
    else { r=parse(it,{fontFace:FONTS[k%3],fontSize:20,color:INK},LEADS[k%4]); k++; }
    if(i<items.length-1) r[r.length-1].options.breakLine=true; arr.push(...r); });
  s.addText(arr,{...box,valign:'top',margin:[4,4,4,4],isTextBox:true,objectName:'Body',fit:'none'}); }
function caption(s,cap,y){ s.addText(cap,{x:R.x,y:y??R.y+R.h+0.08,w:R.w,h:0.45,fontFace:'Arial',fontSize:12,italic:true,color:MUTED,margin:0,valign:'top',isTextBox:true}); }
function img(s,name,cap){ const [pw,ph]=SZ[name]; const sc=Math.min(R.w/pw,R.h/ph); const w=pw*sc,h=ph*sc;
  s.addImage({path:`img/${name}.png`,x:R.x+(R.w-w)/2,y:R.y+(R.h-h)/2,w,h,altText:cap||name});
  if(cap) caption(s,cap); }
function table(s,rows,colW,fs=13){ // header row navy, first column blue bold, zebra rows
  const data=rows.map((r,i)=>r.map((c,j)=>({text:c,options:{fontFace:i===0?'Arial':'Times New Roman',fontSize:fs,bold:i===0||j===0,
    color:i===0?'FFFFFF':(j===0?'1D4ED8':INK),fill:{color:i===0?NAVY:(i%2?'FFFFFF':'F1F5F9')},valign:'middle',margin:[2,6,2,6]}})));
  s.addTable(data,{x:R.x,y:R.y,w:R.w,colW,border:{type:'solid',color:'CBD5E1',pt:0.75},autoPage:false}); }
const S=(t,sub,b,im,cap)=>{const s=newSlide(t); body(s,sub,b,HALF); img(s,im,cap); return s;};
const T=(t,sub,b)=>{const s=newSlide(t); body(s,sub,b,FULL); return s;};
const TB=(t,sub,b,rows,colW,cap,fs)=>{const s=newSlide(t); body(s,sub,b,HALF); table(s,rows,colW,fs); if(cap) caption(s,cap,6.6); return s;};
// Usage: SEC('Section 9.3','Induced Polarization Measurements','Chargeability · frequency effect · metal factor'); then T(...)/S(...)/TB(...)
// Equation slide example:
// T('Chargeability M (Eq. 9.1)','The most used time-domain quantity',[
//   '§ M = (1 / V_{c}) ∫_{t₁}^{t₂} V(t) dt          (9.1)',
//   '› M | chargeability (ms)', '› V_{c} | steady voltage during current-on', '› V(t) | decay voltage at time t',
//   'Normal bullet explaining use...']);
pres.writeFile({fileName:'Deck.pptx'});
```

Table cells are plain text (no markup): write "ρa", not `ρ_{a}`.

## 7. Post-processing (python-pptx): real bullets per paragraph type

pptxgenjs splits runs with stray `<a:pPr>` elements. After `writeFile`, for every shape keep one `<a:pPr>` per paragraph as its first child. In the `Body` shape classify each paragraph (first run's font: `Cambria Math` = equation; `Cambria` 18 pt = symbol line; index 0 = subtitle / divider contents line; otherwise normal), remove existing bullet/spacing children, then add in schema order (lnSpc, spcBef, spcAft, buClr, buFont, buChar/buNone):

- **Subtitle / divider line:** `marL=0`, `indent=0`, `spcAft` 12 pt, `<a:buNone/>`.
- **Equation:** `marL=457200`, `indent=0`, `spcBef` 4 pt, `spcAft` 6 pt, `<a:buNone/>`.
- **Symbol line:** `marL=914400`, `indent=-228600`, `spcAft` 3 pt, `<a:buClr><a:srgbClr val="0E7490"/></a:buClr>`, `<a:buFont typeface="Arial"/>`, `<a:buChar char="▸"/>`.
- **Normal bullet:** `marL=285750`, `indent=-285750`, `spcAft` 10 pt, `<a:buFont typeface="Arial"/>`, `<a:buChar char="•"/>`.
- If the package contains `.jpg` media, make sure `[Content_Types].xml` has `<Default Extension="jpg" ContentType="image/jpeg"/>`, otherwise validate.py fails.

## 8. Content rules

- Stay faithful to the source. Keep its numbers, names, equations, tables and figure numbers, and credit figures in captions.
- Mark anything not from the source (synthetic diagrams, illustrative values, worked examples) as such in the subtitle or caption.
- If a requested image cannot be obtained (blocked site, no figure in the source), say so plainly and use the best available alternative rather than silently skipping it.
- US English only unless the user asks otherwise.