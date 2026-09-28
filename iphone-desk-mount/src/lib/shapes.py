"""Reusable CadQuery shape helpers (all mm, axis conventions noted per function)."""
from __future__ import annotations

import math
import cadquery as cq


def rrect(wp: cq.Workplane, w: float, h: float, r: float) -> cq.Workplane:
    """Rounded rectangle sketch on the given workplane (centred)."""
    if r <= 0:
        return wp.rect(w, h)
    return wp.sketch().rect(w, h).vertices().fillet(r).finalize()


def rrect_prism(w: float, d: float, h: float, r: float = 0.0) -> cq.Workplane:
    """Rounded-rectangle prism, base centred at origin, extruded +Z by h."""
    return rrect(cq.Workplane("XY"), w, d, r).extrude(h)


def square_tube(outer: float, wall: float, length: float, corner_r: float = 2.0) -> cq.Workplane:
    """Square tube along +Z from z=0 to z=length (print orientation: standing)."""
    outer_p = rrect_prism(outer, outer, length, corner_r)
    inner_r = max(corner_r - wall, 0.0)
    inner_p = rrect_prism(outer - 2 * wall, outer - 2 * wall, length + 2, inner_r).translate((0, 0, -1))
    return outer_p.cut(inner_p)


def tapered_prism(w0: float, d0: float, w1: float, d1: float, h: float, r: float = 0.0) -> cq.Workplane:
    """Loft from a (w0 x d0) rect at z=0 to (w1 x d1) at z=h; the four slanted corner edges are
    filleted with radius r (r=0 -> sharp).  Used for taper-wedge spigots and their sockets."""
    wp = cq.Workplane("XY").rect(w0, d0).workplane(offset=h).rect(w1, d1).loft(combine=True)
    if r > 0:
        wp = wp.edges().filter(lambda e: abs(e.tangentAt().z) > 0.5).fillet(r)
    return wp


def cross_hole(diameter: float, through: float, z: float, axis: str = 'x') -> cq.Workplane:
    """Cylinder cutter for a horizontal cross-hole at height z along the given axis."""
    cyl = cq.Workplane("YZ" if axis == 'x' else "XZ").circle(diameter / 2).extrude(through / 2, both=True)
    return cyl.translate((0, 0, z))


def chamfer_all_vertical_edges(wp: cq.Workplane, c: float) -> cq.Workplane:
    try:
        return wp.edges("|Z").chamfer(c)
    except Exception:
        return wp


def hirth_ring(n: int, r0: float, r1: float, sink: float = 0.2, included_deg: float = 90.0, trunc: float = 0.3) -> cq.Workplane:
    """TRUE Hirth ring: n radial wedge teeth whose base width equals the pitch 2*pi*r/n at EVERY radius (no root
    flats), so two identical rings interlock at a half-pitch offset with flank-to-flank contact -> self-centring,
    zero rotational play.  Geometric tooth height h(r) = (pitch/2) / tan(included/2); the crest is truncated by
    `trunc` so that, when the flanks touch, each crest keeps `trunc` of clearance from the mating root (crest/root
    relief, as in a machined Hirth coupling).  Teeth stand on the XY plane pointing +Z, centred on the origin,
    tooth k centred at angle k*360/n from +X; bases sunk `sink` below z=0."""
    t = math.tan(math.radians(included_deg / 2))
    def prof(r):
        b = 2 * math.pi * r / n + 0.02          # tiny overlap so neighbours fuse
        h = (b / 2) / t
        w_top = trunc * t                        # half-width of the flat crest
        return [(-b / 2, -sink), (b / 2, -sink), (w_top, h - trunc), (-w_top, h - trunc)]
    tooth = (cq.Workplane("YZ").workplane(offset=r0).polyline(prof(r0)).close()
             .workplane(offset=r1 - r0).polyline(prof(r1)).close().loft(ruled=True))
    teeth = tooth
    for k in range(1, n):
        teeth = teeth.union(tooth.rotate((0, 0, 0), (0, 0, 1), 360.0 * k / n))
    return teeth


def hirth_height(n: int, r: float, included_deg: float = 90.0) -> float:
    return (math.pi * r / n) / math.tan(math.radians(included_deg / 2))


def gabled_hole_xz(diameter: float, length: float) -> cq.Workplane:
    """Horizontal hole along Y (through length, centred) with a 45-deg gable toward +Z so its roof prints without a
    flat ceiling.  Translate to the axis position yourself."""
    r = diameter / 2
    c = r * math.cos(math.radians(45))
    circ = cq.Workplane("XZ").circle(r).extrude(length / 2, both=True)
    gable = cq.Workplane("XZ").polyline([(-c, c), (0, r * math.sqrt(2)), (c, c)]).close().extrude(length / 2, both=True)
    return circ.union(gable)
