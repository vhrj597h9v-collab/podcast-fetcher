"""Clamp screw: scalloped knob + Tr16x3 thread + neck + ball for the swivel pad.  Prints standing on the knob."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    knob = cq.Workplane("XY").circle(P.KNOB_D / 2).extrude(P.KNOB_H)
    r_s = P.KNOB_D / 2 + 1.0
    for i in range(P.KNOB_LOBES):
        a = 2 * math.pi * i / P.KNOB_LOBES
        knob = knob.cut(cq.Workplane("XY").circle(5.5).extrude(P.KNOB_H + 2).translate((r_s * math.cos(a), r_s * math.sin(a), -1)))
    knob = knob.faces(">Z").edges().chamfer(1.0).faces("<Z").edges().chamfer(0.8)
    z0 = P.KNOB_H
    thread = th.external_thread(P.SCREW_D, P.SCREW_P, P.SCREW_THREAD_LEN).translate((0, 0, z0))
    z1 = z0 + P.SCREW_THREAD_LEN
    neck = cq.Workplane("XY").circle(P.BALL_NECK_D / 2).extrude(P.BALL_NECK_H + 1.0).translate((0, 0, z1 - 0.5))
    zc = z1 + P.BALL_NECK_H + P.BALL_D / 2 - 1.0
    ball = cq.Workplane("XY").sphere(P.BALL_D / 2).translate((0, 0, zc))
    # small collar so the thread run-out sits on a solid shoulder
    collar = cq.Workplane("XY").circle(P.SCREW_D / 2 + 2).extrude(2.0).translate((0, 0, z0 - 0.01)).faces(">Z").chamfer(1.5)
    return knob.union(collar).union(thread).union(neck).union(ball)
