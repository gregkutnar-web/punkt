#!/usr/bin/env python3
"""Zimski letaki, 4 osnutki s placeholderji za fotografije (LUNA, MARS 1, MARS 2, Balthazar).

Uporaba: python3 build_osnutki.py <docx> <LOGO_VSI_LOKALI.svg> <mapa_s_fotografijami_1..13.png> [izhod.svg]
Ponovno uporabi branje docx, popravke besedila in logotipe iz build_letaki.py.
"""
import base64
import io
import math
import random
import re
import sys
from pathlib import Path

from PIL import Image

import build_letaki as bl
from build_letaki import BARS, FOOT, GREEN, H, M, NAVY, SLOGAN, TEAL, W, WHITE, esc, flake, place_logo, text

AMBER, CREAM = "#f0a74a", "#f7f5f5"
BLOCK_GAP = 140.0
TOP_PAD = 70.0

# Fotografije (placeholderji) po straneh: letak -> [stran A, stran B]
PHOTOS = {
    "luna": [[11, 8, 1, 10, 13, 9], [4, 6, 7, 12]],
    "mars1": [[8, 11, 2, 12, 13, 9, 10, 5], [4, 6, 7, 1]],
    "mars2": [[3, 9, 10, 13], [5, 13, 9, 10]],
    "balthazar": [[8, 11, 2, 12, 5], [4, 6, 7]],
}
OPTIONS = [("1", "Osnutek 1"), ("2", "Osnutek 2"), ("3a", "Osnutek 3a"), ("3b", "Osnutek 3b")]


# ---- Letaki iz docx --------------------------------------------------------
def build_flyers(bars):
    by = {b["docx"]: bars[b["docx"]] for b in BARS}
    luna, mars, balt = (by["LUNA"], by["MARS"], by["Baltazar"])
    return [
        dict(id="luna", bar=BARS[0], pages=luna["pages"]),
        dict(id="mars1", bar=BARS[1], pages=[{"sections": [mars["pages"][0]["sections"][0]]},
                                              {"sections": [mars["pages"][0]["sections"][1]]}]),
        dict(id="mars2", bar=BARS[1], pages=[{"sections": [mars["pages"][1]["sections"][0]]},
                                              {"sections": [mars["pages"][1]["sections"][1]]}]),
        dict(id="balthazar", bar=BARS[2], pages=balt["pages"]),
    ]


# ---- Fotografije -----------------------------------------------------------
class Photos:
    def __init__(self, folder):
        self.folder, self.cache = Path(folder), {}

    def uri(self, n):
        if n not in self.cache:
            im = Image.open(self.folder / f"{n}.png").convert("RGB")
            im.thumbnail((560, 560), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=72, optimize=True)
            self.cache[n] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        return self.cache[n]


class Ctx:
    """Števec id-jev za clipPath in dostop do fotografij."""

    def __init__(self, photos):
        self.photos, self.n = photos, 0

    def nid(self, p="k"):
        self.n += 1
        return f"{p}{self.n}"


def picture(ctx, n, x, y, w, h, shape="rect", rx=10.0, focus=0.55, stroke=None, gid=None, clip_d=None):
    """Placeholder fotografije v okvirju (clipPath). Slika je kvadratna, pokrije okvir."""
    s = max(w, h)
    ix, iy = x - (s - w) / 2, y - (s - h) * focus
    cid = ctx.nid("klip")
    if clip_d:
        shape_svg = f'<path d="{clip_d}"/>'
    elif shape == "circle":
        shape_svg = f'<circle cx="{x + w / 2:.2f}" cy="{y + h / 2:.2f}" r="{w / 2:.2f}"/>'
    else:
        shape_svg = f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}"/>'
    frame = ""
    if stroke:
        if clip_d:
            frame = f'<path d="{clip_d}" fill="none" stroke="{stroke}" stroke-width="1" stroke-opacity="0.85"/>'
        elif shape == "circle":
            frame = (f'<circle cx="{x + w / 2:.2f}" cy="{y + h / 2:.2f}" r="{w / 2:.2f}" fill="none" '
                     f'stroke="{stroke}" stroke-width="1.4"/>')
        else:
            frame = (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="none" '
                     f'stroke="{stroke}" stroke-width="1" stroke-opacity="0.85"/>')
    gid = gid or ctx.nid("placeholder_slika_")
    return (f'<g id="{gid}"><clipPath id="{cid}">{shape_svg}</clipPath>'
            f'<image clip-path="url(#{cid})" x="{ix:.2f}" y="{iy:.2f}" width="{s:.2f}" height="{s:.2f}" '
            f'preserveAspectRatio="xMidYMid slice" xlink:href="{ctx.photos.uri(n)}"/>{frame}</g>')


# ---- Dekor -----------------------------------------------------------------
def sparkle(cx, cy, r, color, op):
    d = (f"M{cx:.1f} {cy - r:.1f}Q{cx:.1f} {cy:.1f} {cx + r:.1f} {cy:.1f}Q{cx:.1f} {cy:.1f} {cx:.1f} {cy + r:.1f}"
         f"Q{cx:.1f} {cy:.1f} {cx - r:.1f} {cy:.1f}Q{cx:.1f} {cy:.1f} {cx:.1f} {cy - r:.1f}Z")
    return f'<path d="{d}" fill="{color}" fill-opacity="{op}"/>'


def decor(seed, avoid_top):
    """Topel zimski dekor; avoid_top = višina glave, kjer ne rišemo drobnih elementov čez fotografije."""
    rnd = random.Random(seed)
    out = [f'<rect id="sij_zgoraj" width="{W}" height="{H}" fill="url(#g_teal)"/>',
           f'<rect id="sij_spodaj" width="{W}" height="{H}" fill="url(#g_amber)"/>']
    fl = []
    big = [(W - 22, 60, 62, TEAL, 0.28), (-6, H * 0.52, 44, WHITE, 0.13), (W + 6, H * 0.78, 40, AMBER, 0.2)]
    for x, y, r, c, o in big:
        fl.append(flake(x, y, r, rnd.uniform(0, 60), c, o, 0.9))
    for _ in range(10):
        x = rnd.choice((rnd.uniform(6, M - 10), rnd.uniform(W - M + 10, W - 6)))
        y = rnd.uniform(avoid_top, H - 80)
        fl.append(flake(x, y, rnd.uniform(4, 9), rnd.uniform(0, 60), WHITE, rnd.choice((0.2, 0.3, 0.42)), 0.6))
    out.append('<g id="snezinke">' + "".join(fl) + "</g>")
    bok = []
    for _ in range(11):
        x = rnd.uniform(8, W - 8)
        y = rnd.choice((rnd.uniform(avoid_top, H - 70), rnd.uniform(H - 150, H - 66)))
        if M - 6 < x < W - M + 6 and y < H - 60:
            x = rnd.choice((rnd.uniform(6, M - 12), rnd.uniform(W - M + 12, W - 6)))
        bok.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice((2.5, 4, 6, 9))}" fill="{AMBER}" '
                   f'fill-opacity="{rnd.choice((0.14, 0.22, 0.32))}"/>')
    out.append('<g id="lucke">' + "".join(bok) + "</g>")
    st = []
    for _ in range(7):
        x = rnd.choice((rnd.uniform(10, M - 14), rnd.uniform(W - M + 16, W - 10)))
        st.append(sparkle(x, rnd.uniform(avoid_top, H - 100), rnd.choice((4, 5.5, 7)), AMBER, rnd.choice((0.55, 0.8))))
    out.append('<g id="zvezdice">' + "".join(st) + "</g>")
    y0 = H - 80
    d1 = (f"M0 {y0 + 8}C{W * .2:.1f} {y0 - 8} {W * .38:.1f} {y0 + 14} {W * .6:.1f} {y0 + 2}"
          f"S{W * .92:.1f} {y0 - 10} {W} {y0 + 4}V{H}H0Z")
    out.append(f'<path id="zamet" d="{d1}" fill="{CREAM}" fill-opacity="0.07"/>')
    return "".join(out)


# ---- Glava, značka, podnožje -----------------------------------------------
def badge(cx, cy, w=196.0, h=23.0, fill=AMBER, ink=NAVY, label="Posebna zimska ponudba", gid="znacka"):
    out = [f'<g id="{gid}">',
           f'<rect x="{cx - w / 2:.2f}" y="{cy - h / 2:.2f}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>',
           sparkle(cx - w / 2 + 14, cy, 4.2, ink, 0.9), sparkle(cx + w / 2 - 14, cy, 4.2, ink, 0.9),
           text(cx, cy + 3.8, label, 10.6, 700, ink, anchor="middle", ls=0.5), "</g>"]
    return "".join(out)


def logo_svg(bar, logo, cx, top, width, plate_r=None):
    """Logotip; Balthazar na svetli plošči. Vrne (svg, spodnji rob)."""
    if bar["logo"] == "BALTHAZAR":
        r = plate_r or width * 0.36
        lw = r * 1.58
        svg, _ = place_logo(logo, cx, top + r - (609 * lw / 879) / 2, lw)
        return (f'<circle id="luna_plosca" cx="{cx:.2f}" cy="{top + r:.2f}" r="{r:.2f}" fill="{CREAM}"/>' + svg,
                top + 2 * r)
    svg, h = place_logo(logo, cx, top, width)
    return svg, top + h


def footer():
    fy = H - 62
    return (f'<g id="podnozje"><line x1="{M}" y1="{fy}" x2="{W - M}" y2="{fy}" stroke="{WHITE}" '
            f'stroke-opacity="0.28" stroke-width="0.5"/>'
            + text(M, fy + 15, SLOGAN, 8.5, 600, AMBER, ls=0.4, gid="slogan")
            + text(M, fy + 30, FOOT[0], 6.3, 400, op=0.7, gid="podnozje_1")
            + text(M, fy + 38.5, FOOT[1], 6.3, 400, op=0.7, gid="podnozje_2") + "</g>")


# ---- Vsebina ---------------------------------------------------------------
def body(bar, secs, top, bot, head_h, head_fn, pmax=34.0):
    n_items = sum(len(s["items"]) for s in secs)
    n_heads = sum(1 for s in secs if s["title"])
    n_gaps = sum(1 for s in secs for it in s["items"] if it["gap"])
    sec_gap, item_gap = 18.0, 12.0
    fixed = head_h * n_heads + sec_gap * (len(secs) - 1) + item_gap * n_gaps
    pitch = max(18.0, min(pmax, (bot - top - fixed) / n_items))
    ns, ds = (9.6, 7.0) if pitch < 24 else (10.5, 7.8)
    y, out = top, []
    for si, s in enumerate(secs):
        if si:
            y += sec_gap
        if s["title"]:
            out.append(head_fn(s, y, si))
            y += head_h
        for it in s["items"]:
            if it["gap"]:
                y += item_gap
            out.append(text(M, y + ns, it["name_fixed"], ns, 600))
            out.append(text(W - M, y + ns, it["price_txt"], ns, 700, AMBER, anchor="end"))
            if it["desc_fixed"]:
                out.append(text(M, y + ns + ds + 3.2, it["desc_fixed"], ds, 400, op=0.68))
            y += pitch
    return "".join(out), y


def title_plain(bar):
    def fn(s, y, si):
        gid = "naslov_" + re.sub(r"[^a-z]", "", s["title"].lower())
        return (text(M, y + 13, s["title"], 14, 700, bar["head"], gid=gid)
                + f'<line x1="{M}" y1="{y + 21:.2f}" x2="{W - M}" y2="{y + 21:.2f}" stroke="{AMBER}" '
                  f'stroke-opacity="0.6" stroke-width="0.7"/>')
    return fn


# ---- Postavitve osnutkov ---------------------------------------------------
def page(ctx, opt, flyer, pi, seed):
    bar, pg = flyer["bar"], flyer["pages"][pi]
    logos = ctx.logos[bar["logo"]]
    ph = PHOTOS[flyer["id"]][pi]
    secs = pg["sections"]
    parts = [f'<rect id="ozadje" width="{W}" height="{H}" fill="{NAVY}"/>']
    zone_bot = H - 62 - 14

    def pick(k, n=1):
        return [ph[(k + i) % len(ph)] for i in range(n)]

    if opt == "1":  # slike v nogi
        parts.append(f'<g id="zimski_dekor">{decor(seed, 130)}</g>')
        lg, lb = logo_svg(bar, logos, W / 2, 30, 100, 40)
        parts.append(lg)
        parts.append(badge(W / 2, lb + 20))
        strip_h, gap = 92.0, 9.0
        strip_y = zone_bot - strip_h + 2
        fw = (W - 2 * M - 2 * gap) / 3
        top = lb + 20 + 12 + 16
        content, _ = body(bar, secs, top, strip_y - 14, 28, title_plain(bar))
        parts.append(f'<g id="vsebina">{content}</g>')
        pics = [picture(ctx, p, M + i * (fw + gap), strip_y, fw, strip_h, rx=12, stroke=AMBER)
                for i, p in enumerate(pick(0, 3))]
        parts.append('<g id="slike_noga">' + "".join(pics) + "</g>")
    elif opt == "2":  # slike pri naslovih
        parts.append(f'<g id="zimski_dekor">{decor(seed, 130)}</g>')
        lg, lb = logo_svg(bar, logos, W / 2, 30, 100, 40)
        parts.append(lg)
        parts.append(badge(W / 2, lb + 20))
        pics = []

        def head(s, y, si):
            d, rr = 56.0, 28.0
            cx2 = W - M - rr
            pa = pick(2 * si, 2)
            for k, p in enumerate(pa):
                pics.append(picture(ctx, p, cx2 - k * 40 - rr, y + 2, d, d, shape="circle", stroke=AMBER))
            gid = "naslov_" + re.sub(r"[^a-z]", "", s["title"].lower())
            return (text(M, y + 28, s["title"], 15, 700, bar["head"], gid=gid)
                    + f'<line x1="{M}" y1="{y + 64:.2f}" x2="{W - M}" y2="{y + 64:.2f}" stroke="{AMBER}" '
                      f'stroke-opacity="0.6" stroke-width="0.7"/>')

        top = lb + 20 + 12 + 14
        content, _ = body(bar, secs, top, zone_bot, 72, head)
        parts.append(f'<g id="vsebina">{content}</g>')
        parts.append('<g id="slike_naslovi">' + "".join(pics) + "</g>")
    elif opt == "3a":  # velika fotografija v glavi
        parts.append(f'<g id="zimski_dekor">{decor(seed, 215)}</g>')
        hh = 188.0
        r = 26.0
        clip = f"M0 0H{W}V{hh - r}Q{W} {hh} {W - r} {hh}H{r}Q0 {hh} 0 {hh - r}Z"
        parts.append(picture(ctx, ph[0], 0, 0, W, hh, focus=0.42, clip_d=clip, stroke=None, gid="placeholder_slika_hero"))
        parts.append(f'<rect id="hero_zatemnitev" width="{W}" height="64" fill="url(#g_hero)"/>')
        lg, lb = logo_svg(bar, logos, M + 48, 22, 92, 44)
        parts.append(lg)
        parts.append(badge(W / 2, hh, w=206, h=25))
        top = hh + 25 + 22
        content, _ = body(bar, secs, top, zone_bot, 28, title_plain(bar))
        parts.append(f'<g id="vsebina">{content}</g>')
    else:  # 3b: polaroidi
        parts.append(f'<g id="zimski_dekor">{decor(seed, 230)}</g>')
        lg, lb = logo_svg(bar, logos, M + 50, 30, 100, 46)
        parts.append(lg)
        words = ["Posebna", "zimska", "ponudba"]
        ty = lb + 34
        parts.append('<g id="zimska_ponudba_napis">'
                     + "".join(text(M, ty + i * 24, w_, 23, 700, AMBER if i == 1 else WHITE) for i, w_ in enumerate(words))
                     + sparkle(M + 108, ty - 12, 6, AMBER, 0.9) + "</g>")
        pol = []
        for k, (px, py, rot) in enumerate(((W - M - 176, 38, -7), (W - M - 108, 70, 6))):
            pw, pht = 112.0, 134.0
            inner = picture(ctx, pick(k)[0], px + 7, py + 7, pw - 14, pht - 36, rx=2, focus=0.5)
            pol.append(f'<g id="polaroid_{k + 1}" transform="rotate({rot} {px + pw / 2:.1f} {py + pht / 2:.1f})">'
                       f'<rect x="{px}" y="{py}" width="{pw}" height="{pht}" rx="3" fill="{CREAM}"/>{inner}</g>')
        parts.append('<g id="slike_polaroidi">' + "".join(pol) + "</g>")
        top = max(ty + 3 * 24 + 6, 38 + 134 + 40) + 8
        content, _ = body(bar, secs, top, zone_bot, 28, title_plain(bar))
        parts.append(f'<g id="vsebina">{content}</g>')
    parts.append(footer())
    return "".join(parts)


def build(bars, logos, photos_dir):
    ctx = Ctx(Photos(photos_dir))
    ctx.logos = logos
    flyers = build_flyers(bars)
    BW = 2 * W + bl.GAP
    TW = len(OPTIONS) * BW + (len(OPTIONS) - 1) * BLOCK_GAP
    TH = TOP_PAD + 4 * H + 3 * bl.GAP
    defs = [
        f'<radialGradient id="g_teal" gradientUnits="userSpaceOnUse" cx="{W / 2}" cy="0" r="{H * 0.6:.1f}">'
        f'<stop offset="0" stop-color="{TEAL}" stop-opacity="0.34"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="g_amber" gradientUnits="userSpaceOnUse" cx="{W / 2}" cy="{H}" r="{H * 0.55:.1f}">'
        f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.22"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="g_hero" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="64">'
        f'<stop offset="0" stop-color="{NAVY}" stop-opacity="0.65"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>',
    ]
    body_svg, seed = [], 100
    for oi, (opt, label) in enumerate(OPTIONS):
        ox0 = oi * (BW + BLOCK_GAP)
        body_svg.append(text(ox0, 40, label, 26, 700, "#222625", gid=f"oznaka_{opt}"))
        for ri, fl in enumerate(flyers):
            for pi, side in enumerate("AB"):
                seed += 1
                ox, oy = ox0 + pi * (W + bl.GAP), TOP_PAD + ri * (H + bl.GAP)
                body_svg.append(f'<g id="osnutek{opt}_{fl["id"]}_{side}" transform="translate({ox:.2f} {oy:.2f})">'
                                + page(ctx, opt, fl, pi, seed) + "</g>")
    head = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="{bl.NS}" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {TW:.2f} {TH:.2f}" width="{TW:.2f}" height="{TH:.2f}">\n'
            "<title>Zimski letaki Odiseja: osnutki 1, 2, 3a, 3b (148 × 220 mm)</title>\n"
            "<defs>" + "".join(defs) + "</defs>\n")
    return head + "\n".join(body_svg) + "\n</svg>", ctx


def main():
    docx, logo_svg_path, photos_dir = sys.argv[1:4]
    out = Path(sys.argv[4] if len(sys.argv) > 4 else "letaki/zimski_letaki_osnutki.svg")
    bars = bl.read_docx(docx)
    bl.clean(bars)
    logos = bl.load_logos(logo_svg_path)
    svg, ctx = build(bars, logos, photos_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf8")
    print(out, f"{len(svg) / 1e6:.1f} MB", ctx.n, "elementov")


if __name__ == "__main__":
    main()
