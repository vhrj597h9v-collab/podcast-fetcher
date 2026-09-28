"""Cradle: 12 mm spine + bottom V-lip (60-deg incline leaning 12.4 mm over the phone: any 7-14 mm phone is pinched
against the back, no rattle) + back pad carrying the boss socket, a 45-deg hopper and a Tr10 retaining thread
printed vertically.  Frame: x across the phone, y along the phone (phone foot at y = 0, lip block y -8..0),
z = thickness (back face on the bed at z = 0).  The phone rests on the pad front (z = REST_Z) and the slider."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def _sk_rect(w, d, r, z):
    return cq.Sketch().rect(w, d).vertices().fillet(r).moved(cq.Location(cq.Vector(0, 0, z)))


def build() -> cq.Workplane:
    W = P.SPINE_W
    T = P.SPINE_T_CRADLE
    y_end = P.SPINE_LEN - P.LIP_H
    z_top = P.REST_Z + P.JAW_H
    lean = P.JAW_LEAN
    prof = [(-P.LIP_H, 0), (-P.LIP_H, z_top), (lean, z_top), (0, P.REST_Z), (0, T), (y_end, T), (y_end, 0)]
    body = cq.Workplane("YZ").polyline(prof).close().extrude(W / 2, both=True)
    body = body.edges("|Z").edges(">Y").fillet(6.0)
    cy = P.PAD_Y
    pad = cq.Workplane("XY").box(P.PAD_SQ, P.PAD_SQ, P.REST_Z, centered=(True, True, False)).translate((0, cy, 0))
    pad = pad.edges("|Z").fillet(4.0)
    body = body.union(pad)
    # grip ridges across the lip incline (diamond prisms along x, ~0.5 mm proud)
    for i in range(P.JAW_RIDGES):
        f = (i + 1) / (P.JAW_RIDGES + 1)
        yz = (lean * f, P.REST_Z + P.JAW_H * f)
        ridge = cq.Workplane("YZ").rect(1.4, 1.4).extrude(W / 2 - 1.0, both=True).rotate((0, 0, 0), (1, 0, 0), 45).translate((0, yz[0], yz[1]))
        body = body.union(ridge)
    # boss socket (mouth at the back face) -> 45-deg hopper -> Tr10 thread up to the rest face
    tan_b = math.tan(math.radians(P.BOSS_TAPER_DEG))
    m = P.CRADLE_SOCKET_MOUTH
    bottom = m - 2 * P.CRADLE_SOCKET_DEPTH * tan_b
    sock = (cq.Workplane("XY").workplane(offset=-1.0).rect(m + 2 * tan_b, m + 2 * tan_b)
            .workplane(offset=P.CRADLE_SOCKET_DEPTH + 1.0).rect(bottom, bottom).loft(ruled=True))
    sock = sock.edges().filter(lambda e: abs(e.tangentAt().z) > 0.5).fillet(1.0)
    z_h = P.CRADLE_SOCKET_DEPTH
    hopper = cq.Workplane("XY").placeSketch(_sk_rect(bottom, bottom, 1.0, z_h - 0.01), _sk_rect(12.0, 12.0, 1.0, z_h + P.CRADLE_HOPPER_H)).loft(ruled=True)
    body = body.cut(sock.translate((0, cy, 0))).cut(hopper.translate((0, cy, 0)))
    cutter = th.internal_thread_cutter(P.RETAIN_D, P.RETAIN_P, P.CRADLE_THREAD_LEN, P.TILT_CLR).translate((0, cy, z_h + P.CRADLE_HOPPER_H))
    body = body.cut(cutter)
    # port cut-out through the whole lip (open to the phone side and the lip top), leaves the V-lip on both sides
    port = cq.Workplane("XY").box(P.PORT_CUT_W, P.LIP_H + lean + 2, z_top, centered=(True, False, False)).translate((0, -P.LIP_H - 1.0, P.REST_Z - 1.0))
    body = body.cut(port)
    # anti-elephant-foot: socket mouth chamfer and 0.5 mm on the bed-face perimeter (the slider channel rides these edges)
    ch = cq.Workplane("XY").workplane(offset=-0.01).rect(m + 2.4, m + 2.4).workplane(offset=1.21).rect(m - 0.01, m - 0.01).loft(ruled=True)
    body = body.cut(ch.translate((0, cy, 0)))
    body = body.faces("<Z").chamfer(0.5)
    return body
