"""Elbow lock screw: Tr16x3 with a 60 x 16 T-bar, 56 mm thread.  Prints standing on the bar."""
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    bar = (cq.Workplane("XY").slot2D(P.ELBOW_TBAR_L, P.ELBOW_TBAR_W).extrude(P.ELBOW_TBAR_H)
           .faces(">Z").edges().chamfer(1.5).faces("<Z").edges().chamfer(0.8))
    flare = (cq.Workplane("XY").workplane(offset=P.ELBOW_TBAR_H - 0.01).rect(P.ELBOW_TBAR_W, P.ELBOW_TBAR_W)
             .workplane(offset=2.5).circle(P.ELBOW_D / 2 + 0.3).loft(ruled=True))
    thread = th.external_thread(P.ELBOW_D, P.ELBOW_P, P.ELBOW_THREAD_LEN).translate((0, 0, P.ELBOW_TBAR_H + 2.0))
    return bar.union(flare).union(thread)
