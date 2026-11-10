import base64,sys
S=sys.argv[1]  # scratchpad with bg.jpg, star_gold.png
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
bg=b64(f'{S}/bg.jpg')
import qrcode
URL='https://odiseja-production.up.railway.app/zvezda/#zo-prijava'
q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,border=0,box_size=1); q.add_data(URL); q.make(fit=True)
M=q.get_matrix(); N=len(M); QS=34; ms=QS/N; qx,qy=167,243
qpath=''.join(f'M{qx+x*ms:.3f} {qy+y*ms:.3f}h{ms:.3f}v{ms:.3f}h-{ms:.3f}z' for y in range(N) for x in range(N) if M[y][x])
W,H=226,306   # mm: 220x300 + 3 mm porezave na vsaki strani
svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Zvezda Odiseje oglas 220x300 mm + 3 mm porezave (skupaj 226x306 mm). Enota viewBox = 1 mm. Besedilo je živo (Archivo 800/300/700, serif). -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="oder"><path d="M0 0H{W}V172Q113 238 0 172Z"/></clipPath>
  <linearGradient id="gumb" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#e3c89b"/><stop offset=".5" stop-color="#b89560"/><stop offset="1" stop-color="#8d6c41"/>
  </linearGradient>
  <linearGradient id="zlato" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#e9c98e"/><stop offset="1" stop-color="#a77f45"/>
  </linearGradient>
  <linearGradient id="rob" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#14424b" stop-opacity="0"/><stop offset=".5" stop-color="#1b5560"/><stop offset="1" stop-color="#14424b" stop-opacity="0"/>
  </linearGradient>
  <filter id="sence" x="-20%" y="-40%" width="140%" height="200%"><feDropShadow dx="0" dy=".8" stdDeviation=".9" flood-color="#000" flood-opacity=".55"/></filter>
</defs>

<g id="ozadje">
  <rect id="temna-podlaga" width="{W}" height="{H}" fill="#091c21"/>
  <g clip-path="url(#oder)">
    <image id="oder-render" x="0" y="0" width="{W}" height="205" preserveAspectRatio="xMidYMin slice" xlink:href="data:image/jpeg;base64,{bg}"/>
  </g>
  <path id="rob-loka" d="M0 172Q113 238 226 172" fill="none" stroke="url(#rob)" stroke-width=".5"/>
</g>

<g id="logotip-odiseja-ZAMENJAJ">
  <!-- Začasen približek: zamenjaj z vektorskim logotipom Odiseje -->
  <text x="22" y="27" font-family="Archivo, 'Archivo ExtraBold', Arial Black, sans-serif" font-weight="800" font-size="14.5" fill="#12adbb" textLength="66" lengthAdjust="spacingAndGlyphs">ODISEJA</text>
  <g fill="#12adbb">
    <circle cx="100" cy="21" r="6.6"/>
    <circle cx="99" cy="21" r="2" fill="#091c21"/>
  </g>
  <g stroke="#12adbb" stroke-width="1" stroke-linecap="round">
    <path d="M109 14.5l1.6-2.2M112 17.3l2.4-1.4M113.3 21h2.7M112 24.7l2.4 1.4M109 27.5l1.6 2.2"/>
  </g>
</g>

<g id="nagrade-znacka" filter="url(#sence)">
  <rect x="82" y="195" width="62" height="12.5" rx="6.25" fill="url(#gumb)"/>
  <text x="113" y="203.1" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="4.9" letter-spacing=".45" fill="#1a1208">BOGATE NAGRADE</text>
</g>

<g id="besedilo">
  <text id="naslov" x="22" y="223" font-family="Archivo, 'Archivo ExtraBold', Arial, sans-serif" font-weight="800" font-size="15.4" fill="#ffffff">Postani zvezda Odiseje</text>
  <text id="podnaslov" x="22" y="235" font-family="'Archivo Light', Archivo, Arial, sans-serif" font-weight="300" font-size="11.5" fill="#ffffff">in nastopi na velikem odru</text>
  <text id="uvod" font-family="'Archivo Light', Archivo, Arial, sans-serif" font-weight="300" font-size="4.3" fill="#cfe3e6">
    <tspan x="22" y="247.5">Imaš glas, talent ali nastop, ki ga mora videti občinstvo?</tspan>
    <tspan x="22" y="253.5">Prijavi se na Zvezdo Odiseje in pokaži, kaj znaš –</tspan>
    <tspan x="22" y="259.5">na pravem velikem odru in osvoji <tspan font-family="Archivo, Arial, sans-serif" font-weight="800" fill="#e9c98e">bogate nagrade</tspan>.</tspan>
  </text>
</g>

<g id="koraki" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="3.9" fill="#ffffff">
  <g fill="url(#gumb)"><circle cx="24.4" cy="270.4" r="2.8"/><circle cx="66.4" cy="270.4" r="2.8"/><circle cx="108.4" cy="270.4" r="2.8"/></g>
  <g font-size="3.6" fill="#1a1208" text-anchor="middle"><text x="24.4" y="271.7">1</text><text x="66.4" y="271.7">2</text><text x="108.4" y="271.7">3</text></g>
  <text x="29.5" y="271.7">Prijavi se</text>
  <text x="71.5" y="271.7">Pokaži talent</text>
  <text x="113.5" y="271.7">Nastopi na odru</text>
</g>

<a id="gumb-prijava" xlink:href="https://odiseja-production.up.railway.app/zvezda/#zo-prijava">
  <rect x="22" y="279" width="54" height="14" rx="2.4" fill="url(#gumb)" filter="url(#sence)"/>
  <text x="32.5" y="287.9" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="5.6" fill="#1a1208">Prijavi se</text>
  <path d="M58.5 285.8h8.2M63.8 282.4l3.6 3.4-3.6 3.4" fill="none" stroke="#1a1208" stroke-width=".75" stroke-linecap="round" stroke-linejoin="round"/>
</a>

<g id="qr-prijava">
  <rect x="164" y="240" width="40" height="40" rx="2.2" fill="#ffffff"/>
  <path d="{qpath}" fill="#091c21"/>
  <text x="184" y="285.5" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="3.3" fill="#ffffff">Skeniraj in se prijavi</text>
</g>

<!-- Vodila: izklopljena. Vklopi (display) za kontrolo. Rez = 3 mm znotraj, varno območje = 10 mm znotraj reza. -->
<g id="vodila" display="none" fill="none" stroke-width=".25">
  <rect x="3" y="3" width="220" height="300" stroke="#ff0066"/>
  <rect x="13" y="13" width="200" height="280" stroke="#00b36b" stroke-dasharray="2 1.5"/>
</g>
</svg>
'''
open('zvezda-odiseje-oglas-220x300.svg','w').write(svg)
