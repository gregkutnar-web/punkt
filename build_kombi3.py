# Sestavi kombi-odiseja-predlogi.html: 3 osnutki poslikave kombija (SVG čez fotografijo praznega kombija).
import base64, io, math, sys
sys.path.insert(0, 'tools')
from PIL import Image
from kombi_parts import *

SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-user-punkt/48b3d78d-1599-5d3a-acc8-93dab4d65a91/images/11.jpg'
im = Image.open(SRC).convert('RGB')
b = io.BytesIO(); im.resize((1600, round(im.height * 1600 / im.width))).save(b, 'JPEG', quality=84, optimize=True)
PHOTO = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
W, H = im.size  # 1774x887

PILLARS = ['Kino · Oder · Koncerti', 'Otroci · Hrana & pijača · Terasa']

def brand(x, y, s, fill=TEAL, ink=INK, anchor='start', sub=True, pill=True):
    """Napis ODISEJA + BTC City Ljubljana + stebri; (x,y) = osnovna črta napisa."""
    d, w = text('ODISEJA', x, y, 40 * s, 'Inter-Black.otf', .10, 1.22, fill, anchor=anchor)
    o = f'<g class="a" style="--i:0">{d}</g>'
    if sub:
        d2, _ = text('BTC City Ljubljana', x, y + 44 * s, 19 * s, 'Inter-Bold.otf', .02, 1.0, ink, anchor=anchor)
        o += f'<g class="a" style="--i:1">{d2}</g>'
    if pill:
        for k, ln in enumerate(PILLARS):
            d3, _ = text(ln, x, y + (84 + 22 * k) * s, 15 * s, 'Inter-Bold.otf', .03, 1.0, ink, anchor=anchor)
            o += f'<g class="a" style="--i:{2 + k}">{d3}</g>'
    return o

def cab():  # majhen napis na vratih kabine
    return brand(282, 498, .32, sub=False, pill=False).replace('--i:0', '--i:0') + \
        f'<g class="a" style="--i:1">{text("BTC City Ljubljana", 282, 514, 6.5, "Inter-Bold.otf", .02, 1.0, INK)[0]}</g>'

def wrap(inner):
    return f'<svg viewBox="0 0 {W} {H}" class="ov" xmlns="http://www.w3.org/2000/svg"><g style="mix-blend-mode:multiply">{inner}</g></svg>'

# ---------- Osnutek 1: pot (od pike do sonca) ----------
def o1():
    s = ''
    n = 15
    for i in range(n):
        t = i / (n - 1)
        x = 330 + t * 740
        y = 600 - t * 200 + math.sin(t * 6.3) * 26
        s += f'<circle class="a" style="--i:{i}" cx="{x:.0f}" cy="{y:.0f}" r="{6 + t * 30:.1f}" fill="{TEAL}"/>'
    cx, cy = 1370, 380
    s += f'<circle class="a" style="--i:16" cx="{cx}" cy="{cy}" r="120" fill="{TEAL}"/>'
    s += rays(cx, cy, [(a, 165, 245 if k % 2 == 0 else 215, 32) for k, a in enumerate(range(-100, 260, 30)) if not (65 < a < 115)], TEAL, 32)
    return wrap(s + brand(628, 250, 1.05) + cab())

# ---------- Osnutek 2: valovi ----------
def o2():
    cx, cy = 1480, 470
    s = '<svg x="598" y="118" width="1060" height="512" viewBox="598 118 1060 512" overflow="hidden">'
    for i, r in enumerate(range(150, 490, 68)):
        col = TEAL if i % 2 == 0 else TEAL2
        s += (f'<circle class="a" style="--i:{i}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{22 + i * 1.5:.1f}" '
              f'stroke-dasharray="{54 + i * 6} {30 + i * 3}" stroke-dashoffset="{i * 37}" opacity="{max(.4, 1 - i * .08):.2f}"/>')
    s += '</svg>'
    s += f'<circle class="a" style="--i:0" cx="{cx}" cy="{cy}" r="95" fill="{DARK}"/>'
    d, _ = text('Odkrij.', 630, 440, 46, 'Inter-Black.otf', .02, 1.1, TEAL)
    return wrap(s + brand(628, 250, 1.05) + f'<g class="a" style="--i:4">{d}</g>' + cab())

# ---------- Osnutek 3: prag ----------
def o3():
    x0, y0, x1, y1 = 1092, 120, 1652, 626
    s = f'<rect class="a" style="--i:0" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="44" fill="{DARK}"/>'
    fan = [(180 - 54, 50, 170, 22), (180 - 36, 50, 250, 24), (180 - 18, 50, 310, 24), (180, 50, 380, 26), (180 + 18, 50, 310, 24), (180 + 36, 50, 250, 24), (180 + 54, 50, 170, 22)]
    s += rays(1072, 372, fan, TEAL2, 24)
    ax, ay, aw, ah = 1292, 160, 160, 240  # loku podobna vrata (prag), izrezana
    s += f'<path class="a" style="--i:2" d="M{ax},{ay+ah} V{ay+aw/2} A{aw/2},{aw/2} 0 0 1 {ax+aw},{ay+aw/2} V{ay+ah} Z" fill="#fff"/>'
    s += f'<g class="a" style="--i:3">{brand(1372, 462, .85, "#fff", "#fff", "middle")}</g>'
    return wrap(s + cab())

SVGS = [o1(), o2(), o3()]
if __name__ == '__main__':
    tpl = open('src/kombi3.html', encoding='utf-8').read()
    out = tpl.replace('@PHOTO', PHOTO)
    for i, sv in enumerate(SVGS, 1): out = out.replace(f'@SVG{i}', sv)
    open('kombi-odiseja-predlogi.html', 'w', encoding='utf-8').write(out)
