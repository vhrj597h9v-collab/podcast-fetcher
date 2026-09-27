"""C-clamp body.  Modelled IN USE coordinates (x inboard from the desk edge at x=0, z up with the desk top at
z=0, y along the edge), then rotated so it prints ON ITS SIDE (use -Y face on the bed).  The pole socket is a
2.5-deg tapered square rotated 45 deg (diamond) so that, printed on its side, its roof is two 45-deg faces."""
import math
import cadquery as cq
import params as P


def _profile_solid(x0, x1, z0, z1, w):
    """box spanning x0..x1, z0..z1, centred in y with width w"""
    return cq.Workplane("XY").box(x1 - x0, w, z1 - z0).translate(((x0 + x1) / 2, 0, (z0 + z1) / 2))


def build_use_coords() -> cq.Workplane:
    W = P.CLAMP_W
    z_bot = -(P.THROAT + P.BOTTOM_JAW_T)          # -96
    # spine + top jaw + bottom jaw (C profile)
    spine = _profile_solid(-P.SPINE_T, 0, z_bot, P.TOP_JAW_T, W)
    top_jaw = _profile_solid(-P.SPINE_T, P.PAD_LEN, 0, P.TOP_JAW_T, W)
    bj_x1 = P.SCREW_X + P.NUT_BLOCK / 2 + 8.0
    bottom_jaw = _profile_solid(-P.SPINE_T, bj_x1, z_bot, -P.THROAT, W)
    tower = _profile_solid(P.TOWER_X0, P.TOWER_X1, P.TOP_JAW_T, P.TOP_JAW_T + P.TOWER_H, W)
    body = spine.union(top_jaw).union(bottom_jaw).union(tower).clean()
    # round only the CONVEX profile corners (edges parallel to Y), selected by position
    zt = P.TOP_JAW_T + P.TOWER_H
    convex = [(-P.SPINE_T, z_bot), (bj_x1, z_bot), (bj_x1, -P.THROAT), (P.PAD_LEN, 0.0), (P.PAD_LEN, P.TOP_JAW_T),
              (P.TOWER_X1, zt), (P.TOWER_X0, zt)]
    def is_convex_corner(e):
        c = e.Center()
        return abs(e.tangentAt().y) > 0.99 and any(abs(c.x - x) < 0.01 and abs(c.z - z) < 0.01 for (x, z) in convex)
    body = body.edges().filter(is_convex_corner).fillet(P.CLAMP_CORNER_R)
    # diamond tapered pole socket (mouth at the tower top, floor = top-jaw top face)
    sock = (cq.Workplane("XY")
            .rect(P.CLAMP_SOCKET_BOTTOM, P.CLAMP_SOCKET_BOTTOM).workplane(offset=P.CLAMP_SOCKET_DEPTH + 1.0)
            .rect(P.CLAMP_SOCKET_MOUTH + 2 * P.TAN_T, P.CLAMP_SOCKET_MOUTH + 2 * P.TAN_T).loft(ruled=True))
    sock = sock.edges().filter(lambda e: abs(e.tangentAt().z) > 0.5).fillet(P.POLE_CORNER_R - 0.5)   # smaller than the pole corner radius -> flats seat, corners clear
    sock = sock.rotate((0, 0, 0), (0, 0, 1), P.DIAMOND_DEG).translate((P.TOWER_CENTER_X, 0, P.TOP_JAW_T))
    body = body.cut(sock)
    # nut-block pocket in the bottom jaw: open to +Z (desk side) and +Y (print top)
    pw = P.NUT_BLOCK + 2 * P.POCKET_CLR
    ph = P.NUT_BLOCK_H + 2 * P.POCKET_CLR
    pocket = (cq.Workplane("XY").box(pw, W / 2 + pw / 2 + 1.0, ph + 1.0, centered=(True, False, False))
              .translate((P.SCREW_X, -pw / 2, -P.THROAT - ph)))
    body = body.cut(pocket)
    # screw clearance hole through the pocket floor: circle + 45-deg gable toward use +Y (= print top) so the
    # horizontal 19 mm hole has no flat roof in the side print
    r = P.SHAFT_CLR_HOLE / 2
    c45 = r * math.cos(math.radians(45))
    gable = cq.Workplane("XY").polyline([(-c45, c45), (0, r * math.sqrt(2)), (c45, c45)]).close().extrude(P.BOTTOM_JAW_T + 2)
    hole = cq.Workplane("XY").circle(r).extrude(P.BOTTOM_JAW_T + 2).union(gable).translate((P.SCREW_X, 0, z_bot - 1))
    body = body.cut(hole)
    # two desk-contact rails along X on the pad face (defined two-line contact -> no rocking on an uneven desk)
    for sy in (-1, 1):
        rail = cq.Workplane("XY").box(P.PAD_LEN - 4.0, P.PAD_RAIL_W, P.PAD_RAIL_H + 0.01, centered=(False, True, False)).translate((2.0, sy * P.PAD_RAIL_Y, -P.PAD_RAIL_H))
        body = body.union(rail)
    # 45-deg lead-in on the diamond socket mouth
    m = P.CLAMP_SOCKET_MOUTH
    ch = P.CLAMP_MOUTH_CHAMFER
    lead = (cq.Workplane("XY").workplane(offset=zt - ch).rect(m - 0.02, m - 0.02).workplane(offset=ch + 0.02).rect(m + 2 * ch, m + 2 * ch)
            .loft(ruled=True).rotate((0, 0, 0), (0, 0, 1), P.DIAMOND_DEG).translate((P.TOWER_CENTER_X, 0, 0)))
    body = body.cut(lead)
    return body


def build() -> cq.Workplane:
    body = build_use_coords()
    # print on its side: use -Y face on the bed  (rotate +90 deg about X: y -> z)
    return body.rotate((0, 0, 0), (1, 0, 0), 90)
