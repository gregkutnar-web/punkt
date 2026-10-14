#!/usr/bin/env python3
"""Zgradi samostojni index.html iz src/deck.html + assets/ (brez omrežja)."""
import re, base64, pathlib
R = pathlib.Path(__file__).parent
A = R / 'assets' / 'idea1'

def inner(k):
    s = (A / f't{k:02d}.svg').read_text()
    s = re.sub(r'<style>.*?</style>', '', s, flags=re.S)
    s = re.sub(r'^<svg[^>]*>|</svg>$', '', s.strip())
    s = re.sub(r' xmlns(:\w+)?="[^"]*"', '', s)
    return re.sub(r'\s+/>', '/>', s)

def split_gold(k):
    """Loči zlato črto (class st2) od sivih elementov."""
    body = inner(k)
    gold = re.findall(r'<g class="st2"[^>]*>.*?</g>', body, flags=re.S)
    gray = body
    for g in gold:
        gray = gray.replace(g, '')
    return gray, ''.join(gold)

def b64(name, mime):
    return f'data:{mime};base64,' + base64.b64encode((A / name).read_bytes()).decode()

tiles = ''.join(f'<g id="t{k:02d}">{inner(k)}</g>' for k in (0, 3, 4, 5, 6, 8, 10, 11, 12))

g3, gold3 = split_gold(3)
g4, gold4 = split_gold(4)
anim = f'''<svg id="anim" viewBox="0 0 1200 460" aria-hidden="true">
<defs><clipPath id="wipe"><rect id="wipeRect" x="1790" y="215" width="0" height="120"/></clipPath></defs>
<g id="cam">
<g id="L10"><g transform="translate(-5754.5,-286)">{inner(10)}</g></g>
<g id="L6"><g transform="translate(-3552,-272.95)">{inner(6)}</g></g>
<g id="L5"><g transform="translate(-3002.05,-273)">{inner(5)}</g></g>
<g id="L4"><g transform="translate(-2452.05,-273)">{inner(4)}</g></g>
<g id="L3"><g transform="translate(-1862.15,-273)">{g3}<g clip-path="url(#wipe)">{gold3}</g></g></g>
<g id="L0"><g transform="translate(39.9,0) scale(.943) translate(-252,-272.95)">{inner(0)}</g></g>
</g></svg>'''

html = (R / 'src' / 'deck.html').read_text()
for key, val in {
    '__TILES__': tiles, '__ANIM__': anim,
    '__IMG1__': b64('fasada1.jpg', 'image/jpeg'), '__IMG2__': b64('fasada2.jpg', 'image/jpeg'),
}.items():
    html = html.replace(key, val)
(R / 'index.html').write_text(html)
print('index.html', round(len(html) / 1024), 'KB')
