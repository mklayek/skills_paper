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
const HALF={x:0.6,y:1.3,w:5.9,h:5.7}, FULL={x:0.6,y:1.3,w:12.1,h:5.7}, R={x:6.85,y:1.35,w:5.9,h:5.2};
const BC={'◆':'B91C1C','■':'1D4ED8','●':'15803D'};
// Titles (ported from v7 on 2026-10-28). A TOPIC is the title without its level marker, without " (continued)" and without
// a " › sub-topic" part. Every slide of one topic shares one title font and one dark text color.
// The font changes at every new topic, cycling TPOOL. First slide of a topic: centered title.
// Later slides of the same topic: left-aligned. Every third topic gets a light fill, the rest none.
// '★' before the marker = very important title, drawn as a gold oval (always centered).
// 'Topic › Sub' on a continued slide = black label (white text) with the topic at the top left,
// and the sub-topic as the title. On a topic's first slide the sub-topic moves into the subtitle.
const TPOOL=[['Copperplate Gothic Bold',0.80,false],['Bookman Old Style',0.56,true],['MV Boli',0.55,false],
  ['Footlight MT Light',0.47,false],['Copperplate Gothic Light',0.78,false],['Rockwell',0.56,true],
  ['Book Antiqua',0.53,true],['Californian FB',0.48,true]];
const TDARK=['0B2A55','991B1B','14532D','4C1D95','134E4A','7C2D12','1E3A8A','831843','3F3F46'];
const TLIGHT=['FFF2B3','DBEAFE','DCFCE7','EDE9FE','FCE7F3','E0F2FE','FFEDD5'];
const OVAL_FILL='FFC000';
const SYMFONT='Times New Roman';   // symbol lines: 18 pt black, see body()
// v7: the title bullet (marker) has its own glyph and color per topic, so no two topics in a row share one.
// The ◆ ■ ● written in a title string only switch the marker on; the topic decides how it looks.
const TMARK=[['◆','B91C1C'],['■','1D4ED8'],['●','15803D'],['▶','6D28D9'],['❖','0E7490'],
  ['✦','C2410C'],['▲','0B2A55'],['◉','831843'],['➤','14532D'],['✿','7C2D12']];
const MARKFONT='Segoe UI Symbol';
let topicIdx=-1, lastTopic=null;
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
  const label=!ti.first && !!ti.sub;              // topic continues with a sub-topic title
  let shown, mk=ti.mk;
  if(label){ shown=ti.sub+(ti.cont?' (continued)':''); 
    const lw=Math.min(6.5,ti.topic.length*16*cw/72+0.35);
    s.addText(ti.topic,{x:0,y:0,w:lw,h:0.36,fontFace:ff,fontSize:16,color:'FFFFFF',fill:{color:'000000'},
      valign:'middle',align:'left',margin:[0,6,0,6],isTextBox:true,objectName:'TopicLabel'}); }
  else shown=ti.topic+(ti.cont?' (continued)':'');
  const y=label?0.42:0.35, h=label?0.78:0.8;
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
function SEC(name, contents){ const s=pres.addSlide(); n++; const c=SECC[secN%7];
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
// v6 arrow-chain bullet: 'Concept → mechanism → meaning' or 'Effect ← cause ← origin'.
// Each segment takes its own color (never the same on both sides of an arrow), the first
// segment (the concept or term) is always bold, and the format set changes from bullet to bullet.
const CPAL=['B91C1C','1D4ED8','15803D','6D28D9','0E7490','C2410C'];
const CFMT=[[{bold:true},{},{italic:true}],[{bold:true,italic:true},{},{bold:true}],
  [{bold:true,underline:{style:'sng'}},{italic:true},{}],[{bold:true},{italic:true},{bold:true,italic:true}]];
const ARROW_C='374151';
function chain(it,k,face){ const R=it.includes('→'), L=it.includes('←');
  if(R&&L) throw new Error('v6: one arrow direction per bullet, got both in: '+it.slice(0,60));
  const a=R?'→':'←', segs=it.split(/\s*[→←]\s*/), out=[];
  segs.forEach((sg,j)=>{ const c=CPAL[(k*2+j)%CPAL.length], f=CFMT[k%CFMT.length][Math.min(j,2)];
    if(j) out.push({text:' '+a+' ',options:{fontFace:face,fontSize:22,bold:true,color:ARROW_C}});
    out.push(...parse(sg,{fontFace:face,fontSize:22,color:c,...f},c)); });
  return out; }
function body(s, subtitle, items, box){ let si=(n-1)%SUBS.length;
  // never repeat the previous slide's subtitle style, dividers included
  for(let g=0; g<SUBS.length && lastSig && SUBS[si].font===lastSig[0] && SUBS[si].color===lastSig[1]; g++) si=(si+1)%SUBS.length;
  const st=SUBS[si]; lastSig=[st.font,st.color];
  const arr=!subtitle?[]:[{text:subtitle,options:{fontFace:st.font,fontSize:22,bold:true,italic:!!st.italic,color:st.color,underline:{style:st.u,color:st.color},breakLine:true}}];
  if(!subtitle) lastSig=null;
  let k=0;
  items.forEach((it,i)=>{ let r;
    if(it.startsWith('§')){ (EQL[n]=EQL[n]||{half:box===HALF,eqs:[]}).eqs.push(it);
      r=it.startsWith('§#')?[{text:eqtext(it),options:{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true}}]
        :parse(it.slice(1).trim().replace(/"/g,''),{fontFace:'Cambria Math',fontSize:22,color:EQC,bold:true},EQC); }
    else if(it.startsWith('›')){ r=[];
      // v7 symbol line, directly under the equation, one continuous line:
      // 'A | meaning;  B | meaning'  ->  A: meaning ; B: meaning   (Times New Roman 18 pt, black, symbol bold)
      const SY={fontFace:SYMFONT,fontSize:18,color:'000000'};
      it.slice(1).split(/;\s+/).forEach((part,q)=>{ const p=part.indexOf('|');
        const sym=p<0?'':part.slice(0,p).trim(), mean=(p<0?part:part.slice(p+1)).trim();
        if(q) r.push({text:' ; ',options:SY});
        if(sym) r.push(...parse(sym,{...SY,bold:true},'000000'));
        r.push(...parse((sym?': ':'')+mean,SY,'000000')); }); }
    else { r=/[→←]/.test(it)?chain(it,k,FONTS[k%3]):parse(it,{fontFace:FONTS[k%3],fontSize:22,color:INK},LEADS[k%4]); k++; }
    if(i<items.length-1) r[r.length-1].options.breakLine=true; arr.push(...r); });
  s.addText(arr,{...box,valign:'top',margin:[4,4,4,4],isTextBox:true,objectName:'Body',fit:'none'}); }
// v7 caption: 'description | source' -> Figure : description (source), Figure bold italic, description italic
// near-black, source in Agency FB orange-brown, placed directly under the image and left-aligned with it.
function caption(s,cap,y,x,w){ const [d,src]=cap.split(/\s*\|\s*/); const u=t=>t.replace(/_([A-Za-zρθφ0-9])(?![{])/g,'_{$1}');
  const runs=[{text:'Figure : ',options:{fontFace:'Arial',fontSize:12,bold:true,italic:true,color:INK}},
    ...parse(u(d),{fontFace:'Arial',fontSize:12,italic:true,color:INK},INK)];
  if(src) runs.push({text:'  ('+src+')',options:{fontFace:'Agency FB',fontSize:12,color:'C2410C'}});
  s.addText(runs,{x:x??R.x,y:y??R.y+R.h+0.08,w:w??R.w,h:0.5,margin:0,valign:'top',isTextBox:true,objectName:'Caption'}); }
function captionOld(s,cap,y){ s.addText(parse(cap.replace(/_([A-Za-zρθφ0-9])(?![{])/g,'_{$1}'),{fontFace:'Arial',fontSize:12,italic:true,color:MUTED},MUTED),{x:R.x,y:y??R.y+R.h+0.08,w:R.w,h:0.45,fontFace:'Arial',fontSize:12,italic:true,color:MUTED,margin:0,valign:'top',isTextBox:true}); }
function img(s,name,cap){ const [pw,ph]=SZ[name]; const sc=Math.min(R.w/pw,R.h/ph); const w=pw*sc,h=ph*sc;
  const x=R.x+(R.w-w)/2, y=R.y+(R.h-h)/2;
  s.addImage({path:`${IMG}/${name}.${SZ[name][2]||'png'}`,x,y,w,h,altText:cap||name});
  if(cap) caption(s,cap,y+h+0.06,x,R.x+R.w-x); }
function table(s,rows,colW,fs=13){
  const data=rows.map((r,i)=>r.map((c,j)=>({text:c,options:{fontFace:i===0?'Arial':'Times New Roman',fontSize:fs,bold:i===0||j===0,
    color:i===0?'FFFFFF':(j===0?'1D4ED8':INK),fill:{color:i===0?NAVY:(i%2?'FFFFFF':'F1F5F9')},valign:'middle',margin:[2,6,2,6]}})));
  s.addTable(data,{x:R.x,y:R.y,w:R.w,colW,border:{type:'solid',color:'CBD5E1',pt:0.75},autoPage:false}); }
const plain=t=>t.replace(/\*\*/g,'').replace(/[_^]\{([^}]*)\}/g,'a');
function hgt(it,half,k){ const f=half?1:2.15;
  if(it.startsWith('§')){ const m=EQM[it]; if(m){ const L=Math.max(1,Math.ceil(m[0]/(half?34:72))); return L*(m[1]?46:28)+7; } return 34; }
  if(it.startsWith('›')) return Math.max(1,Math.ceil(plain(it).length/(56*f)))*22+4;
  return Math.max(1,Math.ceil(plain(it).length/([41,34,36][k%3]*f)))*27+8; }
// per-slide calibration from a measured render (calibrate.py): SCALE[title] multiplies the estimate
let SCALE={}; try { SCALE=JSON.parse(fs.readFileSync('scale.json')); } catch(e) {}
const NOSPLIT=fs.existsSync('nosplit.flag'); const EST={};
function estTotal(sub,items,half){ let h=sub?Math.ceil(sub.length/(half?36:75))*27+8:0, k=0;
  for(const it of items){ h+=hgt(it,half,k); if(!/^[§›]/.test(it)) k++; } return h; }
// titles repeat ("X (continued)"), so calibration is keyed by title plus the first item
const KEYS={};
function fitSplit(sub,items,half,title){ const key=title+'¦'+(items[0]||'').slice(0,40); KEYS[n+1]=key;
  const f=SCALE[key]||1; EST[key]=estTotal(sub,items,half);
  if(NOSPLIT) return items.length;
  let h=(sub?Math.ceil(sub.length/(half?36:75))*27+8:0)*f, k=0; const BUD=398;
  // anti-orphan: a (continued) slide holding one lone bullet reads badly, so if the whole list
  // only just overruns the budget, keep it together rather than splitting off a single item.
  { let tot=h, kk=0;
    for(const it of items){ tot+=hgt(it,half,kk)*f; if(!/^[§›]/.test(it)) kk++; }
    if(tot<=BUD*1.12) return items.length; }
  for(let i=0;i<items.length;i++){ h+=hgt(items[i],half,k)*f; if(!/^[§›]/.test(items[i])) k++;
    if(h>BUD){ let j=i;
      while(j>1&&(items[j].startsWith('›')||/^§\s{3,}/.test(items[j])||/^§\s*[+−-]\s/.test(items[j]))) j--;
      if(j>1&&items[j].startsWith('§')&&/:\s*$/.test(items[j-1])) j--; return Math.max(j,1); } }
  return items.length; }
const T=(t,sub,b)=>{ sub=subOf(t,sub); const k=fitSplit(sub,b,false,t); const s=newSlide(t); body(s,sub,b.slice(0,k),FULL);
  if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub.replace(/ \(continued\)$/,'')+' (continued)'),b.slice(k)); return s; };
const S=(t,sub,b,im,cap)=>{ sub=subOf(t,sub); const k=fitSplit(sub,b,true,t); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); img(s,im,cap);
  if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub+' (continued)'),b.slice(k)); return s; };
const TB=(t,sub,b,rows,colW,cap,fs)=>{ sub=subOf(t,sub); const k=fitSplit(sub,b,true,t); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); table(s,rows,colW,fs);
  if(cap) caption(s,cap,6.6); if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub+' (continued)'),b.slice(k)); return s; };


