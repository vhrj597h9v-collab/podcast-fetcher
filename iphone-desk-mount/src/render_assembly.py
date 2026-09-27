#!/usr/bin/env python3
"""Compose the exported STLs into the assembled mount (desk top = z 0, desk edge = x 0) and write
../stl/ASSEMBLED_PREVIEW.stl plus a PNG.  Preview only: not for printing."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, trimesh
import params as P

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stl')
def load(n): return trimesh.load(os.path.join(S, n + '.stl'), force='mesh')
def rot(m, ax, deg, about=(0, 0, 0)):
    m = m.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), ax, about)); return m
def tr(m, v): m = m.copy(); m.apply_translation(v); return m

parts = []
# clamp body -> use frame
cl = rot(load('clamp_body'), [1, 0, 0], -90); b = cl.bounds
cl = tr(cl, [-(b[0][0] + P.SPINE_T), -(b[0][1] + b[1][1]) / 2, -(b[1][2] - (P.TOP_JAW_T + P.TOWER_H))]); parts.append(cl)
z_mouth = P.TOP_JAW_T + P.TOWER_H
# clamp screw (T-bar down), nut block, pad: desk 30 mm thick -> pad face at z=-30 (desk underside)
desk_t = 30.0
scr = load('clamp_screw')                       # print frame: bar at z 0, ball at top
z_thread_top = P.TBAR_H + 2.0 + P.SCREW_THREAD_LEN
pad_face_z = -desk_t
r_cav = P.BALL_D / 2 + P.PAD_SOCKET_CLR; opening = P.BALL_D - 2 * P.PAD_SNAP_OVERLAP
zc = (P.PAD_H + 2.0) - math.sqrt(r_cav ** 2 - (opening / 2) ** 2)   # ball centre below the pad's desk face
ball_c_use = pad_face_z - zc
ball_c_print = z_thread_top + P.BALL_NECK_H + P.BALL_D / 2 - 1.0
scr = tr(scr, [P.SCREW_X, 0, ball_c_use - ball_c_print]); parts.append(scr)
pad = rot(load('swivel_pad'), [1, 0, 0], 180); pad = tr(pad, [P.SCREW_X, 0, pad_face_z - pad.bounds[1][2]]); parts.append(pad)
parts.append(tr(load('nut_block'), [P.SCREW_X, 0, -P.THROAT - P.NUT_BLOCK_H]))
# desk slab for context
desk = trimesh.creation.box((160, 220, desk_t)); desk = tr(desk, [80, 0, -desk_t / 2]); parts.append(desk)
# pole: 3 segments (diamond), head
seg = rot(load('pole_segment'), [0, 0, 1], 45)
z = z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)
tops = []
for i in range(P.SEG_COUNT):
    parts.append(tr(seg, [P.TOWER_CENTER_X, 0, z])); tops.append(z + P.SEG_LEN); z = z + P.SEG_LEN - P.SPIGOT_LEN + P.SEAT_GAP
head = rot(load('head'), [0, 0, 1], 45); head = tr(head, [P.TOWER_CENTER_X, 0, z]); parts.append(head)
# carrier + cradle + slider in the fork frame (x toward the user = phone direction), then rotate by 45+? The fork is at
# FORK_ROT_DEG from the head base; the head base is at 45 -> fork direction = 90 deg = along -y? Compute: fork x axis
# after both rotations points at 45 + 45 = 90 deg from +x -> along +y.  Rotate the fork-frame assembly by 90 about z.
za = z + P.HEAD_TOP + P.TILT_AXIS_H
car = rot(load('carrier'), [0, 1, 0], 90); cb = car.bounds
car = tr(car, [-(cb[1][0] - (P.TONGUE_X1 + P.BOSS_LEN)), -(cb[0][1] + cb[1][1]) / 2, 0])
tipv = car.vertices[car.vertices[:, 0] > P.TONGUE_X1 + P.BOSS_LEN - 0.1]
car = tr(car, [0, 0, -(tipv[:, 2].min() + tipv[:, 2].max()) / 2 + P.BOSS_Z])
car = rot(car, [0, 1, 0], 180.0 / P.HIRTH_N); car = tr(car, [0, P.TONGUE_ENGAGED_OFFSET, 0])
fork = [car]
# cradle / slider / phone live in the cradle frame (x across the phone, y along the phone, z = thickness).
# Map cradle -> fork: x -> +y (across), y -> +z (up, portrait), z -> +x (toward the user).  Cyclic permutation = rotation.
Mc = np.eye(4); Mc[:3, :3] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)   # columns = images of x, y, z
def to_fork(m):
    m = m.copy(); m.apply_transform(Mc); return m
x_back = P.TONGUE_X1 + P.BOSS_LEN + P.BOSS_SEAT_GAP           # cradle back face, boss seated
cy = P.PAD_Y - (P.SPINE_LEN - 2 * P.LIP_H) / 2                # socket axis y in the bbox-centred cradle export
y_foot = -P.LIP_H - (P.SPINE_LEN - 2 * P.LIP_H) / 2 + P.LIP_H  # phone foot (y=0 of the cradle frame) in export coords = -87
shift = [x_back, 0, P.BOSS_Z - cy]
cr = load('cradle')
fork.append(tr(to_fork(cr), shift))
sl = rot(load('slider'), [1, 0, 0], 90); sb = sl.bounds
sl = tr(sl, [-(sb[0][0] + sb[1][0]) / 2, -sb[0][1] - P.JAW_LEAN, -sb[0][2] - (P.SLIDE_CLR + P.SLIDER_BACK_WALL)])
phone_len = 160.0
sl = tr(sl, [0, y_foot + phone_len, 0])                        # jaw foot at the phone's top edge (export coords)
fork.append(tr(to_fork(sl), shift))
phone = trimesh.creation.box((76.0, phone_len, 8.0)); phone = tr(phone, [0, y_foot + phone_len / 2, P.REST_Z + 4.0])
fork.append(tr(to_fork(phone), shift))
forkm = trimesh.util.concatenate(fork)
forkm = tr(rot(forkm, [0, 0, 1], 45 + P.FORK_ROT_DEG), [P.TOWER_CENTER_X, 0, za])
parts.append(forkm)
asm = trimesh.util.concatenate(parts)
asm.export(os.path.join(S, 'ASSEMBLED_PREVIEW.stl'))
print('assembled bounds', asm.bounds.round(1).tolist(), 'phone top z', round(forkm.bounds[1][2], 1))
