#!/usr/bin/env python3
"""Pleško kuponi 210x99 mm: generira 3 SVG predloge (stran A + stran B)."""
import base64, io, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = Path(__file__).parent
W, H, R, GAP = 210, 99, 5, 12
YEL, BLK, WHT = "#ffd000", "#0c0c0d", "#ffffff"
VAN_SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "avtodom.webp"
LOGO_SRC = HERE / "plesko-logo-source.svg"
FD = "/usr/share/fonts/opentype/inter/"
FONTS = {k: TTFont(FD + f"Inter-{k}.otf") for k in ("Bold", "SemiBold", "Medium", "ExtraBold")}

# ---------- tekst -> orisane poti ----------
def text(s, font, size, x, y, fill, track=0.0, anchor="start", cid=None):
    f = FONTS[font]; upm = f["head"].unitsPerEm; sc = size / upm
    cmap = f.getBestCmap(); gs = f.getGlyphSet(); hm = f["hmtx"]
    names = [cmap[ord(c)] for c in s]
    adv = [hm[n][0] * sc + track * size for n in names]
    total = sum(adv) - track * size
    cx = x - (total if anchor == "end" else total / 2 if anchor == "middle" else 0)
    ds = []
    for n, a in zip(names, adv):
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
        gs[n].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        d = pen.getCommands()
        if d: ds.append(d)
        cx += a
    return f'<path id="{cid or "txt"}" aria-label="{s}" fill="{fill}" d="{" ".join(ds)}"/>', total

# ---------- logotip ----------
def load_logo():
    ns = "{http://www.w3.org/2000/svg}"
    root = ET.parse(LOGO_SRC).getroot()
    top = root.findall(ns + "g")[0]
    g_exp, g_pl = top.findall(ns + "g")
    def leaves(g):
        for e in g:
            yield e.tag.replace(ns, ""), dict(e.attrib)
    return list(leaves(g_exp)), list(leaves(g_pl))
EXP, PLE = load_logo()
LX0, LX1, LY0, LY1 = 59.9, 377.1, 84.66, 126.9

def logo(cx, cy, width, dark_bg, cid="Plesko-logo"):
    k = width / (LX1 - LX0)
    c_pl = WHT if dark_bg else "#231f20"
    c_ex = "#8b8d90" if dark_bg else "#bbbdbf"
    out = [f'<g id="{cid}" transform="translate({cx:.3f} {cy:.3f}) scale({k:.5f}) translate({-(LX0+LX1)/2:.3f} {-(LY0+LY1)/2:.3f})">']
    def el(tag, a, fill):
        if tag == "path": return f'<path fill="{fill}" d="{a["d"]}"/>'
        return f'<polygon fill="{fill}" points="{a["points"]}"/>'
    out.append('<g id="EXPERIENCE">' + "".join(el(t, a, c_ex) for t, a in EXP) + "</g>")
    out.append('<g id="PLESKO">' + "".join(el(t, a, YEL if a.get("class") == "st0" else c_pl) for t, a in PLE) + "</g>")
    out.append("</g>")
    return "".join(out)

# ---------- QR ----------
_q = (HERE / "plesko-qr-source.svg").read_text(encoding="utf-8")
QR_BODY = _q[_q.index('<g fill="#000000"'):_q.index("<metadata")]
def qr(x, y, size, dark_bg, cid="QR-koda-A"):
    tile = f'{rr(0, 0, 370, 370, 36)} fill="#ffffff"/>' if dark_bg else ""
    return f'<g id="{cid}" transform="translate({x} {y}) scale({size/370:.5f})">{tile}{QR_BODY}</g>'

# ---------- kontakt ----------
def contact(dark_bg):
    c1, c2 = (WHT, "#8b8d90") if dark_bg else (BLK, "#8b8d90")
    a = text("01/365-8010", "SemiBold", 3.5, 12, 79.6, c1, track=0.04, cid="Kontakt-telefon")[0]
    b = text("info@plesko-cars.si", "Medium", 3.5, 12, 85.2, c2, track=0.04, cid="Kontakt-email")[0]
    return f'<g id="Kontakt">{a}{b}</g>'

# ---------- avtodom ----------
def van_data():
    im = Image.open(VAN_SRC).convert("RGBA"); im = im.crop(im.split()[3].getbbox())
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size
VAN, (VW, VH) = van_data()
def van(x, y, w, cid="Avtodom"):
    return f'<image id="{cid}" x="{x}" y="{y}" width="{w}" height="{w*VH/VW:.3f}" preserveAspectRatio="xMidYMid meet" xlink:href="{VAN}"/>'

def rr(x, y, w, h, r): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}"'

# ---------- ogrodje ----------
def card(side, bg, body, cid):
    oy = 0 if side == "A" else H + GAP
    return (f'<g id="{cid}" transform="translate(0 {oy})"><clipPath id="clip-{cid}">{rr(0,0,W,H,R)}/></clipPath>'
            f'<g id="Vsebina-{cid}" clip-path="url(#clip-{cid})">{rr(0,0,W,H,R)} fill="{bg}"/>{body}</g>'
            f'<g id="Rez-{cid}">{rr(0,0,W,H,R)} fill="none" stroke="#e6007e" stroke-width="0.25"/></g></g>')

def doc(title, a, b):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}mm" height="{2*H+GAP}mm" viewBox="0 0 {W} {2*H+GAP}"><title>{title}</title>'
            f'<defs><radialGradient id="glow"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fadeW" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient></defs>'
            f'{a}{b}</svg>')

# ---------- Predlog 1: črna, tekst levo, avtodom desno ----------
def p1():
    t = []
    t.append(text("VIKEND NAJEM", "SemiBold", 3.1, 14, 24, YEL, track=0.28, cid="Kicker")[0])
    for i, (s, c) in enumerate([("Avtodom", WHT), ("Ahorn", WHT), ("Camp", YEL)]):
        pass
    L = [("Vikend najem", WHT), ("avtodoma", WHT), ("Ahorn Camp", YEL)]
    body = ['<ellipse cx="143" cy="82" rx="68" ry="9" fill="url(#glow)"/>', van(76, 16, 131)]
    y = 41
    for i, (s, c) in enumerate(L):
        body.append(text(s, "Bold", 10.5, 13, y + i * 12.6, c, track=-0.025, cid=f"Naslov-{i+1}")[0])
    body.append(text("VIKEND NAJEM", "SemiBold", 0.01, 0, 0, YEL)[0] if False else "")
    body.append(qr(12, 71, 18, True))
    a = card("A", BLK, "".join(body), "Stran-A")
    b = card("B", BLK, logo(W/2, H/2, 112, True) + contact(True) + qr(W-12-18, H-12-18, 18, True, "QR-koda-B"), "Stran-B")
    return doc("Plesko kupon - predlog 1 (crna)", a, b)

# ---------- Predlog 2: bela, veliki napis zgoraj, avtodom spodaj ----------
def p2():
    body = []
    body.append(text("Vikend najem", "ExtraBold", 17.5, 12, 33, BLK, track=-0.035, cid="Naslov-1")[0])
    body.append(f'{rr(12, 40, 14, 1.2, .6)} fill="{YEL}"/>')
    body.append(text("AVTODOMA", "SemiBold", 4.1, 12, 52, BLK, track=0.3, cid="Naslov-2")[0])
    body.append(text("AHORN CAMP", "SemiBold", 4.1, 12, 59.5, "#8b8d90", track=0.3, cid="Naslov-3")[0])
    body.append(f'<rect x="12" y="89.6" width="{W-24}" height="0.25" fill="{BLK}"/>')
    body.append(van(96, 30, 102))
    body.append(qr(W-12-18, 8, 18, False))
    a = card("A", WHT, "".join(body), "Stran-A")
    b = card("B", WHT, logo(W/2, H/2, 112, False) + contact(False) + qr(W-12-18, H-12-18, 18, False, "QR-koda-B"), "Stran-B")
    return doc("Plesko kupon - predlog 2 (bela)", a, b)

# ---------- Predlog 3: črna, centrirano, rumena črta ceste ----------
def p3():
    body = []
    body.append(text("VIKEND NAJEM AVTODOMA", "SemiBold", 3.8, W/2, 15.5, WHT, track=0.34, anchor="middle", cid="Naslov-1")[0])
    body.append(text("Ahorn Camp", "ExtraBold", 15, W/2, 31.5, YEL, track=-0.03, anchor="middle", cid="Naslov-2")[0])
    body.append(f'<ellipse cx="{W/2}" cy="86" rx="62" ry="7" fill="url(#glow)"/>')
    body.append(f'<rect x="12" y="89.2" width="{W-24}" height="0.5" fill="{YEL}"/>')
    body.append(van(W/2-47, 37, 94))
    body.append(qr(W-12-18, 69, 18, True))
    a = card("A", BLK, "".join(body), "Stran-A")
    fr = f'{rr(6, 6, W-12, H-12, R-1.5)} fill="none" stroke="#3a3a3c" stroke-width="0.3" id="Okvir"/>'
    b = card("B", BLK, fr + logo(W/2, H/2, 104, True) + contact(True) + qr(W-12-18, H-12-18, 18, True, "QR-koda-B"), "Stran-B")
    return doc("Plesko kupon - predlog 3 (crna, sredinska)", a, b)

def inner(svg, n):
    body = svg[svg.index("</defs>") + 7: svg.rindex("</svg>")]
    ids = set(re.findall(r'id="([^"]+)"', body)) - {"glow", "fadeW"}
    for k in sorted(ids, key=len, reverse=True):
        body = body.replace(f'id="{k}"', f'id="P{n}-{k}"').replace(f"url(#{k})", f"url(#P{n}-{k})")
    return body

GX, TOP = 20, 14
TW, TH = 3 * W + 2 * GX, TOP + 2 * H + GAP
parts, labels = [], []
for n, f in enumerate((p1, p2, p3), 1):
    x = (n - 1) * (W + GX)
    parts.append(f'<g id="Predlog-{n}" transform="translate({x} {TOP})">{inner(f(), n)}</g>')
    labels.append(text(f"PREDLOG {n}", "SemiBold", 3.2, x, 8, "#8b8d90", track=0.2, cid=f"Oznaka-{n}")[0])
defs = ('<defs><radialGradient id="glow"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="fadeW" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient></defs>')
out = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
       f'width="{TW}mm" height="{TH}mm" viewBox="0 0 {TW} {TH}"><title>Plesko kuponi 210x99 mm - 3 predlogi</title>{defs}'
       f'<g id="Oznake">{"".join(labels)}</g>{"".join(parts)}</svg>')
(HERE / "plesko-kuponi.svg").write_text(out, encoding="utf-8")
print("ok", len(out) // 1024, "KB")
