"""Slider (top jaw): C-channel around the cradle spine + front rest wall + 60-deg V-jaw (mirror of the lip), with a
diamond nut pocket in the back wall for the Tr8 lock thumbscrew that presses the spine's back face (friction lock).
Frame: x across the spine, y along the spine (jaw foot / phone side at y = 0), z = thickness (spine occupies z 0..T).
Printed standing on its far end (y = SLIDER_LEN on the bed): the profile is a vertical extrusion and the jaw incline
faces upward (30 deg from horizontal), so nothing overhangs."""
import cadquery as cq
import params as P


def build_frame() -> cq.Workplane:
    c = P.SLIDE_CLR
    W = P.SPINE_W
    T = P.SPINE_T_CRADLE
    L = P.SLIDER_LEN
    xi = W / 2 + c
    xo = xi + P.SLIDER_SIDE_WALL
    z_in0, z_in1 = -c, T + c
    z_out0 = z_in0 - P.SLIDER_BACK_WALL
    z_out1 = P.REST_Z
    outer = cq.Workplane("XY").box(2 * xo, L, z_out1 - z_out0, centered=(True, False, False)).translate((0, 0, z_out0))
    outer = outer.edges("|Y").fillet(3.0)
    inner = cq.Workplane("XY").box(2 * xi, L + 2, z_in1 - z_in0, centered=(True, False, False)).translate((0, -1, z_in0))
    body = outer.cut(inner)
    # V-jaw: from the rest face up JAW_H, leaning JAW_LEAN over the phone (toward -y)
    z_top = P.REST_Z + P.JAW_H
    prof = [(0.0, P.REST_Z - 1.0), (-P.JAW_LEAN, z_top), (L, z_top), (L, P.REST_Z - 1.0)]
    jaw = cq.Workplane("YZ").polyline(prof).close().extrude(xo, both=True)
    body = body.union(jaw)
    # diamond nut pocket in the back wall, open toward the spine (nut inserted from inside), axis z
    s = P.SQ_NUT + 2 * P.SQ_NUT_CLR
    pocket = (cq.Workplane("XY").rect(s, s).extrude(P.SQ_NUT_T + 0.4 + 1.0).rotate((0, 0, 0), (0, 0, 1), 45)
              .translate((0, L / 2, z_in0 - (P.SQ_NUT_T + 0.4))))
    body = body.cut(pocket)
    hole = cq.Workplane("XY").circle(P.TS_HOLE / 2).extrude(P.SLIDER_BACK_WALL + 2).translate((0, L / 2, z_out0 - 1))
    body = body.cut(hole)
    return body


def build() -> cq.Workplane:
    return build_frame().rotate((0, 0, 0), (1, 0, 0), -90)      # +y (frame) -> -z: the far end lands on the bed
