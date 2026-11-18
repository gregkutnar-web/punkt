#!/usr/bin/env python3
"""Iz PDF-ja »Odiseja – Oglaševanje, priročnik CGP« (str. 4, vodoravni logotip brez pripisa, črna različica)
izlušči vektorske dele v assets/odiseja.json.
Uporaba: python3 tools/extract_odiseja.py pot/do/Odiseja_oglasevanje_CGP.pdf   (potrebuje pdftocairo)"""
import json, re, subprocess, sys, tempfile, pathlib
import xml.etree.ElementTree as ET

pdf = sys.argv[1]
out = pathlib.Path(__file__).parent.parent / 'assets' / 'odiseja.json'
NS = '{http://www.w3.org/2000/svg}'
INK = (7.8, 11.1, 12.1)  # temna barva logotipa v PDF-ju (rgb %)


def paths():
    with tempfile.TemporaryDirectory() as t:
        f = pathlib.Path(t) / 'p.svg'
        subprocess.run(['pdftocairo', '-svg', '-f', '3', '-l', '3', pdf, str(f)], check=True)
        root = ET.parse(f).getroot()
    res = []
    def walk(e):
        for c in e:
            if c.tag == NS + 'defs':
                continue
            if c.tag == NS + 'path':
                res.append((c.get('fill', ''), c.get('d', '')))
            else:
                walk(c)
    walk(root)
    return res


def bbox(d):
    n = [float(v) for v in re.findall(r'-?\d+\.?\d*', d)]
    xs, ys = n[0::2], n[1::2]
    return min(xs), min(ys), max(xs), max(ys)


sel = []
for fill, d in paths():
    m = re.match(r'rgb\(([\d.]+)%, ([\d.]+)%, ([\d.]+)%\)', fill)
    if not m or any(abs(float(a) - b) > .3 for a, b in zip(m.groups(), INK)):
        continue
    x0, y0, x1, y1 = bbox(d)
    if 460 < y0 and y1 < 515 and x1 < 450 and x1 - x0 < 300:   # spodnji levi logotip (črn, brez pripisa)
        sel.append((x0, y0, x1, y1, d))
print(len(sel), 'poti')
letters = [s for s in sel if s[2] < 365]     # črke ODISEJA
sun = [s for s in sel if s[2] >= 365]
print('črke', len(letters), 'sonce', len(sun))
tx = lambda s: re.sub(r'(\d+\.\d{3})\d+', r'\1', s)
data = {'letters': [tx(s[4]) for s in sorted(letters)], 'sun': [tx(s[4]) for s in sorted(sun)],
        'bbox': [min(s[0] for s in sel), min(s[1] for s in sel), max(s[2] for s in sel), max(s[3] for s in sel)]}
out.write_text(json.dumps(data))
print(data['bbox'])
