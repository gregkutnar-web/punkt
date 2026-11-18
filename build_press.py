#!/usr/bin/env python3
"""Zgradi medijski paket Odiseja (SL + EN): press/press-{sl,en}.html + ZIP s pravili in logotipi.
Vir: assets/odiseja.json (tools/extract_odiseja.py). Gradnja: python3 build_press.py
PNG in PDF izrisuje tools/press_raster.js (Playwright): NODE_PATH=$(npm root -g) je nujen."""
import json, pathlib, re, shutil, subprocess, sys, tempfile, zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent / 'src'))
from press_i18n import T  # noqa: E402

R = pathlib.Path(__file__).parent
S = R / 'src'
OUT = R / 'press'
D = json.loads((R / 'assets' / 'odiseja.json').read_text())
LET, SUN = D['letters'], D['sun']
HEX = {'t': '#00868f', 'k': '#000000', 'w': '#ffffff'}
BG = {'w': '#ffffff', 'k': '#000000', 't': '#00868f'}


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
    valid = {'w': 'tk', 'k': 'tw', 't': 'w'}
    out = ''
    for bg in 'wkt':
        for c in 'tkw':
            ok = c in valid[bg]
            out += (f'<div class="mxc {"ok" if ok else "no"}{" on-t" if bg == "t" else ""}" style="background:{BG[bg]}" title="{t["m_ok"] if ok else t["m_no"]}">'
                    f'<svg viewBox="{VIEW["h"][0]:.2f} {VIEW["h"][1]:.2f} {VIEW["h"][2]:.2f} {VIEW["h"][3]:.2f}" style="color:{HEX[c]}" aria-hidden="true">{body("h")}</svg><u>{"✓" if ok else "✕"}</u></div>')
    return out


def page(t):
    h = (S / 'press.html').read_text()
    style = (S / 'landing.css').read_text() + (S / 'press.css').read_text()
    rep = {'__HERO_LOGO__': svg('h'), '__STYLE__': style, '__JS__': (S / 'press.js').read_text(), '__DEFS__': DEFS,
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
    """Pravila uporabe kot PDF (A4 ležeče)."""
    logos = ''
    for o in 'hvs':
        for c, bg in (('t', 'w'), ('k', 'w'), ('w', 'k')):
            logos += (f'<div class="lc" style="background:{BG[bg]};color:{HEX[c]}">{svg(o)}</div>')
    css = ('@page{size:A4 landscape;margin:0}*{box-sizing:border-box;margin:0;padding:0}body{font-family:"Helvetica Neue",Arial,sans-serif;color:#101415}'
           '.pg{width:297mm;height:210mm;padding:16mm 18mm;page-break-after:always;position:relative;overflow:hidden}'
           'h1{font-size:30pt;letter-spacing:.06em;margin-bottom:6mm}h2{font-size:11pt;letter-spacing:.2em;text-transform:uppercase;margin-bottom:5mm}'
           'p{font-size:10.5pt;line-height:1.5;color:#4a5352;max-width:120mm;margin-top:4mm}'
           '.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}.lc{height:30mm;display:flex;align-items:center;justify-content:center;border:.3mm solid #ddd;border-radius:3mm}'
           '.lc svg{height:60%;width:auto;max-width:80%}.two{display:flex;gap:8mm;align-items:center}.two svg{height:62mm;width:auto;color:#000}'
           '.sw{display:flex;gap:6mm}.sc{width:50mm;height:50mm;border-radius:4mm;padding:4mm;display:flex;flex-direction:column;justify-content:flex-end;font-size:10pt;border:.3mm solid #ddd}'
           '.mx{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;width:130mm;margin-top:6mm}.mxc{height:20mm;border-radius:3mm;display:flex;align-items:center;justify-content:center;position:relative;border:.3mm solid #ddd}'
           '.mxc svg{width:60%}.mxc u{position:absolute;right:2mm;bottom:1mm;text-decoration:none;font-weight:800}.mxc.ok u{color:#00868f}.mxc.on-t.ok u{color:#fff}.mxc.no svg{opacity:.18}.mxc.no u{color:#d33a2c}'
           '.bans{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}.ban{border:.3mm solid #ddd;border-radius:3mm;overflow:hidden}.ban .v{position:relative;height:36mm;display:flex;align-items:center;justify-content:center;color:#000}'
           '.ban svg.lgm{width:100%;height:100%}.ban svg.x{position:absolute;right:2mm;top:2mm;width:7mm;height:7mm}.ban .c{padding:2.5mm 3mm;font-size:9pt;font-weight:600;border-top:.3mm solid #ddd}'
           '.szl{font-size:10pt;margin-top:3mm}.warn{margin-top:5mm;max-width:150mm;padding:3mm 5mm;border:.6mm solid #d98a00;background:#fff4dc;border-radius:3mm;font-weight:700;font-size:11pt;color:#6b4300}')
    sw = ''.join(f'<div class="sc" style="background:{HEX[c]};color:{"#000" if c == "w" else "#fff"}"><b>{t["n_" + c]}</b>{HEX[c].upper()}<br>RGB {r}</div>' for c, r in (('t', '0 134 143'), ('k', '0 0 0'), ('w', '255 255 255')))
    return (f'<!doctype html><html lang="{t["lang"]}"><head><meta charset="utf-8"><title>{t["pdf_title"]}</title><style>{css}</style></head><body>'
            f'<svg width="0" height="0" style="position:absolute"><defs>{DEFS}</defs></svg>'
            f'<div class="pg"><h1>ODISEJA</h1><h2>{t["logo_h"]}</h2><div class="g3">{logos}</div><p>{t["logo_note"]}</p><div class="warn">&#9888; {t["symbol_warn"]}</div></div>'
            f'<div class="pg"><h2>{t["clear_h"]}</h2><div class="two">{clear_svg("h")}{clear_svg("v")}</div><p>{t["clear_p"]}</p>'
            f'<h2 style="margin-top:10mm">{t["min_h"]}</h2><p style="margin-top:0">{t["min_p"]}</p></div>'
            f'<div class="pg"><h2>{t["colors_h"]}</h2><div class="sw">{sw}</div><p>{t["colors_p"]}</p><h2 style="margin-top:8mm">{t["matrix_h"]}</h2><div class="mx">{matrix(t)}</div></div>'
            f'<div class="pg"><h2>{t["dont_h"]}</h2><p style="margin:0 0 6mm">{t["dont_p"]}</p><div class="bans">{bans(t)}</div></div>'
            f'<div class="pg"><h2>{t["perm_h"]}</h2><p>{t["perm"]}</p></div></body></html>')


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
        (root / ('README.txt')).write_text(t['readme'])
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
