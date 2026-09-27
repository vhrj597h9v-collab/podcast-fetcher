"""Pole segment (x3, identical).  Print orientation = use orientation: socket at the bottom (mouth on the
bed), tapered spigot at the top.  All internal transitions are 45-deg hoppers; the outer profile is a ruled
loft through rounded-rectangle sections so it is one clean solid."""
import cadquery as cq
import params as P


def _rr(size: float, r: float) -> cq.Sketch:
    return cq.Sketch().rect(size, size).vertices().fillet(r)


def _loft(sections, ruled: bool = True) -> cq.Workplane:
    """sections: list of (z, size, corner_r).  Returns a solid lofted through rounded squares."""
    wp = cq.Workplane("XY")
    sk = [ _rr(s, r).moved(cq.Location(cq.Vector(0, 0, z))) for (z, s, r) in sections ]
    return wp.placeSketch(*sk).loft(ruled=ruled)


def build() -> cq.Workplane:
    L = P.SEG_LEN
    z_shoulder0 = L - P.SPIGOT_LEN - P.SHOULDER_H      # 167: start of 45-deg shoulder
    z_spigot0 = L - P.SPIGOT_LEN                       # 175: spigot base
    outer = _loft([
        (0.0, P.EXT_TAPER_BOTTOM, P.POLE_CORNER_R),
        (P.EXT_TAPER_LEN, P.POLE_OUTER, P.POLE_CORNER_R),
        (z_shoulder0, P.POLE_OUTER, P.POLE_CORNER_R),
        (z_spigot0, P.SPIGOT_BASE, P.SPIGOT_CORNER_R),
        (L, P.SPIGOT_TIP, P.SPIGOT_CORNER_R),
    ])
    # inner cavity: socket -> 45 hopper out to the tube cavity -> 45 hopper in to the spigot bore
    z_hop1 = P.SOCKET_DEPTH + (P.POLE_INNER - P.SOCKET_BOTTOM) / 2          # 67.8
    z_hop2 = z_spigot0 - (P.POLE_INNER - P.SPIGOT_BORE) / 2                 # 164
    sock_r = P.SPIGOT_CORNER_R - 0.4   # socket corner radius SMALLER than the spigot's so only the flats seat
    inner = _loft([
        (-1.0, P.SOCKET_MOUTH + 2 * 1.0 * P.TAN_T, sock_r),
        (P.SOCKET_DEPTH, P.SOCKET_BOTTOM, sock_r),
        (z_hop1, P.POLE_INNER, 3.0),
        (z_hop2, P.POLE_INNER, 3.0),
        (z_spigot0, P.SPIGOT_BORE, 1.5),
        (L + 1.0, P.SPIGOT_BORE, 1.5),
    ])
    seg = outer.cut(inner)
    # 1 mm chamfer on both edge loops of the bed face (outer taper edge + socket mouth): kills elephant-foot
    # influence on both wedge fits.
    seg = seg.faces("<Z").chamfer(1.0)
    return seg
