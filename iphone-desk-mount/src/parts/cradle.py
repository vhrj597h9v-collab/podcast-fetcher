"""Cradle: 12 mm spine + bottom V-lip (60-deg incline leaning 12.7 mm over the phone: any 7-14 mm phone is pinched
against the back, no rattle) + back pad carrying the boss socket and a Tr8 retaining thread printed vertically.
Frame: x across the phone, y along the phone (phone foot at y = 0, lip block y -8..0), z = thickness (back face on
the bed at z = 0).  The phone rests on the pad front (z = REST_Z) and the slider's rest face."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    W = P.SPINE_W
    T = P.SPINE_T_CRADLE
    y_end = P.SPINE_LEN - P.LIP_H                  # 182: spine top end
    z_top = P.REST_Z + P.JAW_H                     # 42
    lean = P.JAW_LEAN                              # 12.7
    prof = [(-P.LIP_H, 0), (-P.LIP_H, z_top), (lean, z_top), (0, P.REST_Z), (0, T), (y_end, T), (y_end, 0)]
    body = cq.Workplane("YZ").polyline(prof).close().extrude(W / 2, both=True)
    body = body.edges("|Z").edges(">Y").fillet(6.0)
    cy = P.PAD_Y
    pad = cq.Workplane("XY").box(P.PAD_SQ, P.PAD_SQ, P.REST_Z, centered=(True, True, False)).translate((0, cy, 0))
    pad = pad.edges("|Z").fillet(4.0)
    body = body.union(pad)
    # tapered square socket for the carrier boss: mouth at the back face (z=0), narrowing to the ceiling
    tan_b = math.tan(math.radians(P.BOSS_TAPER_DEG))
    m = P.CRADLE_SOCKET_MOUTH
    bottom = m - 2 * P.CRADLE_SOCKET_DEPTH * tan_b
    sock = (cq.Workplane("XY").workplane(offset=-1.0).rect(m + 2 * tan_b, m + 2 * tan_b)
            .workplane(offset=P.CRADLE_SOCKET_DEPTH + 1.0).rect(bottom, bottom).loft(ruled=True))
    sock = sock.edges().filter(lambda e: abs(e.tangentAt().z) > 0.5).fillet(1.0)
    body = body.cut(sock.translate((0, cy, 0)))
    # Tr8 internal thread from the socket ceiling to the pad front (vertical in print)
    cutter = th.internal_thread_cutter(P.TS_D, P.TS_P, P.CRADLE_THREAD_LEN, P.TS_CLR).translate((0, cy, P.CRADLE_SOCKET_DEPTH))
    body = body.cut(cutter)
    # port cut-out through the whole lip (open to the phone side and the lip top), leaves the V-lip on both sides
    port = cq.Workplane("XY").box(P.PORT_CUT_W, P.LIP_H + lean + 2, z_top, centered=(True, False, False)).translate((0, -P.LIP_H - 1.0, P.REST_Z - 1.0))
    body = body.cut(port)
    # anti-elephant-foot chamfer on the socket mouth
    ch = cq.Workplane("XY").workplane(offset=-0.01).rect(m + 2.4, m + 2.4).workplane(offset=1.21).rect(m - 0.01, m - 0.01).loft(ruled=True)
    body = body.cut(ch.translate((0, cy, 0)))
    return body
