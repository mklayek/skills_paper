const pptxgen = require('pptxgenjs'); const fs = require('fs');
const IMG = '../../../figs';   // <output>/figs (figures live next to the deck)
const SZ = JSON.parse(fs.readFileSync('sizes.json'));
let EQM = {}; try { EQM = JSON.parse(fs.readFileSync('eqmeta.json')); } catch (e) {}
const EQL = {};
const EQI = {}; for (const e of JSON.parse(fs.readFileSync('eqinv.json'))) EQI[e.id] = e.latex;
try { Object.assign(EQI, JSON.parse(fs.readFileSync('eqfix.json'))); } catch (e) {}
const GK={alpha:'α',beta:'β',gamma:'γ',delta:'δ',epsilon:'ε',varepsilon:'ε',zeta:'ζ',eta:'η',theta:'θ',kappa:'κ',lambda:'λ',mu:'μ',nu:'ν',xi:'ξ',pi:'π',rho:'ρ',sigma:'σ',tau:'τ',phi:'φ',varphi:'φ',chi:'χ',psi:'ψ',omega:'ω',Gamma:'Γ',Delta:'Δ',Theta:'Θ',Lambda:'Λ',Pi:'Π',Sigma:'Σ',Phi:'Φ',Psi:'Ψ',Omega:'Ω',nabla:'∇',partial:'∂',infty:'∞',int:'∫',oint:'∮',sum:'∑',times:'×',cdot:'·',approx:'≈',pm:'±',le:'≤',ge:'≥',ll:'≪',gg:'≫',to:'→',sqrt:'√'};
// readable linear text for a LaTeX source equation (fallback text and size estimates only)
const delatex=l=>l.replace(/\\(?:mathbf|boldsymbol|mathrm|text|operatorname|mathcal|bm)\{([^}]*)\}/g,'$1').replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g,'($1)/($2)')
  .replace(/\\([A-Za-z]+)/g,(m,w)=>GK[w]??(['left','right','quad','qquad','big','Big','limits','displaystyle'].includes(w)?' ':w)).replace(/[{}]/g,'').replace(/\\[,;!: ]/g,' ').replace(/\s+/g,' ').trim();
const eqtext=it=>it.startsWith('§#')?delatex(EQI[+it.slice(2)]||''):it.slice(1).trim().replace(/"/g,'');
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE';
// calibration pass (calibrate.py): same width, very tall page, so overflowing text is still rendered
if (require('fs').existsSync('nosplit.flag')) { pres.defineLayout({name:'TALL', width:13.333, height:30}); pres.layout='TALL'; }
const NAVY='0B2A55', INK='111827', MUTED='374151', TEAL='0E7490', EQC='0B2A55';
const LEADS=['B91C1C','1D4ED8','15803D','6D28D9'];
const FONTS=['Times New Roman','Comic Sans MS','Bookman Old Style'];
const SUBS=[{font:'Georgia',color:'B91C1C',u:'sng'},{font:'Verdana',color:'1D4ED8',u:'dbl'},{font:'Cambria',color:'15803D',u:'heavy'},
  {font:'Trebuchet MS',color:'6D28D9',u:'dash'},{font:'Georgia',color:'0E7490',u:'wavy',italic:true},{font:'Tahoma',color:'C2410C',u:'dotted'}];
// 2026-11-06 body boxes, PowerPoint order Height x Width, centered left-right on the 13.333 x 7.5 in slide.
// Topic-start slide (title box): 6.53 H x 13.07 W, placed under the title and flush with the slide bottom.
// Continued slide (black topic label, no title box): 6.87 H x 13.04 W, centered on the slide.
// With a figure or table the body takes the left half of the box and the figure the right half.
const SW=13.333, SH=7.5, BOX_T={w:13.07,h:6.53}, BOX_L={w:13.04,h:6.87};
function boxFor(label,half){ const b=label?BOX_L:BOX_T, x=(SW-b.w)/2, y=label?(SH-b.h)/2:SH-b.h;
  return {x,y,w:half?b.w/2:b.w,h:b.h}; }
function figBox(label){ const b=boxFor(label,false); return {x:b.x+b.w/2+0.1,y:b.y+0.1,w:b.w/2-0.2,h:b.h-0.8}; }
const BC={'◆':'B91C1C','■':'1D4ED8','●':'15803D'};
// v7 titles. A TOPIC is the title without its level marker, without " (continued)" and without
// a " › sub-topic" part. Every slide of one topic shares one title font and one dark text color.
// The font changes at every new topic, cycling TPOOL. First slide of a topic: centered title.
// Later slides of the same topic: left-aligned. Every third topic gets a light fill, the rest none.
// '★' before the marker = very important title, drawn as a gold oval (always centered).
// 'Topic › Sub' on a continued slide = black label (white text) with the topic at the top left,
// and the sub-topic as the title. On a topic's first slide the sub-topic moves into the subtitle.
// deck rule: title fonts alternate in a random order (seeded, so rebuilds match) among the user's list,
// never the same font on two topics in a row. Freehand521 BT is in the list but not installed here.
const TFONTS=[['Copperplate Gothic Light',0.78,false],['Bookman Old Style',0.56,true],['Book Antiqua',0.53,true],
  ['MV Boli',0.60,false],['Gabriola',0.40,false],['Monotype Corsiva',0.42,false]];
const TPOOL=(()=>{ let a=20261105>>>0; const rnd=()=>{ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1);
  t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; };
  const out=[]; let prev=-1; for(let i=0;i<400;i++){ let k; do{ k=Math.floor(rnd()*TFONTS.length); }while(k===prev); out.push(TFONTS[k]); prev=k; }
  return out; })();
const TDARK=['0B2A55','991B1B','14532D','4C1D95','134E4A','7C2D12','1E3A8A','831843','3F3F46'];
const TLIGHT=['FFF2B3','DBEAFE','DCFCE7','EDE9FE','FCE7F3','E0F2FE','FFEDD5'];
const OVAL_FILL='FFC000';
const SYMFONT='Times New Roman';   // symbol lines: 18 pt black, see body()
// v7: the title bullet (marker) has its own glyph and color per topic, so no two topics in a row share one.
// The ◆ ■ ● written in a title string only switch the marker on; the topic decides how it looks.
const TMARK=[['◆','B91C1C'],['■','1D4ED8'],['●','15803D'],['▶','6D28D9'],['❖','0E7490'],
  ['✦','C2410C'],['▲','0B2A55'],['◉','831843'],['➤','14532D'],['✿','7C2D12']];
const MARKFONT='Segoe UI Symbol';
let topicIdx=-1, lastTopic=null, curSub=null;
function SUMMARY(){}      // kept for v6 section files: the Summary is an ordinary topic in v7
function titleInfo(title){ let t=title, star=false;
  if(t[0]==='★'){ star=true; t=t.slice(1).trimStart(); }
  const mk=BC[t[0]]?t[0]:''; let txt=mk?t.slice(1).trim():t.trim();
  const cont=/ \(continued\)$/.test(txt); txt=txt.replace(/ \(continued\)$/,'');
  const cut=txt.indexOf(' › '); const topic=(cut<0?txt:txt.slice(0,cut)).trim(), sub=cut<0?'':txt.slice(cut+3).trim();
  return {star, mk, topic, sub, cont, first: topic!==lastTopic}; }
const fitSz=(txt,w,cw,lo=18)=>Math.max(lo,Math.min(28,Math.floor(w*72/(Math.max(txt.length,1)*cw))));
let n=0;
function newSlide(title){ const s=pres.addSlide(); s.background={color:'FFFFFF'}; n++;
  const ti=titleInfo(title);
  if(ti.first){ topicIdx++; lastTopic=ti.topic; }
  const [ff,cw,bd]=TPOOL[topicIdx%TPOOL.length], fc=TDARK[topicIdx%TDARK.length];
  const fill=topicIdx%3===2?TLIGHT[Math.floor(topicIdx/3)%TLIGHT.length]:null;
  // 2026-11-06: a slide that continues its topic gets only the black label with the topic name, no title box
  if(!ti.first){ const lw=Math.min(6.5,ti.topic.length*16*cw/72+0.35);
    s.addText(ti.topic,{x:0,y:0,w:lw,h:0.36,fontFace:ff,fontSize:16,color:'FFFFFF',fill:{color:'000000'},
      valign:'middle',align:'left',margin:[0,6,0,6],isTextBox:true,objectName:'TopicLabel'});
    return s; }
  curSub=ti.sub;
  const shown=ti.topic+(ti.cont?' (continued)':''), mk=ti.mk, y=0.12, h=0.8;
  if(ti.star){
    // wide oval, usable text width ~10 in, long titles may drop to 16 pt so they stay on one line
    s.addText(shown,{shape:pres.shapes.OVAL,x:0.9,y,w:11.55,h,fill:{color:OVAL_FILL},line:{color:OVAL_FILL},
      fontFace:ff,fontSize:fitSz(shown,9.6,cw,16),bold:bd,color:fc,align:'center',valign:'middle',margin:0,objectName:'Title'});
  } else {
    const [mg,mc]=TMARK[topicIdx%TMARK.length];
    const tt=mk?[{text:mg+'  ',options:{fontFace:MARKFONT,color:mc,fontSize:20}},{text:shown}]:shown;
    s.addText(tt,{x:0.6,y,w:12.1,h,fontFace:ff,fontSize:fitSz(shown,11.6,cw),bold:bd,color:fc,
      align:ti.first?'center':'left',valign:'middle',margin:fill?[0,8,0,8]:0,isTextBox:true,objectName:'Title',
      ...(fill?{fill:{color:fill}}:{})});
  }
  return s; }
// on a topic's FIRST slide a ' › sub-topic' part is not a label: it becomes (part of) the subtitle
function subOf(title,sub){ const ti=titleInfo(title);
  return ti.first&&ti.sub?(sub?ti.sub+': '+sub:ti.sub):sub; }
const SECC=['B91C1C','1D4ED8','15803D','6D28D9','0E7490','C2410C','0B2A55']; let secN=0;
function SEC(name, contents){ FLUSH(); const s=pres.addSlide(); n++; const c=SECC[secN%7];
  s.background={path:`${IMG}/sec${secN%7}.png`}; const nt=topicIdx+1, [ff,cw,bd]=TPOOL[nt%TPOOL.length], fc=TDARK[nt%TDARK.length]; secN++;   // the next topic's font and color
  lastTopic=null;                                  // the slide after a divider always starts a topic
  // no section number on the divider: the name alone, large, on the white panel
  s.addText(name,{x:1.0,y:1.95,w:7.6,h:2.55,fontFace:ff,fontSize:Math.max(30,Math.min(54,Math.floor(7.4*72*2/(name.length*cw)))),bold:true,color:fc,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  const df=(lastSig && lastSig[0]==='Verdana' && lastSig[1]===c)?'Trebuchet MS':'Verdana';
  lastSig=[df,c];
  s.addText([{text:contents,options:{fontFace:df,fontSize:18,bold:true,color:c}}],{x:1.0,y:4.6,w:7.6,h:1.2,valign:'top',margin:0,isTextBox:true,objectName:'Body'});
  return s; }
let lastSig=null;   // [font,color] of the previous slide's first body paragraph
function parse(txt, base, lead){ const out=[]; let bold=false, i=0, buf='';
  const push=(t,ex={})=>{ if(!t) return; out.push({text:t,options:{...base,bold:bold||!!base.bold,color:bold?lead:base.color,...ex}}); };
  while(i<txt.length){
    if(txt.startsWith('**',i)){ push(buf); buf=''; bold=!bold; i+=2; continue; }
    if((txt[i]==='_'||txt[i]==='^')&&txt[i+1]==='{'){ push(buf); buf=''; const j=txt.indexOf('}',i);
      push(txt.slice(i+2,j), txt[i]==='_'?{subscript:true}:{superscript:true}); i=j+1; continue; }
    buf+=txt[i]; i++; }
  push(buf); return out; }
// v8 body text. One arrow chain = ONE bullet paragraph that wraps naturally under a hanging indent
// (no bullet on the wrapped rows). Each bullet draws a body font from BFONTS (seeded random, so rebuilds match):
// two bullets in a row never share a font. Body text is black (BODY_C), arrows dark gray. Size factors keep the
// fonts visually alike. The color draw from BCOLS is kept only so the font sequence stays the same.
const BFONTS=[['Times New Roman',1.05],['Comic Sans MS',0.95],['Book Antiqua',1],['Gabriola',1.3],['Cambria Math',1],
  ['Alef',1],['Ink Free',1],['MV Boli',0.92],['Georgia',0.95]];
const BCOLS=['000000','0B2A55','7F1D1D','14532D','4C1D95','134E4A','7C2D12','1E3A8A'];
const ARROW_C='4B5563', ARROW_F='Cambria Math';
const brnd=(()=>{ let a=20261106>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1);
  t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; })();
let prevF=-1, prevC=-1;
function nextStyle(){ let f,c; do{ f=Math.floor(brnd()*BFONTS.length); }while(f===prevF);
  do{ c=Math.floor(brnd()*BCOLS.length); }while(c===prevC); prevF=f; prevC=c;
  // deck rule (2026-11-06, third pass): body text is black. The color is still drawn so the font sequence stays the same.
  return {font:BFONTS[f][0], mult:BFONTS[f][1], color:BODY_C}; }
const BODY_C='000000';
const isBul=it=>!/^[§›#]/.test(it);
const bsz=(st,s)=>Math.round(s*st.mult);
const lsp=sz=>Math.round(sz*1.2);                      // exact line spacing, the same rule for every body font
function chain(it,st,s){ const R=it.includes('→'), L=it.includes('←');
  if(R&&L) throw new Error('v8: one arrow direction per bullet, got both in: '+it.slice(0,60));
  if(!R&&!L) throw new Error('v8: every bullet is an arrow chain (→ or ←), got: '+it.slice(0,70));
  const a=R?'→':'←', sz=bsz(st,s), base={fontFace:st.font,fontSize:sz,color:st.color,lineSpacing:lsp(sz)}, out=[];
  it.split(/\s*[→←]\s*/).forEach((sg,j)=>{
    if(j) out.push({text:' '+a+' ',options:{...base,fontFace:ARROW_F,color:ARROW_C}});
    out.push(...parse(sg.replace(/\*\*/g,''),base,st.color)); });
  return out; }
// widths from fontwidths.json (fontwidths.py), used only to estimate how many rows a paragraph takes
let FW={}; try { FW=JSON.parse(fs.readFileSync('fontwidths.json','utf8')); } catch(e) {}
function runW(t,o){ const st=(o.bold?'b':'')+(o.italic?'i':'')||'r', f=o.fontFace||'Times New Roman';
  const tb=FW[f+'|'+st]||FW[f+'|r']||FW['Times New Roman|r']||{};
  const sz=(o.fontSize||22)*((o.subscript||o.superscript)?0.7:1); let w=0;
  for(const ch of t) w+=(tb[ch]??0.55)*sz; return w; }
function rows(runs,W){ let n=1, w=0;
  for(const r of runs) for(const p of r.text.split(/(\s+)/)){ if(!p) continue; const pw=runW(p,r.options);
    if(w+pw>W && w>0 && !/^\s+$/.test(p)){ n++; w=0; } if(w===0 && /^\s+$/.test(p)) continue; w+=pw; }
  return n; }
const SY={fontFace:SYMFONT,fontSize:18,color:'000000'};
function symRuns(it){ const r=[];
  // v7 symbol line under the equation: 'A | meaning;  B | meaning' -> A: meaning ; B: meaning (18 pt, symbol bold)
  it.slice(1).split(/;\s+/).forEach((part,q)=>{ const p=part.indexOf('|');
    const sym=p<0?'':part.slice(0,p).trim(), mean=(p<0?part:part.slice(p+1)).trim();
    if(q) r.push({text:' ; ',options:{...SY}});   // fresh object: pptxgenjs edits run options
    if(sym) r.push(...parse(sym,{...SY,bold:true},'000000'));
    r.push(...parse((sym?': ':'')+mean,SY,'000000')); });
  return r; }
const headRuns=(t,st)=>[{text:t,options:{fontFace:st.font,fontSize:22,bold:true,italic:!!st.italic,color:st.color,underline:{style:st.u,color:st.color}}}];
// estimated height (pt) of one slide body at bullet size s
function estH(sub,items,sts,box,s){ const W=(box.w*72-8)*0.96, hf=box.w<8; let h=0;
  const hd=t=>rows(headRuns(t,SUBS[0]),W)*28+8;
  if(sub) h+=hd(sub);
  items.forEach((it,i)=>{
    if(it.startsWith('#')) h+=hd(it.slice(1).trim());
    else if(it.startsWith('§')){ const m=EQM[it]; const L=m?Math.max(1,Math.ceil(m[0]/(hf?37:78))):1;
      h+=L*(m&&m[1]?50:30)+8; }
    else if(it.startsWith('›')) h+=rows(symRuns(it),W-36)*22+4;
    else { const sz=bsz(sts[i],s); h+=rows(chain(it,sts[i],s),W-22.5)*lsp(sz)+6; } });
  return h; }
const usable=box=>(box.h*72-8)*0.99;   // estimates run slightly high (check_fill.py)
// cut only in front of a bullet or a '#' heading, so an equation stays with its lead-in and its symbol line
const okCut=it=>isBul(it)||it.startsWith('#');
function greedy(sub,items,sts,boxOf){ const out=[]; let a=0;
  while(a<items.length){ let b=a+1;
    while(b<items.length&&!okCut(items[b])) b++;
    while(b<items.length){ let c=b+1; while(c<items.length&&!okCut(items[c])) c++;
      if(estH(out.length?'':sub,items.slice(a,c),sts.slice(a,c),boxOf(out.length),22)>usable(boxOf(out.length))) break;
      b=c; }
    while(b-1>a&&items[b-1].startsWith('#')) b--;      // a heading never ends a slide
    out.push([a,b]); a=b; }
  return out; }
// same number of slides as the greedy split, with the text spread evenly so no slide is left half empty
function balanced(sub,items,sts,boxOf){ const g=greedy(sub,items,sts,boxOf); if(g.length<2) return g;
  const fits=(a,b,k)=>estH(k?'':sub,items.slice(a,b),sts.slice(a,b),boxOf(k),22)<=usable(boxOf(k));
  const hs=items.map((it,i)=>estH('',[it],[sts[i]],boxOf(1),22)), tot=hs.reduce((x,y)=>x+y,0);
  const out=[]; let a=0, acc=0;
  for(let k=1;k<g.length;k++){ const goal=tot*k/g.length; let best=null, hb=acc;
    for(let b=a+1;b<items.length;b++){ hb+=hs[b-1]; if(!okCut(items[b])) continue; if(!fits(a,b,out.length)) break;
      if(best===null||Math.abs(hb-goal)<Math.abs(best[1]-goal)) best=[b,hb]; }
    if(!best) return g; out.push([a,best[0]]); acc=best[1]; a=best[0]; }
  if(a>=items.length||!fits(a,items.length,out.length)) return g;
  out.push([a,items.length]); return out; }
// deck rule (2026-11-06, second pass): body bullets stay at 22 pt with 6 pt after each bullet.
// Slides are filled by pulling bullets forward from the next slides of the same topic (greedy split).
function fill(sub,items,sts,box){ const s=22;
  FILL[n]={s,est:Math.round(estH(sub,items,sts,box,s)),use:Math.round(usable(box))};
  return {s, aft:6}; }
const FILL={};
function body(s, subtitle, items, sts, box){ if(!items.length&&!subtitle) return;
  let si=(n-1)%SUBS.length;
  if(subtitle) subtitle=subtitle.replace(/^Definitions?\s*:\s*/i,'').replace(/^./,c=>c.toUpperCase());
  const nextSub=()=>{ for(let g=0; g<SUBS.length && lastSig && SUBS[si].font===lastSig[0] && SUBS[si].color===lastSig[1]; g++) si=(si+1)%SUBS.length;
    const st=SUBS[si]; lastSig=[st.font,st.color]; si=(si+1)%SUBS.length; return st; };
  const {s:sz, aft}=fill(subtitle,items,sts,box), arr=[];
  // sub-points (the slide subtitle and '# Heading' items): bold and underlined, no bullet
  if(subtitle) arr.push(...headRuns(subtitle,nextSub())); else lastSig=null;
  items.forEach((it,i)=>{ let r;
    if(it.startsWith('§')){ (EQL[n]=EQL[n]||{half:box.w<8,eqs:[]}).eqs.push(it);
      r=it.startsWith('§#')?[{text:eqtext(it),options:{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true}}]
        :parse(it.slice(1).trim().replace(/"/g,''),{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true},EQC); }
    else if(it.startsWith('›')) r=symRuns(it);
    else if(it.startsWith('#')) r=headRuns(it.slice(1).trim(),nextSub());
    else { r=chain(it,sts[i],sz); r[0].options={...r[0].options,paraSpaceAfter:aft}; }
    if(arr.length) arr[arr.length-1].options={...arr[arr.length-1].options,breakLine:true};
    arr.push(...r); });
  s.addText(arr,{...box,valign:'top',align:'left',margin:[4,4,4,4],isTextBox:true,objectName:'Body',fit:'none'}); }
// v7 caption: 'description | source' -> Figure : description (source), directly under the image, left-aligned with it
function caption(s,cap,y,x,w){ const [d,src]=cap.split(/\s*\|\s*/); const u=t=>t.replace(/_([A-Za-zρθφ0-9])(?![{])/g,'_{$1}');
  const runs=[{text:'Figure : ',options:{fontFace:'Arial',fontSize:12,bold:true,italic:true,color:INK}},
    ...parse(u(d),{fontFace:'Arial',fontSize:12,italic:true,color:INK},INK)];
  if(src) runs.push({text:'  ('+src+')',options:{fontFace:'Agency FB',fontSize:12,color:'C2410C'}});
  s.addText(runs,{x,y,w,h:0.5,margin:0,valign:'top',isTextBox:true,objectName:'Caption'}); }
function img(s,name,cap,R){ const [pw,ph]=SZ[name]; const sc=Math.min(R.w/pw,R.h/ph); const w=pw*sc,h=ph*sc;
  const x=R.x+(R.w-w)/2, y=R.y+(R.h-h)/2;
  s.addImage({path:`${IMG}/${name}.${SZ[name][2]||'png'}`,x,y,w,h,altText:cap||name});
  if(cap) caption(s,cap,y+h+0.06,x,R.x+R.w-x); }
function table(s,rows_,colW,fs,R){ fs=fs||13;
  const data=rows_.map((r,i)=>r.map((c,j)=>({text:c,options:{fontFace:i===0?'Arial':'Times New Roman',fontSize:fs,bold:i===0||j===0,
    color:i===0?'FFFFFF':(j===0?'1D4ED8':INK),fill:{color:i===0?NAVY:(i%2?'FFFFFF':'F1F5F9')},valign:'middle',margin:[2,6,2,6]}})));
  s.addTable(data,{x:R.x,y:R.y,w:R.w,colW,border:{type:'solid',color:'CBD5E1',pt:0.75},autoPage:false}); }
// kept for build.sh / calibrate.py, which write these maps
const EST={}, KEYS={};
const contOf=t=>t.replace(/ \(continued\)$/,'')+' (continued)';
// what the slide shows under the title or the label: the sub-part name only where that sub-part starts
function subFor(t,sub){ const ti=titleInfo(t);
  if(ti.first) return subOf(t,sub);
  if(ti.cont||!ti.sub||ti.sub===curSub) return '';
  curSub=ti.sub; return sub?ti.sub+': '+sub:ti.sub; }
const topicOf=t=>titleInfo(t).topic, subOfT=t=>titleInfo(t).sub;
// consecutive T() slides of one topic are pooled and re-split, so every slide is filled with 22 pt bullets.
// A new sub-part joining the pool is marked by its name as a '#' heading (bold, underlined) in the body.
let PEND=null;
function FLUSH(){ if(!PEND) return; const p=PEND; PEND=null; emit(p); }
// p.draw (figure or table) puts the first slide's body on the left half and the figure on the right half
function emit(p){ const first0=titleInfo(p.t).first, sb=subFor(p.t,p.sub);
  const boxOf=k=>(k===0&&p.draw)?boxFor(!first0,true):boxFor(k>0||!first0,false);
  let g=greedy(sb,p.items,p.sts,boxOf); if(!g.length) g=[[0,0]];
  g.forEach(([a,b],k)=>{ const sl=newSlide(k?contOf(p.t):p.t);
    body(sl,k?'':sb,p.items.slice(a,b),p.sts.slice(a,b),boxOf(k));
    if(k===0&&p.draw) p.draw(sl,figBox(!first0)); }); }
const styles=b=>b.map(it=>isBul(it)?nextStyle():null);
const T=(t,sub,b)=>{ if(PEND&&!sub&&topicOf(t)===topicOf(PEND.t)){ const ns=subOfT(t);
    if(ns&&ns!==PEND.last){ PEND.items.push('# '+ns); PEND.sts.push(null); PEND.last=ns; curSub=ns; }
    PEND.items.push(...b); PEND.sts.push(...styles(b)); return; }
  FLUSH(); PEND={t,sub,items:[...b],sts:styles(b),last:subOfT(t)}; };
// a figure or table slide: body on the left half, figure on the right half. It is pooled like T(), so its half
// box also fills with bullets pulled forward from the next T() slides of the same topic.
// A thin last slide of the pool before it (same topic, under half full) moves onto the figure slide.
function half(t,sub,b,draw){ let lead=null;
  if(PEND&&!sub&&topicOf(t)===topicOf(PEND.t)){ const p=PEND, first0=titleInfo(p.t).first, cs=curSub, sb=subFor(p.t,p.sub); curSub=cs;   // subFor sets curSub, so undo it
    const boxOf=k=>(k===0&&p.draw)?boxFor(!first0,true):boxFor(k>0||!first0,false), g=greedy(sb,p.items,p.sts,boxOf), [a0]=g[g.length-1]||[0];
    const k=g.length-1;
    if(g.length&&!(p.draw&&a0===0)&&estH(k?'':sb,p.items.slice(a0),p.sts.slice(a0),boxOf(k),22)<0.5*usable(boxOf(k))){
      lead={t:a0?contOf(p.t):p.t,sub:a0?'':p.sub,items:p.items.slice(a0),sts:p.sts.slice(a0),last:p.last};   // never p.draw: a0>0 when the pool has a figure
      if(a0){ PEND={...p,items:p.items.slice(0,a0),sts:p.sts.slice(0,a0)}; FLUSH(); } else PEND=null; } }
  FLUSH();
  if(lead){ const ns=subOfT(t);
    if(ns&&ns!==lead.last){ lead.items.push('# '+ns); lead.sts.push(null); curSub=ns; }
    PEND={...lead,items:[...lead.items,...b],sts:[...lead.sts,...styles(b)],last:ns||lead.last,draw}; return; }
  PEND={t,sub,items:[...b],sts:styles(b),last:subOfT(t),draw}; }
const S=(t,sub,b,im,cap)=>half(t,sub,b,(s,R)=>img(s,im,cap,R));
const TB=(t,sub,b,rows_,colW,cap,fs)=>half(t,sub,b,(s,R)=>{ table(s,rows_,colW,fs,R); if(cap) caption(s,cap,R.y+rows_.length*(fs||13)*1.75/72+0.12,R.x,R.w); });   // just under the table
