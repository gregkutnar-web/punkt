import base64,sys
S=sys.argv[1]  # scratchpad with bg.jpg, star_gold.png
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
bg=b64(f'{S}/bg.jpg'); star=b64(f'{S}/star_gold.png')
W,H=226,306   # mm: 220x300 + 3 mm porezave na vsaki strani
svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Zvezda Odiseje oglas 220x300 mm + 3 mm porezave (skupaj 226x306 mm). Enota viewBox = 1 mm. Besedilo je živo (Archivo 800/300/700, serif). -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="oder"><path d="M0 0H{W}V186Q113 256 0 186Z"/></clipPath>
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
    <image id="oder-render" x="0" y="0" width="{W}" height="222" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{bg}"/>
  </g>
  <path id="rob-loka" d="M0 186Q113 256 226 186" fill="none" stroke="url(#rob)" stroke-width=".5"/>
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

<g id="besedilo">
  <text id="naslov" x="22" y="246" font-family="Archivo, 'Archivo ExtraBold', Arial, sans-serif" font-weight="800" font-size="15.4" fill="#ffffff">Postani zvezda Odiseje</text>
  <text id="podnaslov" x="22" y="262.5" font-family="'Archivo Light', Archivo, Arial, sans-serif" font-weight="300" font-size="12" fill="#ffffff">in nastopi na velikem odru</text>
</g>

<a id="gumb-prijava" xlink:href="https://odiseja-production.up.railway.app/zvezda/#zo-prijava">
  <rect x="22" y="274" width="54" height="14.5" rx="2.4" fill="url(#gumb)" filter="url(#sence)"/>
  <text x="32.5" y="283.4" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="5.6" fill="#1a1208">Prijavi se</text>
  <path d="M58.5 281.3h8.2M63.8 277.9l3.6 3.4-3.6 3.4" fill="none" stroke="#1a1208" stroke-width=".75" stroke-linecap="round" stroke-linejoin="round"/>
</a>

<g id="logotip-zvezda-odiseje">
  <image id="zvezda-ikona" x="181" y="262" width="24" height="15.9" xlink:href="data:image/png;base64,{star}"/>
  <text id="zvezda-napis" x="193" y="288" text-anchor="middle" font-family="'Times New Roman', Georgia, serif" font-weight="400" font-size="7.4" letter-spacing=".25" fill="url(#zlato)">ZVEZDA</text>
  <text id="odiseje-napis" x="193" y="292.3" text-anchor="middle" font-family="'Times New Roman', Georgia, serif" font-weight="700" font-size="3.1" letter-spacing=".5" fill="url(#zlato)">ODISEJE</text>
</g>

<!-- Vodila: izklopljena. Vklopi (display) za kontrolo. Rez = 3 mm znotraj, varno območje = 10 mm znotraj reza. -->
<g id="vodila" display="none" fill="none" stroke-width=".25">
  <rect x="3" y="3" width="220" height="300" stroke="#ff0066"/>
  <rect x="13" y="13" width="200" height="280" stroke="#00b36b" stroke-dasharray="2 1.5"/>
</g>
</svg>
'''
open('zvezda-odiseje-oglas-220x300.svg','w').write(svg)
