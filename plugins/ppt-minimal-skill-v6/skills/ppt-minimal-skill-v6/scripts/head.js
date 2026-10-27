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
// v2 rule: Copperplate Gothic Bold is the default title font, each section has its own font and color
const TF=[['Copperplate Gothic Bold','0B2A55',0.80,false],['Copperplate Gothic Bold','0B2A55',0.80,false],['Copperplate Gothic Light','B91C1C',0.78,true],
  ['Rockwell','1D4ED8',0.56,true],['Gill Sans MT','15803D',0.50,true],['Book Antiqua','6D28D9',0.53,true],['Century','0E7490',0.55,true],
  ['Garamond','C2410C',0.48,true],['Palatino Linotype','0B2A55',0.53,true],['Trebuchet MS','B91C1C',0.53,true]];
let summary=false; function SUMMARY(){ summary=true; }
const tfont=()=>TF[summary?0:Math.min(secN,TF.length-1)];
let lastSig=null;   // [font,color] of the previous slide's first body paragraph
let n=0;
function newSlide(title){ const s=pres.addSlide(); s.background={color:'FFFFFF'}; n++;
  const [ff,fc,cw,bd]=tfont(); const txt=BC[title[0]]?title.slice(2).trim():title;
  const fsz=Math.max(18,Math.min(28,Math.floor(11.6*72/(txt.length*cw))));
  const tt=BC[title[0]]?[{text:title[0]+'  ',options:{fontFace:'Arial',color:BC[title[0]],fontSize:title[0]==='●'?22:20}},{text:txt}]:title;
  s.addText(tt,{x:0.6,y:0.35,w:12.1,h:0.8,fontFace:ff,fontSize:fsz,bold:bd,color:fc,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  return s; }
const SECC=['B91C1C','1D4ED8','15803D','6D28D9','0E7490','C2410C','0B2A55']; let secN=0;
function SEC(name, contents){ const s=pres.addSlide(); n++; const c=SECC[secN%7];
  s.background={path:`${IMG}/sec${secN%7}.png`}; secN++; const [ff,fc,cw,bd]=tfont();
  // no section number on the divider: the name alone, large, on the white panel
  s.addText(name,{x:1.0,y:1.95,w:7.6,h:2.55,fontFace:ff,fontSize:Math.max(30,Math.min(54,Math.floor(7.4*72*2/(name.length*cw)))),bold:true,color:fc,valign:'middle',margin:0,isTextBox:true,objectName:'Title'});
  const df=(lastSig && lastSig[0]==='Verdana' && lastSig[1]===c)?'Trebuchet MS':'Verdana';
  lastSig=[df,c];
  s.addText([{text:contents,options:{fontFace:df,fontSize:18,bold:true,color:c}}],{x:1.0,y:4.6,w:7.6,h:1.2,valign:'top',margin:0,isTextBox:true,objectName:'Body'});
  return s; }
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
      // several symbols on one line: 'A | meaning;  B | meaning' renders as  A: meaning   ▸ B: meaning
      it.slice(1).split(/;\s+/).forEach((part,q)=>{ const p=part.indexOf('|');
        const sym=p<0?'':part.slice(0,p).trim(), mean=(p<0?part:part.slice(p+1)).trim();
        if(q) r.push({text:'     ▸ ',options:{fontFace:'Arial',fontSize:20,color:TEAL}});
        if(sym) r.push(...parse(sym,{fontFace:'Cambria',fontSize:20,color:TEAL,bold:true},TEAL));
        r.push(...parse((sym?': ':'')+mean,{fontFace:'Cambria',fontSize:20,color:INK},TEAL)); }); }
    else { r=/[→←]/.test(it)?chain(it,k,FONTS[k%3]):parse(it,{fontFace:FONTS[k%3],fontSize:22,color:INK},LEADS[k%4]); k++; }
    if(i<items.length-1) r[r.length-1].options.breakLine=true; arr.push(...r); });
  s.addText(arr,{...box,valign:'top',margin:[4,4,4,4],isTextBox:true,objectName:'Body',fit:'none'}); }
function caption(s,cap,y){ s.addText(parse(cap.replace(/_([A-Za-zρθφ0-9])(?![{])/g,'_{$1}'),{fontFace:'Arial',fontSize:12,italic:true,color:MUTED},MUTED),{x:R.x,y:y??R.y+R.h+0.08,w:R.w,h:0.45,fontFace:'Arial',fontSize:12,italic:true,color:MUTED,margin:0,valign:'top',isTextBox:true}); }
function img(s,name,cap){ const [pw,ph]=SZ[name]; const sc=Math.min(R.w/pw,R.h/ph); const w=pw*sc,h=ph*sc;
  const x=R.x+(R.w-w)/2, y=R.y+(R.h-h)/2;
  s.addImage({path:`${IMG}/${name}.${SZ[name][2]||'png'}`,x,y,w,h,altText:cap||name});
  if(cap) caption(s,cap); }
function table(s,rows,colW,fs=13){
  const data=rows.map((r,i)=>r.map((c,j)=>({text:c,options:{fontFace:i===0?'Arial':'Times New Roman',fontSize:fs,bold:i===0||j===0,
    color:i===0?'FFFFFF':(j===0?'1D4ED8':INK),fill:{color:i===0?NAVY:(i%2?'FFFFFF':'F1F5F9')},valign:'middle',margin:[2,6,2,6]}})));
  s.addTable(data,{x:R.x,y:R.y,w:R.w,colW,border:{type:'solid',color:'CBD5E1',pt:0.75},autoPage:false}); }
const plain=t=>t.replace(/\*\*/g,'').replace(/[_^]\{([^}]*)\}/g,'a');
function hgt(it,half,k){ const f=half?1:2.15;
  if(it.startsWith('§')){ const m=EQM[it]; if(m){ const L=Math.max(1,Math.ceil(m[0]/(half?34:72))); return L*(m[1]?46:28)+7; } return 34; }
  if(it.startsWith('›')) return Math.max(1,Math.ceil(plain(it).length/(47*f)))*24.5+4;
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
const T=(t,sub,b)=>{ const k=fitSplit(sub,b,false,t); const s=newSlide(t); body(s,sub,b.slice(0,k),FULL);
  if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub.replace(/ \(continued\)$/,'')+' (continued)'),b.slice(k)); return s; };
const S=(t,sub,b,im,cap)=>{ const k=fitSplit(sub,b,true,t); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); img(s,im,cap);
  if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub+' (continued)'),b.slice(k)); return s; };
const TB=(t,sub,b,rows,colW,cap,fs)=>{ const k=fitSplit(sub,b,true,t); const s=newSlide(t); body(s,sub,b.slice(0,k),HALF); table(s,rows,colW,fs);
  if(cap) caption(s,cap,6.6); if(k<b.length) T(t.replace(/ \(continued\)$/,'')+' (continued)',sub&&(sub+' (continued)'),b.slice(k)); return s; };


