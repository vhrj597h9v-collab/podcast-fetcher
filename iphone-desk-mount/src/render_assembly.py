#!/usr/bin/env python3
"""Compose the exported STLs into the assembled mount (desk top = z 0, desk edge = x 0, arm straight up) and write
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
cl = rot(load('clamp_body'), [1, 0, 0], -90); b = cl.bounds
cl = tr(cl, [-(b[0][0] + P.SPINE_T), -(b[0][1] + b[1][1]) / 2, -(b[1][2] - (P.TOP_JAW_T + P.TOWER_H))]); parts.append(cl)
z_mouth = P.TOP_JAW_T + P.TOWER_H
desk_t = 30.0
scr = load('clamp_screw'); z_thread_top = P.TBAR_H + 2.0 + P.SCREW_THREAD_LEN
r_cav = P.BALL_D / 2 + P.PAD_SOCKET_CLR; opening = P.BALL_D - 2 * P.PAD_SNAP_OVERLAP
zc = (P.PAD_H + 2.0) - math.sqrt(r_cav ** 2 - (opening / 2) ** 2)
ball_c_print = z_thread_top + P.BALL_NECK_H + P.BALL_D / 2 - 1.0
parts.append(tr(scr, [P.SCREW_X, 0, (-desk_t - zc) - ball_c_print]))
pad = rot(load('swivel_pad'), [1, 0, 0], 180); parts.append(tr(pad, [P.SCREW_X, 0, -desk_t - pad.bounds[1][2]]))
parts.append(tr(load('nut_block'), [P.SCREW_X, 0, -P.THROAT - P.NUT_BLOCK_H]))
desk = trimesh.creation.box((160, 220, desk_t)); parts.append(tr(desk, [80, 0, -desk_t / 2]))
# lower arm (its base is diamond vs its tube; the tube ends up square to the desk edge)
arm_bottom = z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)
parts.append(tr(load('arm_lower'), [P.TOWER_CENTER_X, 0, arm_bottom]))
za_arm = arm_bottom + P.ARM_LOWER_H - P.ELBOW_EAR_TOP_R
# elbow tongue: flip (spigot up), half-pitch, engaged offset
tg = rot(load('elbow_tongue'), [1, 0, 0], 180)
tg = tr(tg, [0, 0, P.SPIGOT_LEN + P.ELBOW_FLARE2_H + P.ELBOW_TONGUE_UP])
tg = rot(tg, [0, 1, 0], 180.0 / P.ELBOW_HIRTH_N)
parts.append(tr(tg, [P.TOWER_CENTER_X, P.ELBOW_TONGUE_ENGAGED_OFFSET, za_arm]))
spigot_base = za_arm + P.ELBOW_TONGUE_UP + P.ELBOW_FLARE2_H
seg_bottom = spigot_base + P.SEAT_GAP
parts.append(tr(load('pole_segment'), [P.TOWER_CENTER_X, 0, seg_bottom]))
head_bottom = seg_bottom + P.SEG_LEN - P.SPIGOT_LEN + P.SEAT_GAP
parts.append(tr(load('head'), [P.TOWER_CENTER_X, 0, head_bottom]))
za = head_bottom + P.HEAD_TOP + P.TILT_AXIS_H
# carrier in the fork frame (hinge at the origin), rotated half a pitch, engaged offset
car = rot(load('carrier'), [0, 1, 0], 90); cb = car.bounds
car = tr(car, [-(cb[1][0] - (P.TONGUE_X1 + P.BOSS_LEN)), -(cb[0][1] + cb[1][1]) / 2, 0])
tipv = car.vertices[car.vertices[:, 0] > P.TONGUE_X1 + P.BOSS_LEN - 0.1]
car = tr(car, [0, 0, -(tipv[:, 2].min() + tipv[:, 2].max()) / 2 + P.BOSS_Z])
car = rot(car, [0, 1, 0], 180.0 / P.HIRTH_N); car = tr(car, [0, P.TONGUE_ENGAGED_OFFSET, 0])
fork = [car]
Mc = np.eye(4); Mc[:3, :3] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=float)
def to_fork(m):
    m = m.copy(); m.apply_transform(Mc); return m
x_back = P.TONGUE_X1 + P.BOSS_LEN + P.BOSS_SEAT_GAP
cy = P.PAD_Y - (P.SPINE_LEN - 2 * P.LIP_H) / 2
y_foot = -(P.SPINE_LEN - 2 * P.LIP_H) / 2
shift = [x_back, 0, P.BOSS_Z - cy]
fork.append(tr(to_fork(load('cradle')), shift))
sl = rot(load('slider'), [1, 0, 0], 90); sb = sl.bounds
sl = tr(sl, [-(sb[0][0] + sb[1][0]) / 2, -sb[0][1], -sb[0][2] - (P.SLIDE_CLR + P.SLIDER_BACK_WALL)])
phone_len, phone_t = 160.0, 8.0
foot = phone_len + 2 * phone_t * math.tan(math.radians(90 - P.JAW_INCLINE_DEG))
sl = tr(sl, [0, y_foot + foot - P.SLIDER_LEN, 0])
fork.append(tr(to_fork(sl), shift))
phone = trimesh.creation.box((76.0, phone_len, phone_t)); phone = tr(phone, [0, y_foot + phone_t * 0.577 + phone_len / 2, P.REST_Z + phone_t / 2])
fork.append(tr(to_fork(phone), shift))
forkm = trimesh.util.concatenate(fork)
forkm = tr(rot(forkm, [0, 0, 1], P.FORK_ROT_DEG), [P.TOWER_CENTER_X, 0, za])
parts.append(forkm)
asm = trimesh.util.concatenate(parts)
asm.export(os.path.join(S, 'ASSEMBLED_PREVIEW.stl'))
print('assembled bounds', asm.bounds.round(1).tolist(), 'phone top z', round(forkm.bounds[1][2], 1))
