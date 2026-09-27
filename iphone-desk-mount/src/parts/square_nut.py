"""Square nut for the Tr8x2 thumbscrews (x3).  Prints flat."""
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    n = cq.Workplane("XY").box(P.SQ_NUT, P.SQ_NUT, P.SQ_NUT_T, centered=(True, True, False)).edges("|Z").chamfer(1.0)
    n = n.cut(th.internal_thread_cutter(P.TS_D, P.TS_P, P.SQ_NUT_T, P.TS_CLR))
    ch = th.nut_entry_chamfer_cutter(P.TS_D, P.TS_P, P.TS_CLR, depth=0.6)
    return n.cut(ch).cut(ch.mirror("XY").translate((0, 0, P.SQ_NUT_T)))
