#!/usr/bin/env python3
"""Zgradi samostojni monday-party.html iz src/monday.{html,css,js} + vdelani Monday logotip."""
import pathlib, re
R = pathlib.Path(__file__).parent
S = R / 'src'
svg = pathlib.Path(R / 'assets' / 'monday.svg').read_text()
svg = re.sub(r'<\?xml.*?\?>|<!--.*?-->', '', svg, flags=re.S).strip()
svg = re.sub(r'width="800px" height="800px" viewBox="[^"]*"', 'viewBox="0 -2 512 98"', svg)
svg = svg.replace('preserveAspectRatio="xMidYMid"', 'preserveAspectRatio="xMinYMid meet"')
page = (S / 'monday.html').read_text()
for k, v in {'__STYLE__': (S / 'monday.css').read_text(), '__JS__': (S / 'monday.js').read_text(), '__LOGO__': svg}.items():
    page = page.replace(k, v)
(R / 'monday-party.html').write_text(page)
print('monday-party.html', round(len(page) / 1024), 'KB')
