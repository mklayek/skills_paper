// Markdown copy of the deck, built from the same section sources as deck.js.
// Output: <output>/docs/<deck_name>.md (figures linked from ../figs). Settings in deck_config.json.
const fs = require('fs');
const CFG = JSON.parse(fs.readFileSync('deck_config.json', 'utf8'));
const out = []; let secN = 0;
const EQI = {}; for (const e of JSON.parse(fs.readFileSync('eqinv.json'))) EQI[e.id] = e.latex;
try { Object.assign(EQI, JSON.parse(fs.readFileSync('eqfix.json'))); } catch (e) {}
const md = s => s.replace(/_\{([^}]*)\}/g, '<sub>$1</sub>').replace(/\^\{([^}]*)\}/g, '<sup>$1</sup>');
const tex = s => s.replace(/"([^"]*)"/g, (m, t) => '\\text{' + t + '}').replace(/%/g, '\\%');
function items(b) {
  for (const it of b) {
    if (it.startsWith('§#')) out.push('', '$$ ' + EQI[+it.slice(2)].replace(/\s+/g, ' ') + ' $$', '');
    else if (it.startsWith('§')) out.push('', '$$ ' + tex(it.slice(1).trim()) + ' $$', '');
    else if (it.startsWith('›')) {
      const parts = it.slice(1).split(/;\s+/).map(p => { const [s, ...m] = p.split('|'); return m.length ? `**${md(s.trim())}**: ${md(m.join(': ').trim())}` : md(p.trim()); });
      out.push('', parts.join(' ; '), '');   // v7: one continuous symbol line
    } else if (/[→←]/.test(it) && !it.startsWith('**')) {
      const m = it.match(/^(.*?)(\s*[→←]\s*)([\s\S]*)$/);
      out.push('- **' + md(m[1].trim()) + '**' + m[2] + md(m[3]));
    } else out.push('- ' + md(it));
  }
}
const capmd = c => { const [d, s] = c.split(/\s*\|\s*/); return `*Figure :* ${md(d)}` + (s ? ` (${s})` : ''); };
// titles: drop the oval mark, show 'Topic › Sub-topic' as written
function head(t, sub) { out.push('', '## ' + t.replace(/^★\s*/, ''), ''); if (sub) out.push(`*${sub}*`, ''); }
global.SUMMARY = () => {};
global.SEC = (name, contents) => { secN++; out.push('', '---', '', `# 📘 ${name}`, '', `> ${contents}`, ''); };
global.T = (t, sub, b) => { head(t, sub); items(b); };
global.S = (t, sub, b, im, cap) => { head(t, sub); items(b); out.push('', `![${cap}](../figs/${im}.${SZ[im][2] || 'png'})`, '', `<small>${capmd(cap)}</small>`); };
global.TB = (t, sub, b, rows, colW, cap) => { head(t, sub); items(b);
  out.push('', '| ' + rows[0].join(' | ') + ' |', '|' + rows[0].map(() => '---').join('|') + '|');
  for (const r of rows.slice(1)) out.push('| ' + r.map(md).join(' | ') + ' |');
  out.push('', `<small>${capmd(cap)}</small>`); };
const SZ = JSON.parse(fs.readFileSync('sizes.json'));
let src = '';
for (const f of fs.readdirSync('../sections').filter(f => /^c\d.*\.js$/.test(f)).sort()) src += fs.readFileSync('../sections/' + f, 'utf8') + '\n';
eval(src);
const lec = String(CFG.lecture || '').padStart(2, '0');
const doc = [`# ⚡ ${CFG.method_name}: lecture deck (Markdown copy)`, '',
  `> 🎓 Title slide: **${CFG.method_name}** · *${CFG.method_group}* · Lecture ${lec}`,
  `> 📑 Markdown companion of \`${CFG.deck_name}.pptx\`, generated from the same slide sources.`,
  `> 📚 Source: ${CFG.source_credit}`, ...out, '', '---', '', '## 🙏 Thank you!', '', '*Questions & discussion*', ''].join('\n');
fs.writeFileSync(`../../../docs/${CFG.deck_name}.md`, doc);
console.log(`✅ docs/${CFG.deck_name}.md written,`, doc.split('\n').length, 'lines,', secN, 'sections');
