#!/usr/bin/env python3
"""Zgradi samostojni pravi-punkt.html (izbrani logotip) iz src/pravi*.{html,css,js} + assets/pravi.json."""
import json, pathlib

R = pathlib.Path(__file__).parent
S = R / 'src'
D = json.loads((R / 'assets' / 'pravi.json').read_text())
TEAL = D['teal']
L = D['lock']


def path(ident, d, color, extra=''):
    return f'<path id="{ident}" d="{d}" fill="currentColor" style="color:{color}"{extra}/>'


def lockup(prefix, color_letters='#e5e5e5'):
    """Deli logotipa (siva izhodiščna barva) z id-ji <prefix>_P, _N, _K, _T, _U, _dot, _pr0-4, _sk0-14."""
    o = ''.join(path(f'{prefix}_{k}', L[k], color_letters) for k in ('P', 'N', 'K', 'T'))
    o += ''.join(path(f'{prefix}_pr{i}', d, color_letters) for i, d in enumerate(L['pravi']))
    o += ''.join(path(f'{prefix}_sk{i}', d, color_letters) for i, d in enumerate(L['skupina']))
    o += path(f'{prefix}_U', L['U'], TEAL) + path(f'{prefix}_dot', L['dot'], TEAL)
    return o


def group(ident, ds, color):
    return f'<g id="{ident}" style="color:{color}">' + ''.join(f'<path d="{d}" fill="currentColor"/>' for d in ds) + '</g>'


def badge(ident, dx):
    b = D['badge']
    return f'<g transform="translate({dx} 0)"><g id="{ident}"><path d="{b["circle"]}" fill="{b["red"]}"/><path d="{b["eight"]}" fill="#fff"/></g></g>'


# --- Nastanek: vsi sloji animacije ---
GH = '#d9d9d9'
cart = D['cart']; bk = D['basket']; bg = D['bag']; DOT = L['dot']


def letters(prefix, color):
    o = ''.join(path(f'{prefix}_{k}', L[k], color) for k in ('P', 'K', 'T', 'N'))
    o += ''.join(path(f'{prefix}_pr{i}', d, color) for i, d in enumerate(L['pravi']))
    o += ''.join(path(f'{prefix}_sk{i}', d, color) for i, d in enumerate(L['skupina']))
    return o


def cart_markup(ident, color, with_ids=True):
    lines = ''.join(f'<path d="{d}" fill="currentColor"/>' for d in cart['lines'])
    return (f'<g id="{ident}" style="color:{color}"><g id="{ident}_l">{lines}</g>'
            f'<path id="{ident}_b" d="{cart["body"]}" fill="currentColor"/></g>')


cine = '<circle id="c_disc" cx="600" cy="618" r="402" fill="#fff" style="filter:drop-shadow(0 26px 40px rgba(0,0,0,.2))"/>'
cine += '<g id="c_road" style="color:#d9d9d9">' + ''.join(f'<line x1="{x}" x2="{x + 90}" y1="752" y2="752" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>' for x in range(-700, 1700, 190)) + '</g>'
cine += ''.join(f'<line id="c_w{i}" stroke="#d9d9d9" stroke-width="6" stroke-linecap="round" opacity="0"/>' for i in range(6))
cine += '<ellipse id="c_sh" cx="428" cy="752" rx="105" ry="9" fill="#000" opacity="0"/>'
cine += ''.join(cart_markup(f'c_gc{i}', GH) for i in range(4))
cine += ''.join(f'<path id="c_gd{i}" d="{DOT}" fill="currentColor" style="color:{GH}"/>' for i in range(4))
cine += group('c_basket', bk['handles'] + [bk['rim']] + bk['bits'] + [bk['body']], TEAL)
cine += group('c_bag', [bg['handle'], bg['body']], TEAL)
cine += badge('c_b1', 0) + badge('c_b2', 349) + badge('c_b3', 683)
cine += ('<g id="c_lock"><rect id="c_hl" x="290" y="481" width="275" height="275" rx="62" fill="currentColor" style="color:' + TEAL + '"/>'
         + letters('c', GH) + path('c_U', L['U'], TEAL) + cart_markup('c_cart', TEAL).replace('id="c_cart_l"', 'id="c_lines"').replace('id="c_cart_b"', 'id="c_body"')
         + path('c_dot', DOT, TEAL) + '</g>')
cine += ('<g id="c_ic2" style="filter:drop-shadow(0 12px 22px rgba(0,0,0,.22))"><rect x="290" y="481" width="275" height="275" rx="62" fill="#fff"/>'
         f'<path d="{L["U"]}" fill="{TEAL}"/><path id="c_id2" d="{DOT}" fill="{TEAL}"/></g>')
cine += ''.join(f'<text id="c_l{i}" x="{x}" y="792" text-anchor="middle" font-size="34" font-weight="600" fill="currentColor" style="color:#0b3a3f;font-family:\'Helvetica Neue\',Arial,sans-serif">Pravi Punkt</text>' for i, x in ((1, 329.5), (2, 720)))
cine += ''.join(f'<circle id="c_s{i}" r="6" fill="currentColor" opacity="0"/>' for i in range(70))

# --- Logotip (končni, S poudarkom / brez) ---
def lockup_svg(hl):
    return ('<svg viewBox="140 424 920 352" role="img" aria-label="Pravi Punkt, Skupina Boscarol">'
            + ('<rect class="hl" x="290" y="481" width="275" height="275" rx="62"/>' if hl else '')
            + ''.join(f'<path class="tx" d="{L[k]}"/>' for k in ('P', 'N', 'K', 'T'))
            + ''.join(f'<path class="tx" d="{d}"/>' for d in L['pravi'])
            + ''.join(f'<path class="ac" d="{d}"/>' for d in L['skupina'])
            + f'<path class="ac" d="{L["U"]}"/><path class="ac" d="{L["dot"]}"/></svg>')


# --- Ikona ---
def icon(bg_white):
    col = TEAL if bg_white else '#fff'
    return (f'<svg viewBox="0 0 275 275" role="img" aria-label="Ikona Pravi Punkt"><g transform="translate(-290.5 -480.5)" fill="{col}">'
            f'<path d="{L["U"]}"/><path class="dt" d="{L["dot"]}"/></g></svg>')

page = (S / 'pravi.html').read_text()
subs = {
    '__STYLE__': (S / 'landing.css').read_text() + (S / 'pravi.css').read_text(),
    '__CINE__': cine, '__ICON_A__': icon(False), '__ICON_B__': icon(True), '__LK__': lockup_svg(False), '__LKH__': lockup_svg(True),
    '__TLJS__': (S / 'timeline.js').read_text(), '__SCENJS__': (S / 'cine_scen.js').read_text(), '__PAGEJS__': (S / 'cine.js').read_text() + (S / 'pravi_page.js').read_text(),
}
for k, v in subs.items():
    page = page.replace(k, v)
(R / 'pravi-punkt.html').write_text(page)
print('pravi-punkt.html', round(len(page) / 1024), 'KB')
