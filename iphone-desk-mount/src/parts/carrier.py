"""Carrier: tongue (hangs between the head's ears) + head plate + 5-deg tapered square index boss with a
central Tr8 bore for the retaining thumbscrew.  Modelled in the fork frame (x = phone direction, y = hinge axis,
z up, hinge axis at z=0) and printed ON ITS BACK (the x = TONGUE_X0 face on the bed) so the boss points up and
the tongue lies on the bed as a wall; the retaining bore is vertical in print."""
import math
import cadquery as cq
import params as P


def build_fork_frame() -> cq.Workplane:
    x0, x1 = P.TONGUE_X0, P.TONGUE_X1
    t = P.TONGUE_T
    # tongue: box + rounded bottom (cylinder about the hinge axis), clipped to x >= x0
    box = cq.Workplane("XY").box(x1 - x0, t, P.HEADPLATE_Z0 + P.TONGUE_DOWN, centered=(True, True, False)).translate(((x0 + x1) / 2, 0, -P.TONGUE_DOWN))
    cyl = cq.Workplane("XZ").circle(P.TONGUE_DOWN).extrude(t / 2, both=True)
    clip = cq.Workplane("XY").box(x1 - x0, t + 2, 200, centered=(True, True, True)).translate(((x0 + x1) / 2, 0, 0))
    tongue = box.union(cyl).intersect(clip)
    # proud contact rings on both faces (clamped by the ears)
    for sgn in (-1, 1):
        ring = (cq.Workplane("XZ").circle(P.TILT_RING_R1).circle(P.TILT_RING_R0).extrude(P.TILT_RING_PROUD + 0.2)
                .translate((0, 0, 0)))
        # Workplane("XZ") extrudes toward -Y; place so the ring sits on the face y = sgn*t/2 and protrudes outward
        if sgn > 0:
            ring = ring.translate((0, t / 2 + P.TILT_RING_PROUD, 0))
        else:
            ring = ring.translate((0, -t / 2 + 0.2, 0))
        tongue = tongue.union(ring)
    # hinge hole
    tongue = tongue.cut(cq.Workplane("XZ").circle(P.TS_HOLE / 2).extrude(30, both=True))
    # head plate
    hp = cq.Workplane("XY").box(x1 - x0, P.HEADPLATE_W, P.HEADPLATE_Z1 - P.HEADPLATE_Z0, centered=(True, True, False)).translate(((x0 + x1) / 2, 0, P.HEADPLATE_Z0))
    body = tongue.union(hp)
    # index boss: tapered square along +x from x1 to x1+BOSS_LEN, centred at z = BOSS_Z
    boss = (cq.Workplane("YZ").rect(P.BOSS, P.BOSS).workplane(offset=P.BOSS_LEN).rect(P.BOSS_TIP, P.BOSS_TIP).loft(ruled=True))
    boss = boss.edges().filter(lambda e: abs(e.tangentAt().x) > 0.5).fillet(1.5)
    boss = boss.translate((x1, 0, P.BOSS_Z))
    body = body.union(boss)
    # retaining-screw bore along x through head plate and boss
    bore = cq.Workplane("YZ").circle(P.TS_HOLE / 2).extrude(x1 + P.BOSS_LEN - x0 + 2).translate((x0 - 1, 0, P.BOSS_Z))
    body = body.cut(bore)
    # chamfer the boss tip edges lightly (elephant foot: the tip is the bed face)
    return body


def build() -> cq.Workplane:
    body = build_fork_frame()
    # print on its back: rotate so +x (use) -> +z (print).  Rotation about Y by -90: (x,y,z) -> (-z, y, x)
    return body.rotate((0, 0, 0), (0, 1, 0), -90)
