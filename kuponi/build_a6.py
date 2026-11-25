#!/usr/bin/env python3
"""Odisejin druzinski kviz: 3 kartoncki A6 (105x148 mm) v enem SVG. Pisava Archivo (outlined + skrita zivа plast)."""
import base64, io
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = Path(__file__).parent
W, H, GAP, TOP = 105, 148, 12, 10
BLUE, PINK, BLK = "#3ca7ed", "#fc29a0", "#000000"
FONTS = {w: [TTFont(HERE / "fonts" / f"archivo-{p}-{w}-normal.woff") for p in ("latin-ext", "latin")] for w in (800, 900)}

def text(s, weight, size, x, y, fill=BLK, anchor="middle", cid="txt"):
    fl = FONTS[weight]; ds = []; adv = []; items = []
    for c in s:
        f = next((f for f in fl if ord(c) in f.getBestCmap()), None)
        if f is None: raise SystemExit(f"manjka glif {c!r}")
        n = f.getBestCmap()[ord(c)]; sc = size / f["head"].unitsPerEm
        items.append((f, n, sc)); adv.append(f["hmtx"][n][0] * sc)
    total = sum(adv); cx = x - (total / 2 if anchor == "middle" else 0)
    for (f, n, sc), a in zip(items, adv):
        pen = SVGPathPen(f.getGlyphSet(), ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
        f.getGlyphSet()[n].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        if pen.getCommands(): ds.append(pen.getCommands())
        cx += a
    path = f'<path id="{cid}" aria-label="{s}" fill="{fill}" d="{" ".join(ds)}"/>'
    live = f'<text id="{cid}-zivo" x="{x}" y="{y}" font-family="Archivo" font-weight="{weight}" font-size="{size}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
    return path, live

im = Image.open(HERE / "a6" / "logo-odisejin-kviz.webp").convert("RGBA"); im = im.crop(im.split()[3].getbbox())
im.thumbnail((800, 800)); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
LOGO = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
LW = 49; LH = LW * im.size[1] / im.size[0]

def card(n, cid, bg, lines, defs=""):
    """lines: (tekst, utez, velikost, y)"""
    paths, lives = [], []
    for i, (s, wt, sz, y) in enumerate(lines, 1):
        p, l = text(s, wt, sz, W / 2, y, cid=f"{cid}-vrstica{i}"); paths.append(p); lives.append(l)
    x = (n - 1) * (W + GAP)
    g = (f'<g id="{cid}" transform="translate({x} {TOP})">'
         f'<rect id="{cid}-ozadje" width="{W}" height="{H}" fill="{bg}"/>'
         f'<image id="{cid}-logotip" x="{(W-LW)/2:.3f}" y="6.5" width="{LW}" height="{LH:.3f}" xlink:href="{LOGO}"/>'
         f'<g id="{cid}-besedilo">{"".join(paths)}</g></g>')
    live = f'<g id="{cid}-zivo" transform="translate({x} {TOP})">{"".join(lives)}</g>'
    return g, live

NAME, BIG, SMALL = 9.6, 29, 17
c1 = card(1, "A6-1-Vlahovic", BLUE, [("DRUŽINA", 800, NAME, 52), ("VLAHOVIČ", 800, NAME, 62.6), ("10", 900, BIG, 102), ("TOČK", 900, SMALL, 122)])
c2 = card(2, "A6-2-Ulaga", PINK, [("DRUŽINA", 800, NAME, 52), ("ULAGA", 800, NAME, 62.6), ("10", 900, BIG, 102), ("TOČK", 900, SMALL, 122)])
c3 = card(3, "A6-3-Bonus", "url(#zlato)", [("BONUS", 800, NAME, 52), ("VPRAŠANJE", 800, NAME, 62.6), ("ZA", 800, NAME, 78), ("50", 900, BIG, 106), ("TOČK", 900, SMALL, 126)])
labels = "".join(text(t, 800, 3, (n - 1) * (W + GAP), 6, "#8b8d90", anchor="start", cid=f"Oznaka-{n}")[0] for n, t in ((1, "A6 - 1"), (2, "A6 - 2"), (3, "A6 - 3 BONUS")))
TW, TH = 3 * W + 2 * GAP, TOP + H
defs = '<defs><linearGradient id="zlato" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd84d"/><stop offset=".5" stop-color="#f9b800"/><stop offset="1" stop-color="#e39a00"/></linearGradient></defs>'
out = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{TW}mm" height="{TH}mm" viewBox="0 0 {TW} {TH}">'
       f'<title>Odisejin druzinski kviz - kartoncki A6</title>{defs}<g id="Oznake">{labels}</g>{c1[0]}{c2[0]}{c3[0]}'
       f'<g id="Zivo-besedilo-skrito" display="none">{c1[1]}{c2[1]}{c3[1]}</g></svg>')
(HERE / "odisejin-kviz-a6.svg").write_text(out, encoding="utf-8")
print("ok", len(out) // 1024, "KB")
