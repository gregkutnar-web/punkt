#!/usr/bin/env python3
"""Zgradi medijski paket Odiseja (SL + EN): press/press-{sl,en}.html + ZIP s pravili in logotipi.
Vir: assets/odiseja.json (tools/extract_odiseja.py). Gradnja: python3 build_press.py
PNG in PDF izrisuje tools/press_raster.js (Playwright): NODE_PATH=$(npm root -g) je nujen."""
import json, pathlib, re, shutil, subprocess, sys, tempfile, zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent / 'src'))
from press_i18n import T  # noqa: E402
from press_terms import TERMS, terms_html, terms_txt  # noqa: E402

for _lg in T:
    T[_lg].update(TERMS[_lg]['ui'])
    T[_lg]['perm_h'] = TERMS[_lg]['ui']['terms_head']
    T[_lg]['perm'] = TERMS[_lg]['ui']['perm_short']

R = pathlib.Path(__file__).parent
S = R / 'src'
OUT = R / 'press'
D = json.loads((R / 'assets' / 'odiseja.json').read_text())
LET, SUN = D['letters'], D['sun']
HEX = {'t': '#00b1bc', 'k': '#000000', 'w': '#ffffff'}      # ena sama turkizna
BG = {'w': '#ffffff', 'k': '#000000', 't': '#00b1bc'}


def bbox(ds):
    n = []
    for d in ds:
        v = [float(x) for x in re.findall(r'-?\d+\.?\d*', d)]
        n.append((min(v[0::2]), min(v[1::2]), max(v[0::2]), max(v[1::2])))
    return min(b[0] for b in n), min(b[1] for b in n), max(b[2] for b in n), max(b[3] for b in n)


LB, SB, AB = bbox(LET), bbox(SUN), bbox(LET + SUN)
# središče žarkov: zgornji žarek (navpičen) daje x, desni žarek daje y
rays = [bbox([d]) for d in SUN if bbox([d])[2] - bbox([d])[0] < 6 and bbox([d])[3] - bbox([d])[1] < 10]
top = min(rays, key=lambda b: b[1])
M = round(top[3] - top[1], 2)                          # dolžina monolita (višina enega žarka)
CX = (top[0] + top[2]) / 2
right = max((b for b in (bbox([d]) for d in SUN) if b[3] - b[1] < 6), key=lambda b: b[2])
CY = (right[1] + right[3]) / 2
KS = 1.9                                               # povečava znaka v navpični različici
TXW = LB[2] - LB[0]
TXC = (LB[0] + LB[2]) / 2
sun_up = (CY - SB[1]) * KS                             # od središča do vrha znaka
sun_dn = (SB[3] - CY) * KS
GAP = M * KS
TY0 = sun_up + sun_dn + GAP                            # vrh napisa v navpični različici
VH = TY0 + (LB[3] - LB[1])
MV = M * KS

paths = lambda ds, col='currentColor': ''.join(f'<path d="{d}" fill="{col}"/>' for d in ds)
VSUN = f'translate({TXC - KS * CX:.3f} {sun_up - KS * CY:.3f}) scale({KS})'
VTXT = f'translate(0 {TY0 - LB[1]:.3f})'
VX0 = min(LB[0], TXC + KS * (SB[0] - CX))
VX1 = max(LB[2], TXC + KS * (SB[2] - CX))
VIEW = {'h': (AB[0], AB[1], AB[2] - AB[0], AB[3] - AB[1]),
        's': (SB[0], SB[1], SB[2] - SB[0], SB[3] - SB[1]),
        'v': (VX0, 0, VX1 - VX0, VH)}
CAP = LB[3] - LB[1]                                    # višina črke O = varni prostor x (CGP, str. 4)
OB = bbox(LET[:1])
OCX, OCY = (OB[0] + OB[2]) / 2, (OB[1] + OB[3]) / 2


def body(o, col='currentColor'):
    if o == 'h':
        return paths(LET + SUN, col)
    if o == 's':
        return paths(SUN, col)
    return f'<g transform="{VSUN}">{paths(SUN, col)}</g><g transform="{VTXT}">{paths(LET, col)}</g>'


def svg(o, col='currentColor', cls='olg', w=None, extra=''):
    x, y, vw, vh = VIEW[o]
    wh = f' width="{w}" height="{round(w * vh / vw)}"' if w else ''
    return f'<svg class="{cls}" viewBox="{x:.2f} {y:.2f} {vw:.2f} {vh:.2f}"{wh} xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Odiseja" style="aspect-ratio:{vw:.2f}/{vh:.2f}"{extra}>{body(o, col)}</svg>'


def clear_svg(o):
    """Varni prostor po dokumentu Varne_cone_odiseja_logo.ai: x = višina črke O.
    Vodoravno: polje = napis (levo, zgoraj, spodaj) + znak (desno), povsod + x.
    Navpično: polje = celoten logotip + x. Ploščice (črka O) in vodila kot v dokumentu."""
    x, y, vw, vh = VIEW[o]
    m = CAP
    ow = OB[2] - OB[0]
    if o == 'h':
        rx0, ry0, rx1, ry1 = LB[0], LB[1], SB[2], LB[3]
        wy0, wy1 = ry0, ry1                 # napis
        gx = (rx0, rx1)
        gy = (ry0, ry1)
        tl = [(rx0 + ow / 2, ry0 - m / 2, 0), (rx0 + ow / 2, ry1 + m / 2, 0),
              (rx0 - m / 2, ry0 + ow / 2, 90), (rx1 + m / 2, ry0 + m * .1 + ow / 2, 90)]
    else:
        rx0, ry0, rx1, ry1 = x, y, x + vw, y + vh
        wy0, wy1 = TY0, TY0 + CAP
        gx = (LB[0], LB[2])
        gy = (y, wy0, wy1)   # vrh znaka, zgornji in spodnji rob napisa
        tl = [(TXC, ry0 - m / 2, 0), (LB[0] + ow / 2, ry1 + m / 2, 0),
              (rx0 - m / 2, (wy0 + wy1) / 2, 90), (rx1 + m / 2, (wy0 + wy1) / 2, 90)]
    X0, Y0, X1, Y1 = rx0 - m, ry0 - m, rx1 + m, ry1 + m
    k = m / 31.0

    def tile(cx, cy, rot):
        return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({rot}) translate({-OCX:.2f} {-OCY:.2f})">'
                f'<path d="{LET[0]}" fill="#c6e9fa"/></g>')
    tiles = ''.join(tile(*t) for t in tl)
    ys = sorted({Y0, ry0, Y1, ry1} | set(gy))
    xs = sorted({X0, rx0, rx1, X1} | set(gx))
    g = (f'<g stroke="#00adee" stroke-width="{.19 * k:.3f}" stroke-dasharray="{3 * k:.2f} {2.2 * k:.2f}" fill="none">'
         + ''.join(f'<path d="M{X0 - m * .5:.2f} {yy:.2f}H{X1 + m * .5:.2f}"/>' for yy in ys)
         + ''.join(f'<path d="M{xx:.2f} {Y0 - m * .5:.2f}V{Y1 + m * .5:.2f}"/>' for xx in xs) + '</g>')
    pad = m * .7
    cls = 'cv' if o == 'v' else ''
    return (f'<svg class="{cls}" viewBox="{X0 - pad:.2f} {Y0 - pad:.2f} {X1 - X0 + 2 * pad:.2f} {Y1 - Y0 + 2 * pad:.2f}" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'{g}{tiles}<rect x="{X0:.2f}" y="{Y0:.2f}" width="{X1 - X0:.2f}" height="{Y1 - Y0:.2f}" fill="none" stroke="#eb008b" stroke-width="{.55 * k:.3f}"/>'
            f'<g style="color:#808285">{body(o)}</g></svg>')


# --- defs za »use« (prepovedane uporabe, matrika) ---
DEFS = (f'<g id="gH">{paths(LET + SUN)}</g><g id="gL">{paths(LET)}</g><g id="gS">{paths(SUN)}</g>')
BCX, BCY = (AB[0] + AB[2]) / 2, (AB[1] + AB[3]) / 2
LCX, LCY = (LB[0] + LB[2]) / 2, (LB[1] + LB[3]) / 2
SCX, SCY = (SB[0] + SB[2]) / 2, (SB[1] + SB[3]) / 2


def use(i, cx, cy, s, bx, by, pre='', style=''):
    st = f' style="{style}"' if style else ''
    return f'<use href="#{i}" transform="translate({cx} {cy}) {pre} scale({s}) translate({-bx:.2f} {-by:.2f})"{st}/>'


XMARK = ('<svg class="x" viewBox="0 0 30 30"><circle cx="15" cy="15" r="13" fill="#fff" stroke="#d33a2c" stroke-width="2.4"/>'
         '<path d="M9.5 9.5l11 11M20.5 9.5l-11 11" stroke="#d33a2c" stroke-width="2.6" stroke-linecap="round"/></svg>')


def tile(inner, bg='#fff'):
    return f'<div class="v" style="background:{bg}"><svg class="lgm" viewBox="0 0 200 137" width="100%">{inner}</svg>{XMARK}</div>'


def bans(t):
    s = .5
    lw, sw = (LB[2] - LB[0]) * s, (SB[2] - SB[0]) * s
    gap = 8
    x0 = 100 - (lw + gap + sw) / 2
    lt = use('gL', x0 + lw / 2, 68, s, LCX, LCY)
    sx = x0 + lw + gap + sw / 2
    items = []
    items.append(tile(use('gL', 100, 68, .62, LCX, LCY)))                                                           # 1 napis brez znaka
    big = .86
    items.append(tile(use('gL', 21 + lw / 2, 68, s, LCX, LCY) + use('gS', 129 + (SB[2] - SB[0]) * big / 2, 68, big, SCX, SCY)))   # 2 razmerja
    items.append(tile(use('gH', 100, 68, .5, BCX, BCY, 'rotate(-14)')))                                            # 3 nagib
    items.append(tile(lt + use('gS', sx, 68, s, SCX, SCY, 'scale(-1 1)')))                                          # 4 zrcaljenje
    items.append(tile(use('gL', 100, 68, .5, BCX, BCY, '', 'color:#d6409f') + use('gS', 100, 68, .5, BCX, BCY, '', 'color:#f2a007')))  # 5 druge barve
    pw, ph = (AB[2] - AB[0]) * .5, (AB[3] - AB[1]) * .5
    items.append(tile(f'<rect x="{100 - pw / 2 - 12}" y="{68 - ph / 2 - 12}" width="{pw + 24}" height="{ph + 24}" fill="#e6e6e6" stroke="#000" stroke-width="3"/>'
                      + use('gH', 100, 68, .5, BCX, BCY)))                                                           # 6 okvir
    pat = ''.join(use('gS', 26 + c * 37 + (r % 2) * 18, 24 + r * 30, .42, SCX, SCY, '', 'color:#000;opacity:.28') for r in range(4) for c in range(5))
    items.append(tile(pat, '#e9e9e9'))                                                                               # 7 vzorec
    items.append(tile(lt + use('gS', sx, 68, s, SCX, SCY, 'rotate(180)')))                                           # 8 na glavo
    keys = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
    return ''.join(f'<div class="ban">{it}<div class="c">{t[k]}</div></div>' for it, k in zip(items, keys))


def matrix(t):
    hx, bgm = HEX, BG
    valid = {'w': 'tk', 'k': 'tw', 't': 'w'}
    out = ''
    for bg in 'wkt':
        for c in 'tkw':
            ok = c in valid[bg]
            out += (f'<div class="mxc {"ok" if ok else "no"}{" on-t" if bg == "t" else ""}" style="background:{bgm[bg]}" title="{t["m_ok"] if ok else t["m_no"]}">'
                    f'<svg viewBox="{VIEW["h"][0]:.2f} {VIEW["h"][1]:.2f} {VIEW["h"][2]:.2f} {VIEW["h"][3]:.2f}" style="color:{hx[c]}" aria-hidden="true">{body("h")}</svg><u>{"✓" if ok else "✕"}</u></div>')
    return out


def page(t):
    h = (S / 'press.html').read_text()
    import base64
    bg = base64.b64encode((R / 'assets' / 'cgp-background.svg').read_bytes()).decode()
    style = (S / 'landing.css').read_text() + (S / 'press.css').read_text() + '#hero,#prenos{background:url(data:image/svg+xml;base64,' + bg + ') center/cover no-repeat,#071d22}#hero p{color:rgba(255,255,255,.82)}#hero .cue{background:linear-gradient(#fff,transparent)}' + (
             '#prenos{--ink:#fff;--bg:#071d22;--mute:rgba(255,255,255,.86);--line:rgba(255,255,255,.4)}'
             '#prenos .dlist li{color:#fff;background:rgba(7,29,34,.28);border-color:rgba(255,255,255,.45)}'
             '#prenos .btn.big{background:#fff;border-color:#fff;color:#071d22}#prenos .btn.big:hover{background:#fff;color:#071d22;filter:brightness(.94)}'
             '#prenos .perm{border:1px dashed rgba(255,255,255,.55);background:rgba(7,29,34,.22)}#prenos .perm b,#prenos .perm p{color:#fff}')
    rep = {'__TERMS_BODY__': terms_html(t['lang'], 'tm'), '__HERO_LOGO__': svg('h'), '__STYLE__': style, '__JS__': (S / 'press.js').read_text(), '__DEFS__': DEFS,
           '__LG_H__': svg('h'), '__LG_V__': svg('v'), '__LG_S__': svg('s'),
           '__CLEAR_H__': clear_svg('h'), '__CLEAR_V__': clear_svg('v'),
           '__MATRIX__': matrix(t), '__BANS__': bans(t),
           '__DLIST__': ''.join(f'<li>{x}</li>' for x in t['dl_list'])}
    for k, v in rep.items():
        h = h.replace(k, v)
    for k, v in t.items():
        if isinstance(v, str):
            h = h.replace('{{' + k + '}}', v)
    left = re.findall(r'\{\{\w+\}\}', h)
    assert not left, left
    return h


def print_html(t):
    """Pravila uporabe kot PDF (A4 ležeče): gradient naslovnica in zadnja stran, vmes svetle strani z glavo in nogo."""
    import base64
    bg = base64.b64encode((R / 'assets' / 'cgp-background.svg').read_bytes()).decode()
    logos = ''
    for o in 'hvs':
        for c, bgk in (('t', 'w'), ('k', 'w'), ('w', 'k')):
            logos += f'<div class="lc" style="background:{BG[bgk]};color:{HEX[c]}">{svg(o)}</div>'
    css = ('@page{size:A4 landscape;margin:0}*{box-sizing:border-box;margin:0;padding:0}'
           'body{font-family:"Helvetica Neue",Arial,sans-serif;color:#101415;-webkit-print-color-adjust:exact;print-color-adjust:exact}'
           '.pg{width:297mm;height:210mm;page-break-after:always;position:relative;overflow:hidden;background:#fff}'
           '.pg:last-child{page-break-after:auto}'
           '.gr{background:url(data:image/svg+xml;base64,' + bg + ') center/cover no-repeat,#071d22;color:#fff}'
           '.cover{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}'
           '.cover .big svg{display:block;width:210mm;height:auto;color:#f2f2f0}'
           '.cover .sub{margin-top:14mm;font-size:13pt;letter-spacing:.42em;text-transform:uppercase;color:rgba(255,255,255,.9)}'
           '.cover .ttl{margin-top:5mm;font-size:11pt;letter-spacing:.14em;color:rgba(255,255,255,.7)}'
           '.hd{position:absolute;left:18mm;right:18mm;top:12mm;display:flex;justify-content:space-between;align-items:center}'
           '.hd svg{height:7mm;width:auto;color:#00b1bc;display:block}.hd span{font-size:8.5pt;letter-spacing:.2em;text-transform:uppercase;color:#7b8483}'
           '.ft{position:absolute;left:18mm;right:18mm;bottom:10mm;display:flex;justify-content:space-between;font-size:8.5pt;letter-spacing:.14em;color:#9aa3a2;border-top:.25mm solid #e3e6e6;padding-top:3mm}'
           '.body{position:absolute;left:18mm;right:18mm;top:28mm;bottom:20mm}'
           'h2{font-size:17pt;font-weight:800;margin-bottom:6mm;padding-left:4mm;border-left:1.4mm solid #00b1bc;line-height:1.1}'
           'h3{font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:#4f7478;margin:6mm 0 3mm}'
           'p{font-size:10.5pt;line-height:1.5;color:#4a5352;max-width:140mm;margin-top:3mm}'
           '.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}.lc{height:34mm;display:flex;align-items:center;justify-content:center;border:.3mm solid #dfe3e3;border-radius:4mm}'
           '.lc svg{height:58%;width:auto;max-width:80%}.two{display:flex;flex-direction:column;gap:6mm;align-items:center;margin-top:2mm}.two svg{display:block;max-width:100%;height:auto;color:#000;width:118mm}.two svg.cv{width:auto;height:46mm}'
           '.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12mm}.cols>div{min-width:0}.card{background:#f4f7f7;border-radius:5mm;padding:8mm}'
           '.mm{display:flex;align-items:flex-end;gap:14mm;margin-top:6mm;height:46mm}.mm figure{display:flex;flex-direction:column;gap:2mm}'
           '.mm svg{display:block;height:auto;color:#000}.mm .d{height:2.4mm;border-left:.25mm solid #e5007d;border-right:.25mm solid #e5007d;position:relative}'
           '.mm .d::before{content:"";position:absolute;left:0;right:0;top:1.1mm;border-top:.25mm solid #e5007d}'
           '.mm figcaption{font-size:9pt;font-weight:700;color:#e5007d}.mm .l{font-size:8.5pt;color:#4a5352;letter-spacing:.08em;text-transform:uppercase}'
           '.sw{display:flex;gap:6mm}.sc{width:56mm;height:56mm;border-radius:5mm;padding:5mm;display:flex;flex-direction:column;justify-content:flex-end;font-size:10pt;line-height:1.5;border:.3mm solid #dfe3e3}'
           '.sc b{font-size:12pt}'
           '.mx{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;width:150mm}.mxc{height:20mm;border-radius:3mm;display:flex;align-items:center;justify-content:center;position:relative;border:.3mm solid #dfe3e3}'
           '.mxc svg{width:60%}.mxc u{position:absolute;right:2mm;bottom:1mm;text-decoration:none;font-weight:800}.mxc.ok u{color:#00b1bc}.mxc.on-t.ok u{color:#fff}.mxc.no svg{opacity:.18}.mxc.no u{color:#d33a2c}'
           '.bans{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}.ban{border:.3mm solid #dfe3e3;border-radius:4mm;overflow:hidden}.ban .v{position:relative;height:38mm;display:flex;align-items:center;justify-content:center;color:#000}'
           '.ban svg.lgm{width:100%;height:100%}.ban svg.x{position:absolute;right:2mm;top:2mm;width:7mm;height:7mm}.ban .c{padding:2.5mm 3mm;font-size:9pt;font-weight:600;border-top:.3mm solid #dfe3e3}'
           '.warn{margin-top:6mm;max-width:170mm;padding:3.5mm 6mm;border:.6mm solid #e08a00;background:#fff3d6;border-radius:4mm;font-weight:800;font-size:11pt;color:#5f3b00}'
           '.tmp{column-count:2;column-gap:12mm;font-size:8.6pt;line-height:1.42;color:#2d3536}.tmp .tm-t{font-size:12pt;letter-spacing:.06em;margin:0 0 1mm;column-span:all}.tmp .tm-s{column-span:all;margin:0 0 4mm;max-width:none;font-size:9.5pt;color:#4f7478}'
           '.tmp h4{font-size:9.4pt;margin:0 0 1mm;padding-top:3.2mm;color:#101415;break-after:avoid}.tmp p{font-size:8.6pt;line-height:1.42;margin:0 0 1.2mm;max-width:none}.tmp ul{margin:0 0 1.2mm 4mm}.tmp li{margin-bottom:.8mm}.tmp .ct{margin-top:1.5mm}.tmp a{color:#00727a;text-decoration:none}'
           '.end{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}'
           '.end .logo svg{display:block;width:120mm;height:auto;color:#f2f2f0}'
           '.end .pm{margin-top:16mm;padding:6mm 12mm;border:.35mm dashed rgba(255,255,255,.6);border-radius:5mm;background:rgba(7,29,34,.25);max-width:150mm}'
           '.end .pm b{display:block;font-size:10pt;letter-spacing:.22em;text-transform:uppercase;margin-bottom:2mm}.end .pm p{color:#fff;margin:0 auto;font-size:11pt}.end .ct{margin-top:3mm!important;font-size:10.5pt}')
    cells = [(t['n_t'], '#00b1bc', '0 177 188', 'CMYK 75 / 5 / 28 / 0', '#fff'),
             (t['n_k'], '#000000', '0 0 0', '', '#fff'), (t['n_w'], '#ffffff', '255 255 255', '', '#000')]
    sw = ''.join(f'<div class="sc" style="background:{h};color:{fg}"><b>{n}</b>{h.upper()}<br>RGB {r}' + (f'<br>{cm}' if cm else '') + '</div>' for n, h, r, cm, fg in cells)
    N = 7
    hd = lambda title: f'<div class="hd">{svg("h")}<span>{title}</span></div>'
    ft = lambda n: f'<div class="ft"><span>ODISEJA · {t["hero_p"]}</span><span>{n} / {N}</span></div>'
    vbh = VIEW['h']; vbv = VIEW['v']
    mh = f'<figure><div class="l">{t["min_h_l"]}</div>{svg("h", w=round(40 * 3.7795, 1))}<div class="d" style="width:40mm"></div><figcaption>40 mm</figcaption></figure>'
    mv = f'<figure><div class="l">{t["min_v_l"]}</div>{svg("v", w=round(23 * 3.7795, 1))}<div class="d" style="width:23mm"></div><figcaption>23 mm</figcaption></figure>'
    return (f'<!doctype html><html lang="{t["lang"]}"><head><meta charset="utf-8"><title>{t["pdf_title"]}</title><style>{css}</style></head><body>'
            f'<svg width="0" height="0" style="position:absolute"><defs>{DEFS}</defs></svg>'
            f'<div class="pg gr cover"><div class="big">{svg("h")}</div><div class="sub">{t["hero_p"]}</div><div class="ttl">{t["pdf_title"]}</div></div>'
            f'<div class="pg">{hd(t["logo_h"])}<div class="body"><h2>{t["logo_h"]}</h2><div class="g3">{logos}</div><p>{t["logo_note"]}</p><div class="warn">&#9888; {t["symbol_warn"]}</div></div>{ft(2)}</div>'
            f'<div class="pg">{hd(t["rules_h"])}<div class="body"><div class="cols"><div><h2>{t["clear_h"]}</h2><div class="two">{clear_svg("h")}{clear_svg("v")}</div><p>{t["clear_p"]}</p></div>'
            f'<div><h2>{t["min_h"]}</h2><div class="card"><div class="mm">{mh}{mv}</div></div><p>{t["min_p"]}</p></div></div></div>{ft(3)}</div>'
            f'<div class="pg">{hd(t["colors_h"])}<div class="body"><h2>{t["colors_h"]}</h2><div class="sw">{sw}</div><p>{t["colors_p"]}</p><h3>{t["matrix_h"]}</h3><div class="mx">{matrix(t)}</div></div>{ft(4)}</div>'
            f'<div class="pg">{hd(t["dont_h"])}<div class="body"><h2>{t["dont_h"]}</h2><p style="margin:0 0 6mm">{t["dont_p"]}</p><div class="bans">{bans(t)}</div></div>{ft(5)}</div>'
            f'<div class="pg">{hd(t["terms_head"])}<div class="body"><div class="tmp">{terms_html(t["lang"], "tm")}</div></div>{ft(6)}</div>'
            f'<div class="pg gr end"><div class="logo">{svg("h")}</div><div class="pm"><b>{t["perm_h"]}</b><p>{t["perm"]}</p><p class="ct">{TERMS[t["lang"]]["sections"][3]["contact"][0]} · {TERMS[t["lang"]]["sections"][3]["contact"][1]}<br>{TERMS[t["lang"]]["sections"][3]["contact"][2]}</p></div></div>'
            f'</body></html>')


def colored_svg(o, c):
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + svg(o, HEX[c], cls='odiseja', w=1200)


def main():
    OUT.mkdir(exist_ok=True)
    work = pathlib.Path(tempfile.mkdtemp())
    jobs = []   # (svg_path, png_path_1200, png_path_3600, pdf_path)
    zips = {}
    for lg, t in T.items():
        root = work / lg
        (root / 'logo').mkdir(parents=True)
        for o in 'hvs':
            for c in 'tkw':
                base = f'odiseja-{t["folder"][o]}-{t["colname"][c]}'
                d = root / 'logo' / t['folder'][o]
                for sub in ('svg', 'png', 'pdf'):
                    (d / sub).mkdir(parents=True, exist_ok=True)
                (d / 'svg' / f'{base}.svg').write_text(colored_svg(o, c))
                jobs.append({'svg': str(d / 'svg' / f'{base}.svg'), 'png': [str(d / 'png' / f'{base}-1200px.png'), str(d / 'png' / f'{base}-3600px.png')], 'pdf': str(d / 'pdf' / f'{base}.pdf')})
        (root / t['colors_txt']).write_text(t['colors_txt_body'])
        (root / ('README.txt')).write_text(t['readme'] + '\n' + t['terms_file'] + '\n')
        (root / t['terms_file']).write_text(terms_txt(lg))
        ph = work / f'print-{lg}.html'
        ph.write_text(print_html(t))
        jobs.append({'html': str(ph), 'pdf': str(root / t['rules_pdf'])})
        (OUT / t['out'].replace('press-', 'press-')).write_text(page(t))
    (work / 'jobs.json').write_text(json.dumps(jobs))
    subprocess.run(['node', str(R / 'tools' / 'press_raster.js'), str(work / 'jobs.json')], check=True)
    for lg, t in T.items():
        z = OUT / t['zip']
        if z.exists():
            z.unlink()
        root = work / lg
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(root.rglob('*')):
                if f.is_file():
                    zf.write(f, f.relative_to(root))
        print(lg, z.name, round(z.stat().st_size / 1024), 'KB', (OUT / t['out']).stat().st_size // 1024, 'KB html')
    shutil.rmtree(work, ignore_errors=True)
    print('M =', M, 'CX,CY =', round(CX, 2), round(CY, 2))


if __name__ == '__main__':
    main()
