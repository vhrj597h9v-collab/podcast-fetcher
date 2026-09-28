"""Carrier: tongue (floats between the head's ears; Hirth ring on its near face; a Tr10 square nut captured in a
slot from the rounded end) + head plate + 5-deg tapered square index boss with a central Tr8 bore for the retaining
thumbscrew.  Modelled in the fork frame (x = phone direction, y = hinge axis, z up, hinge axis at z=0, tongue centred
on y=0) and printed ON ITS BACK (the x = TONGUE_X0 face on the bed): boss up, tongue lying on the bed as a wall, the
retaining bore vertical, the nut slot a horizontal 8.6 mm channel."""
import cadquery as cq
import params as P
from lib import shapes as S


def build_fork_frame() -> cq.Workplane:
    x0, x1 = P.TONGUE_X0, P.TONGUE_X1
    t = P.TONGUE_T
    box = cq.Workplane("XY").box(x1 - x0, t, P.HEADPLATE_Z0, centered=(True, True, False)).translate(((x0 + x1) / 2, 0, 0))   # from the axis up: the cylinder makes a TRUE half-round end
    cyl = cq.Workplane("XZ").circle(P.TONGUE_DOWN).extrude(t / 2, both=True)
    clip = cq.Workplane("XY").box(x1 - x0, t + 2, 200, centered=(True, True, True)).translate(((x0 + x1) / 2, 0, 0))
    tongue = box.union(cyl).intersect(clip)
    # Hirth ring on the near face (y = -t/2), teeth pointing -y (toward the knob-side ear)
    ring = (S.hirth_ring(P.HIRTH_N, P.HIRTH_R0, P.HIRTH_R1, P.HIRTH_SINK, P.HIRTH_INCLUDED_DEG, P.HIRTH_TRUNC)
            .rotate((0, 0, 0), (1, 0, 0), 90)                     # +Z -> -Y
            .translate((0, -t / 2, 0)))
    tongue = tongue.union(ring)
    # nut slot: from below the rounded end up to just past the axis; the 20 x 20 x 8 nut slides in from the end
    sw = P.TILT_NUT + 2 * P.SQ_NUT_CLR
    st = P.TILT_NUT_T + 2 * P.SQ_NUT_CLR
    slot = cq.Workplane("XY").box(sw, st, P.TONGUE_SLOT_TOP + P.TONGUE_DOWN + 2.0, centered=(True, True, False)).translate((0, 0, -P.TONGUE_DOWN - 2.0))
    tongue = tongue.cut(slot)
    # hinge bore
    tongue = tongue.cut(S.gabled_hole_xz(P.TILT_HOLE_NEAR, 60))          # gable roof: horizontal in print
    # head plate
    hp = cq.Workplane("XY").box(x1 - x0, P.HEADPLATE_W, P.HEADPLATE_Z1 - P.HEADPLATE_Z0, centered=(True, True, False)).translate(((x0 + x1) / 2, 0, P.HEADPLATE_Z0))
    body = tongue.union(hp)
    # index boss along +x
    boss = (cq.Workplane("YZ").rect(P.BOSS, P.BOSS).workplane(offset=P.BOSS_LEN).rect(P.BOSS_TIP, P.BOSS_TIP).loft(ruled=True))
    boss = boss.edges().filter(lambda e: abs(e.tangentAt().x) > 0.5).fillet(1.5)
    body = body.union(boss.translate((x1, 0, P.BOSS_Z)))
    # retaining-screw bore along x through head plate and boss
    bore = cq.Workplane("YZ").circle(P.RETAIN_HOLE / 2).extrude(x1 + P.BOSS_LEN - x0 + 2).translate((x0 - 1, 0, P.BOSS_Z))
    return body.cut(bore)


def build() -> cq.Workplane:
    return build_fork_frame().rotate((0, 0, 0), (0, 1, 0), -90)   # +x (use) -> +z (print)
