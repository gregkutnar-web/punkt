import random
random.seed(7)
F="font-family=\"'Inter','Helvetica Neue',Helvetica,Arial,sans-serif\""

def stars(W,H):
    s=[]
    for _ in range(90):
        x=random.uniform(0,W);y=random.uniform(0,H*0.5);r=random.choice([1,1.4,2])
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{random.uniform(.3,.9):.2f}"/>')
    return ''.join(s)

def snow(W,H,n=70):
    return ''.join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.choice([2,3,4,5])}" fill="#fff" opacity="{random.uniform(.25,.7):.2f}"/>' for _ in range(n))

def small_house(x,y,w,h,col,roof):
    return f'''<g transform="translate({x},{y})">
<rect x="0" y="{-h}" width="{w}" height="{h}" fill="{col}"/>
<path d="M-8 {-h} L{w/2} {-h-w*.5} L{w+8} {-h} Z" fill="{roof}"/>
<path d="M-8 {-h} L{w/2} {-h-w*.5} L{w+8} {-h} L{w+8} {-h+8} Q{w/2} {-h-w*.5+26} -8 {-h+8} Z" fill="#fff" opacity=".92"/>
<rect x="{w*.3}" y="{-h*.62}" width="{w*.4}" height="{h*.32}" rx="4" fill="#ffc86b" filter="url(#glow)"/>
</g>'''

def fir(x,y,s):
    return f'''<g transform="translate({x},{y}) scale({s})"><rect x="-6" y="-6" width="12" height="16" fill="#3b2a3a"/>
<path d="M0 -150 L42 -70 L18 -70 L52 -10 L-52 -10 L-18 -70 L-42 -70 Z" fill="#12503f"/>
<path d="M0 -150 L22 -105 L-22 -105 Z" fill="#fff" opacity=".9"/>
<circle cx="-14" cy="-50" r="4" fill="#ff6b5e"/><circle cx="20" cy="-30" r="4" fill="#ffd36b"/><circle cx="0" cy="-88" r="4" fill="#7fe0d0"/></g>'''

def babicina(cx,by):
    # house centred at cx, base at by
    w,h=330,230
    x=cx-w/2
    return f'''<g>
<ellipse cx="{cx}" cy="{by+6}" rx="{w*.62}" ry="20" fill="#000" opacity=".25"/>
<g transform="translate({x},{by})">
<rect x="236" y="{-h-92}" width="42" height="90" fill="#7a3b3b"/><rect x="230" y="{-h-100}" width="54" height="16" fill="#fff"/>
<g opacity=".55" fill="#fff"><circle cx="258" cy="{-h-130}" r="16"/><circle cx="276" cy="{-h-166}" r="22"/><circle cx="304" cy="{-h-210}" r="28"/></g>
<rect x="0" y="{-h}" width="{w}" height="{h}" fill="#b5503f"/>
<g stroke="#9a4033" stroke-width="3" opacity=".6">{''.join(f'<line x1="0" y1="{-h+i*26}" x2="{w}" y2="{-h+i*26}"/>' for i in range(1,9))}</g>
<path d="M-26 {-h} L{w/2} {-h-170} L{w+26} {-h} Z" fill="#5b2f4a"/>
<path d="M-26 {-h} L{w/2} {-h-170} L{w+26} {-h} L{w+26} {-h+14} Q{w*.75} {-h-82} {w/2} {-h-110} Q{w*.25} {-h-82} -26 {-h+14} Z" fill="#fff"/>
<circle cx="{w/2}" cy="{-h-70}" r="26" fill="#ffc86b" filter="url(#glow)"/><circle cx="{w/2}" cy="{-h-70}" r="26" fill="none" stroke="#fff" stroke-width="5"/>
<rect x="18" y="{-h+50}" width="82" height="86" rx="6" fill="#ffc86b" filter="url(#glow)"/>
<path d="M59 {-h+50}V{-h+136}M18 {-h+93}H100" stroke="#fff" stroke-width="6"/>
<rect x="230" y="{-h+50}" width="82" height="86" rx="6" fill="#ffc86b" filter="url(#glow)"/>
<path d="M271 {-h+50}V{-h+136}M230 {-h+93}H312" stroke="#fff" stroke-width="6"/>
<rect x="124" y="{-150}" width="82" height="150" rx="41" ry="41" fill="#3b1f3a"/><rect x="124" y="-110" width="82" height="110" fill="#3b1f3a"/>
<circle cx="190" cy="-70" r="5" fill="#ffc86b"/>
<circle cx="165" cy="-118" r="30" fill="none" stroke="#1f7a55" stroke-width="10"/><circle cx="148" cy="-100" r="5" fill="#ff6b5e"/><circle cx="182" cy="-100" r="5" fill="#ff6b5e"/>
<rect x="104" y="-4" width="122" height="10" fill="#fff" opacity=".9"/>
<path d="M-26 {-h+16} Q{w/2} {-h+60} {w+26} {-h+16}" fill="none" stroke="#ffe7a8" stroke-width="3"/>
{''.join(f'<circle cx="{-26+i*(w+52)/10:.0f}" cy="{-h+16+ (44*(1-((i-5)/5)**2)):.0f}" r="7" fill="{["#ffd36b","#ff6b5e","#7fe0d0"][i%3]}" filter="url(#glow)"/>' for i in range(11))}
</g></g>'''

def foto(cx,by):
    w,h=250,330
    x=cx-w/2
    return f'''<g>
<ellipse cx="{cx}" cy="{by+6}" rx="{w*.62}" ry="16" fill="#000" opacity=".25"/>
<g transform="translate({x},{by})">
<path d="M0 0V{-h+110}A125 125 0 0 1 {w} {-h+110}V0" fill="none" stroke="#7fe0d0" stroke-width="16" stroke-linecap="round"/>
<path d="M0 0V{-h+110}A125 125 0 0 1 {w} {-h+110}V0" fill="none" stroke="#fff" stroke-width="4" opacity=".6" transform="translate(0,0)"/>
<path d="M30 0V{-h+120}A95 95 0 0 1 {w-30} {-h+120}V0Z" fill="#ffc86b" opacity=".13"/>
{''.join(f'<circle cx="{125-125*__import__("math").cos(t*3.14159/ 13):.0f}" cy="{-h+110-125*__import__("math").sin(t*3.14159/13):.0f}" r="7" fill="{["#ffd36b","#ff6b5e","#fff"][t%3]}" filter="url(#glow)"/>' for t in range(1,13))}
<g transform="translate(125,{-h+190}) rotate(-6)"><rect x="-58" y="-70" width="116" height="140" rx="6" fill="#fff"/><rect x="-48" y="-60" width="96" height="96" fill="#2a2160"/>
<circle cx="-10" cy="-20" r="14" fill="#ffc86b"/><path d="M-48 36 L-14 -4 L10 20 L28 2 L48 36 Z" fill="#7fe0d0"/>
<path d="M30 -48 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4Z" fill="#fff"/></g>
<path d="M-30 0 H{w+30}" stroke="#fff" stroke-width="10" stroke-linecap="round"/>
</g>
{fir(cx+w/2+40,by,.62)}
</g>'''

def card(x,y,w,h,title,sub,icon):
    return f'''<g transform="translate({x},{y})">
<rect width="{w}" height="{h}" rx="26" fill="#2a2160" stroke="#ffc86b" stroke-opacity=".6" stroke-width="2"/>
<circle cx="52" cy="{h/2}" r="26" fill="#ffc86b"/>{icon}
<text x="100" y="{h/2-6}" {F} font-size="34" font-weight="700" fill="#fff">{title}</text>
<text x="100" y="{h/2+30}" {F} font-size="22" fill="#fff" fill-opacity=".8">{sub}</text></g>'''

ico_foto='<g transform="translate(52,%s)" fill="#2a2160"><rect x="-14" y="-8" width="28" height="18" rx="4"/><circle cx="0" cy="1" r="6" fill="#ffc86b"/><rect x="-6" y="-13" width="12" height="6" rx="2"/></g>'
ico_hisa='<g transform="translate(52,%s)" fill="#2a2160"><path d="M-15 0 L0 -14 L15 0 V13 H-15Z"/><rect x="-4" y="3" width="8" height="10" fill="#ffc86b"/></g>'

def build(W,H,ty,sy,cy,name,ox):
    random.seed(7)
    ch=96; cw=(W-160-24)/2
    cards=card(80,cy,cw,ch,'Foto kotiček','Ujemi praznični trenutek',ico_foto%(ch/2))+card(80+cw+24,cy,cw,ch,'Babičina hiška','Vstopi v toplino praznikov',ico_hisa%(ch/2))
    svg=f'''<g id="{name}" clip-path="url(#clip-{name})" transform="translate({ox},0)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars(W,H)}
<circle cx="{W-190}" cy="{ty+250}" r="170" fill="url(#moon)"/><circle cx="{W-190}" cy="{ty+250}" r="46" fill="#fff6d8"/>
<g fill="#fff">
<text x="{W/2}" y="{ty}" text-anchor="middle" font-size="26" letter-spacing="8" fill-opacity=".8">ODISEJA · BTC CITY LJUBLJANA</text>
<text x="{W/2}" y="{ty+135}" text-anchor="middle" font-weight="800" font-size="132" letter-spacing="-3">Praznična</text>
<text x="{W/2}" y="{ty+255}" text-anchor="middle" font-weight="800" font-size="132" letter-spacing="-3" fill="#ffc86b">vasica</text></g>
<g transform="translate({W/2-250},{ty+300})"><rect width="500" height="64" rx="32" fill="#ffc86b"/>
<text x="250" y="43" text-anchor="middle" {F} font-size="32" font-weight="700" fill="#2a2160">29. 11. – 30. 12. 2026</text></g>
<g transform="translate(0,{sy})">
<path d="M0 260 Q260 170 520 240 T{W} 220 V{H-sy} H0Z" fill="#cfd6f2"/>
<path d="M0 320 Q300 250 600 310 T{W} 290 V{H-sy} H0Z" fill="#eef1fc"/>
{small_house(40,300,90,70,'#6d4a7a','#3b2a5a')}{small_house(150,308,70,56,'#8a5a5a','#3b2a5a')}
{small_house(W-170,302,100,76,'#6d4a7a','#3b2a5a')}{small_house(W-270,310,70,54,'#8a5a5a','#3b2a5a')}
{fir(W-60,330,.8)}{fir(70,345,.7)}
{foto(W/2-250,380)}
{babicina(W/2+130,390)}
</g>
{snow(W,H)}
{cards}
<text x="{W/2}" y="{cy+ch+54}" text-anchor="middle" {F} font-size="22" letter-spacing="3" fill="#2a2160" fill-opacity=".75">ODISEJA.SI</text>
</g>'''
    return svg


import base64,io
from fontTools import subset
from fontTools.ttLib import TTFont
def font_face(file,weight):
    opts=subset.Options();opts.flavor='woff2';opts.layout_features=['kern','liga']
    f=TTFont('/usr/share/fonts/opentype/inter/'+file)
    sub=subset.Subsetter(opts)
    sub.populate(unicodes=list(range(0x20,0x7f))+[ord(c) for c in 'čšžČŠŽćđĆĐ·–—…'])
    sub.subset(f);b=io.BytesIO();f.flavor='woff2';f.save(b)
    return "@font-face{font-family:'Inter';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2');}"%(weight,base64.b64encode(b.getvalue()).decode())
# css=''.join(font_face(a,b) for a,b in [('Inter-Regular.otf',400),('Inter-Bold.otf',700),('Inter-ExtraBold.otf',800)])
GAP=120
clips=''.join(f'<clipPath id="clip-{n}"><rect width="1080" height="{h}"/></clipPath>' for n,h in [('artboard-feed-1080x1350',1350),('artboard-story-1080x1920',1920)])
feed=build(1080,1350,110,540,1130,'artboard-feed-1080x1350',0)
story=build(1080,1920,320,1010,1490,'artboard-story-1080x1920',1080+GAP)
TW=1080*2+GAP;TH=1920
lab=lambda x,y,t:f'<text x="{x}" y="{y}" font-family="\'Inter\',Helvetica,Arial,sans-serif" font-size="22" font-weight="700" fill="#666">{t}</text>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH+50}" viewBox="0 0 {TW} {TH+50}" version="1.1">
<title>Praznična vasica – Odiseja BTC City</title>
<defs>{clips}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f1233"/><stop offset=".55" stop-color="#2a2160"/><stop offset="1" stop-color="#7a3a62"/></linearGradient>
<radialGradient id="moon"><stop offset="0" stop-color="#fff6d8" stop-opacity=".9"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x="0" y="0" width="{TW}" height="{TH+50}" fill="#e9e9ee"/><g transform="translate(0,50)">
{lab(0,-16,'Feed 1080×1350')}{lab(1080+GAP,-16,'Story 1080×1920')}
{feed}
{story}
</g></svg>'''
import re
def fixtext(m):
    t=m.group(0)
    w=re.search(r'font-weight="(\d+)"',t)
    ps={'800':'Inter-ExtraBold','700':'Inter-Bold'}.get(w.group(1) if w else '', 'Inter-Regular')
    t=re.sub(r' font-family="[^"]*"','',t)
    return t.replace('<text ','<text font-family="%s, Inter, Helvetica, Arial, sans-serif" '%ps,1)
svg=re.sub(r'<text [^>]*>',fixtext,svg)
svg=re.sub(r'="\.(\d)',r'="0.\1',svg)
svg=svg.replace('<g fill="#fff">','<g fill="#fff">')
svg='<?xml version="1.0" encoding="UTF-8"?>\n'+svg
open('/home/user/punkt/vasica/vasica-artboards.svg','w',encoding='utf-8').write(svg)

# --- validacija ---
import collections,subprocess,sys
_s=open('/home/user/punkt/vasica/vasica-artboards.svg',encoding='utf-8').read()
_ids=re.findall(r'\bid="([^"]+)"',_s)
_dup=[i for i,c in collections.Counter(_ids).items() if c>1]
_miss=set(re.findall(r'url\(#([^)]+)\)',_s))-set(_ids)
assert not _dup,f'podvojeni id: {_dup}'
assert not _miss,f'manjkajoče reference: {_miss}'
assert subprocess.run(['xmllint','--noout','/home/user/punkt/vasica/vasica-artboards.svg']).returncode==0,'xmllint'
print('VALIDACIJA OK: id-ji unikatni, reference obstajajo, XML veljaven')
