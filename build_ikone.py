import re, math
svg = open('assets/ikone-test.svg').read()
paths = re.findall(r'<path class="st1" d="([^"]+)"', svg)
U, DOT = paths[0], paths[1]
S = 275.05

def squircle(n=5.0, N=96):
    h = S/2; pts = []
    for i in range(N):
        t = 2*math.pi*i/N
        c, s = math.cos(t), math.sin(t)
        x = h + h*math.copysign(abs(c)**(2/n), c)
        y = h + h*math.copysign(abs(s)**(2/n), s)
        pts.append('%.2f,%.2f' % (x, y))
    return 'M' + 'L'.join(pts) + 'Z'
SQ = squircle()
T = 'translate(0,-30.45)'

defs = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<path id="sq" d="{SQ}"/>
<path id="gu" d="{U}"/><path id="gd" d="{DOT}"/>
<clipPath id="csq"><use href="#sq"/></clipPath>
<filter id="fg" x="-20%" y="-20%" width="140%" height="150%" color-interpolation-filters="sRGB">
 <feDropShadow dx="0" dy="7" stdDeviation="6" flood-color="#00282b" flood-opacity=".38"/></filter>
<filter id="fgl" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
 <feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="fgs" x="-20%" y="-20%" width="140%" height="150%" color-interpolation-filters="sRGB">
 <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity=".18"/></filter>
<!-- osnutek 1: turkizna -->
<linearGradient id="b1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27b9c0"/><stop offset=".55" stop-color="#00868f"/><stop offset="1" stop-color="#006870"/></linearGradient>
<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#d7eef0"/></linearGradient>
<!-- osnutek 2: bela -->
<linearGradient id="b2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#e3e9ea"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#17b2ba"/><stop offset="1" stop-color="#00717a"/></linearGradient>
<!-- osnutek 3: temna -->
<radialGradient id="b3" cx=".5" cy=".12" r=".95"><stop offset="0" stop-color="#2c4a4c"/><stop offset=".6" stop-color="#101c1d"/><stop offset="1" stop-color="#050a0a"/></radialGradient>
<linearGradient id="g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5de6ee"/><stop offset="1" stop-color="#00a8b3"/></linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="gloss2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient>
</defs></svg>'''

def icon(n):
    glyph = lambda fill, f: (f'<g filter="url(#{f})"><use href="#gu" transform="{T}" fill="{fill}"/>'
                             f'<use href="#gd" transform="{T}" fill="{fill}"/></g>')
    extra = ''
    if n == 1:
        body = '<use href="#sq" fill="url(#b1)"/>'
        # odsev
        body += '<g clip-path="url(#csq)"><ellipse cx="137" cy="-30" rx="190" ry="120" fill="url(#gloss)"/>'
        body += '<circle cx="137.5" cy="126" r="22.68" fill="#00868f" opacity="0"/></g>'
        body += glyph('url(#g1)', 'fg')
        body += '<use href="#sq" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="2"/>'
    elif n == 2:
        body = '<use href="#sq" fill="url(#b2)"/>'
        body += '<g clip-path="url(#csq)"><rect width="275" height="275" fill="url(#shade)"/>'
        body += '<ellipse cx="137" cy="-40" rx="190" ry="110" fill="url(#gloss2)" opacity=".7"/></g>'
        body += glyph('url(#g2)', 'fgs')
        body += '<use href="#sq" fill="none" stroke="#fff" stroke-opacity=".9" stroke-width="2"/>'
    else:
        body = '<use href="#sq" fill="url(#b3)"/>'
        body += '<g clip-path="url(#csq)"><ellipse cx="137" cy="-40" rx="190" ry="110" fill="url(#gloss)" opacity=".35"/></g>'
        body += glyph('url(#g3)', 'fgl')
        body += '<use href="#sq" fill="none" stroke="#5de6ee" stroke-opacity=".35" stroke-width="2"/>'
    return f'<svg viewBox="-12 -6 299 299" role="img" aria-label="Predlog {n}">{body}</svg>'

page = f'''<!doctype html>
<html lang="sl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ikone</title>
<style>
*{{box-sizing:border-box;margin:0}}
body{{font-family:"Helvetica Neue",Inter,system-ui,sans-serif;min-height:100vh;color:#fff;background:radial-gradient(circle at 18% 22%,#d2ab90,transparent 55%),radial-gradient(circle at 85% 75%,#8fb4ac,transparent 55%),linear-gradient(160deg,#a9785f,#7f8f78);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7vh;padding:8vh 5vw}}
.row{{display:flex;gap:min(7vw,80px);flex-wrap:wrap;justify-content:center}}
figure{{display:flex;flex-direction:column;align-items:center;gap:14px}}
figure .big{{width:min(260px,26vw);min-width:130px;transition:transform .45s cubic-bezier(.2,.8,.2,1)}}
figure .big:hover{{transform:translateY(-8px) scale(1.04)}}
svg{{display:block;width:100%;height:auto;overflow:visible}}
figcaption{{font-weight:600;font-size:17px;text-shadow:0 1px 6px rgba(0,0,0,.35)}}
.small{{display:flex;gap:18px;align-items:flex-end}}
.small span{{display:block}}
@media (prefers-reduced-motion:reduce){{figure .big{{transition:none}}}}
</style></head><body>
{defs}
<div class="row">
''' + ''.join(f'<figure><div class="big">{icon(i)}</div><div class="small"><span style="width:60px">{icon(i)}</span><span style="width:40px">{icon(i)}</span><span style="width:29px">{icon(i)}</span></div><figcaption>Predlog {i}</figcaption></figure>\n' for i in (1,2,3)) + '''</div></body></html>'''
open('ikone-predlogi.html','w').write(page)
print(len(page))
