// Iz IDEJA.svg izlušči artboarde (3 ideje), slog, defs in makete.
// Uporaba: NODE_PATH=$(npm root -g) node tools/extract.js pot/do/IDEJA.svg
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), cp = require('child_process');
const src = process.argv[2];
const out = path.join(__dirname, '..', 'assets');
const ren = s => s.replace(/\bst(\d+)\b/g, 'k$1');

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const svgText = fs.readFileSync(src, 'utf8');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 9000, height: 2500 } });
  await p.setContent('<body style="margin:0">' + svgText.replace('<svg ', '<svg width="8906" height="2421" style="display:block" ') + '</body>');
  const data = await p.evaluate(() => {
    const svg = document.querySelector('svg');
    const kids = [...svg.children].filter(e => !['defs', 'style'].includes(e.tagName));
    const isAB = e => e.tagName === 'rect' && Math.abs(+e.getAttribute('width') - 504.05) < 1 && Math.abs(+e.getAttribute('height') - 502) < 1;
    const boards = kids.filter(isAB).map(e => ({ x: +e.getAttribute('x') || 0, y: +e.getAttribute('y'), w: +e.getAttribute('width'), h: +e.getAttribute('height'), cls: e.getAttribute('class') }));
    const items = [], images = [];
    kids.forEach(e => {
      if (isAB(e)) return;
      if (e.tagName === 'image') { images.push({ tr: e.getAttribute('transform'), href: e.getAttribute('xlink:href') || e.getAttribute('href') }); return; }
      const r = e.getBoundingClientRect();
      items.push({ cx: r.x + r.width / 2, cy: r.y + r.height / 2, html: e.outerHTML });
    });
    return { boards, items, images, style: svg.querySelector('style').textContent, defs: [...svg.querySelectorAll('clipPath,filter')].map(e => e.outerHTML) };
  });
  await b.close();

  const ideaOf = y => (y < 500 ? 1 : y < 1500 ? 2 : 3);
  const res = { 1: [], 2: [], 3: [] };
  data.boards.sort((a, c) => a.x - c.x).forEach(bd => res[ideaOf(bd.y)].push({ ...bd, items: [] }));
  data.items.forEach(it => {
    const hit = data.boards.map((bd, i) => ({ bd, i })).find(({ bd }) => it.cx >= bd.x && it.cx <= bd.x + bd.w && it.cy >= bd.y && it.cy <= bd.y + bd.h);
    if (!hit) { console.log('brez artboarda', it.cx | 0, it.cy | 0, it.html.slice(0, 60)); return; }
    const arr = res[ideaOf(hit.bd.y)];
    arr.find(a => a.x === hit.bd.x && a.y === hit.bd.y).items.push(ren(it.html));
  });
  // makete
  const mock = {};
  data.images.forEach(im => {
    const m = /translate\(([\d.]+) ([\d.]+)\)/.exec(im.tr);
    const idea = ideaOf(+m[2]);
    const f = path.join(out, `mock${idea}.png`);
    fs.writeFileSync(f, Buffer.from(im.href.split(',', 2)[1], 'base64'));
    cp.execFileSync('convert', [f, '-resize', '1800x', '-quality', '82', path.join(out, `mock${idea}.jpg`)]);
    fs.unlinkSync(f);
    mock[idea] = { x: +m[1], y: +m[2] };
  });
  const bds = {};
  for (const k of [1, 2, 3]) bds[k] = res[k].map(a => ({ x: a.x, y: a.y, w: a.w, h: a.h, cls: ren(a.cls), items: a.items }));
  fs.writeFileSync(path.join(out, 'boards.json'), JSON.stringify({ boards: bds, mock }));
  fs.writeFileSync(path.join(out, 'style.css'), ren(data.style).replace(/\s+/g, ' '));
  fs.writeFileSync(path.join(out, 'defs.html'), ren(data.defs.join('')));
  for (const k of [1, 2, 3]) console.log('osnutek', k, 'artboardov', bds[k].length, bds[k].map(a => a.items.length).join(','));
})();
