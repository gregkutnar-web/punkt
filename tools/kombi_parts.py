"""Gradniki za poslikave kombija (SVG v koordinatah fotografije 1774x887): logotip Radio Odiseja, žarki, orisano besedilo."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

TEAL, TEAL2, DARK, INK = '#0097a7', '#27b9c4', '#0d4450', '#25525f'
FONT = '/usr/share/fonts/opentype/inter/'
_f = {}


def font(name):
    if name not in _f:
        t = TTFont(FONT + name); _f[name] = (t, t.getGlyphSet(), t.getBestCmap(), t['head'].unitsPerEm)
    return _f[name]


def text(s, x, y, cap, fname='Inter-Black.otf', track=0.0, xs=1.0, fill=INK, spans=None, anchor='start', cls=''):
    """Orisano besedilo; y = osnovna črta, cap = višina velikih črk v px, track v em, xs = raztegnitev po x.
    spans: seznam (od, do, barva) za barvanje delov niza."""
    t, gs, cmap, upm = font(fname)
    capH = t['OS/2'].sCapHeight
    k = cap / capH
    total = 0
    for ch in s:
        total += gs[cmap[ord(ch)]].width * k * xs + track * cap / 0.72 * xs
    total -= track * cap / 0.72 * xs
    ox = x - (total if anchor == 'end' else total / 2 if anchor == 'middle' else 0)
    cur = ox; parts = []
    for i, ch in enumerate(s):
        g = gs[cmap[ord(ch)]]
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (k * xs, 0, 0, -k, cur, y)))
        d = pen.getCommands()
        col = fill
        for a, b, c in (spans or []):
            if a <= i < b: col = c
        if d: parts.append((d, col))
        cur += g.width * k * xs + track * cap / 0.72 * xs
    out = {}
    for d, c in parts: out.setdefault(c, []).append(d)
    return ''.join(f'<path{(" class=%s" % cls) if cls else ""} d="{" ".join(v)}" fill="{c}"/>' for c, v in out.items()), total


# ---- glif (lokalne koordinate ~ 0..430 x 0..540) ----
GLYPH_BODY = 'M35,38 L395,265 L158,500 Z'
SLOTS = [(185, 150, 92, 30, 20), (205, 268, 92, 36, -12), (268, 385, 92, 30, -45)]


def glyph(x, y, s, fill=TEAL, rot=0, slots=True, extra=''):
    """Zaobljen play-trikotnik z tremi režami; (x,y) = zgornji levi kot lokalnega okvirja, s = merilo."""
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" {extra}>'
    o += f'<path d="{GLYPH_BODY}" fill="{fill}" stroke="{fill}" stroke-width="70" stroke-linejoin="round"/>'
    if slots:
        for cx, cy, w, h, r in SLOTS:
            o += f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="#fff" transform="translate({cx} {cy}) rotate({r})"/>'
    return o + '</g>'


def rays(cx, cy, specs, fill=TEAL, w=36):
    """specs: (kot v stopinjah [0=desno, 90=dol], r1, r2[, w])."""
    o = ''
    for i, sp in enumerate(specs):
        a, r1, r2 = sp[:3]; ww = sp[3] if len(sp) > 3 else w
        t = math.radians(a)
        x1, y1, x2, y2 = cx + r1 * math.cos(t), cy + r1 * math.sin(t), cx + r2 * math.cos(t), cy + r2 * math.sin(t)
        o += f'<line class="a" style="--i:{i}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{fill}" stroke-width="{ww}"/>'
    return o


def icon(x, y, s, fill=TEAL):
    """Majhna ikona: glif + pikčasti žarki (izhodišče = levo-zgoraj)."""
    o = f'<g transform="translate({x} {y}) scale({s})">'
    o += glyph(0, 0, .2, fill)
    cx, cy = 76, 54
    for a in range(-80, 81, 20):
        t = math.radians(a); r1, r2 = 36, 36 + (14 if a % 40 == 0 else 9)
        o += f'<line x1="{cx+r1*math.cos(t):.1f}" y1="{cy+r1*math.sin(t):.1f}" x2="{cx+r2*math.cos(t):.1f}" y2="{cy+r2*math.sin(t):.1f}" stroke="{fill}" stroke-width="5"/>'
    return o + '</g>'


def lockup(x, y, s, fill=TEAL, ink=INK, claim=True, site=True, icon_right=True):
    """Napis RADIO ODISEJA + 'Poiščite nas na DAB-u' + spletni naslov; (x,y) = levi rob osnovne črte napisa."""
    cap = 40 * s
    d, w = text('RADIO ODISEJA', x, y, cap, 'Inter-Black.otf', .10, 1.22, fill)
    o = f'<g class="a" style="--i:0">{d}'
    if icon_right: o += icon(x + w + 22 * s, y - 62 * s, 1.0 * s * 1.0, fill)
    o += '</g>'
    if claim:
        d1, w1 = text('Poiščite nas na ', x, y - 70 * s - 6, 22 * s, 'Inter-Bold.otf', .01, 1.0, ink)
        d2, _ = text('DAB-u', x + w1, y - 70 * s - 6, 22 * s, 'Inter-Black.otf', .01, 1.0, fill)
        o += f'<g class="a" style="--i:1">{d1}{d2}</g>'
    if site:
        d3, _ = text('radio-odiseja.si', x, y + 48 * s, 24 * s, 'Inter-Bold.otf', .0, 1.0, ink)
        o += f'<g class="a" style="--i:2">{d3}</g>'
    return o, w
