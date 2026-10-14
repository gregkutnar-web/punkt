#!/usr/bin/env python3
"""Iz IDEJA-1.svg izvleče vsako sličico (tile, 550 px razmik) v assets/idea1/tNN.svg.
Uporaba: python3 tools/extract_tiles.py pot/do/IDEJA-1.svg"""
import re, sys, pathlib, xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
src, out = sys.argv[1], pathlib.Path(__file__).parent.parent / 'assets' / 'idea1'
ns = '{http://www.w3.org/2000/svg}'
STYLE = ('<style>.st0{fill:#ff6b4a}.st1{fill:#087f8c}.st2{fill:#c69c6d}.st3{fill:none}'
         '.st5{fill:#666}.st6{fill:#809f9c}.st7{fill:#708180}.st9{fill:#e6e6e6}</style>')

def firstx(e):
    for p in e.iter():
        d = p.get('d')
        if d:
            m = re.match(r'M\s*(-?[\d.]+)', d)
            if m: return float(m.group(1))
        if p.get('points'): return float(p.get('points').split()[0].split(',')[0])
        if p.tag.endswith('rect') and p.get('x'): return float(p.get('x'))
    return None

tiles = {}
for e in ET.parse(src).getroot():
    tag = e.tag.replace(ns, '')
    if tag in ('defs', 'rect', 'image'): continue
    x = firstx(e)
    if x is None: continue
    k = int(x // 550)
    if k >= 14: continue            # vzorec (5354 drobnih poti) in fotografije
    tiles.setdefault(k, []).append(ET.tostring(e, encoding='unicode'))
for k, v in sorted(tiles.items()):
    (out / f't{k:02d}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{k*550} 21.98 504.05 502">{STYLE}' + ''.join(v) + '</svg>')
print(sorted(tiles))
