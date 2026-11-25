#!/usr/bin/env python3
"""Odisejin druzinski kviz: 3 kartoncki A6 (105x148 mm) v enem SVG. Pisava Archivo (outlined + skrita zivа plast)."""
import base64, io, math, random
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = Path(__file__).parent
W, H, GAP, TOP = 105, 148, 12, 10
BLUE, PINK, BLK = "#3ca7ed", "#fc29a0", "#000000"
FONTS = {w: [TTFont(HERE / "fonts" / f"archivo-{p}-{w}-normal.woff") for p in ("latin-ext", "latin")] for w in (800, 900)}

def text(s, weight, size, x, y, fill=BLK, anchor="middle", cid="txt", track=0.0, maxw=None):
    fl = FONTS[weight]; ds = []; adv = []; items = []
    for c in s:
        f = next((f for f in fl if ord(c) in f.getBestCmap()), None)
        if f is None: raise SystemExit(f"manjka glif {c!r}")
        n = f.getBestCmap()[ord(c)]; sc = size / f["head"].unitsPerEm
        items.append((f, n, sc)); adv.append(f["hmtx"][n][0] * sc)
    k = 1.0
    if maxw and sum(adv) + track * size * (len(s) - 1) > maxw:
        k = maxw / (sum(adv) + track * size * (len(s) - 1))
    size *= k; items = [(f, n, sc * k) for f, n, sc in items]; adv = [a * k for a in adv]
    tr = track * size; adv = [a + tr for a in adv]
    total = sum(adv) - tr; cx = x - (total / 2 if anchor == "middle" else 0)
    for (f, n, sc), a in zip(items, adv):
        pen = SVGPathPen(f.getGlyphSet(), ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
        f.getGlyphSet()[n].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        if pen.getCommands(): ds.append(pen.getCommands())
        cx += a
    path = f'<path id="{cid}" aria-label="{s}" fill="{fill}" d="{" ".join(ds)}"/>'
    live = f'<text id="{cid}-zivo" x="{x}" y="{y}" font-family="Archivo" font-weight="{weight}" font-size="{size:.3f}" letter-spacing="{tr:.3f}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
    return path, live

im = Image.open(HERE / "a6" / "logo-odisejin-kviz.webp").convert("RGBA"); im = im.crop(im.split()[3].getbbox())
im.thumbnail((800, 800)); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
LOGO = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
LW = 54; LH = LW * im.size[1] / im.size[0]
PURPLE, GOLD, CREAM = "#3a1670", "#ffd84d", "#fffbea"
CX, CY, BR = W / 2, 110, 28   # sredisce in polmer znacke

def rays(n=28, r=200):
    out = []
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        out.append(f"M{CX:.2f} {CY:.2f}L{CX + r*math.cos(a0):.2f} {CY + r*math.sin(a0):.2f}L{CX + r*math.cos(a1):.2f} {CY + r*math.sin(a1):.2f}Z")
    return " ".join(out)

def star4(x, y, r, rot, fill, op):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.32
        a = math.radians(rot + i * 45); pts.append(f"{x + rr*math.cos(a):.2f},{y + rr*math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" opacity="{op}"/>'

def confetti(seed, pal):
    rng = random.Random(seed); out = []; n = 0
    while n < 26:
        x, y = rng.uniform(5, W - 5), rng.uniform(5, H - 5)
        if 4 < x < W - 4 and 4 < y < 43 and 20 < x < W - 20: continue       # logotip
        if 8 < x < W - 8 and 44 < y < 77: continue                         # ploscica
        if math.hypot(x - CX, y - CY) < BR + 3: continue                    # znacka
        c, r, t = rng.choice(pal), rng.uniform(1.0, 2.2), n % 3
        if t == 0: out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r*0.8:.2f}" fill="{c}"/>')
        elif t == 1: out.append(star4(x, y, r * 1.9, rng.uniform(0, 45), c, 1))
        else: out.append(f'<rect x="{x-r:.2f}" y="{y-r*0.45:.2f}" width="{r*2:.2f}" height="{r*0.9:.2f}" rx="{r*0.45:.2f}" fill="{c}" transform="rotate({rng.uniform(0,180):.0f} {x:.2f} {y:.2f})"/>')
        n += 1
    return "".join(out)

def marquee(step=6.2, inset=3.6, r=0.85, fill="#ffffff", op=0.85):
    xs = [inset + i * (W - 2 * inset) / round((W - 2 * inset) / step) for i in range(round((W - 2 * inset) / step) + 1)]
    ys = [inset + i * (H - 2 * inset) / round((H - 2 * inset) / step) for i in range(round((H - 2 * inset) / step) + 1)]
    pts = [(x, inset) for x in xs] + [(x, H - inset) for x in xs] + [(inset, y) for y in ys[1:-1]] + [(W - inset, y) for y in ys[1:-1]]
    return "".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}"/>' for x, y in pts), fill, op

def burst(cx, cy, ro, ri, n=20):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri; a = math.pi * i / n - math.pi / 2
        pts.append(f"{cx + r*math.cos(a):.2f},{cy + r*math.sin(a):.2f}")
    return " ".join(pts)

def card(n, cid, bg, lines, pal, badge, dark_badge=False, pill=None):
    """lines: (mala vrstica, velika vrstica); badge: (stevilka, 'TOCK')"""
    x0 = (n - 1) * (W + GAP); P, Lv = [], []
    def add(t):
        P.append(t[0]); Lv.append(t[1])
    # ploscica z imenom
    small, big = lines
    add(text(small, 800, 6.4, W / 2, 56.6, cid=f"{cid}-vrstica1", track=0.18))
    add(text(big, 800, 12.5, W / 2, 70.4, cid=f"{cid}-vrstica2", track=0.02, maxw=77))
    bfill, bstroke, nfill, tfill = (PURPLE, GOLD, "#ffe27a", "#ffffff") if dark_badge else (GOLD, BLK, BLK, BLK)
    add(text(badge[0], 900, 31, CX, CY + 5.5, nfill, cid=f"{cid}-stevilka", maxw=32))
    add(text(badge[1], 900, 11.5, CX, CY + 17, tfill, cid=f"{cid}-tock", track=0.04))
    mq, mf, mo = marquee()
    g = (f'<g id="{cid}" transform="translate({x0} {TOP})"><clipPath id="clip-{cid}"><rect width="{W}" height="{H}"/></clipPath>'
         f'<g clip-path="url(#clip-{cid})">'
         f'<rect id="{cid}-ozadje" width="{W}" height="{H}" fill="{bg}"/>'
         f'<path id="{cid}-zarki" d="{rays()}" fill="#ffffff" opacity="{0.2 if dark_badge else 0.16}"/>'
         f'<g id="{cid}-konfeti">{confetti(n * 7 + 3, pal)}</g>'
         f'<g id="{cid}-lucke" fill="{mf}" opacity="{mo}">{mq}</g>'
         f'<image id="{cid}-logotip" x="{(W-LW)/2:.3f}" y="5" width="{LW}" height="{LH:.3f}" xlink:href="{LOGO}"/>'
         f'<g id="{cid}-ploscica"><rect x="9.2" y="46.6" width="{W-18.4}" height="29" rx="5" fill="{BLK}"/>'
         f'<rect x="8" y="45.4" width="{W-16}" height="29" rx="5" fill="{CREAM}" stroke="{BLK}" stroke-width="0.8"/></g>'
         f'<g id="{cid}-znacka"><polygon points="{burst(CX+1.3, CY+1.3, BR+3.2, BR-0.6)}" fill="{BLK}"/>'
         f'<polygon points="{burst(CX, CY, BR+3.2, BR-0.6)}" fill="{bfill}" stroke="{BLK}" stroke-width="0.8" stroke-linejoin="round"/>'
         f'<circle cx="{CX}" cy="{CY}" r="{BR-3.6}" fill="none" stroke="{bstroke}" stroke-width="0.7" stroke-dasharray="0.1 1.9" stroke-linecap="round"/></g>')
    if pill:
        g += (f'<g id="{cid}-ZA"><rect x="{CX-10.5+1}" y="{CY-BR-8.3+1}" width="21" height="9.6" rx="4.8" fill="{BLK}"/>'
              f'<rect x="{CX-10.5}" y="{CY-BR-8.3}" width="21" height="9.6" rx="4.8" fill="{PURPLE}" stroke="{BLK}" stroke-width="0.8"/>'
              f'{text(pill, 800, 6.4, CX, CY-BR-1.3, "#ffffff", cid=f"{cid}-ZA-besedilo")[0]}</g>')
        Lv.append(text(pill, 800, 6.4, CX, CY - BR - 1.3, "#ffffff", cid=f"{cid}-ZA-besedilo")[1])
    g += f'<g id="{cid}-besedilo">{"".join(P)}</g></g></g>'
    return g, f'<g id="{cid}-zivo" transform="translate({x0} {TOP})">{"".join(Lv)}</g>'

CYAN, MAG = "#19b5f0", "#ff2fa0"
c1 = card(1, "A6-1-Vlahovic", BLUE, ("DRUŽINA", "VLAHOVIČ"), [GOLD, "#ffffff", MAG, PURPLE, "#ffffff"], ("10", "TOČK"))
c2 = card(2, "A6-2-Ulaga", PINK, ("DRUŽINA", "ULAGA"), [GOLD, "#ffffff", CYAN, PURPLE, "#ffffff"], ("10", "TOČK"))
c3 = card(3, "A6-3-Bonus", "url(#zlato)", ("BONUS", "VPRAŠANJE"), ["#ffffff", MAG, CYAN, PURPLE, "#ffffff"], ("50", "TOČK"), dark_badge=True, pill="ZA")
labels = "".join(text(t, 800, 3, (n - 1) * (W + GAP), 6, "#8b8d90", anchor="start", cid=f"Oznaka-{n}")[0] for n, t in ((1, "A6 - 1"), (2, "A6 - 2"), (3, "A6 - 3 BONUS")))
TW, TH = 3 * W + 2 * GAP, TOP + H
defs = '<defs><linearGradient id="zlato" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd84d"/><stop offset=".5" stop-color="#f9b800"/><stop offset="1" stop-color="#e39a00"/></linearGradient></defs>'
out = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{TW}mm" height="{TH}mm" viewBox="0 0 {TW} {TH}">'
       f'<title>Odisejin druzinski kviz - kartoncki A6</title>{defs}<g id="Oznake">{labels}</g>{c1[0]}{c2[0]}{c3[0]}'
       f'<g id="Zivo-besedilo-skrito" display="none">{c1[1]}{c2[1]}{c3[1]}</g></svg>')
(HERE / "odisejin-kviz-a6.svg").write_text(out, encoding="utf-8")
print("ok", len(out) // 1024, "KB")
