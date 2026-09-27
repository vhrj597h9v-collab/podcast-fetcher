"""Reusable CadQuery shape helpers (all mm, axis conventions noted per function)."""
from __future__ import annotations

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
