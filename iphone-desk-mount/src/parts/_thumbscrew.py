"""Shared Tr8x2 thumbscrew builder (prints standing on the knob)."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def thumbscrew(length: float, knob_d: float = None) -> cq.Workplane:
    kd = knob_d or P.TS_KNOB_D
    knob = cq.Workplane("XY").circle(kd / 2).extrude(P.TS_KNOB_H)
    r_s = kd / 2 + 0.5
    for i in range(P.TS_KNOB_LOBES):
        a = 2 * math.pi * i / P.TS_KNOB_LOBES
        knob = knob.cut(cq.Workplane("XY").circle(kd * 0.14).extrude(P.TS_KNOB_H + 2).translate((r_s * math.cos(a), r_s * math.sin(a), -1)))
    knob = knob.faces(">Z").edges().chamfer(0.8).faces("<Z").edges().chamfer(0.6)
    collar = cq.Workplane("XY").circle(P.TS_D / 2 + 1.5).extrude(1.5).translate((0, 0, P.TS_KNOB_H - 0.01)).faces(">Z").chamfer(1.0)
    thread = th.external_thread(P.TS_D, P.TS_P, length).translate((0, 0, P.TS_KNOB_H))
    return knob.union(collar).union(thread)
