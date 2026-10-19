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


# --- Ideja: ikone, voziček, pike, U + siva PUNKT ---
cart = D['cart']; bk = D['basket']; bg = D['bag']
idea = lockup('i')
idea = idea.replace(path('i_U', L['U'], TEAL), '').replace(path('i_dot', L['dot'], TEAL), '')   # U/pika se narišeta nad ikonami
idea += path('i_U', L['U'], TEAL)
idea += group('i_basket', bk['handles'] + [bk['rim']] + bk['bits'] + [bk['body']], TEAL)
idea += group('i_bag', [bg['handle'], bg['body']], TEAL)
idea += group('i_cart', cart['lines'] + [cart['body']], TEAL)
idea += badge('i_b1', 0) + badge('i_b2', 349) + badge('i_b3', 683)
idea += path('i_d1', L['dot'], TEAL) + path('i_d2', L['dot'], TEAL) + path('i_dot', L['dot'], TEAL)

# --- Logotip: oblike ---
logo = f'<rect id="l_hl" x="290" y="481" width="275" height="275" rx="62" fill="{TEAL}"/>' + lockup('l', '#e5e5e5')

# --- Ikona ---
def icon(bg_white):
    col = TEAL if bg_white else '#fff'
    return (f'<svg viewBox="0 0 275 275" role="img" aria-label="Ikona Pravi Punkt"><g transform="translate(-290.5 -480.5)" fill="{col}">'
            f'<path d="{L["U"]}"/><path class="dt" d="{L["dot"]}"/></g></svg>')

# --- Različice: logotip z barvami po razredih ---
lk = ('<svg viewBox="140 424 920 352" role="img" aria-label="Pravi Punkt, Skupina Boscarol">'
      + ''.join(f'<path class="tx" d="{L[k]}"/>' for k in ('P', 'N', 'K', 'T'))
      + ''.join(f'<path class="tx" d="{d}"/>' for d in L['pravi'])
      + ''.join(f'<path class="ac" d="{d}"/>' for d in L['skupina'])
      + f'<path class="ac" d="{L["U"]}"/><path class="ac" d="{L["dot"]}"/></svg>')

page = (S / 'pravi.html').read_text()
subs = {
    '__STYLE__': (S / 'landing.css').read_text() + (S / 'pravi.css').read_text(),
    '__IDEA__': idea, '__LOGO__': logo, '__ICON_A__': icon(False), '__ICON_B__': icon(True), '__LK__': lk,
    '__TLJS__': (S / 'timeline.js').read_text(), '__SCENJS__': (S / 'pravi_scen.js').read_text(), '__PAGEJS__': (S / 'pravi_page.js').read_text(),
}
for k, v in subs.items():
    page = page.replace(k, v)
(R / 'pravi-punkt.html').write_text(page)
print('pravi-punkt.html', round(len(page) / 1024), 'KB')
