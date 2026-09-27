"""Square nut 20 x 20 x 8 for the Tr10x2.5 tilt thumbscrew, captured in the carrier tongue.  Prints flat."""
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    n = cq.Workplane("XY").box(P.TILT_NUT, P.TILT_NUT, P.TILT_NUT_T, centered=(True, True, False)).edges("|Z").chamfer(1.0)
    n = n.cut(th.internal_thread_cutter(P.TILT_D, P.TILT_P, P.TILT_NUT_T, P.TILT_CLR))
    ch = th.nut_entry_chamfer_cutter(P.TILT_D, P.TILT_P, P.TILT_CLR, depth=0.8)
    return n.cut(ch).cut(ch.mirror("XY").translate((0, 0, P.TILT_NUT_T)))
