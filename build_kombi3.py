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

def cab():  # majhen logotip na vratih kabine
    d, w = lockup(282, 496, .30, claim=False, site=False)
    d1, w1 = text('Poiščite nas na ', 282, 470, 8, 'Inter-Bold.otf', .01, 1.0, INK)
    d2, _ = text('DAB-u', 282 + w1, 470, 8, 'Inter-Black.otf', .01, 1.0, TEAL)
    return f'<g class="a" style="--i:0">{d1}{d2}</g>' + d

def wrap(inner):
    return f'<svg viewBox="0 0 {W} {H}" class="ov" xmlns="http://www.w3.org/2000/svg"><g style="mix-blend-mode:multiply">{inner}</g></svg>'

# ---------- Osnutek 1: pot (od pike do žarkov) ----------
def o1():
    s = ''
    # pot: krogci, ki se proti zadku spremenijo v play-trikotnike
    n, pts = 15, []
    for i in range(n):
        t = i / (n - 1)
        x = 300 + t * 830
        y = 575 - t * 215 + math.sin(t * 6.3) * 26
        pts.append((x, y, t))
    for i, (x, y, t) in enumerate(pts):
        r = 7 + t * 26
        if t < .38:
            s += f'<circle class="a" style="--i:{i}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{TEAL}"/>'
        else:
            k = r * 2.1 / 430
            s += f'<g class="a" style="--i:{i}">{glyph(x - 170*k, y - 260*k, k, TEAL, slots=False)}</g>'
    # končni sij
    gx, gy, gk = 1180, 170, .78
    s += f'<g class="a" style="--i:16">{glyph(gx, gy, gk, TEAL)}</g>'
    cx, cy = gx + 395 * gk, gy + 265 * gk
    s += rays(cx, cy, [(-80, 150, 215, 30), (-52, 170, 250, 34), (-24, 160, 240, 34), (4, 150, 225, 34), (32, 160, 240, 34), (60, 170, 235, 30)], TEAL, 32)
    d, w = lockup(628, 250, .68, icon_right=False)
    return wrap(s + d + cab())

# ---------- Osnutek 2: valovi (oddajanje) ----------
def o2():
    cx, cy = 1520, 470
    s = '<svg x="598" y="118" width="1060" height="512" viewBox="598 118 1060 512" overflow="hidden">'
    for i, r in enumerate(range(150, 490, 68)):
        col = TEAL if i % 2 == 0 else TEAL2
        circ = 2 * math.pi * r
        seg = 54 + i * 6; gap = 30 + i * 3
        wdt = 22 + i * 1.5
        s += (f'<circle class="a" style="--i:{i}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{wdt:.1f}" '
              f'stroke-dasharray="{seg} {gap}" stroke-dashoffset="{i*37}" opacity="{max(.4, 1 - i*.08):.2f}"/>')
    s += '</svg>'
    s += f'<g class="a" style="--i:0">{glyph(cx - 105, cy - 150, .42, DARK)}</g>'
    d, w = lockup(628, 250, .72, icon_right=False)
    d3, _ = text('Poslušaj. Odkrij.', 630, 420, 30, 'Inter-Black.otf', .02, 1.1, TEAL)
    return wrap(s + d + f'<g class="a" style="--i:3">{d3}</g>' + cab())

# ---------- Osnutek 3: prag (portal) ----------
def o3():
    x0, y0, x1, y1 = 1092, 120, 1652, 626
    s = f'<rect class="a" style="--i:0" x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="44" fill="{DARK}"/>'
    # svetloba iz portala čez drsna vrata
    fan = [(180 - 54, 50, 170, 22), (180 - 36, 50, 250, 24), (180 - 18, 50, 310, 24), (180, 50, 380, 26), (180 + 18, 50, 310, 24), (180 + 36, 50, 250, 24), (180 + 54, 50, 170, 22)]
    s += rays(1072, 372, fan, TEAL2, 24)
    s += f'<g class="a" style="--i:2">{glyph(1235, 140, .56, "#fff").replace(chr(34)+"#fff"+chr(34)+" transform", chr(34)+DARK+chr(34)+" transform")}</g>'
    d, w = text('RADIO ODISEJA', 1372, 520, 30, 'Inter-Black.otf', .10, 1.22, '#fff', anchor='middle')
    d2, _ = text('Poiščite nas na DAB-u', 1372, 566, 19, 'Inter-Bold.otf', .01, 1.0, '#fff', anchor='middle')
    s += f'<g class="a" style="--i:3">{d}</g><g class="a" style="--i:4">{d2}</g>'
    return wrap(s + cab())

SVGS = [o1(), o2(), o3()]
if __name__ == '__main__':
    tpl = open('src/kombi3.html', encoding='utf-8').read()
    out = tpl.replace('@PHOTO', PHOTO)
    for i, sv in enumerate(SVGS, 1): out = out.replace(f'@SVG{i}', sv)
    open('kombi-odiseja-predlogi.html', 'w', encoding='utf-8').write(out)
