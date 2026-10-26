#!/usr/bin/env python3
"""Sestavi punkt-animacija.svg: voziček pripelje, izdelki padejo v U, postanejo črke,
pika pade v košarico (= nakup). Vir logotipa: assets/logo-punkt.svg."""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "assets/logo-punkt.svg").read_text()
paths = re.findall(r'<path (?:class="(\w+)" )?d="([^"]+)"', src)
black = [d for c, d in paths if c in ("", "st1") and not d.startswith("M153.57")]
teal = [d for c, d in paths if c == "st0"]
U = next(d for c, d in paths if d.startswith("M153.57"))
P, K, T, N = black[0], black[1], black[2], black[3]
PRAVI = black[4:9]

D = 12.4                       # trajanje zanke (s)
TEAL, INK, TINT = "#00868f", "#000", "#8fd0d4"
CX, CY = 121.83, 74.89         # pika
FLOOR = 98.9                   # dno košarice
EASE = "cubic-bezier(.2,.8,.2,1)"
css, n = [], 0

def kf(name, stops, base=None):
    """stops: (čas s, {lastnosti}, easing do naslednje točke)"""
    first = stops[0][1]
    out = [f"@keyframes {name}{{"]
    allst = list(stops) + [(D - .01, stops[-1][1], None), (D, first, None)]
    for t, props, ease in allst:
        body = ";".join(f"{k}:{v}" for k, v in props.items())
        if ease: body += f";animation-timing-function:{ease}"
        out.append(f"{t / D * 100:.3f}%{{{body}}}")
    out.append("}")
    css.append("".join(out))
    return name

def anim(cls, name, extra=""):
    css.append(f".{cls}{{animation:{name} {D}s linear infinite;{extra}}}")

fill = "transform-box:fill-box;transform-origin:center"
def tr(x=0, y=0, r=0, sx=1, sy=1, o=None):
    d = {"transform": f"translate({x}px,{y}px) rotate({r}deg) scale({sx},{sy})"}
    if o is not None: d["opacity"] = o
    return d

# ---------- voziček ----------
kf("cart", [(0, tr(-340), None), (0.2, tr(-340), "cubic-bezier(.15,.7,.3,1)"),
            (1.5, tr(7), "ease-in-out"), (1.85, tr(0), None)])
anim("cart", "cart")
kf("spin", [(0.2, tr(r=0), "cubic-bezier(.15,.7,.3,1)"), (1.8, tr(r=900), None)])
anim("spin", "spin", fill)
kf("streak", [(0, {"opacity": 0}, "ease-out"), (0.4, {"opacity": .9}, "linear"),
              (1.2, {"opacity": .9}, "ease-in"), (1.8, {"opacity": 0}, None)])
anim("streak", "streak")
kf("gear", [(0, {"opacity": 1, "transform": "translateY(0px)"}, "linear"),
            (6.5, {"opacity": 1, "transform": "translateY(0px)"}, EASE),
            (7.3, {"opacity": 0, "transform": "translateY(10px)"}, None)])
anim("gear", "gear")
kf("handle", [(0, {"opacity": 1, "transform": "translateX(0px)"}, "linear"),
              (3.0, {"opacity": 1, "transform": "translateX(0px)"}, EASE),
              (3.7, {"opacity": 0, "transform": "translateX(-14px)"}, None)])
anim("handle", "handle")

# ---------- izdelki -> črke ----------
items = [  # (id, risba, ciljni x črke, pot črke, ime razreda)
 ("box", f'<rect x="-11" y="-10" width="22" height="20" rx="3" fill="{TEAL}"/>'
         f'<rect x="-2.2" y="-10" width="4.4" height="20" fill="#fff" opacity=".85"/>'
         f'<rect x="-11" y="-3" width="22" height="3" fill="#000" opacity=".12"/>', 36, P),
 ("bag", f'<path d="M-9,-6H9L10.5,9a3,3 0 0 1-3,3h-15a3,3 0 0 1-3-3Z" fill="{INK}"/>'
         f'<path d="M-4,-6v-3a4,4 0 0 1 8,0v3" fill="none" stroke="{INK}" stroke-width="2"/>'
         f'<circle cx="-4" cy="-2" r="1.3" fill="#fff"/><circle cx="4" cy="-2" r="1.3" fill="#fff"/>', 196, N),
 ("cup", f'<path d="M-8,-8H8L6.2,9a3,3 0 0 1-3,3h-6.4a3,3 0 0 1-3-3Z" fill="{TEAL}"/>'
         f'<path d="M7.6,-4h2.6a3.2,3.2 0 0 1 0,7H6.6" fill="none" stroke="{TEAL}" stroke-width="2"/>'
         f'<rect x="-8" y="-8" width="16" height="3" rx="1.5" fill="{TINT}"/>', 273, K),
 ("tag", f'<path d="M-10,-10H0L10,0L0,10L-10,0Z" fill="{INK}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
         f'<circle cx="-4.6" cy="-4.6" r="2" fill="#fff"/>', 356, T),
]
LETTER_Y = 80
S0, STEP = 1.9, 0.6
item_svg, letter_svg, flash_svg = [], [], []
for i, (name, art, tx, lpath) in enumerate(items):
    s = S0 + STEP * i
    land, lift, arrive = s + .5, s + .95, s + 1.8
    kf(f"ix_{name}", [(0, {"transform": f"translateX({CX}px)"}, None), (lift, {"transform": f"translateX({CX}px)"}, "cubic-bezier(.45,0,.55,1)"),
                      (arrive, {"transform": f"translateX({tx}px)"}, None)])
    kf(f"iy_{name}", [(0, {"transform": "translateY(-125px)"}, None), (s, {"transform": "translateY(-125px)"}, "cubic-bezier(.55,0,1,.6)"),
                      (land, {"transform": f"translateY({FLOOR-12}px)"}, "ease-out"),
                      (lift, {"transform": f"translateY({FLOOR-12}px)"}, "cubic-bezier(.2,.7,.4,1)"),
                      (lift + .42, {"transform": "translateY(-28px)"}, "cubic-bezier(.6,0,.9,.5)"),
                      (arrive, {"transform": f"translateY({LETTER_Y}px)"}, None)])
    kf(f"ir_{name}", [(0, tr(o=0, r=-40), None), (s, tr(o=0, r=-40), "linear"), (s + .02, tr(o=1, r=-40), "cubic-bezier(.4,0,.8,.6)"),
                      (land, tr(r=0), "ease-out"), (land + .08, tr(sx=1.28, sy=.72), "ease-out"),
                      (land + .24, tr(sx=.94, sy=1.08), "ease-out"), (land + .36, tr(), "linear"),
                      (lift, tr(), "cubic-bezier(.3,.6,.4,1)"),
                      (arrive - .1, tr(r=330, sx=2.5, sy=2.5, o=1), "ease-out"),
                      (arrive + .12, tr(r=360, sx=2.9, sy=2.9, o=0), None)])
    anim(f"ix_{name}", f"ix_{name}"); anim(f"iy_{name}", f"iy_{name}")
    anim(f"ir_{name}", f"ir_{name}", "transform-box:fill-box;transform-origin:50% 100%")
    item_svg.append(f'<g class="item ix_{name}"><g class="iy_{name}"><g class="ir_{name}">{art}</g></g></g>')
    # črka
    kf(f"l_{name}", [(0, tr(o=0, sx=.7, sy=.7), None), (arrive - .1, tr(o=0, sx=.7, sy=.7), "cubic-bezier(.3,1.6,.5,1)"),
                     (arrive + .3, tr(o=1, sx=1, sy=1), None), (D - .3, tr(o=1), None)])
    anim(f"l_{name}", f"l_{name}", fill + ";opacity:1")
    letter_svg.append(f'<path class="l_{name}" d="{lpath}"/>')
    # bliskavica ob nastanku črke
    kf(f"f_{name}", [(0, {"opacity": 0, "transform": "scale(.2)"}, None), (arrive - .05, {"opacity": 0, "transform": "scale(.2)"}, "ease-out"),
                     (arrive + .05, {"opacity": .3, "transform": "scale(.5)"}, "ease-out"), (arrive + .7, {"opacity": 0, "transform": "scale(1.6)"}, None)])
    anim(f"f_{name}", f"f_{name}", fill)
    flash_svg.append(f'<circle class="f_{name}" cx="{tx}" cy="{LETTER_Y}" r="38" fill="{TEAL}" opacity="0"/>')

# ---------- pika = nakup ----------
DS = S0 + STEP * 3 + 2.2          # začetek padca pike
DL = DS + .5
kf("dot", [(0, tr(y=-200, o=0), None), (DS, tr(y=-200, o=0), "linear"), (DS + .01, tr(y=-200, o=1), "cubic-bezier(.55,0,1,.6)"),
           (DL, tr(y=FLOOR - 11.18 - CY), "ease-out"), (DL + .08, tr(y=FLOOR - 11.18 - CY, sx=1.18, sy=.82), "ease-out"),
           (DL + .3, tr(y=-5), "ease-in-out"), (DL + .6, tr(), "linear"), (D - .3, tr(), None)])
anim("dot", "dot", "transform-box:fill-box;transform-origin:50% 100%")
ring = lambda t: [(t, {"opacity": .75, "transform": "scale(1)"}, "ease-out"), (t + .9, {"opacity": 0, "transform": "scale(3.4)"}, None)]
cap_t = DL + 2.4
kf("ring", [(0, {"opacity": 0, "transform": "scale(1)"}, None)] + [(DL - .01, {"opacity": 0, "transform": "scale(1)"}, None)] + [x for p in (ring(DL), ring(cap_t + .2)) for x in p] + [(D - .2, {"opacity": 0}, None)])
css[-1] = css[-1]  # (zadnji ključ je že pokrit)
anim("ring", "ring", fill)
kf("glow", [(0, {"opacity": 0, "transform": "scale(.6)"}, None), (DL, {"opacity": 0, "transform": "scale(.6)"}, EASE),
            (DL + 1.2, {"opacity": 1, "transform": "scale(1)"}, None)])
anim("glow", "glow", fill)

# ---------- napisi ----------
def rise(name, t):
    kf(name, [(0, {"opacity": 0, "transform": "translateY(10px)"}, None), (t, {"opacity": 0, "transform": "translateY(10px)"}, EASE),
              (t + .9, {"opacity": 1, "transform": "translateY(0px)"}, None)])
    anim(name, name)
rise("pravi", DL + .9); rise("tagl", DL + 1.4); rise("cap", cap_t)
kf("all", [(0, {"opacity": 0}, "ease-out"), (.25, {"opacity": 1}, "linear"), (D - 1.1, {"opacity": 1}, "ease-in"), (D - .45, {"opacity": 0}, None)])
anim("all", "all")

fallback = """@media (prefers-reduced-motion:reduce){*{animation:none!important}.item,.streak,.ring,.gear,.handle,[class^=f_]{opacity:0}}"""
css.insert(0, fallback)
css.insert(0, "svg{font-family:'Helvetica Neue',Inter,Arial,sans-serif}")

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-130 -110 654.69 368.26" role="img" aria-label="Animacija logotipa Punkt: pika v črki U je nakup">
<style>{"".join(css)}</style>
<defs><radialGradient id="g"><stop offset="0" stop-color="{TEAL}" stop-opacity=".16"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient></defs>
<rect x="-130" y="-110" width="654.69" height="368.26" rx="22" fill="#f4f8f8"/>
<g class="all">
<circle class="glow" cx="{CX}" cy="{CY}" r="170" fill="url(#g)"/>
<g class="pravi" fill="{INK}">{"".join(f'<path d="{d}"/>' for d in PRAVI)}</g>
<g class="tagl" fill="{TEAL}">{"".join(f'<path d="{d}"/>' for d in teal)}</g>
<g fill="{INK}">{"".join(letter_svg)}</g>
{"".join(flash_svg)}
<g class="cart">
  <g class="streak" stroke="{TINT}" stroke-width="3" stroke-linecap="round"><path d="M70,84h-34M62,96h-44M74,108h-26"/></g>
  <g class="handle" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M88,58H78V34H62"/></g>
  <g class="gear">
    <path d="M102,108v8M141,108v8" stroke="{INK}" stroke-width="4"/>
    <g class="spin"><circle cx="102" cy="122" r="7" fill="{INK}"/><path d="M102,116v12M96,122h12" stroke="#fff" stroke-width="1.8"/></g>
    <g class="spin"><circle cx="141" cy="122" r="7" fill="{INK}"/><path d="M141,116v12M135,122h12" stroke="#fff" stroke-width="1.8"/></g>
  </g>
  <path d="{U}" fill="{INK}"/>
</g>
{"".join(item_svg)}
<circle class="ring" cx="{CX}" cy="{CY}" r="11.18" fill="none" stroke="{TEAL}" stroke-width="2.5"/>
<circle class="dot" cx="{CX}" cy="{CY}" r="11.18" fill="{TEAL}"/>
<text class="cap" x="197.3" y="196" text-anchor="middle" font-size="15" letter-spacing=".6" fill="{TEAL}">Pika v črki U je nakup.</text>
</g>
</svg>'''
(root / "punkt-animacija.svg").write_text(svg)
print(len(svg))
