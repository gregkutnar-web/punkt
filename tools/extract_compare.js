// Iz Primerjava_logotipov.svg izlušči tri končne logotipe (skupine) v assets/logo{1,2,3}.json
// Uporaba: NODE_PATH=$(npm root -g) node tools/extract_compare.js pot/do/Primerjava_logotipov.svg
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const svg = fs.readFileSync(process.argv[2], 'utf8');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1600, height: 3000 } });
  await p.setContent('<body style="margin:0">' + svg.replace('<svg ', '<svg width="1535" height="2917" style="display:block" ') + '</body>');
  const groups = await p.evaluate(() => [...document.querySelector('svg').children].filter(e => e.tagName === 'g').map(e => {
    const r = e.getBBox(); return { bb: [r.x, r.y, r.width, r.height], html: e.outerHTML };
  }));
  await b.close();
  const out = path.join(__dirname, '..', 'assets');
  groups.forEach(g => {
    const idea = g.bb[1] < 400 ? 1 : g.bb[1] < 2000 ? 2 : 3;
    const html = g.html.replace(/\bst(\d)\b/g, 'pl$1');
    fs.writeFileSync(path.join(out, `logo${idea}.json`), JSON.stringify({ bb: g.bb.map(v => +v.toFixed(2)), html }));
    console.log(idea, g.bb.map(v => Math.round(v)).join(','));
  });
})();
