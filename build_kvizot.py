#!/usr/bin/env python3
"""Letak DON KVIZOT ponudba, A5 pokonci (148 × 210 mm), 2 strani, pravi koti.

Uporaba: python3 build_kvizot.py <Logo_odiseja.svg> <assets/don_kvizot_logo.json> [izhod.svg]
"""
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import build_letaki as bl
from build_letaki import NAVY, NBSP, TEAL, WHITE, GREEN, text

MM = 72 / 25.4
W, H = round(148 * MM, 2), round(210 * MM, 2)  # 419.53 x 595.28 pt
GAP = round(20 * MM, 2)
M = 34.0

ALERGENI = "Alergeni so navedeni v tabeli pri šanku."

OFFER = [  # ime, cena (kot na letaku)
    ("Pizza", f"9,90{NBSP}€"),
    ("Hot dog", f"4,50{NBSP}€"),
    ("Popcorn XL", f"6,50{NBSP}€"),
    ("Nacho 2 omaki", f"6,80{NBSP}€"),
    ("Heineken 4+1", f"18,40{NBSP}€"),
    ("Brezalkoholna pijača", f"20{NBSP}%{NBSP}popusta"),
]


def load_odiseja(path):
    root = ET.parse(path).getroot()
    ns = bl.NS
    vb = [float(v) for v in root.get("viewBox").split()]
    out = []
    for e in root:
        if e.tag.split("}")[1] in ("defs", "style"):
            continue
        for el in e.iter():
            if el.attrib.pop("class", None):
                el.set("fill", TEAL)
        s = ET.tostring(e, encoding="unicode")
        out.append(s.replace(f' xmlns="{ns}"', "").replace("ns0:", ""))
    return "".join(out), vb[2], vb[3]


def load_kvizot(path):
    """Vektorski logotip (assets/don_kvizot_logo.json, izdelan z tools/trace_logo.py)."""
    d = json.loads(Path(path).read_text(encoding="utf8"))
    return d["d"], d["w"], d["h"]


def odiseja(od, x, y, width):
    svg, vw, vh = od
    s = width / vw
    return f'<g id="logotip_odiseja" transform="translate({x:.2f} {y:.2f}) scale({s:.5f})">{svg}</g>', vh * s


def kvizot(kv, x, y, width):
    d, w, h = kv
    s = width / w
    return (f'<path id="logotip_don_kvizot" transform="translate({x:.2f} {y:.2f}) scale({s:.5f})" d="{d}" '
            f'fill="#fafafa" fill-rule="evenodd"/>'), h * s


def frame(x, y, w, h, name):
    gid = "placeholder_slika_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return (f'<g id="{gid}"><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{TEAL}" fill-opacity="0.10" '
            f'stroke="{TEAL}" stroke-opacity="0.6" stroke-width="0.8"/>'
            + text(x + w / 2, y + h / 2 + 3, "slika izdelka", 8.5, 500, WHITE, anchor="middle", op=0.45) + "</g>")


def page_a(od, kv):
    p = [f'<rect id="ozadje" width="{W}" height="{H}" fill="{NAVY}"/>',
         f'<rect id="sij" width="{W}" height="{H}" fill="url(#g_teal)"/>']
    lg, _ = odiseja(od, M, 30, 96)
    p.append(lg)
    kw = 340.0
    k, kh = kvizot(kv, (W - kw) / 2, 175, kw)
    p.append(k)
    y = 175 + kh
    p.append(text(W / 2, y + 58, "ponudba", 36, 700, TEAL, anchor="middle", gid="naslov_ponudba"))
    p.append(f'<line x1="{W / 2 - 40}" y1="{y + 80:.2f}" x2="{W / 2 + 40}" y2="{y + 80:.2f}" stroke="{TEAL}" stroke-width="1"/>')
    p.append(text(W / 2, y + 122, "8. 11. 2026", 24, 600, WHITE, anchor="middle", gid="datum"))
    p.append(text(W / 2, y + 148, "Odiseja", 13, 500, WHITE, anchor="middle", op=0.8, gid="kraj"))
    return "".join(p)


def page_b(od, kv):
    p = [f'<rect id="ozadje" width="{W}" height="{H}" fill="{NAVY}"/>',
         f'<rect id="sij" width="{W}" height="{H}" fill="url(#g_teal)"/>']
    k, kh = kvizot(kv, M, 30, 120)
    p.append(k)
    lg, lh = odiseja(od, W - M - 96, 30 + (kh - 96 * od[2] / od[1]) / 2, 96)
    p.append(lg)
    p.append(f'<line x1="{M}" y1="84" x2="{W - M}" y2="84" stroke="{TEAL}" stroke-opacity="0.5" stroke-width="0.7"/>')
    gap, fw, fh = 14.0, (W - 2 * M - 14.0) / 2, 92.0
    pics, txt = [], []
    for i, (name, price) in enumerate(OFFER):
        r, c = divmod(i, 2)
        x, y = M + c * (fw + gap), 104 + r * 148
        pics.append(frame(x, y, fw, fh, name))
        accent = GREEN if "popusta" in price else TEAL
        txt.append(text(x, y + fh + 20, name, 12.5, 600, WHITE))
        txt.append(text(x, y + fh + 38, price, 13, 700, accent))
    p.append('<g id="slike">' + "".join(pics) + "</g>")
    p.append('<g id="ponudba">' + "".join(txt) + "</g>")
    p.append(f'<g id="podnozje"><line x1="{M}" y1="{H - 46}" x2="{W - M}" y2="{H - 46}" stroke="{WHITE}" stroke-opacity="0.28" stroke-width="0.5"/>'
             + text(M, H - 30, ALERGENI, 6.8, 400, WHITE, op=0.7, gid="alergeni") + "</g>")
    return "".join(p)


def build(od, kv):
    TW = 2 * W + GAP
    defs = (f'<radialGradient id="g_teal" gradientUnits="userSpaceOnUse" cx="{W / 2}" cy="0" r="{H * 0.6:.1f}">'
            f'<stop offset="0" stop-color="{TEAL}" stop-opacity="0.34"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>')
    pages = [f'<g id="stran_kvizot_A">{page_a(od, kv)}</g>',
             f'<g id="stran_kvizot_B" transform="translate({W + GAP:.2f} 0)">{page_b(od, kv)}</g>']
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="{bl.NS}" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {TW:.2f} {H}" width="{TW:.2f}" height="{H}">\n'
            f"<title>Don Kvizot ponudba, A5 (148 × 210 mm)</title>\n<defs>{defs}</defs>\n" + "\n".join(pages) + "\n</svg>")


def main():
    bl.AI_FONTS = True
    od = load_odiseja(sys.argv[1])
    kv = load_kvizot(sys.argv[2])
    out = Path(sys.argv[3] if len(sys.argv) > 3 else "letaki/don_kvizot_a5.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(od, kv), encoding="utf8")
    print(out, f"{out.stat().st_size / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
