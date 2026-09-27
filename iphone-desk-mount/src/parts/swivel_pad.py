"""Swivel pressure pad: snaps over the screw ball.  Prints with the flat desk face on the bed, socket opening up."""
import math
import cadquery as cq
import params as P


def build() -> cq.Workplane:
    r_cav = P.BALL_D / 2 + P.PAD_SOCKET_CLR            # 7.2
    opening = P.BALL_D - 2 * P.PAD_SNAP_OVERLAP        # 13.2: retains the 14 ball with a gentle 0.4/side snap; the 10 neck swivels +-18 deg
    d = math.sqrt(r_cav ** 2 - (opening / 2) ** 2)     # centre depth below the top face
    h = P.PAD_H + 2.0                                  # 14
    zc = h - d
    pad = cq.Workplane("XY").circle(P.PAD_D / 2).extrude(h).faces(">Z").edges().chamfer(1.5).faces("<Z").edges().chamfer(0.8)
    pad = pad.cut(cq.Workplane("XY").sphere(r_cav).translate((0, 0, zc)))
    # 4 radial flex slots around the opening
    for i in range(P.PAD_SLOTS):
        slot = cq.Workplane("XY").box(12.0, 1.0, 7.0, centered=(False, True, False)).translate((opening / 2 - 4.0, 0, h - 6.0))
        pad = pad.cut(slot.rotate((0, 0, 0), (0, 0, 1), 360.0 * i / P.PAD_SLOTS + 30))
    return pad
