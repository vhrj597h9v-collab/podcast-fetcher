"""Square nut 26 x 26 x 14 for the Tr16x3 elbow screw, captured in the elbow tongue.  Prints flat."""
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    n = cq.Workplane("XY").box(P.ELBOW_NUT, P.ELBOW_NUT, P.ELBOW_NUT_T, centered=(True, True, False)).edges("|Z").chamfer(1.5).faces("<Z").chamfer(0.6)
    n = n.cut(th.internal_thread_cutter(P.ELBOW_D, P.ELBOW_P, P.ELBOW_NUT_T, P.ELBOW_CLR))
    ch = th.nut_entry_chamfer_cutter(P.ELBOW_D, P.ELBOW_P, P.ELBOW_CLR)
    return n.cut(ch).cut(ch.mirror("XY").translate((0, 0, P.ELBOW_NUT_T)))
