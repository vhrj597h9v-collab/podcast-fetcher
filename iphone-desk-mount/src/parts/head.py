"""Head: standard socket at the bottom (prints mouth-down like a pole segment), 45-deg flare to a wider cap, and a
two-ear fork rotated 45 deg relative to the socket (the pole runs diamond-wise in the clamp, so this makes the phone
face square to the desk edge).  Tilt lock = Hirth ring on the knob-side ear's inner face; the carrier tongue (with
the mating ring and a captured Tr10 nut) is pulled onto it by the tilt thumbscrew -> positive 12-degree index,
zero play.  The far ear only guides the screw shank."""
import cadquery as cq
import params as P
from parts.pole_segment import _loft
from lib import shapes as S


def build() -> cq.Workplane:
    z0f = P.HEAD_FLARE_Z0
    top = P.HEAD_TOP
    outer = _loft([
        (0.0, P.HEAD_BASE, P.POLE_CORNER_R),
        (z0f, P.HEAD_BASE, P.POLE_CORNER_R),
        (z0f + P.HEAD_FLARE_H, P.HEAD_CAP, P.HEAD_CAP_R),
        (top, P.HEAD_CAP, P.HEAD_CAP_R),
    ])
    sock_r = P.SPIGOT_CORNER_R - 0.4
    roof_top = P.SOCKET_DEPTH + (P.SOCKET_BOTTOM - 2.0) / 2      # 45-deg pyramid roof ending in a 2 mm square
    cavity = _loft([
        (-1.0, P.SOCKET_MOUTH + 2 * 1.0 * P.TAN_T, sock_r),
        (P.SOCKET_DEPTH, P.SOCKET_BOTTOM, sock_r),
        (roof_top, 2.0, 0.5),
    ])
    head = outer.cut(cavity).faces("<Z").chamfer(1.0)

    # ---- fork in its own frame (x = phone direction, y = hinge axis), rotated FORK_ROT_DEG afterwards ----
    za = top + P.TILT_AXIS_H
    def ear(y0, y1):
        t = y1 - y0
        box = cq.Workplane("XY").box(P.EAR_W, t, za - top, centered=(True, True, False)).translate((0, (y0 + y1) / 2, top))
        cyl = cq.Workplane("XZ").circle(P.EAR_TOP_R).extrude(t / 2, both=True).translate((0, (y0 + y1) / 2, za))
        return box.union(cyl)
    near = ear(-P.EAR_GAP / 2 - P.EAR_T, -P.EAR_GAP / 2)          # knob side, carries the Hirth ring
    far = ear(P.EAR_GAP / 2, P.EAR_GAP / 2 + P.EAR_T)
    fork = near.union(far)
    # Hirth ring on the near ear's inner face (y = -EAR_GAP/2), teeth pointing +y into the gap
    ring = (S.hirth_ring(P.HIRTH_N, P.HIRTH_R0, P.HIRTH_R1, P.HIRTH_SINK, P.HIRTH_INCLUDED_DEG, P.HIRTH_TRUNC)
            .rotate((0, 0, 0), (1, 0, 0), -90)                    # +Z -> +Y
            .translate((0, -P.EAR_GAP / 2, za)))
    fork = fork.union(ring)
    # hinge hole through both ears (10.8: knob-side clearance; far ear guides the Tr10 shank)
    fork = fork.cut(S.gabled_hole_xz(P.TILT_HOLE_NEAR, 120).translate((0, 0, za)))   # gable roof: horizontal in print
    fork = fork.rotate((0, 0, 0), (0, 0, 1), P.FORK_ROT_DEG)
    return head.union(fork)
