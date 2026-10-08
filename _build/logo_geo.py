#!/usr/bin/env python3
"""Redraws the BlueTech Sanitaire wordmark as clean geometric strokes.
Letter boxes and stroke widths were measured on the client's logo (_build/measure.py),
so the shapes match the original while the outlines stay perfectly smooth at any size."""
import math, os

W, w = 14.6, 9.5          # stroke widths: BlueTech / Sanitaire
h, hs = W / 2, w / 2


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def P(*pts):
    return " ".join(f(p) for p in pts)


def ell(cx, cy, rx, ry, a):
    a = math.radians(a)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


def e_glyph(x0, y0, x1, y1, sw, end=38):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2 - sw / 2, (y1 - y0) / 2 - sw / 2
    ex, ey = ell(cx, cy, rx, ry, end)
    return "M%s H%s A%s 0 1 0 %s" % (P(cx - rx, cy), f(cx + rx), P(rx, ry), P(ex, ey))


def c_glyph(x0, y0, y1, sw, rx_ratio=0.93, a=40):
    ry = (y1 - y0) / 2 - sw / 2
    rx = ry * rx_ratio
    cx, cy = x0 + sw / 2 + rx, (y0 + y1) / 2
    sx, sy = ell(cx, cy, rx, ry, -a)
    ex, ey = ell(cx, cy, rx, ry, a)
    return "M%s A%s 0 1 0 %s" % (P(sx, sy), P(rx, ry), P(ex, ey))


def bowl(x0, y0, x1, y1, sw):
    """single-storey a: round bowl + stem on the right"""
    sx = x1 - sw / 2
    top, bot = y0 + sw / 2, y1 - sw / 2
    rx, ry = (sx - (x0 + sw / 2)) / 2, (bot - top) / 2
    cx, cy = x0 + sw / 2 + rx, (top + bot) / 2
    return "M%s A%s 0 1 0 %s A%s 0 1 0 %s M%s V%s" % (P(cx - rx, cy), P(rx, ry), P(cx + rx, cy), P(rx, ry), P(cx - rx, cy), P(sx, top), f(bot))


blue = []
# B
x0, x1, top, bot = 14.5 + h, 92 - h, 22.5 + h, 119.8 - h
ym = top + (bot - top) * 0.465
xu = x1 - 6.5
ru, rl = min(16, (ym - top) / 2), min(19, (bot - ym) / 2)
blue.append("M%s V%s" % (P(x0, top), f(bot)))
blue.append("M%s H%s A%s 0 0 1 %s V%s A%s 0 0 1 %s H%s" % (P(x0, top), f(xu - ru), P(ru, ru), P(xu, top + ru), f(ym - ru), P(ru, ru), P(xu - ru, ym), f(x0)))
blue.append("M%s H%s A%s 0 0 1 %s V%s A%s 0 0 1 %s H%s" % (P(x0, ym), f(x1 - rl), P(rl, rl), P(x1, ym + rl), f(bot - rl), P(rl, rl), P(x1 - rl, bot), f(x0)))
# l (tailed)
lx, lt, lb, lr = 103.8 + h, 16 + h, 120.2 - h, 129.8 - h
rt = lr - lx
blue.append("M%s V%s A%s 0 0 0 %s" % (P(lx, lt), f(lb - rt), P(rt, rt), P(lr, lb)))
# u
ux0, ux1, ut, ub = 138.2 + h, 204.5 - h, 46.8 + h, 121.2 - h
ur = (ux1 - ux0) / 2
blue.append("M%s V%s A%s 0 0 0 %s M%s V%s" % (P(ux0, ut), f(ub - ur), P(ur, ur), P(ux1, ub - ur), P(ux1, ut), f(ub)))
# e
blue.append(e_glyph(215.8, 46.5, 286.2, 121.0, W))
# T
blue.append("M%s H%s M%s V%s" % (P(283.5 + h, 22.5 + h), f(361.8 - h), P((283.5 + 361.8) / 2, 22.5 + h), f(120.2 - h)))
# e
blue.append(e_glyph(351.5, 46.5, 422.0, 121.5, W))
# c
blue.append(c_glyph(429.0, 46.2, 121.0, W))
# h
hx0, hx1, ht, hb, hxt = 503.8 + h, 569.5 - h, 16.8 + h, 120.5 - h, 46.5 + h
hr = (hx1 - hx0) / 2
blue.append("M%s V%s M%s A%s 0 0 1 %s V%s" % (P(hx0, ht), f(hb), P(hx0, hxt + hr), P(hr, hr), P(hx1, hxt + hr), f(hb)))

grey, dots = [], []
# S — two stacked loops
sx0, sx1, st, sb = 113.5 + hs, 161 - hs, 142 + hs, 206 - hs
cxm, mid = (sx0 + sx1) / 2 + 0.6, (st + sb) / 2
ryu, ryl = (mid - st) / 2, (sb - mid) / 2
rxu, rxl = (sx1 - sx0) / 2 * 0.92, (sx1 - sx0) / 2
p0 = ell(cxm, st + ryu, rxu, ryu, -28)
p2 = ell(cxm, mid + ryl, rxl, ryl, 152)
grey.append("M%s A%s 0 1 0 %s A%s 0 1 1 %s" % (P(*p0), P(rxu, ryu), P(cxm, mid), P(rxl, ryl), P(*p2)))
# a
grey.append(bowl(166.0, 157.8, 213.8, 206.2, w))
# n
nx0, nx1, nt, nb = 224.8 + hs, 268 - hs, 157.5 + hs, 205.5 - hs
nr = (nx1 - nx0) / 2
grey.append("M%s V%s M%s A%s 0 0 1 %s V%s" % (P(nx0, nt), f(nb), P(nx0, nt + nr), P(nr, nr), P(nx1, nt + nr), f(nb)))
# i
grey.append("M%s V%s" % (P(284.25, 158.2 + hs), f(205.8 - hs)))
dots.append((284.25, 145.5, 6.6))
# t
tx, tt, tb, tr = 308.5, 147 + hs, 206.2 - hs, 327.5 - hs
trr = tr - tx
grey.append("M%s V%s A%s 0 0 0 %s M%s H%s" % (P(tx, tt), f(tb - trr), P(trr, trr), P(tr, tb), P(295.8 + hs, 157.8 + hs), f(321)))
# a
grey.append(bowl(330.0, 157.8, 378.0, 206.2, w))
# i
grey.append("M%s V%s" % (P(394.1, 158.5 + hs), f(205.5 - hs)))
dots.append((394.3, 145.5, 6.5))
# r
rx_, rt_, rb_, rr_ = 410.8 + hs, 157.8 + hs, 205.5 - hs, 439.2 - hs
rrad = rr_ - rx_
grey.append("M%s V%s M%s A%s 0 0 1 %s" % (P(rx_, rt_), f(rb_), P(rx_, rt_ + rrad), P(rrad, rrad), P(rr_, rt_)))
# e
grey.append(e_glyph(441.2, 157.8, 488.0, 206.0, w))

VB = "8 10 568 202"
DB, DG = " ".join(blue), " ".join(grey)
DOTS = "".join('<circle cx="%s" cy="%s" r="%s"/>' % (f(x), f(y), f(r)) for x, y, r in dots)


def svg(b="#2A5598", s="#9AA0AC", attrs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s"%s><g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            '<path stroke="%s" stroke-width="%s" d="%s"/><path stroke="%s" stroke-width="%s" d="%s"/></g><g fill="%s">%s</g></svg>') % (
        VB, attrs, b, W, DB, s, w, DG, s, DOTS)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(root, "docs", "assets", "img", "logo.svg"), "w").write(svg())
    print(len(DB) + len(DG), "chars")
