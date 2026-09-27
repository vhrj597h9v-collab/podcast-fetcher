"""Captured nut block for the clamp screw (Tr16x3).  Prints flat (thread axis vertical)."""
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    n = P.NUT_BLOCK
    h = P.NUT_BLOCK_H
    blk = cq.Workplane("XY").box(n, n, h, centered=(True, True, False)).edges("|Z").chamfer(1.5)
    blk = blk.cut(th.internal_thread_cutter(P.SCREW_D, P.SCREW_P, h, P.THREAD_CLR))
    ch = th.nut_entry_chamfer_cutter(P.SCREW_D, P.SCREW_P, P.THREAD_CLR)
    blk = blk.cut(ch).cut(ch.mirror("XY").translate((0, 0, h)))
    return blk
