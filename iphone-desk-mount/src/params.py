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
SEG_LEN = 225.0           # overall segment height incl. spigot (print Z)
SEG_COUNT = 3

SPIGOT_LEN = 50.0
SPIGOT_BASE = 34.0        # square at the shoulder (largest)
SPIGOT_TIP = SPIGOT_BASE - 2 * SPIGOT_LEN * TAN_T          # 29.63
SPIGOT_BORE = 22.0        # hollow inside the spigot
SPIGOT_CORNER_R = 2.0
SHOULDER_H = (POLE_OUTER - SPIGOT_BASE) / 2                # 8 mm 45-deg flare from 34 to 50

SOCKET_DEPTH = 60.0
# mouth sized so the taper seats with SEAT_GAP between shoulder and mouth: W_mouth = tip + 2*(SPIGOT_LEN - SEAT_GAP)*tan
SOCKET_MOUTH = SPIGOT_TIP + 2 * (SPIGOT_LEN - SEAT_GAP) * TAN_T   # 33.65
SOCKET_BOTTOM = SOCKET_MOUTH - 2 * SOCKET_DEPTH * TAN_T           # 28.41 (< tip -> never bottoms out)
HOPPER_45 = True          # every internal cavity transition is a 45-deg hopper

# external taper on the bottom 60 mm of every segment (segment 1 plugs into the clamp socket with it)
EXT_TAPER_LEN = 55.0      # < clamp socket depth 56 - 4 seat gap -> segment bottom stops 5 mm above the floor
EXT_TAPER_BOTTOM = POLE_OUTER - 2 * EXT_TAPER_LEN * TAN_T          # 44.76

# ---------------- clamp body (printed on its side: use-Y -> print Z) ----------------
CLAMP_W = 90.0            # use-Y width (print height)
SPINE_T = 22.0            # use-X thickness of the spine at the desk edge
PAD_LEN = 75.0            # use-X length of the top jaw pad from the spine's inner face (desk edge); pry lever
TOP_JAW_T = 14.0
THROAT = 68.0             # opening between top-jaw underside and bottom-jaw top face (max desk ~55 mm, see README)
BOTTOM_JAW_T = 26.0
CLAMP_SOCKET_DEPTH = 56.0
CLAMP_SEAT_GAP = 4.0
CLAMP_SOCKET_MOUTH = EXT_TAPER_BOTTOM + 2 * (EXT_TAPER_LEN - CLAMP_SEAT_GAP) * TAN_T   # 49.65
CLAMP_SOCKET_BOTTOM = CLAMP_SOCKET_MOUTH - 2 * CLAMP_SOCKET_DEPTH * TAN_T              # 43.97
TOWER_H = CLAMP_SOCKET_DEPTH                                                            # socket floor = top-jaw top face
TOWER_CENTER_X = 25.0     # pole axis inboard of the desk edge (x=0 at the spine inner face)
TOWER_X0 = -SPINE_T       # tower outboard face flush with the spine (no step -> clean fillets)
TOWER_X1 = TOWER_CENTER_X + 44.0   # 69: inboard face (diamond half-diagonal 35.1 + 8.9 wall)
DIAMOND_DEG = 45.0        # socket rotated 45 deg so the printed roof is two 45-deg faces
CLAMP_CORNER_R = 4.0
# nut-block pocket in the bottom jaw (open toward use +Z (desk) and use +Y (print top))
SCREW_X = 45.0            # clamp-screw axis inboard of the desk edge
NUT_BLOCK = 30.0          # square nut block
NUT_BLOCK_H = 20.0
POCKET_CLR = 0.30
POCKET_FLOOR_T = BOTTOM_JAW_T - NUT_BLOCK_H                        # 6
SHAFT_CLR_HOLE = 19.0     # clearance hole for the Tr16 screw through the pocket floor

# ---------------- clamp screw / pad ----------------
SCREW_D = 16.0            # Tr16x3
SCREW_P = 3.0
SCREW_THREAD_LEN = 80.0
KNOB_D = 50.0
KNOB_H = 14.0
KNOB_LOBES = 8
BALL_D = 14.0
BALL_NECK_D = 9.0         # >= 0.6 x BALL_D keeps the sphere underside printable
BALL_NECK_H = 2.0
PAD_D = 50.0
PAD_H = 11.5
PAD_SOCKET_CLR = 0.20
PAD_SLOTS = 4

# ---------------- small printed thumbscrews / nuts (ALL Tr8x2, one nut design) ----------------
TS_D = 8.0                # Tr8x2.5 thumbscrews: tilt lock, cradle retainer, slider lock
TS_P = 2.5
TS_CLR = 0.25             # radial thread clearance for the small threads (0.35 would eat the 2.5 pitch)
TS_HOLE = TS_D + 0.8      # clearance hole for a Tr8 shaft
TS_KNOB_D = 24.0
TS_KNOB_D_TILT = 30.0     # bigger knob on the tilt lock (more torque -> more clamp)
TS_KNOB_H = 8.0
TS_KNOB_LOBES = 6
TS_LEN_TILT = 44.0        # thread lengths
TS_LEN_RETAIN = 60.0      # through 40 head plate + 10 boss + ~9 into the cradle thread
TS_LEN_LOCK = 26.0
SQ_NUT = 16.0             # square nut 16 x 16 x 8 (x3)
SQ_NUT_T = 6.0            # 3 turns of Tr8x2 - plenty at 300 N
SQ_NUT_CLR = 0.30         # pocket clearance per side

# ---------------- head (prints standing, socket mouth on the bed) ----------------
HEAD_BASE = POLE_OUTER    # 50 square base with the standard socket (mouth SOCKET_MOUTH, SOCKET_DEPTH)
HEAD_ROOF_H = SOCKET_BOTTOM / 2                  # 45-deg pyramid roof above the socket cavity (14.2)
HEAD_FLARE_Z0 = 66.0      # 45-deg flare from the 50 base to the wider cap starts here
HEAD_CAP = 64.0           # cap square (rounded) that carries the 45-deg-rotated fork
HEAD_CAP_R = 6.0
HEAD_FLARE_H = (HEAD_CAP - HEAD_BASE) / 2        # 6 -> 45 deg
HEAD_CAP_T = 8.0
HEAD_TOP = HEAD_FLARE_Z0 + HEAD_FLARE_H + HEAD_CAP_T   # 80: top of the cap = ear root
EAR_T = 10.0              # plain ear (flexes ~0.1 mm under the tilt screw)
EAR_NUT_T = 14.0          # nut-side ear (houses a 6.4-deep diamond pocket for the square nut)
EAR_GAP = 20.0            # inner faces at +-10
EAR_W = 40.0              # along the fork x (phone direction)
TILT_AXIS_H = 26.0        # hinge axis above the cap top
EAR_TOP_R = 20.0          # semicircular ear top around the axis (ear height = 26 + 20)
FORK_ROT_DEG = 45.0       # fork rotated 45 deg vs the socket so the phone faces square to the desk edge
SERRATION_N = 0           # radial teeth on the tilt faces; 0 = plain friction faces (chosen: stiff ears cannot disengage teeth)
SERRATION_H = 0.8
SERRATION_W = 2.4
SERRATION_R0 = 8.0
SERRATION_R1 = 16.5
TILT_RING_PROUD = 0.4     # tongue contact rings stand proud (per side) so the ears clamp them at a large radius
TILT_RING_R0 = 9.0
TILT_RING_R1 = 17.0

# ---------------- carrier (tongue + head plate + index boss; prints on its back, boss up) ----------------
TONGUE_T = EAR_GAP - 1.0         # 19.0 body; with rings 19.8 -> 0.1 per side at the rings
TONGUE_X0 = -20.0                # tongue/head-plate back face (fork x); hinge axis centred in the 40-wide tongue
TONGUE_X1 = 20.0                 # tongue front edge
TONGUE_DOWN = 20.0               # tongue extends this far below the hinge axis (rounded end)
HEADPLATE_Z0 = 30.0              # head plate from hinge+30 ...
HEADPLATE_Z1 = 62.0              # ... to hinge+62
HEADPLATE_W = 40.0               # head plate width (fork y)
BOSS = 20.0                      # square index boss (portrait/landscape), 5-deg taper
BOSS_LEN = 10.0
BOSS_TAPER_DEG = 5.0
BOSS_TIP = BOSS - 2 * BOSS_LEN * math.tan(math.radians(BOSS_TAPER_DEG))   # 18.25
BOSS_Z = 46.0                    # boss axis height above the hinge axis (centre of the head plate)
BOSS_SEAT_GAP = 1.5              # boss tip stops this short of the socket ceiling at nominal seat

# ---------------- cradle (prints flat, back face down) ----------------
SPINE_W = 50.0
SPINE_T_CRADLE = 10.0
SPINE_LEN = 190.0         # lip outer face to top end: 8 lip + 165 phone + >=17 slider engagement
LIP_H = 8.0               # lip wall thickness along the phone length
LIP_FWD = 17.0            # lip protrudes forward of the rest plane: 14 phone + 3 hook wall
LIP_HOOK = 5.0            # hook over the phone's front face
LIP_HOOK_T = 3.0
PORT_CUT_W = 16.0
PORT_CUT_H = 9.0
PAD_SQ = 40.0             # square back pad (boss socket + retaining thread), part of the spine
PAD_Y = 25.0              # pad centre above the lip's inner face
REST_Z = 20.0             # phone rest plane above the back face (= pad front = slider rest face)
CRADLE_SOCKET_DEPTH = BOSS_LEN
CRADLE_SOCKET_MOUTH = BOSS_TIP + 2 * (BOSS_LEN - BOSS_SEAT_GAP) * math.tan(math.radians(BOSS_TAPER_DEG))  # 19.74
CRADLE_THREAD_LEN = REST_Z - CRADLE_SOCKET_DEPTH     # 10 mm of Tr8 thread printed vertically

# ---------------- slider (top jaw; prints standing on its end = extrusion along the spine) ----------------
SLIDER_LEN = 22.0
SLIDER_SIDE_WALL = 5.0
SLIDER_BACK_WALL = 12.0          # houses the diamond nut pocket
SLIDER_FRONT_T = REST_Z - SPINE_T_CRADLE   # 10: front wall so the rest face is at REST_Z
SLIDER_HOOK_FWD = LIP_FWD
SLIDER_HOOK = LIP_HOOK
SLIDER_HOOK_T = LIP_HOOK_T

# ---------------- plate layout (module, instance, x, y, rot) plate coords 0..250, footprint centred ----------------
PLATE_LAYOUT = [
    # (module, instance, x_centre, y_centre, rot_deg) — plate 0..250, footprints centred, 4 mm gaps, 3 mm margin.
    ('clamp_body', 1, 51.5, 85.0, 0),          # x 3..100, y 3..167 (tower at low y, throat at y 73..141)
    ('clamp_screw', 1, 53.5, 101.5, 0),        # nested inside the clamp throat
    ('square_nut', 1, 89.9, 85.0, 0),          # nested inside the clamp throat
    ('square_nut', 2, 89.9, 105.0, 0),
    ('square_nut', 3, 89.9, 125.0, 0),
    ('thumbscrew_retain', 1, 116.0, 14.6, 90),
    ('thumbscrew_lock', 1, 144.0, 14.6, 90),
    ('pole_segment', 1, 185.0, 28.0, 0),
    ('pole_segment', 2, 129.0, 55.6, 0),
    ('nut_block', 1, 229.0, 18.0, 0),
    ('thumbscrew_tilt', 1, 229.0, 51.5, 90),
    ('head', 1, 190.0, 101.9, 0),
    ('pole_segment', 3, 129.0, 109.6, 0),
    ('carrier', 1, 199.0, 157.9, 0),
    ('swivel_pad', 1, 129.0, 163.6, 0),
    ('cradle', 1, 98.0, 217.6, 90),
    ('slider', 1, 221.7, 212.2, 90),
]
