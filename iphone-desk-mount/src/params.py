"""All dimensions (mm) for the iPhone desk mount.  Coordinates in the comments refer to the part IN USE:
X = inboard (into the desk), Y = along the desk edge, Z = up.  Each part module prints in its own orientation.
BASELINE (lead engineer) — will be reconciled with the design panel's FINAL_SPEC."""
import math

# ---------------- common fits / process ----------------
LAYER = 0.2
SLIDE_CLR = 0.30          # per side, sliding fit
SNUG_CLR = 0.15           # per side, snug slip fit
THREAD_CLR = 0.35         # radial clearance printed threads (lib.threads)
TAPER_DEG = 2.5           # wedge taper per side for every square taper joint
TAN_T = math.tan(math.radians(TAPER_DEG))
SEAT_GAP = 4.0            # nominal gap between a spigot's shoulder and the socket mouth when the wedge is seated

# ---------------- pole ----------------
POLE_OUTER = 50.0         # square tube outer
POLE_WALL = 3.0
POLE_CORNER_R = 3.0
POLE_INNER = POLE_OUTER - 2 * POLE_WALL        # 44 cavity
SEG_LEN = 240.0           # overall segment height incl. spigot (print Z)
SEG_COUNT = 1             # one plain segment above the elbow (arm_lower is the segment below it)

SPIGOT_LEN = 50.0
SPIGOT_BASE = 34.0        # square at the shoulder (largest)
SPIGOT_TIP = SPIGOT_BASE - 2 * SPIGOT_LEN * TAN_T          # 29.63
SPIGOT_BORE = 16.0        # hollow inside the spigot (16: stiffer spigot wall, +37 % spigot I vs 22)
SPIGOT_CORNER_R = 2.0
SHOULDER_H = (POLE_OUTER - SPIGOT_BASE) / 2                # 8 mm 45-deg flare from 34 to 50

SOCKET_DEPTH = 60.0
# mouth sized so the taper seats with SEAT_GAP between shoulder and mouth: W_mouth = tip + 2*(SPIGOT_LEN - SEAT_GAP)*tan
SOCKET_MOUTH = SPIGOT_TIP + 2 * (SPIGOT_LEN - SEAT_GAP) * TAN_T   # 33.65
SOCKET_BOTTOM = SOCKET_MOUTH - 2 * SOCKET_DEPTH * TAN_T           # 28.41 (< tip -> never bottoms out)
KNOCK_SLOT_W = 6.0        # vertical slot through both socket walls spanning the seated spigot tip (+-3.4 seat scatter): lower a rod onto the tip and tap
KNOCK_SLOT_Z0 = 43.0
KNOCK_SLOT_Z1 = 55.0
HOPPER_45 = True          # every internal cavity transition is a 45-deg hopper

# external taper on the bottom 60 mm of every segment (segment 1 plugs into the clamp socket with it)
EXT_TAPER_LEN = 43.0      # < clamp socket depth 44 - 4 seat gap -> the base stops 5 mm above the floor
EXT_TAPER_BOTTOM = POLE_OUTER - 2 * EXT_TAPER_LEN * TAN_T          # 44.76

# ---------------- articulated arm: arm_lower (base taper + tube + elbow fork) and elbow_tongue (tongue + spigot) ----------------
ARM_LOWER_H = 245.0       # overall print height
ARM_BASE_BORE_D = 36.0    # round bore through the base taper and the twist zone
ARM_TWIST_H1 = 12.0       # diamond square -> circle
ARM_TWIST_H2 = 12.0       # circle -> aligned square (45-deg flare at the corners)
ELBOW_EAR_T = 12.0
ELBOW_EAR_GAP = 29.0
ELBOW_EAR_W = 64.0
ELBOW_CAP_X = ELBOW_EAR_W + 4.0                 # 68
ELBOW_CAP_Y = ELBOW_EAR_GAP + 2 * ELBOW_EAR_T + 4.0   # 56
ELBOW_CAP_R = 6.0
ELBOW_CAP_T = 8.0
ELBOW_FLARE_H = (ELBOW_CAP_X - POLE_OUTER) / 2  # 9 -> 45 deg
ELBOW_AXIS_ABOVE_CAP = 36.0   # elbow T-bar r 30 clears the cap by 6
ELBOW_EAR_TOP_R = 32.0
ELBOW_HIRTH_N = 40        # 9-degree elbow index; teeth 1.6-2.4 tall
ELBOW_HIRTH_R0 = 20.0
ELBOW_HIRTH_R1 = 30.0
ELBOW_HIRTH_H1 = math.pi * ELBOW_HIRTH_R1 / ELBOW_HIRTH_N   # 1.96
ELBOW_D = 16.0            # Tr16x3 elbow screw (same thread as the clamp): ~440 N at 1.5 N.m
ELBOW_P = 3.0
ELBOW_CLR = 0.35
ELBOW_HOLE = ELBOW_D + 0.8
ELBOW_NUT = 25.0          # square nut 25 x 25 x 14 captured in the tongue slot (4.1 mm walls around the Tr16 thread)
ELBOW_NUT_T = 14.0
ELBOW_TBAR_L = 60.0
ELBOW_TBAR_W = 16.0
ELBOW_TBAR_H = 14.0
ELBOW_THREAD_LEN = 56.0   # ear 12 + gap 28 + ear 12 + 4
ELBOW_TONGUE_T = 23.5     # floats in the 29 gap: 2.36 teeth engaged + 3.1 free
ELBOW_TONGUE_R = 30.0     # rounded end radius = distance from the axis to the end
ELBOW_TONGUE_UP = 26.0    # tongue continues this far past the axis before the flare to the spigot
ELBOW_FLARE2_H = 15.0     # tongue 64 x 23.5 -> spigot base 34 x 34 (45 deg in x)
ELBOW_TONGUE_ENGAGED_OFFSET = (-ELBOW_EAR_GAP / 2 + ELBOW_HIRTH_H1) + ELBOW_TONGUE_T / 2
ELBOW_TONGUE_UNLOCK_SHIFT = ELBOW_HIRTH_H1 + 0.3
ELBOW_TONGUE_SLOT_TOP = ELBOW_NUT / 2 + 0.3

# ---------------- clamp body (printed on its side: use-Y -> print Z) ----------------
CLAMP_W = 110.0           # use-Y width (print height); rails at +-51 -> side-rocking lever 51 mm; spine 26 x 110
SPINE_T = 26.0            # use-X thickness of the spine at the desk edge (I = 146 000 mm4 with the 100 width)
PAD_LEN = 75.0            # use-X length of the top jaw pad from the spine's inner face (desk edge); pry lever
TOP_JAW_T = 14.0
THROAT = 68.0             # opening between top-jaw underside and bottom-jaw top face (desk up to ~53 mm with the 12 mm ball)
BOTTOM_JAW_T = 20.0
CLAMP_SOCKET_DEPTH = 44.0
CLAMP_SEAT_GAP = 4.0
CLAMP_SOCKET_MOUTH = EXT_TAPER_BOTTOM + 2 * (EXT_TAPER_LEN - CLAMP_SEAT_GAP) * TAN_T   # 49.65
CLAMP_SOCKET_BOTTOM = CLAMP_SOCKET_MOUTH - 2 * CLAMP_SOCKET_DEPTH * TAN_T              # 43.97
TOWER_H = CLAMP_SOCKET_DEPTH                                                            # socket floor = top-jaw top face
TOWER_CENTER_X = 25.0     # pole axis inboard of the desk edge (x=0 at the spine inner face)
TOWER_X0 = -SPINE_T       # tower outboard face flush with the spine (no step -> clean fillets)
TOWER_X1 = TOWER_CENTER_X + 44.0   # 69: inboard face (diamond half-diagonal 35.1 + 8.9 wall)
DIAMOND_DEG = 45.0        # socket rotated 45 deg so the printed roof is two 45-deg faces
CLAMP_CORNER_R = 4.0
PAD_RAIL_W = 8.0          # two desk-contact rails along X at y = +-PAD_RAIL_Y (defined 2-line contact, no rocking)
PAD_RAIL_Y = 51.0
PAD_RAIL_H = 0.6
CLAMP_MOUTH_CHAMFER = 2.0 # 45-deg lead-in on the diamond socket mouth
CLAMP_KNOCK_D = 6.0       # hole along use-Y through the tower at the socket floor: push the arm base out with a rod
PAD_FRAME_W = 8.0         # cross rails at both pad ends join the two long rails -> a contact frame
# nut-block pocket in the bottom jaw (open toward use +Z (desk) and use +Y (print top))
SCREW_X = PAD_LEN / 2     # clamp-screw axis at MID-pad: pry-off capacity = preload x (screw-to-pivot lever), equal both ways (37.5)
NUT_BLOCK = 30.0          # square nut block
NUT_BLOCK_H = 14.0        # Tr16x3: 4.7 turns
POCKET_CLR = 0.30
POCKET_FLOOR_T = BOTTOM_JAW_T - NUT_BLOCK_H                        # 6
SHAFT_CLR_HOLE = 19.0     # clearance hole for the Tr16 screw through the pocket floor (45-deg gable roof in print)

# ---------------- clamp screw / pad ----------------
SCREW_D = 16.0            # Tr16x3
SCREW_P = 3.0
SCREW_THREAD_LEN = 80.0
TBAR_L = 60.0             # T-bar handle: ~1.7x the torque of a 50 mm knob, 60 x 16 footprint (stands nested in the throat)
TBAR_W = 16.0
TBAR_H = 14.0
BALL_D = 12.0
BALL_NECK_D = 8.0         # >= 0.6 x BALL_D keeps the sphere underside printable
BALL_NECK_H = 1.0
PAD_D = 40.0
PAD_H = 10.0
PAD_SOCKET_CLR = 0.20
PAD_SLOTS = 6
PAD_SNAP_OVERLAP = 0.25   # per side; opening = BALL_D - 2*overlap
PAD_RELIEF_R0 = 8.5       # annular relief groove around the petals so the lip ring can flex
PAD_RELIEF_R1 = 10.0
PAD_RELIEF_DEPTH = 7.0

# ---------------- small printed thumbscrews / nuts (ALL Tr8x2, one nut design) ----------------
TS_D = 8.0                # Tr8x2.5 thumbscrews: tilt lock, cradle retainer, slider lock
TS_P = 2.5
TS_CLR = 0.25             # radial thread clearance for the small threads (0.35 would eat the 2.5 pitch)
TS_HOLE = TS_D + 0.8      # clearance hole for a Tr8 shaft
# thumbscrew handles are small T-bars (more torque than a round knob, tiny plate footprint)
TS_TBAR_L = 38.0          # retain / lock screws: 38 x 12 x 10 bar
TS_TBAR_W = 12.0
TS_TBAR_H = 10.0
TS_TBAR_L_TILT = 50.0     # tilt screw: 50 x 14 x 12 bar (~1 N.m by hand -> ~300 N onto the Hirth teeth)
TS_TBAR_W_TILT = 14.0
TS_TBAR_H_TILT = 12.0
TS_LEN_TILT = 42.0        # thread lengths (tilt: Tr10, see TILT_*)
TS_LEN_RETAIN = 66.0      # Tr10: through 44 head plate + 10 boss, 1.5 gap, 3 hopper, ~9 into the cradle's Tr10 thread
TS_LEN_LOCK = 26.0
SQ_NUT = 16.0             # square nut 16 x 16 x 8 (x3)
SQ_NUT_T = 6.0            # 3 turns of Tr8x2 - plenty at 300 N
SQ_NUT_CLR = 0.30         # pocket clearance per side
TILT_D = 10.0             # Tr10x2.5 tilt thumbscrew (screw core carries the Hirth preload: FoS 4.5)
TILT_P = 2.5
TILT_CLR = 0.30
TILT_HOLE_NEAR = TILT_D + 0.8   # 10.8 through the knob-side ear and the tongue
TILT_HOLE_FAR = TILT_D + 0.6    # 10.6 in the far ear: guides the thread when unlocked
RETAIN_D = TILT_D         # retaining thumbscrew is Tr10x2.5 too (core 8.25 mm, 4+ turns in the cradle)
RETAIN_P = TILT_P
RETAIN_HOLE = TILT_D + 0.8
TILT_NUT = 18.0           # square nut 18 x 18 x 8 captured in the tongue slot (3.7 mm walls around the Tr10 thread)
TILT_NUT_T = 8.0

# ---------------- head (prints standing, socket mouth on the bed) ----------------
HEAD_BASE = POLE_OUTER    # 50 square base with the standard socket (mouth SOCKET_MOUTH, SOCKET_DEPTH)
HEAD_ROOF_H = SOCKET_BOTTOM / 2                  # 45-deg pyramid roof above the socket cavity (14.2)
HEAD_FLARE_Z0 = 66.0      # 45-deg flare from the 50 base to the wider cap starts here
HEAD_CAP = 64.0           # cap square (rounded) that carries the 45-deg-rotated fork
HEAD_CAP_R = 6.0
HEAD_FLARE_H = (HEAD_CAP - HEAD_BASE) / 2        # 6 -> 45 deg
HEAD_CAP_T = 8.0
HEAD_TOP = HEAD_FLARE_Z0 + HEAD_FLARE_H + HEAD_CAP_T   # 80: top of the cap = ear root
EAR_T = 10.0              # both ears 10 thick (the nut lives in the tongue, not in an ear)
EAR_GAP = 27.0            # inner faces at +-13.5 (22 tongue + 2.1 teeth + 2.9 free)
EAR_W = 44.0              # along the fork x (phone direction); Hirth ring r 13.5..21 needs >= 44
TILT_AXIS_H = 30.0        # hinge axis above the cap top (tilt T-bar r 25 clears the cap by 5)
EAR_TOP_R = 22.0          # semicircular ear top around the axis (ear height = 26 + 22)
FORK_ROT_DEG = 0.0        # the arm above the elbow is square to the desk edge (arm_lower carries the 45-deg twist)
# Hirth-type positive tilt lock: radial teeth on the knob-side ear's inner face and on the tongue's near face.
# The tongue FLOATS in the ear gap (17 in 20) and is pulled onto the toothed ear by the screw + captured nut, so
# loosening half a turn lets the tongue slide 1.3 mm and the teeth disengage (stiff ears never need to flex).
HIRTH_N = 30              # true Hirth ring: tooth width = pitch at every radius -> zero rotational play; 12-degree tilt index
HIRTH_INCLUDED_DEG = 90.0 # 45-deg flanks: lift-off force = tangential force (a ~1 N.m T-bar gives ~300 N, bump needs ~150 N)
HIRTH_R0 = 14.0
HIRTH_R1 = 20.0           # pitch 2.9-4.2 mm, teeth 1.5-2.1 tall: crisp at 0.4 mm
HIRTH_H1 = (math.pi * HIRTH_R1 / HIRTH_N)   # 1.48: tooth height at the outer radius (90 deg)
HIRTH_TRUNC = 0.3         # crest truncation = crest-to-root relief when the flanks touch (flanks carry, crests never bottom)
HIRTH_SINK = 0.2          # teeth sunk this far into the face (robust union)

# ---------------- carrier (tongue + head plate + index boss; prints on its back, boss up) ----------------
TONGUE_T = 22.0                  # floats in the 27 gap: 2.1 teeth engaged leaves 2.9 free (> 2.1 + 0.3); 6.7 mm walls beside the nut slot
TONGUE_ENGAGED_OFFSET = (-EAR_GAP / 2 + HIRTH_H1) + TONGUE_T / 2   # -0.52: tongue centre when locked (flank-to-flank)
TONGUE_UNLOCK_SHIFT = HIRTH_H1 + 0.3   # slide this far toward the far ear to re-index (3/4 turn of the Tr10); far-side room = 20 - 16 - 1.48 = 2.5
TONGUE_X0 = -22.0                # tongue/head-plate back face (fork x); hinge axis centred in the 44-wide tongue
TONGUE_X1 = 22.0                 # tongue front edge
TONGUE_DOWN = 22.0               # tongue extends this far below the hinge axis (rounded end)
TONGUE_SLOT_TOP = TILT_NUT / 2 + 0.3   # nut slot runs from the rounded end up to here (nut centred on the axis)
HEADPLATE_Z0 = 30.0              # head plate from hinge+30 ...
HEADPLATE_Z1 = 62.0              # ... to hinge+62
HEADPLATE_W = 40.0               # head plate width (fork y) — clears the ears (outer faces at +-20) because it sits above them
BOSS = 20.0                      # square index boss (portrait/landscape), 5-deg taper
BOSS_LEN = 10.0
BOSS_TAPER_DEG = 5.0
BOSS_TIP = BOSS - 2 * BOSS_LEN * math.tan(math.radians(BOSS_TAPER_DEG))   # 18.25
BOSS_Z = 46.0                    # boss axis height above the hinge axis (centre of the head plate)
BOSS_SEAT_GAP = 1.5              # boss tip stops this short of the socket ceiling at nominal seat

# ---------------- cradle (prints flat, back face down) ----------------
SPINE_W = 50.0
SPINE_T_CRADLE = 12.0     # 12 (was 10): halves the phone-top flex under a bump
SPINE_LEN = 198.0         # 8 lip + 165 phone + 16.2 V-incline offset (14 mm phone) + 8 jaw wall + 1
LIP_H = 8.0               # lip block behind the phone foot (y -8..0)
JAW_H = 21.5              # V-jaws rise this far above the rest plane (14 phone + 7.5)
JAW_RIDGES = 3            # small grip ridges across each V-jaw incline (landscape: the phone's long edge cannot slide)
JAW_INCLINE_DEG = 60.0    # jaw face angle to the rest plane: leans 22*tan(30) = 12.7 mm over the phone -> pinches any
                          # thickness 7..14 against the back, no rattle; in print the lip face is a 30-deg overhang
JAW_LEAN = JAW_H * math.tan(math.radians(90 - JAW_INCLINE_DEG))   # 12.7
PORT_CUT_W = 22.0         # through the whole lip, open to the phone side and the lip top (braided USB-C strain reliefs pass)
PAD_SQ = 40.0             # square back pad (boss socket + retaining thread), part of the spine
PAD_Y = 25.0              # pad centre above the lip's inner face
REST_Z = 24.0             # phone rest plane above the back face (= pad front = slider rest face)
CRADLE_SOCKET_DEPTH = BOSS_LEN
CRADLE_SOCKET_MOUTH = BOSS_TIP + 2 * (BOSS_LEN - BOSS_SEAT_GAP) * math.tan(math.radians(BOSS_TAPER_DEG))  # 19.74
CRADLE_HOPPER_H = (BOSS_TIP - 12.0) / 2               # 45-deg hopper from the socket ceiling down to a 12 sq -> no flat ceiling
CRADLE_THREAD_LEN = REST_Z - CRADLE_SOCKET_DEPTH - CRADLE_HOPPER_H   # ~10.9 mm of Tr10 thread printed vertically

# ---------------- slider (top jaw; prints standing on its end = extrusion along the spine) ----------------
SLIDER_LEN = 22.0         # channel body length UNDER the phone; the jaw wall adds SLIDER_JAW_WALL beyond the phone's top edge
SLIDER_JAW_WALL = 8.0
SLIDER_SIDE_WALL = 5.0
SLIDER_BACK_WALL = 12.0          # houses the diamond nut pocket
SLIDER_FRONT_T = REST_Z - SPINE_T_CRADLE   # 8: front wall so the rest face is at REST_Z

# ---------------- plate layout (module, instance, x, y, rot) plate coords 0..250, footprint centred ----------------
PLATE_LAYOUT = [
    # (module, instance, x_centre, y_centre, rot_deg) — plate 0..250, footprints centred, 4 mm footprint gaps, 3 mm margin.
    ('clamp_body', 1, 53.5, 76.0, 0),          # x 3..104, y 3..149 (tower at low y, throat at y 61..129)
    ('clamp_screw', 1, 63.0, 73.9, 0),         # T-bar nested in the throat, 4 mm above the pad rails
    ('elbow_screw', 1, 63.0, 94.5, 0),         # T-bar nested in the throat
    ('square_nut_tilt', 1, 42.0, 115.8, 0),    # nested in the throat
    ('square_nut', 1, 63.0, 114.8, 0),         # nested in the throat
    ('arm_lower', 1, 142.2, 37.3, 0),           # x 108.1..176.3, y 3.2..71.4
    ('pole_segment', 1, 133.0, 100.4, 0),
    ('thumbscrew_lock', 1, 168.0, 95.4, 90),
    ('elbow_tongue', 1, 140.0, 146.4, 0),
    ('elbow_nut', 1, 120.5, 179.9, 0),
    ('head', 1, 212.4, 35.0, 0),
    ('slider', 1, 210.7, 99.9, 0),             # x 180.2..240.8, y 71..128.8
    ('thumbscrew_tilt', 1, 205.4, 139.8, 0),
    ('thumbscrew_retain', 1, 156.0, 173.4, 0),  # beside the elbow nut
    ('nut_block', 1, 195.4, 165.8, 0),
    ('carrier', 1, 45.0, 173.0, 0),
    ('cradle', 1, 102.0, 222.0, 90),           # x 3..201
    ('swivel_pad', 1, 225.0, 222.0, 0),        # x 205..245
]
