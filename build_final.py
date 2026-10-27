#!/usr/bin/env python3
"""Končni zimski letaki (osnutek 3a), 140 × 260 mm, vse strani v eni SVG.

Uporaba: python3 build_final.py <docx> <LOGO_VSI_LOKALI.svg> <mapa_s_fotografijami_1..13.png> [izhod.svg]
Vsaka stran je skupina `stran_<letak>_<A|B>` z ozadjem `ozadje`; artboarde ustvari artboards_3a.jsx.
"""
import re
import sys
from pathlib import Path

import build_letaki as bl
import build_osnutki as bo
from build_letaki import M, NAVY, TEAL, WHITE, place_logo, text

MM = 72 / 25.4
W, H = round(140 * MM, 2), round(260 * MM, 2)  # 396.85 x 737.01 pt
GAP = round(20 * MM, 2)
AMBER = bo.AMBER
HERO_H, HERO_R = 225.0, 26.0
LOGO_SCALE = 0.8
bo.W, bo.H = W, H  # footer() in body() bereta mere strani iz modula build_osnutki


def badge(cx, cy, w=206.0, h=25.0):
    return (f'<g id="znacka"><rect x="{cx - w / 2:.2f}" y="{cy - h / 2:.2f}" width="{w}" height="{h}" rx="{h / 2}" fill="{AMBER}"/>'
            + text(cx, cy + 3.8, "Posebna zimska ponudba", 10.6, 700, NAVY, anchor="middle", ls=0.5) + "</g>")


def title(s, y, si):
    gid = "naslov_" + re.sub(r"[^a-z]", "", s["title"].lower())
    return (text(M, y + 13, s["title"], 14, 700, AMBER, gid=gid)
            + f'<line x1="{M}" y1="{y + 21:.2f}" x2="{W - M}" y2="{y + 21:.2f}" stroke="{AMBER}" '
              f'stroke-opacity="0.6" stroke-width="0.7"/>')


def page(ctx, flyer, pi):
    bar, secs = flyer["bar"], flyer["pages"][pi]["sections"]
    logo = ctx.logos[bar["logo"]]
    hero = bo.PHOTOS[flyer["id"]][pi][0]
    r = HERO_R
    clip = f"M0 0H{W}V{HERO_H - r}Q{W} {HERO_H} {W - r} {HERO_H}H{r}Q0 {HERO_H} 0 {HERO_H - r}Z"
    parts = [f'<rect id="ozadje" width="{W}" height="{H}" fill="{NAVY}"/>',
             f'<rect id="sij_zgoraj" width="{W}" height="{H}" fill="url(#g_teal)"/>',
             f'<rect id="sij_spodaj" width="{W}" height="{H}" fill="url(#g_amber)"/>',
             bo.picture(ctx, hero, 0, 0, W, HERO_H, focus=0.42, clip_d=clip, gid="placeholder_slika_hero"),
             f'<rect id="hero_zatemnitev" width="{W}" height="80" fill="url(#g_hero)"/>']
    # logotip 80 %, sidran v zgornjem levem kotu (levi rob besedila, 22 pt od vrha)
    if bar["logo"] == "BALTHAZAR":
        pr = 44 * LOGO_SCALE
        lg, _ = bo.logo_svg(bar, logo, M + pr, 22, 0, pr)
    else:
        lw = 92 * LOGO_SCALE
        lg, _ = bo.logo_svg(bar, logo, M + lw / 2, 22, lw)
    parts.append(lg)
    parts.append(badge(W / 2, HERO_H))
    top = HERO_H + 25 + 26
    content, _ = bo.body(bar, secs, top, H - 62 - 14, 28, title, pmax=44.0)
    parts.append(f'<g id="vsebina">{content}</g>')
    parts.append(bo.footer())
    return "".join(parts)


def build(bars, logos, photos_dir):
    ctx = bo.Ctx(bo.Photos(photos_dir))
    ctx.logos = logos
    flyers = bo.build_flyers(bars)
    TW, TH = 2 * W + GAP, 4 * H + 3 * GAP
    defs = (f'<radialGradient id="g_teal" gradientUnits="userSpaceOnUse" cx="{W / 2}" cy="0" r="{H * 0.6:.1f}">'
            f'<stop offset="0" stop-color="{TEAL}" stop-opacity="0.34"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="g_amber" gradientUnits="userSpaceOnUse" cx="{W / 2}" cy="{H}" r="{H * 0.55:.1f}">'
            f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.22"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="g_hero" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="80">'
            f'<stop offset="0" stop-color="{NAVY}" stop-opacity="0.65"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>')
    pages = []
    for ri, fl in enumerate(flyers):
        for pi, side in enumerate("AB"):
            ox, oy = pi * (W + GAP), ri * (H + GAP)
            pages.append(f'<g id="stran_{fl["id"]}_{side}" transform="translate({ox:.2f} {oy:.2f})">{page(ctx, fl, pi)}</g>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="{bl.NS}" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {TW:.2f} {TH:.2f}" width="{TW:.2f}" height="{TH:.2f}">\n'
            "<title>Zimski letaki Odiseja: LUNA, MARS 1, MARS 2, Balthazar (140 × 260 mm)</title>\n"
            f"<defs>{defs}</defs>\n" + "\n".join(pages) + "\n</svg>")


def main():
    docx, logo_svg_path, photos_dir = sys.argv[1:4]
    out = Path(sys.argv[4] if len(sys.argv) > 4 else "letaki/zimski_letaki_3a.svg")
    bars = bl.read_docx(docx)
    bl.clean(bars)
    svg = build(bars, bl.load_logos(logo_svg_path), photos_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf8")
    print(out, f"{len(svg) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
