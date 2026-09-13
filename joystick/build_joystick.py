#!/usr/bin/env python3
"""
Parametric 8-button joystick — model builder.

Thumb-operated head: the 100 x 70 mm button panel stands vertical and faces the
user (tilted a further PANEL_TILT degrees down towards the thumb).  The bottom
row of four buttons sits on the flat panel; the top row sits on an upper block
that overhangs the flat face, its face tipped 45 deg down towards the user so the
thumb reaches it from below.
Every edge of the head, base and grip is rounded.

Exports (all mm, Z up, -Y is towards the user):

  out/joystick_body.stl        head + grip + base, one FDM print
  out/joystick_back_plate.stl  rear access plate, 4x M4 countersunk
  out/joystick_button_cap.stl  one button cap (print 8)
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
BOX_W = 100.0          # X, panel width
BOX_H = 70.0           # panel height (flat face + chamfer rise)
BOX_D = 48.0           # Y, depth of the main head block
OVERHANG = 24.0        # the top row face overhangs the flat face by this much, tipped 45 deg
                       # down towards the user's thumb (rise == run)
EDGE_R = 6.0           # fillet radius on every head edge
WALL = 3.0             # shell wall thickness
PANEL_TILT = 10.0      # extra tilt of the whole head down towards the thumb (deg)

BUTTON_PITCH = 22.0
BUTTON_X = [(-1.5 + i) * BUTTON_PITCH for i in range(4)]   # -33, -11, 11, 33
FLAT_FACE_H = BOX_H - OVERHANG                             # 46: height of the flat front face
FLAT_ROW_Z = 23.0                                          # bottom row, centred on the flat face
TOP_ROW_MID = (-BOX_D / 2 - OVERHANG / 2, FLAT_FACE_H + OVERHANG / 2)  # (y, z) top row, mid-face
TOP_ROW_TILT = 135.0                                       # normal points down + towards the user

CAP_D = 10.0           # button cap diameter (spec: 10 mm)
CAP_H = 8.0            # cap height above bezel (spec: 8 mm)
BEZEL_D = 14.0
BEZEL_H = 2.0
CAP_HOLE_D = 10.6      # panel through hole for cap stem
SWITCH_POCKET = 6.8    # 6x6 tactile switch, +0.8 clearance
SWITCH_POCKET_DEPTH = 1.5
PLUNGER_SOCKET_D = 3.6

M4_CLEAR_D = 4.5
M4_TAP_D = 3.3
M4_CSK_D = 9.0
BOSS = 8.0
PLATE_T = 3.0
PLATE_MARGIN = 8.0     # plate inset from the head outline
LEDGE = 5.0            # ledge behind the plate opening

GRIP_H = 120.0         # base top -> head bottom
GRIP_ELLIP = 0.92      # cross-section: rx = r * ellip (deeper than wide, like a real stick)
COLLAR_R = 23.0
COLLAR_H = 14.0
BASE_R = 36.0
BASE_T = 6.0
BASE_PCD = 58.0
CABLE_D = 8.0

TOP_ROW_COLORS = ["#d81e1e", "#f2f2f2", "#1e64d8", "#1a1a1a"]      # red white blue black
BOTTOM_ROW_COLORS = ["#f2c800", "#22a83a", "#f07f16", "#8a8a8a"]   # yellow green orange grey
BODY_COLOR = "#252528"
PLATE_COLOR = "#1f1f22"


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
    tilt rotates +Z about X: 90 -> faces -Y (the user), 45 -> up and towards the user."""
    return translation_matrix([x, y, z]) @ rotation_matrix(math.radians(tilt_deg), [1, 0, 0])


def tf(mesh, matrix):
    m = mesh.copy()
    m.apply_transform(matrix)
    return m


# --------------------------------------------------------------------------
# Head (button box) — built in head-local coords: origin at bottom centre,
# front face at y = -BOX_D/2, then tilted by PANEL_TILT and placed on the grip.
# --------------------------------------------------------------------------
# The head is the union of two convex rounded blocks: the main block (flat face,
# bottom row) and the upper block whose front face slopes forward over the thumb.
HEAD_LOWER = [(-BOX_D / 2, 0), (BOX_D / 2, 0), (BOX_D / 2, FLAT_FACE_H + 12), (-BOX_D / 2, FLAT_FACE_H + 12)]
HEAD_UPPER = [(-BOX_D / 2, FLAT_FACE_H), (BOX_D / 2, FLAT_FACE_H), (BOX_D / 2, BOX_H),
              (-BOX_D / 2 - OVERHANG, BOX_H)]


def button_frames():
    """Head-local frames; top row first (red, white, blue, black), then bottom row."""
    frames = [panel_frame(x, TOP_ROW_MID[0], TOP_ROW_MID[1], TOP_ROW_TILT) for x in BUTTON_X]
    frames += [panel_frame(x, -BOX_D / 2, FLAT_ROW_Z, 90.0) for x in BUTTON_X]
    return frames


def plate_hole_points():
    hx = BOX_W / 2 - PLATE_MARGIN - 5.0
    return [(sx * hx, z) for sx in (-1, 1) for z in (PLATE_MARGIN + 5.0, BOX_H - PLATE_MARGIN - 5.0)]


def head_parts():
    """Returns (outer, cavity, additions, cuts) all in head-local coords."""
    outer = union(rounded_hull(HEAD_LOWER, BOX_W / 2, EDGE_R, EDGE_R),
                  rounded_hull(HEAD_UPPER, BOX_W / 2, EDGE_R, EDGE_R))
    cavity = union(rounded_hull(HEAD_LOWER, BOX_W / 2, EDGE_R, EDGE_R - WALL),
                   rounded_hull(HEAD_UPPER, BOX_W / 2, EDGE_R, EDGE_R - WALL))

    # rear opening for the access plate, cut clean through the back wall
    ow, oh = BOX_W - 2 * PLATE_MARGIN, BOX_H - 2 * PLATE_MARGIN
    opening = tbox(extents=[ow, WALL + 2, oh])
    opening.apply_translation([0, BOX_D / 2 - WALL / 2 + 0.5, BOX_H / 2])

    # ledge frame + screw bosses just inside the opening
    ledge_outer = tbox(extents=[ow + 2 * LEDGE, LEDGE, oh + 2 * LEDGE])
    ledge_outer.apply_translation([0, BOX_D / 2 - WALL - LEDGE / 2, BOX_H / 2])
    ledge_inner = tbox(extents=[ow - 2 * LEDGE, LEDGE + 2, oh - 2 * LEDGE])
    ledge_inner.apply_translation([0, BOX_D / 2 - WALL - LEDGE / 2, BOX_H / 2])
    ledge = difference(ledge_outer, ledge_inner)

    bosses, boss_holes = [], []
    for bx, bz in plate_hole_points():
        b = tbox(extents=[BOSS, BOSS + LEDGE, BOSS])
        b.apply_translation([bx, BOX_D / 2 - WALL - (BOSS + LEDGE) / 2, bz])
        bosses.append(b)
        h = cyl(M4_TAP_D / 2, BOSS + LEDGE + 1, 0)
        h.apply_transform(rotation_matrix(math.radians(90), [1, 0, 0]))  # +Z -> -Y
        h.apply_translation([bx, BOX_D / 2 - WALL + 0.5, bz])
        boss_holes.append(h)

    # button bezels, through holes, switch pockets
    bezel = cyl(BEZEL_D / 2, BEZEL_H, 0)
    through = cyl(CAP_HOLE_D / 2, WALL + BEZEL_H + 2, -WALL - 1)
    pocket = tbox(extents=[SWITCH_POCKET, SWITCH_POCKET, SWITCH_POCKET_DEPTH + 1])
    pocket.apply_translation([0, 0, -WALL + SWITCH_POCKET_DEPTH / 2 - 0.5])
    bezels, button_cuts = [], []
    for m in button_frames():
        bezels.append(tf(bezel, m))
        button_cuts += [tf(through, m), tf(pocket, m)]

    additions = [ledge] + bosses + bezels
    cuts = [opening] + boss_holes + button_cuts
    return outer, cavity, additions, cuts


def build_back_plate():
    ow, oh = BOX_W - 2 * PLATE_MARGIN - 0.4, BOX_H - 2 * PLATE_MARGIN - 0.4   # 0.2 mm clearance
    plate = tbox(extents=[ow, PLATE_T, oh])
    plate.apply_translation([0, BOX_D / 2 - PLATE_T / 2, BOX_H / 2])
    holes = []
    for bx, bz in plate_hole_points():
        h = csk_hole(M4_CLEAR_D, M4_CSK_D, PLATE_T + 1, 0)
        h.apply_transform(rotation_matrix(math.radians(-90), [1, 0, 0]))  # +Z -> +Y
        h.apply_translation([bx, BOX_D / 2, bz])
        holes.append(h)
    return difference(plate, *holes)


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
SPINE = (np.array([0, 0, 0.0]), np.array([0, -10.0, 50.0]),
         np.array([0, -16.0, 98.0]), np.array([0, -14.0, GRIP_H]))


def grip_spine(t):
    return bezier(*SPINE, t)


def grip_radius(t):
    knots = [0.00, 0.10, 0.25, 0.48, 0.65, 0.80, 0.92, 1.00]
    radii = [21.5, 19.0, 18.5, 21.5, 20.0, 16.5, 17.5, 19.0]
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
        g = tbox(extents=[1.6, 3.0, COLLAR_H - 4])
        g.apply_translation([COLLAR_R, 0, COLLAR_H / 2])
        g.apply_transform(rotation_matrix(2 * math.pi * i / 28, [0, 0, 1]))
        knurls.append(g)

    # fully rounded base disc: hull of a ring of spheres
    sphere = icosphere(subdivisions=3, radius=BASE_T / 2)
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

    tc = np.linspace(-0.02, 1.12, 100)      # wiring channel, base underside -> head cavity
    channel = sweep(grip_spine(tc), np.full(len(tc), CABLE_D / 2), ellip=1.0, sections=32)
    return [grip, collar, base], knurls + base_holes + [channel]


# --------------------------------------------------------------------------
# Assembly / export
# --------------------------------------------------------------------------
def head_transform():
    top = grip_spine(np.array([1.0]))[0]
    return translation_matrix(top + [0, -4.0, 0]) @ rotation_matrix(math.radians(PANEL_TILT), [1, 0, 0])


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
    cap = build_button_cap()
    caps = [(tf(cap, T @ m), c, T @ m) for m, c in zip(button_frames(), TOP_ROW_COLORS + BOTTOM_ROW_COLORS)]

    parts = [("body", body, BODY_COLOR, [0, 0, 0]),
             ("back_plate", plate, PLATE_COLOR, (T[:3, :3] @ [0, 1, 0] * 36).tolist())]
    parts += [(f"cap_{i}", m, c, (fr[:3, :3] @ [0, 0, 1] * 14).tolist()) for i, (m, c, fr) in enumerate(caps)]

    for name, mesh, _, _ in parts:
        assert mesh.is_watertight, f"{name} is not watertight"
        assert mesh.is_volume, f"{name} is not a valid volume"

    body.export(os.path.join(OUT, "joystick_body.stl"))
    plate.export(os.path.join(OUT, "joystick_back_plate.stl"))
    cap.export(os.path.join(OUT, "joystick_button_cap.stl"))
    assembly = trimesh.util.concatenate([m for _, m, _, _ in parts])
    assembly.export(os.path.join(OUT, "joystick_assembly.stl"))

    scene = {
        "units": "mm",
        "bounds": assembly.bounds.tolist(),
        "parts": [{"name": n, "color": c, "explode": e, "stl": stl_b64(m)} for n, m, c, e in parts],
    }
    with open(os.path.join(OUT, "scene.json"), "w") as f:
        json.dump(scene, f)
    meta = {
        "head_transform": T.tolist(),
        "head": {"w": BOX_W, "h": BOX_H, "d": BOX_D, "overhang": OVERHANG, "flat_face_h": FLAT_FACE_H,
                 "panel_tilt": PANEL_TILT},
        "bounds": assembly.bounds.tolist(),
        "buttons": [(T @ m)[:3, 3].tolist() for m in button_frames()],
    }
    with open(os.path.join(OUT, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)

    print(f"assembly bounds (mm): min {assembly.bounds[0].round(1)}  max {assembly.bounds[1].round(1)}")
    for name, mesh, _, _ in parts[:3]:
        print(f"  {name:12s} {len(mesh.faces):6d} tris  volume {mesh.volume / 1000:.1f} cm3")
    print("done ->", OUT)


if __name__ == "__main__":
    main()
