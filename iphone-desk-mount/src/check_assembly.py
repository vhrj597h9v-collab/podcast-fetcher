#!/usr/bin/env python3
"""Virtual assembly check: places the exported STLs in their mating positions and measures clearances /
interference between every mating pair (mesh surface sampling + signed distance).  Also prints the height
stack-up.  Run after build.py.   Exported meshes are bbox-centred in XY with z >= 0 (build.py)."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import trimesh
import params as P
from lib import fitcheck as F

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stl')


def load(n):
    return trimesh.load(os.path.join(S, n + '.stl'), force='mesh')


def rot(m, ax, deg):
    m = m.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), ax)); return m


def tr(m, v):
    m = m.copy(); m.apply_translation(v); return m


def zslice(m, z0, z1):
    return m.slice_plane([0, 0, z0], [0, 0, 1]).slice_plane([0, 0, z1], [0, 0, -1])


def report(label, inner, outer, n=5000, expect=''):
    r = F.clearance_report(inner, outer, n)
    mg = r['min_gap_mm']
    md = r['median_gap_mm']
    mg_s = '-' if mg is None else '%.3f' % mg
    md_s = '-' if md is None else '%.3f' % md
    print("%-58s interf %.3f mm (%4.1f%% pts)  min gap %s  median %s   %s" % (
        label, r['max_interference_mm'], r['interfering_fraction'] * 100, mg_s, md_s, expect))
    return r


def main():
    L = P.SEG_LEN
    seg = load('pole_segment')
    # 1. segment on segment
    zB = L - P.SPIGOT_LEN + P.SEAT_GAP
    spig = zslice(seg, L - P.SPIGOT_LEN + 0.5, L - 0.5)
    B = tr(seg, [0, 0, zB])
    report("segment spigot in next segment socket @nominal seat", spig, B, expect='(expect ~0 both)')
    report("  ... upper segment lifted 1.0 mm", spig, tr(B, [0, 0, 1.0]), expect='(expect gap ~0.044, no interf)')
    report("  ... upper segment pushed 1.0 mm deeper", spig, tr(B, [0, 0, -1.0]), expect='(expect interf ~0.044 on flats)')
    # 2. head on top spigot
    head = load('head')
    report("segment spigot in head socket @nominal seat", spig, tr(head, [0, 0, zB]), expect='(expect ~0 both)')
    # 3. segment external taper in the clamp diamond socket.  clamp export frame: print = (use_x, -use_z, use_y), bbox-centred
    clamp = load('clamp_body')
    cl = rot(clamp, [1, 0, 0], -90)                       # -> (use_x, use_z, ...) up to offsets
    b = cl.bounds
    cl = tr(cl, [-(b[0][0] + 22.0), -(b[0][1] + b[1][1]) / 2, -(b[1][2] - (P.TOP_JAW_T + P.TOWER_H))])
    assert abs(cl.bounds[0][2] + (P.THROAT + P.BOTTOM_JAW_T)) < 0.5, cl.bounds
    segd = rot(seg, [0, 0, 1], 45)
    z_mouth = P.TOP_JAW_T + P.TOWER_H
    segd = tr(segd, [P.TOWER_CENTER_X, 0, z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)])
    low = zslice(segd, segd.bounds[0][2] + 0.5, z_mouth - 0.5)
    report("segment external taper in clamp socket @nominal seat", low, cl, expect='(expect ~0 both)')
    report("  ... segment lifted 1 mm", low, tr(cl, [0, 0, -1.0]), expect='(expect gap ~0.044)')
    # 4. nut block in its pocket
    nb = load('nut_block')
    nb = tr(nb, [P.SCREW_X, 0, -P.THROAT - P.NUT_BLOCK_H])
    report("nut block in clamp pocket", nb, cl, 3000, expect='(expect gap >= 0.3)')
    # 5. carrier: export = (-fork_z, fork_y, fork_x) bbox-centred; rotate +90 about Y -> (fork_x, fork_y, fork_z) + offsets
    car = rot(load('carrier'), [0, 1, 0], 90)
    cb = car.bounds
    car = tr(car, [-(cb[1][0] - (P.TONGUE_X1 + P.BOSS_LEN)), -(cb[0][1] + cb[1][1]) / 2, 0])
    tipv = car.vertices[car.vertices[:, 0] > P.TONGUE_X1 + P.BOSS_LEN - 0.1]
    car = tr(car, [0, 0, -(tipv[:, 2].min() + tipv[:, 2].max()) / 2 + P.BOSS_Z])      # boss tip centre is fork z = BOSS_Z -> hinge axis at z = 0
    assert abs(car.bounds[0][2] + P.TONGUE_DOWN) < 0.3 and abs(car.bounds[1][2] - P.HEADPLATE_Z1) < 0.3, car.bounds
    # 5a. boss in cradle socket.  cradle export: x centred (symmetric), y centred (-L/2..L/2), z >= 0
    cr = load('cradle')
    cy = P.LIP_H + P.PAD_Y - P.SPINE_LEN / 2
    carz = rot(car, [0, 1, 0], -90)                                    # fork +x -> +z ; boss axis -> z axis through (0,0)
    carz = tr(carz, [0, 0, -(P.TONGUE_X1 + P.BOSS_LEN)])               # tip at z = 0
    depth = P.CRADLE_SOCKET_DEPTH - P.BOSS_SEAT_GAP
    carz = tr(carz, [P.BOSS_Z, cy, depth])                             # boss axis (fork z=BOSS_Z -> x=-BOSS_Z) onto the socket axis; tip at seat depth
    boss = zslice(carz, 0.3, depth - 0.3)
    report("carrier boss in cradle socket @nominal seat", boss, cr, 3000, expect='(expect ~0 both)')
    report("  ... boss pulled back 1 mm", boss, tr(cr, [0, 0, 1.0]), 3000, expect='(expect gap ~0.087)')
    # 5b. tongue between the head ears (fork frame aligned: un-rotate the head by -45)
    hd = rot(head, [0, 0, 1], -P.FORK_ROT_DEG)
    za = P.HEAD_TOP + P.TILT_AXIS_H
    tongue = zslice(tr(car, [0, 0, za]), za - P.TONGUE_DOWN + 0.5, za + 12.0)
    report("carrier tongue between head ears", tongue, hd, 4000, expect='(expect gap >= 0.1 at the rings)')
    # 6. slider on the plain spine.  slider export = frame rotated -90 about X: (x, z, -y); inverse +90: (x, -z, y)
    sl = rot(load('slider'), [1, 0, 0], 90)
    sb = sl.bounds
    sl = tr(sl, [-(sb[0][0] + sb[1][0]) / 2, -sb[0][1] - P.SLIDER_HOOK, -sb[0][2] - (P.SLIDE_CLR + P.SLIDER_BACK_WALL)])
    y0 = 150.0 - P.SPINE_LEN / 2
    spine_seg = cr.slice_plane([0, y0, 0], [0, 1, 0]).slice_plane([0, y0 + 20, 0], [0, -1, 0])
    report("slider on cradle spine", spine_seg, tr(sl, [0, y0 - 1.0, 0]), 3000, expect='(expect gap ~0.3)')
    # 7. ball in pad
    pad = load('swivel_pad')
    r_cav = P.BALL_D / 2 + P.PAD_SOCKET_CLR; opening = P.BALL_D - 1.5
    zc = (P.PAD_H + 2.0) - math.sqrt(r_cav ** 2 - (opening / 2) ** 2)
    ball = tr(trimesh.creation.icosphere(subdivisions=4, radius=P.BALL_D / 2), [0, 0, zc])
    report("ball in pad socket", ball, pad, 3000, expect='(expect gap ~0.2)')
    # 8. stack-up
    seg1_bottom = z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)
    tops = []
    bottom = seg1_bottom
    for i in range(P.SEG_COUNT):
        top = bottom + L; tops.append((bottom, top)); bottom = top - P.SPIGOT_LEN + P.SEAT_GAP
    head_bottom = bottom
    axis = head_bottom + P.HEAD_TOP + P.TILT_AXIS_H
    phone_c = axis + P.BOSS_Z
    per_seg = L - P.SPIGOT_LEN + P.SEAT_GAP
    print(f"\nSTACK-UP (desk top = 0 mm): clamp socket mouth {z_mouth:.0f}; segments {[(round(a),round(b)) for a,b in tops]}; "
          f"head base {head_bottom:.0f}; tilt axis {axis:.0f}; phone centre ~{phone_c:.0f} mm = {phone_c/25.4:.1f} in "
          f"(3 segments) | {phone_c-per_seg:.0f} mm (2) | {phone_c-2*per_seg:.0f} mm (1)")


if __name__ == '__main__':
    main()
