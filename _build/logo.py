#!/usr/bin/env python3
"""One-off: vectorises the client's logo (_src/...6.20.42 PM.jpeg) into docs/assets/img/logo-*.svg"""
import os, numpy as np, potrace
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = Image.open(os.path.join(ROOT, "_src", "WhatsApp Image 2026-10-04 at 6.20.42 PM.jpeg")).convert("RGB")
im = im.crop((220, 420, 810, 640))
S = 4
im = im.resize((im.width * S, im.height * S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
blue = (b - r > 38) & (b < 235)
yy = np.arange(a.shape[0])[:, None] * np.ones((1, a.shape[1]))
grey = (~blue) & (r < 205) & (abs(r - b) < 40) & (yy > 128 * S)
# sample colours
print("blue avg", a[blue].mean(0).round(), "grey avg", a[grey].mean(0).round())
def trace(mask):
    bm = potrace.Bitmap(~mask)
    pl = bm.trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    for c in pl:
        x, y = c.start_point.x, c.start_point.y
        s = "M%.1f %.1f" % (x / S, y / S)
        for seg in c.segments:
            if seg.is_corner:
                s += "L%.1f %.1fL%.1f %.1f" % (seg.c.x / S, seg.c.y / S, seg.end_point.x / S, seg.end_point.y / S)
            else:
                s += "C%.1f %.1f %.1f %.1f %.1f %.1f" % (seg.c1.x / S, seg.c1.y / S, seg.c2.x / S, seg.c2.y / S, seg.end_point.x / S, seg.end_point.y / S)
        d.append(s + "Z")
    return "".join(d)
db, dg = trace(blue), trace(grey)
# bbox
ys, xs = np.where(blue | grey)
x0, y0, x1, y1 = xs.min() / S, ys.min() / S, xs.max() / S, ys.max() / S
vb = "%.1f %.1f %.1f %.1f" % (x0 - 2, y0 - 2, x1 - x0 + 4, y1 - y0 + 4)
ysb, xsb = np.where(blue)
vb_word = "%.1f %.1f %.1f %.1f" % (xsb.min() / S - 2, ysb.min() / S - 2, (xsb.max() - xsb.min()) / S + 4, (ysb.max() - ysb.min()) / S + 4)
print("viewBox", vb, "word", vb_word)
out = os.path.join(ROOT, "docs", "assets", "img")
open(os.path.join(out, "logo.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s"><path fill="#2A5598" fill-rule="evenodd" d="%s"/><path fill="#9AA0AC" fill-rule="evenodd" d="%s"/></svg>' % (vb, db, dg))
open(os.path.join(ROOT, "_build", "logo-paths.txt"), "w").write(vb + "\n" + db + "\n" + dg + "\n")
print(len(db), len(dg))
