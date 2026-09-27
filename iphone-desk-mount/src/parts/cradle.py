"""Cradle: spine plate + bottom lip with hook + back pad carrying the boss socket and a Tr8 retaining thread
printed vertically.  Frame: x across the phone, y along the phone (lip at y=0), z = thickness (back face z=0
on the bed).  The phone rests on the pad front (z = REST_Z) and the slider's rest face."""
import math
import cadquery as cq
import params as P
from lib import threads as th


def build() -> cq.Workplane:
    W = P.SPINE_W
    L = P.SPINE_LEN
    T = P.SPINE_T_CRADLE
    lip_top = P.REST_Z + P.LIP_FWD                 # 37
    hook_y = P.LIP_H + P.LIP_HOOK                  # 13
    prof = [(0, 0), (0, lip_top), (hook_y, lip_top), (hook_y, lip_top - P.LIP_HOOK_T),
            (P.LIP_H, lip_top - P.LIP_HOOK_T - P.LIP_HOOK), (P.LIP_H, T), (L, T), (L, 0)]
    body = cq.Workplane("YZ").polyline(prof).close().extrude(W / 2, both=True)
    body = body.edges("|Z").edges(">Y").fillet(6.0)
    cy = P.LIP_H + P.PAD_Y
    pad = cq.Workplane("XY").box(P.PAD_SQ, P.PAD_SQ, P.REST_Z, centered=(True, True, False)).translate((0, cy, 0))
    pad = pad.edges("|Z").fillet(4.0)
    body = body.union(pad)
    # tapered square socket for the carrier boss: mouth at the back face (z=0), narrowing to the ceiling
    tan_b = math.tan(math.radians(P.BOSS_TAPER_DEG))
    m = P.CRADLE_SOCKET_MOUTH
    bottom = m - 2 * P.CRADLE_SOCKET_DEPTH * tan_b
    sock = (cq.Workplane("XY").workplane(offset=-1.0).rect(m + 2 * tan_b, m + 2 * tan_b)
            .workplane(offset=P.CRADLE_SOCKET_DEPTH + 1.0).rect(bottom, bottom).loft(ruled=True))
    sock = sock.edges().filter(lambda e: abs(e.tangentAt().z) > 0.5).fillet(1.0)   # boss corners are r1.5 -> socket corners clear
    body = body.cut(sock.translate((0, cy, 0)))
    # Tr8 internal thread from the socket ceiling to the pad front (vertical in print)
    cutter = th.internal_thread_cutter(P.TS_D, P.TS_P, P.CRADLE_THREAD_LEN, P.TS_CLR).translate((0, cy, P.CRADLE_SOCKET_DEPTH))
    body = body.cut(cutter)
    # port cut-out in the lip centre (leaves the hook on both sides)
    port = cq.Workplane("XY").box(P.PORT_CUT_W, P.LIP_H + P.LIP_HOOK + 2, 16.0, centered=(True, False, False)).translate((0, -1.0, P.REST_Z - 3.0))
    body = body.cut(port)
    # anti-elephant-foot chamfer on the socket mouth
    ch = cq.Workplane("XY").workplane(offset=-0.01).rect(m + 2.4, m + 2.4).workplane(offset=1.21).rect(m - 0.01, m - 0.01).loft(ruled=True)
    body = body.cut(ch.translate((0, cy, 0)))
    return body
