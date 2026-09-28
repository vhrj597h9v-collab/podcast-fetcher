"""Slider (top jaw): C-channel around the cradle spine whose body sits UNDER the phone, ending in a 60-deg V-jaw
wall at the phone's top edge (mirror of the lip), with a diamond nut pocket in the back wall for the Tr8 lock
thumbscrew that presses the spine's back face (friction lock).
Frame: x across the spine, y along the spine (y=0 = body end under the phone, jaw foot at y = SLIDER_LEN, jaw wall
to y = SLIDER_LEN + SLIDER_JAW_WALL), z = thickness (spine occupies z 0..T).
Printed standing on the jaw-wall end (y max on the bed) so the incline faces upward and the channel is vertical."""
import cadquery as cq
import params as P


def build_frame() -> cq.Workplane:
    c = P.SLIDE_CLR
    W = P.SPINE_W
    T = P.SPINE_T_CRADLE
    L = P.SLIDER_LEN
    LJ = L + P.SLIDER_JAW_WALL
    xi = W / 2 + c
    xo = xi + P.SLIDER_SIDE_WALL
    z_in0, z_in1 = -c, T + c
    z_out0 = z_in0 - P.SLIDER_BACK_WALL
    z_out1 = P.REST_Z
    outer = cq.Workplane("XY").box(2 * xo, LJ, z_out1 - z_out0, centered=(True, False, False)).translate((0, 0, z_out0))
    outer = outer.edges("|Y").fillet(3.0)
    inner = cq.Workplane("XY").box(2 * xi, LJ + 2, z_in1 - z_in0, centered=(True, False, False)).translate((0, -1, z_in0))
    body = outer.cut(inner)
    # V-jaw: foot at y = L on the rest plane, leaning JAW_LEAN back over the phone (toward -y), wall out to y = LJ
    z_top = P.REST_Z + P.JAW_H
    prof = [(L, P.REST_Z - 1.0), (L - P.JAW_LEAN, z_top), (LJ, z_top), (LJ, P.REST_Z - 1.0)]
    jaw = cq.Workplane("YZ").polyline(prof).close().extrude(xo, both=True)
    body = body.union(jaw)
    for i in range(P.JAW_RIDGES):
        f = (i + 1) / (P.JAW_RIDGES + 1)
        ridge = (cq.Workplane("YZ").rect(1.4, 1.4).extrude(xo - 1.0, both=True).rotate((0, 0, 0), (1, 0, 0), 45)
                 .translate((0, L - P.JAW_LEAN * f, P.REST_Z + P.JAW_H * f)))
        body = body.union(ridge)
    # diamond nut pocket in the back wall (open toward the spine), and a gabled clearance hole (gable toward -y = print up)
    s = P.SQ_NUT + 2 * P.SQ_NUT_CLR
    yc = L / 2
    pocket = (cq.Workplane("XY").rect(s, s).extrude(P.SQ_NUT_T + 0.4 + 1.0).rotate((0, 0, 0), (0, 0, 1), 45)
              .translate((0, yc, z_in0 - (P.SQ_NUT_T + 0.4))))
    body = body.cut(pocket)
    r = P.TS_HOLE / 2
    c45 = r * 0.7071
    hole = cq.Workplane("XY").circle(r).extrude(P.SLIDER_BACK_WALL + 2).translate((0, yc, z_out0 - 1))
    gable = (cq.Workplane("XY").polyline([(-c45, -c45), (0, -r * 1.4142), (c45, -c45)]).close().extrude(P.SLIDER_BACK_WALL + 2)
             .translate((0, yc, z_out0 - 1)))
    body = body.cut(hole).cut(gable)
    # anti-elephant-foot on the bed end (channel edges)
    body = body.faces(">Y").chamfer(0.5)
    return body


def build() -> cq.Workplane:
    return build_frame().rotate((0, 0, 0), (1, 0, 0), -90)      # +y (frame) -> -z: the jaw-wall end lands on the bed
