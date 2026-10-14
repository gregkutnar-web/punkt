#!/usr/bin/env python3
"""Zgradi samostojni index.html (landing) iz src/ + assets/ (brez omrežja).
Vir artboardov: assets/boards.json (tools/extract.js), logotipi: assets/logo*.json (tools/extract_compare.js)."""
import sys, json, base64, pathlib
R = pathlib.Path(__file__).parent
sys.path.insert(0, str(R / 'tools'))
import parts

A = R / 'assets'
S = R / 'src'
B = parts.BOARDS['boards']


def bg_of(cls):
    return parts.CF.get(cls, ('#f2f2f2', False))[0] or '#f2f2f2'


def cfg_for(idea):
    out = []
    for bd in B[str(idea)]:
        out.append({'x': bd['x'], 'y': bd['y'], 'w': bd['w'], 'h': bd['h'],
                    'cx': bd['x'] + bd['w'] / 2, 'cy': bd['y'] + bd['h'] / 2, 'bg': bg_of(bd['cls'])})
    return out


def data_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def logo_svg(n):
    d = json.loads((A / f'logo{n}.json').read_text())
    x, y, w, h = d['bb']
    pad = max(w, h) * .02
    return f'<svg viewBox="{x - pad:.1f} {y - pad:.1f} {w + 2 * pad:.1f} {h + 2 * pad:.1f}" role="img" aria-label="Osnutek {n}">{d["html"]}</svg>'


cfg = {str(i): {'boards': cfg_for(i)} for i in (1, 2, 3)}
probe = ''.join(f'<g id="ab{i}_{b}">{parts.anim_board(i, b)}</g>' for i in (1, 2) for b in range(len(B[str(i)])))
b3 = cfg['3']['boards'][0]
vb3 = f'{b3["cx"] - 320:.1f} {b3["cy"] - 180:.1f} 640 360'
o3 = parts.anim_board(3, 0)

page = (S / 'landing.html').read_text()
subs = {
    '__STYLE__': parts.STYLE + (S / 'landing.css').read_text(),
    '__DEFS__': (A / 'defs.html').read_text(),
    '__PROBE__': probe,
    '__O3__': o3, '__VB3__': vb3,
    '__N1__': str(len(B['1'])), '__N2__': str(len(B['2'])),
    '__L1__': logo_svg(1), '__L2__': logo_svg(2), '__L3__': logo_svg(3),
    '__CONFIG__': json.dumps(cfg),
    '__MOCK__': json.dumps([data_uri(A / f'mock{i}.jpg', 'image/jpeg') for i in (1, 2, 3)]),
    '__STAGEJS__': (S / 'stage.js').read_text(),
    '__SCENJS__': (S / 'scen.js').read_text(),
    '__PAGEJS__': (S / 'page.js').read_text(),
}
for k, v in subs.items():
    page = page.replace(k, v)
(R / 'index.html').write_text(page)
print('index.html', round(len(page) / 1024), 'KB')
