#!/usr/bin/env python3
"""Vektorizira logotip (PNG z alfa kanalom) v SVG pot; potrebuje paket `potracer`.

Uporaba: PYTHONPATH=<mapa_s_potracer> python3 tools/trace_logo.py <logo.png> <izhod.json>
Izhod: {"w": ..., "h": ..., "d": "<pot>"} v pikslih obrezane slike.
"""
import json
import sys

import numpy as np
import potrace
from PIL import Image

im = Image.open(sys.argv[1]).convert("RGBA")
im = im.crop(im.getbbox())
mask = np.array(im.getchannel("A")) > 127
bm = potrace.Bitmap(~mask)  # potracer sledi nasprotni vrednosti
plist = bm.trace(turdsize=3, alphamax=1.0, opticurve=True, opttolerance=0.2)
d = []
for curve in plist:
    sp = curve.start_point
    d.append(f"M{sp.x:.2f} {sp.y:.2f}")
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f"L{seg.c.x:.2f} {seg.c.y:.2f}L{seg.end_point.x:.2f} {seg.end_point.y:.2f}")
        else:
            d.append(f"C{seg.c1.x:.2f} {seg.c1.y:.2f} {seg.c2.x:.2f} {seg.c2.y:.2f} {seg.end_point.x:.2f} {seg.end_point.y:.2f}")
    d.append("Z")
json.dump({"w": im.width, "h": im.height, "d": "".join(d)}, open(sys.argv[2], "w"))
print(im.size, len(curve.segments), "krivulj:", len(plist))
