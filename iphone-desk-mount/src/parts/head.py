"""Head: standard socket at the bottom (prints mouth-down like a pole segment), 45-deg flare to a wider cap,
and a two-ear fork rotated 45 deg relative to the socket (the pole runs diamond-wise in the clamp, so this
makes the phone face square to the desk edge).  Tilt lock = Tr8 thumbscrew through both ears + square nut in a
diamond pocket on the thick ear; the carrier tongue's proud rings are clamped between the ears (friction)."""
import cadquery as cq
import params as P
from parts.pole_segment import _loft


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
    ear_a = ear(-P.EAR_GAP / 2 - P.EAR_T, -P.EAR_GAP / 2)         # plain ear (knob side)
    ear_b = ear(P.EAR_GAP / 2, P.EAR_GAP / 2 + P.EAR_NUT_T)        # nut ear
    fork = ear_a.union(ear_b)
    # hinge hole through both ears
    hole = cq.Workplane("XZ").circle(P.TS_HOLE / 2).extrude(60, both=True).translate((0, 0, za))
    fork = fork.cut(hole)
    # diamond nut pocket on the outer face of the nut ear (axis y, horizontal in print -> 45-deg roof)
    s = P.SQ_NUT + 2 * P.SQ_NUT_CLR
    depth = P.SQ_NUT_T + 0.4
    y_out = P.EAR_GAP / 2 + P.EAR_NUT_T
    pocket = (cq.Workplane("XZ").rect(s, s).extrude(depth + 1.0).rotate((0, 0, 0), (0, 1, 0), 45)
              .translate((0, y_out + 1.0 - 0.0, za)))
    # Workplane("XZ") extrudes toward -Y; we want the pocket to go from y_out inward: shift so it spans [y_out-depth, y_out+1]
    pocket = cq.Workplane("XZ").workplane(offset=-(y_out + 1.0)).rect(s, s).extrude(depth + 1.0)  # extrude toward -Y from y_out+1
    pocket = pocket.rotate((0, 0, 0), (0, 1, 0), 45).translate((0, 0, za))
    fork = fork.cut(pocket)
    # small 45-deg fillet-like chamfers where the ears meet the cap are not needed (ears sit on the flat cap).
    fork = fork.rotate((0, 0, 0), (0, 0, 1), P.FORK_ROT_DEG)
    return head.union(fork)
