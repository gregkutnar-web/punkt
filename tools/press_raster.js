#!/usr/bin/env node
/* Izriše PNG (prosojno ozadje) in PDF iz SVG-jev ter tiska PDF iz HTML-ja.
   Uporaba: NODE_PATH=$(npm root -g) node tools/press_raster.js jobs.json */
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const ctx = await b.newContext();
  const p = await ctx.newPage();
  for (const j of jobs) {
    if (j.html) {
      await p.goto('file://' + j.html);
      await p.pdf({ path: j.pdf, preferCSSPageSize: true, printBackground: true });
      continue;
    }
    const svg = fs.readFileSync(j.svg, 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/), w0 = +m[1], h0 = +m[2];
    const html = (w, h) => `<!doctype html><html><body style="margin:0;background:transparent"><div style="width:${w}px;height:${h}px">${svg.replace(/width="\d+" height="\d+"/, `width="${w}" height="${h}"`)}</div></body></html>`;
    for (const out of j.png) {
      const w = +out.match(/-(\d+)px\.png$/)[1], h = Math.round(w * h0 / w0);
      await p.setViewportSize({ width: w, height: h });
      await p.setContent(html(w, h));
      await p.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    }
    // PDF: vektorsko, velikost strani = logotip (pt)
    const wpt = 400, hpt = Math.floor(400 * h0 / w0) - 1;  // px (= 300 pt)
    await p.setViewportSize({ width: 800, height: 600 });
    await p.setContent(`<!doctype html><html><head><style>@page{size:${wpt}px ${hpt}px;margin:0}html,body{margin:0;overflow:hidden}svg{display:block}</style></head><body>${svg.replace(/width="\d+" height="\d+"/, `width="${wpt}" height="${hpt}"`)}</body></html>`);
    await p.pdf({ path: j.pdf, width: wpt + 'px', height: hpt + 'px', printBackground: true });
  }
  await b.close();
})();
