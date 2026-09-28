"""Elbow tongue: tongue with the mating Hirth ring and a captured Tr16 nut, flaring into a standard spigot.
Built and printed standing on the spigot TIP (z=0); in use it is flipped: spigot up into the next segment, tongue
down between the arm_lower ears.  The ring is on the +y face here so it faces the near (-y) ear after the flip."""
import cadquery as cq
import params as P
from lib import shapes as S


def _sk_rect(w, d, r, z):
    return cq.Sketch().rect(w, d).vertices().fillet(r).moved(cq.Location(cq.Vector(0, 0, z)))


def build() -> cq.Workplane:
    z_sp = P.SPIGOT_LEN
    z_fl = z_sp + P.ELBOW_FLARE2_H
    za = z_fl + P.ELBOW_TONGUE_UP
    T = P.ELBOW_TONGUE_T
    spig = cq.Workplane("XY").placeSketch(_sk_rect(P.SPIGOT_TIP, P.SPIGOT_TIP, P.SPIGOT_CORNER_R, 0.0),
                                          _sk_rect(P.SPIGOT_BASE, P.SPIGOT_BASE, P.SPIGOT_CORNER_R, z_sp)).loft(ruled=True)
    flare = cq.Workplane("XY").placeSketch(_sk_rect(P.SPIGOT_BASE, P.SPIGOT_BASE, P.SPIGOT_CORNER_R, z_sp),
                                           _sk_rect(P.ELBOW_EAR_W, T, 3.0, z_fl)).loft(ruled=True)
    box = cq.Workplane("XY").box(P.ELBOW_EAR_W, T, za - z_fl, centered=(True, True, False)).translate((0, 0, z_fl))
    cyl = cq.Workplane("XZ").circle(P.ELBOW_TONGUE_R).extrude(T / 2, both=True).translate((0, 0, za))
    clip = cq.Workplane("XY").box(P.ELBOW_EAR_W, T + 2, 400, centered=(True, True, True))
    body = spig.union(flare).union(box).union(cyl.intersect(clip))
    ring = (S.hirth_ring(P.ELBOW_HIRTH_N, P.ELBOW_HIRTH_R0, P.ELBOW_HIRTH_R1, P.HIRTH_SINK, P.HIRTH_INCLUDED_DEG, P.HIRTH_TRUNC)
            .rotate((0, 0, 0), (1, 0, 0), -90).translate((0, T / 2, za)))     # +Z -> +Y, on the +y face
    body = body.union(ring)
    # nut slot from the rounded end (print top) down past the axis
    sw = P.ELBOW_NUT + 2 * P.SQ_NUT_CLR
    st = P.ELBOW_NUT_T + 2 * P.SQ_NUT_CLR
    slot = cq.Workplane("XY").box(sw, st, P.ELBOW_TONGUE_R + P.ELBOW_TONGUE_SLOT_TOP + 2.0, centered=(True, True, False)).translate((0, 0, za - P.ELBOW_TONGUE_SLOT_TOP))
    body = body.cut(slot)
    body = body.cut(S.gabled_hole_xz(P.ELBOW_HOLE, 60).translate((0, 0, za)))     # gable roof: horizontal hole in print
    body = body.faces("<Z").chamfer(1.0)
    return body
