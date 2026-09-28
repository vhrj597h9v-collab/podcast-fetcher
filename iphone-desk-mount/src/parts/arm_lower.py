"""Lower arm: diamond-oriented external taper (plugs into the clamp socket) -> circle -> square tube aligned with the
desk edge -> cap -> elbow fork (two ears, Hirth ring on the near ear).  Prints standing on the taper end."""
import cadquery as cq
import params as P
from lib import shapes as S


def _sk_rect(w, d, r, z, rot=0.0):
    return cq.Sketch().rect(w, d).vertices().fillet(r).moved(cq.Location(cq.Vector(0, 0, z), cq.Vector(0, 0, 1), rot))


def _sk_circle(dia, z):
    return cq.Sketch().circle(dia / 2).moved(cq.Location(cq.Vector(0, 0, z)))


def _loft(*sks, ruled=True):
    return cq.Workplane("XY").placeSketch(*sks).loft(ruled=ruled)


def build() -> cq.Workplane:
    r = P.POLE_CORNER_R
    z1 = P.EXT_TAPER_LEN
    z2 = z1 + P.ARM_TWIST_H1
    z3 = z2 + P.ARM_TWIST_H2
    z_top = P.ARM_LOWER_H
    z_ear0 = z_top - (P.ELBOW_AXIS_ABOVE_CAP + P.ELBOW_EAR_TOP_R)   # cap top / ear root
    z_cap0 = z_ear0 - P.ELBOW_CAP_T
    z_tube1 = z_cap0 - P.ELBOW_FLARE_H
    za = z_ear0 + P.ELBOW_AXIS_ABOVE_CAP
    # outer body
    base = _loft(_sk_rect(P.EXT_TAPER_BOTTOM, P.EXT_TAPER_BOTTOM, r, 0.0, 45), _sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z1, 45))
    t1 = _loft(_sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z1, 45), _sk_circle(P.POLE_OUTER, z2), ruled=False)
    t2 = _loft(_sk_circle(P.POLE_OUTER, z2), _sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z3), ruled=False)
    tube = _loft(_sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z3), _sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z_tube1))
    cap = _loft(_sk_rect(P.POLE_OUTER, P.POLE_OUTER, r, z_tube1), _sk_rect(P.ELBOW_CAP_X, P.ELBOW_CAP_Y, P.ELBOW_CAP_R, z_cap0),
                _sk_rect(P.ELBOW_CAP_X, P.ELBOW_CAP_Y, P.ELBOW_CAP_R, z_ear0))
    body = base.union(t1).union(t2).union(tube).union(cap)
    # ears (fork axis along y), rounded tops
    def ear(y0, y1):
        t = y1 - y0
        box = cq.Workplane("XY").box(P.ELBOW_EAR_W, t, za - z_ear0, centered=(True, True, False)).translate((0, (y0 + y1) / 2, z_ear0))
        cyl = cq.Workplane("XZ").circle(P.ELBOW_EAR_TOP_R).extrude(t / 2, both=True).translate((0, (y0 + y1) / 2, za))
        return box.union(cyl)
    near = ear(-P.ELBOW_EAR_GAP / 2 - P.ELBOW_EAR_T, -P.ELBOW_EAR_GAP / 2)
    far = ear(P.ELBOW_EAR_GAP / 2, P.ELBOW_EAR_GAP / 2 + P.ELBOW_EAR_T)
    ring = (S.hirth_ring(P.ELBOW_HIRTH_N, P.ELBOW_HIRTH_R0, P.ELBOW_HIRTH_R1, P.HIRTH_SINK, P.HIRTH_INCLUDED_DEG, P.HIRTH_TRUNC)
            .rotate((0, 0, 0), (1, 0, 0), -90).translate((0, -P.ELBOW_EAR_GAP / 2, za)))
    body = body.union(near).union(far).union(ring)
    body = body.cut(S.gabled_hole_xz(P.ELBOW_HOLE, 160).translate((0, 0, za)))   # gable roof: 16.8 mm horizontal hole
    # cavities: round bore through base + twist, 45-deg transition to the 44 square tube cavity, pyramid roof under the cap
    bore = cq.Workplane("XY").circle(P.ARM_BASE_BORE_D / 2).extrude(z3 + 2).translate((0, 0, -1))
    z_c1 = z3 + (P.POLE_INNER - P.ARM_BASE_BORE_D) / 2 + 1.0            # 45-deg-ish widening
    z_roof0 = z_tube1 - 4.0 - (P.POLE_INNER - 2.0) / 2
    cav = _loft(_sk_circle(P.ARM_BASE_BORE_D, z3 - 0.5), _sk_rect(P.POLE_INNER, P.POLE_INNER, 3.0, z_c1), ruled=False)
    cav2 = _loft(_sk_rect(P.POLE_INNER, P.POLE_INNER, 3.0, z_c1 - 0.01), _sk_rect(P.POLE_INNER, P.POLE_INNER, 3.0, z_roof0),
                 _sk_rect(2.0, 2.0, 0.5, z_tube1 - 4.0))
    body = body.cut(bore).cut(cav).cut(cav2)
    body = body.faces("<Z").chamfer(1.0)
    return body
