import re
ns = {}; exec(open('build_ikone.py').read().split("page = f'''")[0], ns)
SQ, U, DOT, T = ns['SQ'], ns['U'], ns['DOT'], ns['T']
SH = lambda i, dy, sd, op: (f'<filter id="{i}" x="-20%" y="-20%" width="140%" height="150%"><feOffset dx="0" dy="{dy}"/>'
  f'<feGaussianBlur result="blur" stdDeviation="{sd}"/><feFlood flood-color="#000" flood-opacity="{op}"/>'
  '<feComposite in2="blur" operator="in"/><feComposite in="SourceGraphic"/></filter>')
LG = lambda i, a, b: (f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
OP = lambda i, c, a, b: (f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="{a}"/><stop offset="1" stop-color="{c}" stop-opacity="{b}"/></linearGradient>')
def glyph(fill, f):
    return (f'<g filter="url(#{f})"><path transform="{T}" fill="{fill}" d="{U}"/><path transform="{T}" fill="{fill}" d="{DOT}"/></g>')
def build(n):
    if n == 1:
        defs = LG('b','#27b9c0','#006870').replace('<stop offset="1"','<stop offset=".55" stop-color="#00868f"/><stop offset="1"') + LG('g','#ffffff','#d7eef0') + OP('gl','#ffffff',.42,0) + SH('sh',7,6,.38)
        body = (f'<path fill="url(#b)" d="{SQ}"/><g clip-path="url(#c)"><ellipse cx="137" cy="-30" rx="190" ry="120" fill="url(#gl)"/></g>'
                + glyph('url(#g)','sh') + f'<path fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2" d="{SQ}"/>')
    else:
        defs = LG('b','#ffffff','#e3e9ea') + LG('g','#17b2ba','#00717a') + OP('gl','#ffffff',.9,0) + OP('sd','#000000',0,.16).replace('<stop offset="0"','<stop offset=".55"') + SH('sh',5,4,.18)
        body = (f'<path fill="url(#b)" d="{SQ}"/><g clip-path="url(#c)"><rect width="275" height="275" fill="url(#sd)"/><ellipse cx="137" cy="-40" rx="190" ry="110" fill="url(#gl)" opacity=".7"/></g>'
                + glyph('url(#g)','sh') + f'<path fill="none" stroke="#fff" stroke-width="2" d="{SQ}"/>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-12 -6 299 299" width="1024" height="1024">'
            f'<defs><clipPath id="c"><path d="{SQ}"/></clipPath>{defs}</defs>{body}</svg>')
for n in (1, 2): open(f'export/ikona-predlog-{n}.svg','w').write(build(n))
