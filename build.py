#!/usr/bin/env python3
"""Zgradi samostojni index.html iz src/deck.html + assets/ (brez omrežja)."""
import re, base64, pathlib, xml.etree.ElementTree as ET

R = pathlib.Path(__file__).parent
A = R / 'assets' / 'idea1'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
COL = {'st0': '#ff6b4a', 'st1': '#087f8c', 'st2': '#c69c6d', 'st5': '#666666',
       'st6': '#809f9c', 'st7': '#708180', 'st9': '#e6e6e6'}
# vrstni red sličic v animaciji (indeksi sličic t00..t13); sličica 7 je premaknjena za dve naprej
ORDER = [0, 1, 2, 3, 4, 5, 7, 8, 6, 9, 10, 11, 12, 13]
# dejanski levi rob podlag (artboard) v izvirnem SVG; zadnje štiri niso na 550 px razmaku
TILEX = [k * 550 for k in range(10)] + [5502.43, 6078.43, 6654.17, 7230.69]


def inner(k):
    """Sličica z razredi (barve prek CSS spremenljivk) za interakcijo, ikone, primerjavo."""
    s = (A / f't{k:02d}.svg').read_text()
    s = re.sub(r'<style>.*?</style>', '', s, flags=re.S)
    s = re.sub(r'^<svg[^>]*>|</svg>$', '', s.strip())
    s = re.sub(r' xmlns(:\w+)?="[^"]*"', '', s)
    return re.sub(r'\s+/>', '/>', s)


def anim_src(k):
    """Sličica razdeljena na dele z id (e<k>_<pot>) za animacijo; barva prek currentColor."""
    root = ET.fromstring((A / f't{k:02d}.svg').read_text())
    kids = [c for c in root if not c.tag.endswith('style')]

    def walk(e, ident):
        tag = e.tag.split('}')[1]
        attrs = dict(e.attrib)
        cls = attrs.pop('class', None)
        if tag == 'g':
            return f'<g id="{ident}">' + ''.join(walk(c, f'{ident}_{i}') for i, c in enumerate(e)) + '</g>'
        a = ' '.join(f'{n}="{v}"' for n, v in attrs.items())
        return f'<{tag} id="{ident}" {a} fill="currentColor" data-c="{COL.get(cls, "#708180")}"/>'

    return ''.join(walk(c, f'e{k}_{i}') for i, c in enumerate(kids, start=1))


def b64(name, mime):
    return f'data:{mime};base64,' + base64.b64encode((A / name).read_bytes()).decode()


tiles = ''.join(f'<g id="t{k:02d}">{inner(k)}</g>' for k in range(14))
probe = ''.join(anim_src(k) for k in range(14))
thumbs = ''.join(
    f'<button class="th" data-k="{d}" aria-label="Sličica {d + 1}"><svg viewBox="{TILEX[k]} 21.98 504.05 502">'
    f'<rect x="{TILEX[k]}" y="21.98" width="504.05" height="502" fill="#f2f2f2"/><use href="#t{k:02d}"/></svg></button>'
    for d, k in enumerate(ORDER))

html = (R / 'src' / 'deck.html').read_text()
html = html.replace('__ANIMJS__', (R / 'src' / 'anim.js').read_text())
for key, val in {
    '__TILES__': tiles, '__PROBE__': probe, '__THUMBS__': thumbs,
    '__ORDER__': str(ORDER), '__TILEX__': str(TILEX),
    '__IMG1__': b64('fasada1.jpg', 'image/jpeg'), '__IMG2__': b64('fasada2.jpg', 'image/jpeg'),
}.items():
    html = html.replace(key, val)
(R / 'index.html').write_text(html)
print('index.html', round(len(html) / 1024), 'KB')
