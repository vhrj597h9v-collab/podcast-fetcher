"""Slider (top jaw): C-channel around the cradle spine + front rest wall + hook, with a diamond nut pocket in
the back wall for the Tr8 lock thumbscrew that presses the spine's back face (friction lock).
Frame: x across the spine, y along the spine (phone side at y = 0), z = thickness (spine occupies z 0..T).
Printed standing on its far end (y = SLIDER_LEN on the bed) so the profile is a vertical extrusion and the
hook lip is supported by the hook wall below it."""
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
    lip_top = P.REST_Z + P.SLIDER_HOOK_FWD                       # 37
    # hook + 45-deg gusset as ONE profile in the (y, z) plane, extruded across x.  In print (y -> -z) the
    # gusset's sloped back face is a 45-deg overhang and the lip sits on top of the hook wall.
    prof = [(-P.SLIDER_HOOK, lip_top), (-P.SLIDER_HOOK, lip_top - P.SLIDER_HOOK_T),
            (0.0, lip_top - P.SLIDER_HOOK_T - P.SLIDER_HOOK), (0.0, P.REST_Z - 1.0),
            (P.LIP_H + P.SLIDER_HOOK_FWD, P.REST_Z - 1.0), (P.LIP_H, lip_top)]
    hook = cq.Workplane("YZ").polyline(prof).close().extrude(xo, both=True)
    body = body.union(hook)
    s = P.SQ_NUT + 2 * P.SQ_NUT_CLR
    pocket = (cq.Workplane("XY").rect(s, s).extrude(P.SQ_NUT_T + 0.4 + 1.0).rotate((0, 0, 0), (0, 0, 1), 45)
              .translate((0, L / 2, z_in0 - (P.SQ_NUT_T + 0.4))))
    body = body.cut(pocket)
    hole = cq.Workplane("XY").circle(P.TS_HOLE / 2).extrude(P.SLIDER_BACK_WALL + 2).translate((0, L / 2, z_out0 - 1))
    body = body.cut(hole)
    return body


def build() -> cq.Workplane:
    body = build_frame()
    # stand it on its far end: +y (frame) -> -z (print)  => rotate +90 deg about X maps (x,y,z)->(x,-z,y); we need y->-z: rotate -90
    return body.rotate((0, 0, 0), (1, 0, 0), -90)
