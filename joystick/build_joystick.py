#!/usr/bin/env python3
"""
Parametric 8-button joystick — model builder.

Thumb-operated head, 6 buttons: the button panel stands vertical and faces the
user (tilted a further PANEL_TILT degrees down towards the thumb). The bottom
row of three sits on the flat face; the top row of three sits on an upper block
that overhangs the flat face, its face tipped 45 deg down towards the user so the
thumb reaches it from below. Two more buttons sit on a trigger bump under the
front of the head, facing down and forward for the index finger.

The Pro Micro lives in a pocket in the neck of the grip, just under the head,
USB jack pointing down the cable channel. One back plate covers the head opening
and, with a tab, the neck pocket. Every edge is rounded.

Exports (all mm, Z up, -Y is towards the user):

  out/joystick_body.stl        head + grip + base, one FDM print
  out/joystick_back_plate.stl  rear access plate with neck tab, 4x M4 countersunk
  out/joystick_button_cap.stl  one button cap (print 8)
  out/pro_micro_mockup.stl     board envelope for fit checks (not printed)
  out/joystick_assembly.stl    everything assembled, for preview only
  out/scene.json               coloured parts + explode vectors for the web viewer
  out/meta.json                key transforms for the spec-sheet annotations

Requires: trimesh, manifold3d, shapely, numpy   (pip install trimesh manifold3d shapely)
"""
from __future__ import annotations

import base64
import json
import math
import os

import numpy as np
import trimesh
from shapely.geometry import Polygon
from trimesh.creation import box as tbox
from trimesh.creation import cylinder, icosphere
from trimesh.transformations import rotation_matrix, translation_matrix

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
SEG = 48  # segments per full circle

# --------------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------------
BUTTON_PITCH = 16.0    # bezel is 14 mm, so 2 mm between bezels
BUTTON_X = [(-1 + i) * BUTTON_PITCH for i in range(3)]     # -16, 0, 16
CAP_D = 10.0           # button cap diameter (spec: 10 mm)
CAP_H = 8.0            # cap height above bezel (spec: 8 mm)
BEZEL_D = 14.0
BEZEL_H = 2.0
CAP_HOLE_D = 10.6      # panel through hole for cap stem
SWITCH_POCKET = 6.8    # 6x6 tactile switch, +0.8 clearance
SWITCH_POCKET_DEPTH = 1.5
PLUNGER_SOCKET_D = 3.6

EDGE_R = 5.0           # fillet radius on every head edge
WALL = 3.0             # shell wall thickness
PANEL_TILT = 10.0      # extra tilt of the whole head down towards the thumb (deg)
MARGIN = 1.0           # flat panel margin beyond the outer bezels

BOX_W = 2 * (BUTTON_X[-1] + BEZEL_D / 2 + MARGIN + EDGE_R)        # 58
FLAT_ROW_Z = EDGE_R + MARGIN + BEZEL_D / 2                        # 13: bottom row centre
FLAT_FACE_H = FLAT_ROW_Z + BEZEL_D / 2 + MARGIN + 2.0             # 22: flat face up to the crease
OVERHANG = 14.0        # top row face overhangs the flat face by this (45 deg, rise == run)
BOX_H = FLAT_FACE_H + OVERHANG                                    # 36
BOX_D = 34.0           # Y, head depth == neck diameter (the head cavity only holds switches + wires)
TOP_ROW_MID = (-BOX_D / 2 - OVERHANG / 2, FLAT_FACE_H + OVERHANG / 2)
TOP_ROW_TILT = 135.0   # normal points down + towards the user

# Trigger bump under the front of the head: convex (y, z) profile, index finger
# presses the sloped face (down + towards the user) from below.
TRIGGER_PROFILE = [(-25.0, -2.0), (-8.0, -16.0), (3.0, -16.0), (3.0, 10.0), (-17.0, 10.0), (-25.0, 2.0)]
TRIGGER_HALF_W = 20.0
TRIGGER_X = [-8.0, 8.0]

M4_CLEAR_D = 4.5
M4_TAP_D = 3.3
M4_CSK_D = 9.0
BOSS = 8.0
PLATE_T = 3.0
PLATE_MARGIN = 7.5     # head opening inset from the head outline
LEDGE = 4.0            # ledge behind the head opening
PAD_Y0 = 8.0           # flat pad on the back of the neck that the plate tab sits on
PAD_HALF_W = 14.0
PAD_Z0 = -47.0

# Controller: HiLetgo Pro Micro (ATmega32U4), 33 x 18 mm PCB, micro-USB on a short edge.
# Sits in the neck pocket, PCB parallel to the plate, jack down over the cable channel,
# header pins towards the plate.
PCB_L = 33.0
PCB_W = 18.0
PCB_T = 1.6
PCB_CLEAR = 0.3
JACK_T = 2.8           # micro-USB jack height above the PCB
BOARD_Z0 = -36.0       # head-local z of the PCB bottom edge
POCKET_W = PCB_W + 2 * PCB_CLEAR + 0.4

GRIP_H = 120.0         # base top -> head bottom
GRIP_ELLIP = 0.92      # cross-section: rx = r * ellip (deeper than wide, like a real stick)
COLLAR_R = 23.0
COLLAR_H = 14.0
BASE_R = 36.0
BASE_T = 6.0
BASE_PCD = 58.0
CABLE_D = 12.0         # channel must pass a micro-USB plug (~7 x 11 mm overmould)
BASE_GROOVE_W = 9.0    # cable groove across the underside of the base, out the back
BASE_GROOVE_D = 3.5

TOP_ROW_COLORS = ["#d81e1e", "#f2f2f2", "#1e64d8"]          # red white blue
BOTTOM_ROW_COLORS = ["#f2c800", "#22a83a", "#f07f16"]       # yellow green orange
TRIGGER_COLORS = ["#1a1a1a", "#8a8a8a"]                     # black grey
BODY_COLOR = "#252528"
PLATE_COLOR = "#1f1f22"
PCB_COLOR = "#1b6b3a"
PIN_COLOR = "#d9d9d9"


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def union(*meshes):
    meshes = [m for m in meshes if m is not None]
    return meshes[0] if len(meshes) == 1 else trimesh.boolean.union(meshes, engine="manifold")


def difference(base, *cutters):
    cutters = [c for c in cutters if c is not None]
    if not cutters:
        return base
    cutter = union(*cutters) if len(cutters) > 1 else cutters[0]
    return trimesh.boolean.difference([base, cutter], engine="manifold")


def cyl(r, h, z0=0.0, sections=SEG):
    m = cylinder(radius=r, height=h, sections=sections)
    m.apply_translation([0, 0, z0 + h / 2])
    return m


def box_at(extents, center):
    m = tbox(extents=extents)
    m.apply_translation(center)
    return m


def frustum(r_bottom, r_top, h, z0=0.0, sections=SEG):
    """Cone frustum along +Z (for countersinks)."""
    a = np.linspace(0, 2 * math.pi, sections, endpoint=False)
    bottom = np.c_[r_bottom * np.cos(a), r_bottom * np.sin(a), np.full_like(a, z0)]
    top = np.c_[r_top * np.cos(a), r_top * np.sin(a), np.full_like(a, z0 + h)]
    verts = np.vstack([bottom, top, [[0, 0, z0]], [[0, 0, z0 + h]]])
    cb, ct = 2 * sections, 2 * sections + 1
    faces = []
    for i in range(sections):
        j = (i + 1) % sections
        faces += [[i, j, sections + j], [i, sections + j, sections + i]]
        faces += [[cb, j, i], [ct, sections + i, sections + j]]
    m = trimesh.Trimesh(verts, faces, process=True)
    m.fix_normals()
    return m


def csk_hole(clear_d, csk_d, length, z_surface):
    """Countersunk hole opening at z_surface (countersink on top), running `length` down."""
    depth = (csk_d - clear_d) / 2  # 90 deg countersink
    hole = cyl(clear_d / 2, length + 1, z_surface - length - 0.5)
    cone = frustum(clear_d / 2, csk_d / 2 + 0.6, depth + 0.6, z_surface - depth)
    return union(hole, cone)


def bezier(p0, p1, p2, p3, t):
    t = np.asarray(t)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def sweep(path, radii, ellip=1.0, sections=SEG):
    """Sweep an ellipse (rx = r*ellip, ry = r) along a path lying in the YZ plane."""
    path = np.asarray(path, float)
    n = len(path)
    tan = np.gradient(path, axis=0)
    tan /= np.linalg.norm(tan, axis=1)[:, None]
    bx = np.array([1.0, 0, 0])
    verts = []
    ang = np.linspace(0, 2 * math.pi, sections, endpoint=False)
    for p, t, r in zip(path, tan, radii):
        by = np.cross(t, bx)
        by /= np.linalg.norm(by)
        verts.append(p + np.outer(r * ellip * np.cos(ang), bx) + np.outer(r * np.sin(ang), by))
    verts = np.vstack(verts)
    faces = []
    for i in range(n - 1):
        for k in range(sections):
            k2 = (k + 1) % sections
            a, b = i * sections + k, i * sections + k2
            c, d = (i + 1) * sections + k2, (i + 1) * sections + k
            faces += [[a, b, c], [a, c, d]]
    c0, c1 = len(verts), len(verts) + 1
    verts = np.vstack([verts, path[0], path[-1]])
    for k in range(sections):
        k2 = (k + 1) % sections
        faces.append([c0, k2, k])
        faces.append([c1, (n - 1) * sections + k, (n - 1) * sections + k2])
    m = trimesh.Trimesh(verts, faces, process=True)
    m.fix_normals()
    assert m.is_watertight, "sweep not watertight"
    return m


def rounded_hull(profile_yz, half_width, inset, radius):
    """Convex solid = hull of spheres of `radius` placed at the profile vertices inset
    by `inset` (in y/z and x). inset == radius gives the profile with every edge
    filleted; a smaller radius at the same centres gives the inner (shell) offset."""
    poly = Polygon(profile_yz).buffer(-inset, join_style="mitre")
    sphere = icosphere(subdivisions=3, radius=radius)
    pts = []
    for y, z in list(poly.exterior.coords)[:-1]:
        for x in (-(half_width - inset), half_width - inset):
            pts.append(sphere.vertices + [x, y, z])
    return trimesh.convex.convex_hull(np.vstack(pts))


def panel_frame(x, y, z, tilt_deg):
    """Button frame: origin on the panel surface, +Z = outward normal.
    tilt rotates +Z about X: 90 -> faces -Y (the user), 135 -> down and towards the user."""
    return translation_matrix([x, y, z]) @ rotation_matrix(math.radians(tilt_deg), [1, 0, 0])


def tf(mesh, matrix):
    m = mesh.copy()
    m.apply_transform(matrix)
    return m


# --------------------------------------------------------------------------
# Grip spine (world coords) and head placement
# --------------------------------------------------------------------------
SPINE = (np.array([0, 0, 0.0]), np.array([0, -10.0, 50.0]),
         np.array([0, -16.0, 98.0]), np.array([0, -14.0, GRIP_H]))


def grip_spine(t):
    return bezier(*SPINE, t)


def head_transform():
    top = grip_spine(np.array([1.0]))[0]
    return translation_matrix(top) @ rotation_matrix(math.radians(PANEL_TILT), [1, 0, 0])


def spine_in_head(z_local):
    """head-local y of the grip spine (== cable channel centre) at head-local height z_local."""
    T_inv = np.linalg.inv(head_transform())
    t = np.linspace(0.3, 1.0, 400)
    pts = (T_inv @ np.c_[grip_spine(t), np.ones(len(t))].T).T
    return float(np.interp(z_local, pts[:, 2], pts[:, 1]))


# --------------------------------------------------------------------------
# Head — head-local coords: origin at bottom centre (= spine top),
# front face at y = -BOX_D/2, tilted by PANEL_TILT and placed on the grip.
# --------------------------------------------------------------------------
HEAD_LOWER = [(-BOX_D / 2, 0), (BOX_D / 2, 0), (BOX_D / 2, FLAT_FACE_H + 12), (-BOX_D / 2, FLAT_FACE_H + 12)]
HEAD_UPPER = [(-BOX_D / 2, FLAT_FACE_H), (BOX_D / 2, FLAT_FACE_H), (BOX_D / 2, BOX_H),
              (-BOX_D / 2 - OVERHANG, BOX_H)]
PAD_PROFILE = [(PAD_Y0, PAD_Z0), (BOX_D / 2, PAD_Z0), (BOX_D / 2, 3.0), (PAD_Y0, 3.0)]


def trigger_face():
    """(mid_y, mid_z, tilt_deg) of the trigger face (first profile edge)."""
    (y0, z0), (y1, z1) = TRIGGER_PROFILE[0], TRIGGER_PROFILE[1]
    dy, dz = y1 - y0, z1 - z0
    ny, nz = dz, -dy                      # outward normal of a CCW edge
    n = math.hypot(ny, nz)
    ny, nz = ny / n, nz / n
    tilt = math.degrees(math.atan2(-ny, nz))
    return (y0 + y1) / 2, (z0 + z1) / 2, tilt


def button_frames():
    """Head-local frames: top row (3), bottom row (3), trigger (2)."""
    frames = [panel_frame(x, TOP_ROW_MID[0], TOP_ROW_MID[1], TOP_ROW_TILT) for x in BUTTON_X]
    frames += [panel_frame(x, -BOX_D / 2, FLAT_ROW_Z, 90.0) for x in BUTTON_X]
    ty, tz, tilt = trigger_face()
    frames += [panel_frame(x, ty, tz, tilt) for x in TRIGGER_X]
    return frames


def pcb_plane_y():
    """head-local y of the PCB front face: jack centred over the cable channel."""
    return spine_in_head(BOARD_Z0) + JACK_T / 2


def head_hole_points():
    return [(sx * (BOX_W / 2 - PLATE_MARGIN - 4.0), FLAT_FACE_H / 2 + 7.0) for sx in (-1, 1)]


def pad_hole_points():
    return [(sx * 7.0, BOARD_Z0 - 6.0) for sx in (-1, 1)]


def head_parts():
    """Returns (outer, cavity, additions, cuts) all in head-local coords."""
    hulls = [(HEAD_LOWER, BOX_W / 2), (HEAD_UPPER, BOX_W / 2), (TRIGGER_PROFILE, TRIGGER_HALF_W)]
    outer = union(*[rounded_hull(p, hw, EDGE_R, EDGE_R) for p, hw in hulls],
                  rounded_hull(PAD_PROFILE, PAD_HALF_W, 3.0, 3.0))
    cavity = union(*[rounded_hull(p, hw, EDGE_R, EDGE_R - WALL) for p, hw in hulls])

    y_in = BOX_D / 2 - WALL                       # inner face of the back wall
    y_pcb = pcb_plane_y()

    # head opening + ledge + two side bosses
    ow, oh = BOX_W - 2 * PLATE_MARGIN, BOX_H - 2 * PLATE_MARGIN
    opening = box_at([ow, WALL + 2, oh], [0, y_in + WALL / 2 + 0.5, BOX_H / 2])
    ledge = difference(box_at([ow + 2 * LEDGE, LEDGE, oh + 2 * LEDGE], [0, y_in - LEDGE / 2, BOX_H / 2]),
                       box_at([ow - 2 * LEDGE, LEDGE + 2, oh - 2 * LEDGE], [0, y_in - LEDGE / 2, BOX_H / 2]))
    bosses, boss_holes = [], []
    for bx, bz in head_hole_points():
        bosses.append(box_at([BOSS, BOSS + LEDGE, BOSS], [bx, y_in - (BOSS + LEDGE) / 2, bz]))
        h = cyl(M4_TAP_D / 2, BOSS + LEDGE + 1, 0)
        h.apply_transform(rotation_matrix(math.radians(90), [1, 0, 0]))  # +Z -> -Y
        h.apply_translation([bx, y_in + 0.5, bz])
        boss_holes.append(h)

    # neck pocket for the Pro Micro: open to the back (under the plate tab) and up
    # into the head cavity. Board rests on the pocket floor, jack over the channel.
    pocket_front = y_pcb - JACK_T - 0.7
    pocket = box_at([POCKET_W, y_in + 1.0 - pocket_front, 3.5 - (BOARD_Z0 - 1.5)],
                    [0, (y_in + 1.0 + pocket_front) / 2, (3.5 + BOARD_Z0 - 1.5) / 2])
    # ribs on the pocket side walls behind the header plastic keep the board against the front wall
    rib_y = y_pcb + PCB_T + 2.5 + 0.3
    ribs = [box_at([2.6, 1.2, PCB_L + 2], [sx * (POCKET_W / 2 - 1.0), rib_y + 0.6, BOARD_Z0 + PCB_L / 2 - 1])
            for sx in (-1, 1)]
    # recess in the pad so the plate tab sits flush, + tab bosses below the pocket
    recess = box_at([2 * PAD_HALF_W - 4.6, PLATE_T + 1, PLATE_MARGIN + 0.1 - (PAD_Z0 + 2.8)],
                    [0, y_in + (PLATE_T + 1) / 2, (PLATE_MARGIN + 0.1 + PAD_Z0 + 2.8) / 2])
    for bx, bz in pad_hole_points():
        h = cyl(M4_TAP_D / 2, 9.0, 0)
        h.apply_transform(rotation_matrix(math.radians(90), [1, 0, 0]))
        h.apply_translation([bx, y_in + 0.5, bz])
        boss_holes.append(h)

    # button bezels, through holes, switch pockets
    bezel = cyl(BEZEL_D / 2, BEZEL_H, 0)
    through = cyl(CAP_HOLE_D / 2, WALL + BEZEL_H + 2, -WALL - 1)
    spocket = box_at([SWITCH_POCKET, SWITCH_POCKET, SWITCH_POCKET_DEPTH + 1],
                     [0, 0, -WALL + SWITCH_POCKET_DEPTH / 2 - 0.5])
    bezels, button_cuts = [], []
    for m in button_frames():
        bezels.append(tf(bezel, m))
        button_cuts += [tf(through, m), tf(spocket, m)]

    additions = [ledge] + bosses + ribs + bezels
    cuts = [opening, pocket, recess] + boss_holes + button_cuts
    return outer, cavity, additions, cuts


def build_back_plate():
    y_c = BOX_D / 2 - PLATE_T / 2
    ow, oh = BOX_W - 2 * PLATE_MARGIN - 0.4, BOX_H - 2 * PLATE_MARGIN - 0.4
    head = box_at([ow, PLATE_T, oh], [0, y_c, BOX_H / 2])
    tab_w = 2 * PAD_HALF_W - 4.6 - 0.4
    tab = box_at([tab_w, PLATE_T, PLATE_MARGIN + 0.5 - (PAD_Z0 + 3.0)], [0, y_c, (PLATE_MARGIN + 0.5 + PAD_Z0 + 3.0) / 2])
    plate = union(head, tab)
    holes = []
    for bx, bz in head_hole_points() + pad_hole_points():
        h = csk_hole(M4_CLEAR_D, M4_CSK_D, PLATE_T + 1, 0)
        h.apply_transform(rotation_matrix(math.radians(-90), [1, 0, 0]))  # +Z -> +Y
        h.apply_translation([bx, BOX_D / 2, bz])
        holes.append(h)
    return difference(plate, *holes)


def build_board_mockup():
    """Pro Micro envelope in head-local coords: PCB, micro-USB jack, header plastic and
    pin envelopes. Not printable — for fit checks and the viewer only."""
    y0 = pcb_plane_y()
    pcb = box_at([PCB_W, PCB_T, PCB_L], [0, y0 + PCB_T / 2, BOARD_Z0 + PCB_L / 2])
    jack = box_at([7.5, JACK_T, 6.0], [0, y0 - JACK_T / 2, BOARD_Z0 - 1 + 3])
    parts, pins = [pcb, jack], []
    for sx in (-1, 1):
        x = sx * (PCB_W / 2 - 1.27 - 0.4)
        parts.append(box_at([2.54, 2.5, 12 * 2.54], [x, y0 + PCB_T + 1.25, BOARD_Z0 + 1.5 + 6 * 2.54]))
        pins.append(box_at([0.7, 6.0, 12 * 2.54 - 0.5], [x, y0 + PCB_T + 2.5 + 3.0, BOARD_Z0 + 1.5 + 6 * 2.54]))
    return union(*parts), union(*pins)


def build_button_cap():
    """Cap in panel-local coordinates: z=0 is the panel surface."""
    head = cyl(CAP_D / 2, CAP_H - 0.8, BEZEL_H + 0.4)
    crown = cyl(CAP_D / 2 - 0.8, 0.8, BEZEL_H + 0.4 + CAP_H - 0.8)
    stem = cyl(CAP_HOLE_D / 2 - 0.4, BEZEL_H + 0.4 + 1.5, -1.5)
    cap = union(head, crown, stem)
    socket = cyl(PLUNGER_SOCKET_D / 2, 4.5, -1.6)
    return difference(cap, socket)


# --------------------------------------------------------------------------
# Grip and base
# --------------------------------------------------------------------------
def grip_radius(t):
    knots = [0.00, 0.10, 0.25, 0.48, 0.65, 0.80, 0.92, 1.00]
    radii = [21.5, 19.0, 18.5, 21.5, 20.0, 17.0, 17.0, 17.0]
    r = np.interp(t, knots, radii)
    k = 9
    pad = np.pad(r, (k // 2, k // 2), mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")


def build_grip_parts():
    """Returns (solids, cuts) in world coords."""
    t = np.linspace(0, 1.05, 100)           # ends ~6 mm inside the head floor
    grip = sweep(grip_spine(t), grip_radius(t), ellip=GRIP_ELLIP)

    collar = cyl(COLLAR_R, COLLAR_H, 0)
    knurls = []
    for i in range(28):
        g = box_at([1.6, 3.0, COLLAR_H - 4], [COLLAR_R, 0, COLLAR_H / 2])
        g.apply_transform(rotation_matrix(2 * math.pi * i / 28, [0, 0, 1]))
        knurls.append(g)

    sphere = icosphere(subdivisions=3, radius=BASE_T / 2)          # fully rounded base disc
    rr = BASE_R - BASE_T / 2
    pts = np.vstack([sphere.vertices + [rr * math.cos(a), rr * math.sin(a), -BASE_T / 2]
                     for a in np.linspace(0, 2 * math.pi, 64, endpoint=False)])
    base = trimesh.convex.convex_hull(pts)
    base_holes = []
    for i in range(4):
        a = math.radians(45 + 90 * i)
        h = csk_hole(M4_CLEAR_D, M4_CSK_D, BASE_T + 2, 0)
        h.apply_translation([BASE_PCD / 2 * math.cos(a), BASE_PCD / 2 * math.sin(a), 0])
        base_holes.append(h)

    tc = np.linspace(-0.07, 1.12, 100)      # USB channel, through the base -> head cavity
    channel = sweep(grip_spine(tc), np.full(len(tc), CABLE_D / 2), ellip=1.0, sections=32)
    groove = box_at([BASE_GROOVE_W, BASE_R + 2, BASE_GROOVE_D + 1], [0, (BASE_R + 2) / 2, -BASE_T + BASE_GROOVE_D / 2 - 0.5])
    return [grip, collar, base], knurls + base_holes + [channel, groove]


# --------------------------------------------------------------------------
# Assembly / export
# --------------------------------------------------------------------------
def stl_b64(mesh):
    return base64.b64encode(mesh.export(file_type="stl")).decode("ascii")


def main():
    os.makedirs(OUT, exist_ok=True)
    T = head_transform()

    print("building head ...")
    outer, cavity, additions, cuts = head_parts()
    outer, cavity = tf(outer, T), tf(cavity, T)
    additions = [tf(m, T) for m in additions]
    cuts = [tf(m, T) for m in cuts]

    print("building grip ...")
    grip_solids, grip_cuts = build_grip_parts()

    print("joining ...")
    body = union(outer, *grip_solids)
    body = difference(body, cavity)
    body = union(body, *additions)
    body = difference(body, *cuts, *grip_cuts)

    plate = tf(build_back_plate(), T)
    board, pins = build_board_mockup()
    board, pins = tf(board, T), tf(pins, T)
    cap = build_button_cap()
    colors = TOP_ROW_COLORS + BOTTOM_ROW_COLORS + TRIGGER_COLORS
    caps = [(tf(cap, T @ m), c, T @ m) for m, c in zip(button_frames(), colors)]

    plate_explode = (T[:3, :3] @ [0, 1, 0] * 40).tolist()
    parts = [("body", body, BODY_COLOR, [0, 0, 0]),
             ("back_plate", plate, PLATE_COLOR, plate_explode),
             ("board", board, PCB_COLOR, plate_explode),
             ("board_pins", pins, PIN_COLOR, plate_explode)]
    parts += [(f"cap_{i}", m, c, (fr[:3, :3] @ [0, 0, 1] * 14).tolist()) for i, (m, c, fr) in enumerate(caps)]

    for name, mesh, _, _ in parts:
        assert mesh.is_watertight, f"{name} is not watertight"
        assert mesh.is_volume, f"{name} is not a valid volume"

    # fit checks: the board envelope must not collide with the body or the plate
    for name, other in (("body", body), ("plate", plate)):
        for bname, bm in (("board", board), ("pins", pins)):
            hit = trimesh.boolean.intersection([bm, other], engine="manifold")
            assert hit.is_empty or hit.volume < 0.05, f"{bname} collides with {name}: {hit.volume:.2f} mm3 at {hit.bounds}"
    print("fit check: board and pins clear the body and the plate")

    body.export(os.path.join(OUT, "joystick_body.stl"))
    plate.export(os.path.join(OUT, "joystick_back_plate.stl"))
    cap.export(os.path.join(OUT, "joystick_button_cap.stl"))
    trimesh.util.concatenate([board, pins]).export(os.path.join(OUT, "pro_micro_mockup.stl"))
    assembly = trimesh.util.concatenate([m for n, m, _, _ in parts if not n.startswith("board")])
    assembly.export(os.path.join(OUT, "joystick_assembly.stl"))

    scene = {
        "units": "mm",
        "bounds": assembly.bounds.tolist(),
        "parts": [{"name": n, "color": c, "explode": e, "stl": stl_b64(m)} for n, m, c, e in parts],
    }
    with open(os.path.join(OUT, "scene.json"), "w") as f:
        json.dump(scene, f)
    ty, tz, ttilt = trigger_face()
    meta = {
        "head_transform": T.tolist(),
        "head": {"w": BOX_W, "h": BOX_H, "d": BOX_D, "overhang": OVERHANG, "flat_face_h": FLAT_FACE_H,
                 "panel_tilt": PANEL_TILT, "pitch": BUTTON_PITCH},
        "trigger": {"mid_y": ty, "mid_z": tz, "tilt": ttilt, "profile": TRIGGER_PROFILE},
        "bounds": assembly.bounds.tolist(),
        "buttons": [(T @ m)[:3, 3].tolist() for m in button_frames()],
        "board": {"pcb": [PCB_L, PCB_W, PCB_T], "z0": BOARD_Z0, "pcb_plane_y": pcb_plane_y(), "cable_d": CABLE_D},
    }
    with open(os.path.join(OUT, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)

    print(f"head {BOX_W:.0f} x {BOX_H:.0f} x {BOX_D:.0f} mm (+{OVERHANG:.0f} overhang), trigger face tilt {ttilt:.1f} deg")
    print(f"assembly bounds (mm): min {assembly.bounds[0].round(1)}  max {assembly.bounds[1].round(1)}")
    for name, mesh, _, _ in parts[:4]:
        print(f"  {name:12s} {len(mesh.faces):6d} tris  volume {mesh.volume / 1000:.1f} cm3")
    print("done ->", OUT)


if __name__ == "__main__":
    main()
