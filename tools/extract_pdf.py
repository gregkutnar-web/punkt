#!/usr/bin/env python3
"""Iz PDF-ja »Pravi Punkt« (12 strani) izlušči vektorske dele v assets/pravi.json.
Uporaba: python3 tools/extract_pdf.py pot/do/Modifikacija_Ideje-3.pdf   (potrebuje pdftocairo)"""
import json, re, subprocess, sys, tempfile, pathlib
import xml.etree.ElementTree as ET

pdf = sys.argv[1]
out = pathlib.Path(__file__).parent.parent / 'assets' / 'pravi.json'
NS = '{http://www.w3.org/2000/svg}'


def page_paths(n):
    """Seznam (hex barva, d) vseh poti najvišjega nivoja na strani n."""
    with tempfile.TemporaryDirectory() as t:
        f = pathlib.Path(t) / 'p.svg'
        subprocess.run(['pdftocairo', '-svg', '-f', str(n), '-l', str(n), pdf, str(f)], check=True)
        root = ET.parse(f).getroot()
    res = []
    for e in root:
        if e.tag != NS + 'path':
            res.append(None)
            continue
        m = re.match(r'rgb\(([\d.]+)%, ([\d.]+)%, ([\d.]+)%\)', e.get('fill', ''))
        col = '#' + ''.join(f'{round(float(v) * 2.55):02x}' for v in m.groups()) if m else None
        d = re.sub(r'(\d+\.\d{2})\d+', r'\1', e.get('d', ''))
        res.append((col, d))
    return res


p1, p2, p9 = page_paths(1), page_paths(2), page_paths(9)
D = lambda p, i: p[i][1]

data = {
    # stran 1: voziček, košarica, vrečka, značke
    'cart': {'lines': [D(p1, 0), D(p1, 1), D(p1, 2)], 'body': D(p1, 3)},
    'basket': {'handles': [D(p1, 4), D(p1, 5)], 'rim': D(p1, 6), 'bits': [D(p1, i) for i in (7, 8, 9, 10)], 'body': D(p1, 11)},
    'bag': {'handle': D(p1, 12), 'body': D(p1, 13)},
    'badge': {'circle': D(p1, 14), 'eight': D(p1, 15), 'red': p1[14][0]},
    # stran 2: pika (izdelek)
    'drop': D(p2, 4),
    # stran 9: končni logotip (U, pika, P, K, T, N, PRAVI, SKUPINA BOSCAROL)
    'lock': {
        'U': D(p9, 0), 'dot': D(p9, 1), 'P': D(p9, 2), 'K': D(p9, 3), 'T': D(p9, 4), 'N': D(p9, 5),
        'pravi': [D(p9, i) for i in range(7, 12)], 'skupina': [D(p9, i) for i in range(12, 27)],
    },
    'teal': p9[0][0],
}
out.write_text(json.dumps(data, separators=(',', ':')))
print('assets/pravi.json', out.stat().st_size, 'B; teal', data['teal'], 'red', data['badge']['red'])
