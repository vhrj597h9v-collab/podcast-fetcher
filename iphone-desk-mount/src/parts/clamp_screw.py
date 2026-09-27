"""Clamp screw: T-bar handle + Tr16x3 thread + neck + ball for the swivel pad.  Prints standing on the bar."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    # T-bar handle (stadium 70 x 18, 16 tall) standing on the bed
    bar = (cq.Workplane("XY").slot2D(P.TBAR_L, P.TBAR_W).extrude(P.TBAR_H)
           .faces(">Z").edges().chamfer(1.5).faces("<Z").edges().chamfer(0.8))
    z0 = P.TBAR_H
    # 45-deg flare from an 18 x 18 pad up to the thread major so the thread root is not a stress raiser
    flare = cq.Workplane("XY").workplane(offset=z0 - 0.01).rect(P.TBAR_W, P.TBAR_W).workplane(offset=2.5).circle(P.SCREW_D / 2 + 0.3).loft(ruled=True)
    thread = th.external_thread(P.SCREW_D, P.SCREW_P, P.SCREW_THREAD_LEN).translate((0, 0, z0 + 2.0))
    z1 = z0 + 2.0 + P.SCREW_THREAD_LEN
    neck = cq.Workplane("XY").circle(P.BALL_NECK_D / 2).extrude(P.BALL_NECK_H + 1.0).translate((0, 0, z1 - 0.5))
    zc = z1 + P.BALL_NECK_H + P.BALL_D / 2 - 1.0
    ball = cq.Workplane("XY").sphere(P.BALL_D / 2).translate((0, 0, zc))
    return bar.union(flare).union(thread).union(neck).union(ball)
