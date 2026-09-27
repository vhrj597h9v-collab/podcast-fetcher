"""Shared thumbscrew builder: T-bar handle + trapezoidal thread, prints standing on the bar."""
import cadquery as cq
import params as P
from lib import threads as th


def thumbscrew(length: float, bar_l: float = None, bar_w: float = None, bar_h: float = None,
               d: float = None, p: float = None) -> cq.Workplane:
    bl = bar_l or P.TS_TBAR_L
    bw = bar_w or P.TS_TBAR_W
    bh = bar_h or P.TS_TBAR_H
    d = d or P.TS_D
    p = p or P.TS_P
    bar = (cq.Workplane("XY").slot2D(bl, bw).extrude(bh)
           .faces(">Z").edges().chamfer(1.0).faces("<Z").edges().chamfer(0.6))
    flare = (cq.Workplane("XY").workplane(offset=bh - 0.01).rect(bw, bw)
             .workplane(offset=2.0).circle(d / 2 + 0.3).loft(ruled=True))
    thread = th.external_thread(d, p, length).translate((0, 0, bh + 1.5))
    return bar.union(flare).union(thread)
