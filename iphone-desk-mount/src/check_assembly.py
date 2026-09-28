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
    cl = tr(cl, [-(b[0][0] + P.SPINE_T), -(b[0][1] + b[1][1]) / 2, -(b[1][2] - (P.TOP_JAW_T + P.TOWER_H))])
    assert abs(cl.bounds[0][2] + (P.THROAT + P.BOTTOM_JAW_T)) < 0.5, cl.bounds
    arm = load('arm_lower')                                        # its base is already diamond vs its tube/fork
    z_mouth = P.TOP_JAW_T + P.TOWER_H
    arm = tr(arm, [P.TOWER_CENTER_X, 0, z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)])
    low = zslice(arm, arm.bounds[0][2] + 0.5, z_mouth - 0.5)
    report("arm_lower base taper in clamp socket @nominal seat", low, cl, expect='(expect ~0 both)')
    report("  ... arm lifted 1 mm", low, tr(cl, [0, 0, -1.0]), expect='(expect gap ~0.044)')
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
    cy = P.PAD_Y - (P.SPINE_LEN - 2 * P.LIP_H) / 2        # export frame is bbox-centred: y spans -LIP_H .. SPINE_LEN-LIP_H
    carz = rot(car, [0, 1, 0], -90)                                    # fork +x -> +z ; boss axis -> z axis through (0,0)
    carz = tr(carz, [0, 0, -(P.TONGUE_X1 + P.BOSS_LEN)])               # tip at z = 0
    depth = P.CRADLE_SOCKET_DEPTH - P.BOSS_SEAT_GAP
    carz = tr(carz, [P.BOSS_Z, cy, depth])                             # boss axis (fork z=BOSS_Z -> x=-BOSS_Z) onto the socket axis; tip at seat depth
    boss = zslice(carz, 0.3, depth - 0.3)
    report("carrier boss in cradle socket @nominal seat", boss, cr, 3000, expect='(expect ~0 both)')
    report("  ... boss pulled back 1 mm", boss, tr(cr, [0, 0, 1.0]), 3000, expect='(expect gap ~0.087)')
    # 5b. tongue between the head ears, LOCKED: rotated half a tooth pitch so the Hirth rings interlock, shifted
    #     TONGUE_ENGAGED_OFFSET toward the toothed ear: flanks touch (gap ~0), crests keep 0.4 from the roots.
    hd = rot(head, [0, 0, 1], -P.FORK_ROT_DEG)
    za = P.HEAD_TOP + P.TILT_AXIS_H
    car_half = rot(car, [0, 1, 0], 180.0 / P.HIRTH_N)
    tongue = zslice(tr(car_half, [0, P.TONGUE_ENGAGED_OFFSET, za]), za - P.TONGUE_DOWN + 0.5, za + 12.0)
    report("carrier tongue locked between head ears (Hirth engaged)", tongue, hd, 8000, expect='(expect ~0 interf, min gap ~0)')
    tongue_free = zslice(tr(car_half, [0, P.TONGUE_ENGAGED_OFFSET + P.TONGUE_UNLOCK_SHIFT, za]), za - P.TONGUE_DOWN + 0.5, za + 12.0)
    report("  ... tongue slid toward the far ear (unlocked)", tongue_free, hd, 8000, expect='(expect gap >= 0.3: teeth clear)')
    tongue_cc = zslice(tr(car, [0, P.TONGUE_ENGAGED_OFFSET + P.TONGUE_UNLOCK_SHIFT, za]), za - P.TONGUE_DOWN + 0.5, za + 12.0)
    report("  ... unlocked, crest on crest (worst case)", tongue_cc, hd, 8000, expect='(expect gap >= 0.3)')
    # 5c. tilt nut in the tongue slot (0.3 clearance)
    nut = load('square_nut_tilt')
    nut = rot(nut, [1, 0, 0], 90)                                       # thread axis -> y (hinge direction)
    nb_ = nut.bounds
    nut = tr(nut, [-(nb_[0][0] + nb_[1][0]) / 2, -(nb_[0][1] + nb_[1][1]) / 2, -(nb_[0][2] + nb_[1][2]) / 2])  # centred on the hinge axis
    report("tilt nut inside the tongue slot", nut, car, 3000, expect='(expect gap ~0.3)')
    # 5d. elbow: tongue (flipped, spigot up) between the arm_lower ears, locked at the half-pitch offset
    za_arm = P.ARM_LOWER_H - P.ELBOW_EAR_TOP_R                       # hinge axis height in arm_lower's frame
    armf = load('arm_lower')
    tg = rot(load('elbow_tongue'), [1, 0, 0], 180)                   # spigot up, tongue down, ring on -y
    tb = tg.bounds
    # tongue axis: its hinge hole centre was at z = SPIGOT_LEN + FLARE2 + TONGUE_UP in print; after the flip it is at -that
    z_axis_print = P.SPIGOT_LEN + P.ELBOW_FLARE2_H + P.ELBOW_TONGUE_UP
    tg = tr(tg, [0, 0, z_axis_print])                                # hinge axis at the origin
    tg = rot(tg, [0, 1, 0], 180.0 / P.ELBOW_HIRTH_N)                 # half-pitch: teeth interlock
    tg = tr(tg, [0, P.ELBOW_TONGUE_ENGAGED_OFFSET, za_arm])          # onto arm_lower's axis, locked position
    tongue_e = zslice(tg, za_arm - P.ELBOW_TONGUE_R + 0.5, za_arm + 20.0)
    report("elbow tongue locked in arm_lower fork (Hirth engaged)", tongue_e, armf, 8000, expect='(expect ~0 interf, min gap ~0)')
    tongue_u = zslice(tr(tg, [0, P.ELBOW_TONGUE_UNLOCK_SHIFT, 0]), za_arm - P.ELBOW_TONGUE_R + 0.5, za_arm + 20.0)
    report("  ... elbow tongue slid toward the far ear (unlocked)", tongue_u, armf, 8000, expect='(expect gap >= 0.3)')
    en = rot(load('elbow_nut'), [1, 0, 0], 90); eb = en.bounds
    en = tr(en, [-(eb[0][0] + eb[1][0]) / 2, -(eb[0][1] + eb[1][1]) / 2, -(eb[0][2] + eb[1][2]) / 2])
    # nut sits on the tongue's axis inside its slot: build the tongue in print frame for this check
    tg_print = load('elbow_tongue')
    report("elbow nut inside the tongue slot", tr(en, [0, 0, z_axis_print]), tg_print, 3000, expect='(expect gap ~0.3)')
    # 6. slider on the plain spine.  slider export = frame rotated -90 about X: (x, z, -y); inverse +90: (x, -z, y)
    sl = rot(load('slider'), [1, 0, 0], 90)
    sb = sl.bounds
    sl = tr(sl, [-(sb[0][0] + sb[1][0]) / 2, -sb[0][1], -sb[0][2] - (P.SLIDE_CLR + P.SLIDER_BACK_WALL)])   # frame: body y 0..L
    y0 = 120.0 - (P.SPINE_LEN - 2 * P.LIP_H) / 2
    spine_seg = cr.slice_plane([0, y0, 0], [0, 1, 0]).slice_plane([0, y0 + 20, 0], [0, -1, 0])
    report("slider on cradle spine", spine_seg, tr(sl, [0, y0 - 1.0, 0]), 3000, expect='(expect gap ~0.3)')
    # portrait Pro Max with a case (165 x 14): jaw foot at 165 + 16.2 -> the channel must still be on the spine
    foot = 165.0 + 2 * 14.0 * math.tan(math.radians(90 - P.JAW_INCLINE_DEG))
    print(f"   slider at max phone: jaw foot {foot:.1f} from the phone foot, channel {foot - P.SLIDER_LEN:.1f}..{foot + P.SLIDER_JAW_WALL:.1f}, spine ends at {P.SPINE_LEN - P.LIP_H:.0f} -> engaged {min(P.SPINE_LEN - P.LIP_H, foot + P.SLIDER_JAW_WALL) - (foot - P.SLIDER_LEN):.1f} mm")
    # 7. ball in pad
    pad = load('swivel_pad')
    r_cav = P.BALL_D / 2 + P.PAD_SOCKET_CLR; opening = P.BALL_D - 2 * P.PAD_SNAP_OVERLAP
    zc = (P.PAD_H + 2.0) - math.sqrt(r_cav ** 2 - (opening / 2) ** 2)
    ball = tr(trimesh.creation.icosphere(subdivisions=4, radius=P.BALL_D / 2), [0, 0, zc])
    report("ball in pad socket", ball, pad, 3000, expect='(expect gap ~0.2)')
    # 8. stack-up (arm straight up)
    arm_bottom = z_mouth - (P.EXT_TAPER_LEN - P.CLAMP_SEAT_GAP)
    elbow_axis = arm_bottom + za_arm
    spigot_base = elbow_axis + P.ELBOW_TONGUE_UP + P.ELBOW_FLARE2_H
    seg_bottom = spigot_base + P.SEAT_GAP
    seg_top = seg_bottom + P.SEG_LEN
    head_bottom = seg_top - P.SPIGOT_LEN + P.SEAT_GAP
    axis = head_bottom + P.HEAD_TOP + P.TILT_AXIS_H
    phone_c = axis + P.BOSS_Z
    horiz = (phone_c - elbow_axis)
    print(f"\nSTACK-UP (desk top = 0 mm): clamp mouth {z_mouth:.0f}; arm_lower {arm_bottom:.0f}..{arm_bottom + P.ARM_LOWER_H:.0f}, elbow axis {elbow_axis:.0f}; "
          f"segment {seg_bottom:.0f}..{seg_top:.0f}; head base {head_bottom:.0f}; tilt axis {axis:.0f}; phone centre ~{phone_c:.0f} mm = {phone_c/25.4:.1f} in straight up | "
          f"elbow at 90 deg: phone ~{elbow_axis + P.BOSS_Z:.0f} mm high, ~{horiz - P.BOSS_Z:.0f} mm out from the elbow")


if __name__ == '__main__':
    main()
