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
SPIGOT_BORE = 16.0        # hollow inside the spigot (16: stiffer spigot wall, +37 % spigot I vs 22)
SPIGOT_CORNER_R = 2.0
SHOULDER_H = (POLE_OUTER - SPIGOT_BASE) / 2                # 8 mm 45-deg flare from 34 to 50

SOCKET_DEPTH = 60.0
# mouth sized so the taper seats with SEAT_GAP between shoulder and mouth: W_mouth = tip + 2*(SPIGOT_LEN - SEAT_GAP)*tan
SOCKET_MOUTH = SPIGOT_TIP + 2 * (SPIGOT_LEN - SEAT_GAP) * TAN_T   # 33.65
SOCKET_BOTTOM = SOCKET_MOUTH - 2 * SOCKET_DEPTH * TAN_T           # 28.41 (< tip -> never bottoms out)
KNOCK_HOLE_D = 6.0        # cross hole through the socket walls above the spigot tip: push a rod through to release the wedge
KNOCK_HOLE_Z = 52.0
HOPPER_45 = True          # every internal cavity transition is a 45-deg hopper

# external taper on the bottom 60 mm of every segment (segment 1 plugs into the clamp socket with it)
EXT_TAPER_LEN = 55.0      # < clamp socket depth 56 - 4 seat gap -> segment bottom stops 5 mm above the floor
EXT_TAPER_BOTTOM = POLE_OUTER - 2 * EXT_TAPER_LEN * TAN_T          # 44.76

# ---------------- clamp body (printed on its side: use-Y -> print Z) ----------------
CLAMP_W = 110.0           # use-Y width (print height); rails at +-51 -> side-rocking lever 51 mm; spine 26 x 110
SPINE_T = 26.0            # use-X thickness of the spine at the desk edge (I = 146 000 mm4 with the 100 width)
PAD_LEN = 75.0            # use-X length of the top jaw pad from the spine's inner face (desk edge); pry lever
TOP_JAW_T = 14.0
THROAT = 70.0             # opening between top-jaw underside and bottom-jaw top face (desk up to ~57 mm)
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
PAD_RAIL_W = 8.0          # two desk-contact rails along X at y = +-PAD_RAIL_Y (defined 2-line contact, no rocking)
PAD_RAIL_Y = 51.0
PAD_RAIL_H = 0.6
CLAMP_MOUTH_CHAMFER = 2.0 # 45-deg lead-in on the diamond socket mouth
# nut-block pocket in the bottom jaw (open toward use +Z (desk) and use +Y (print top))
SCREW_X = PAD_LEN / 2     # clamp-screw axis at MID-pad: pry-off capacity = preload x (screw-to-pivot lever), equal both ways (37.5)
NUT_BLOCK = 30.0          # square nut block
NUT_BLOCK_H = 20.0
POCKET_CLR = 0.30
POCKET_FLOOR_T = BOTTOM_JAW_T - NUT_BLOCK_H                        # 6
SHAFT_CLR_HOLE = 19.0     # clearance hole for the Tr16 screw through the pocket floor (45-deg gable roof in print)

# ---------------- clamp screw / pad ----------------
SCREW_D = 16.0            # Tr16x3
SCREW_P = 3.0
SCREW_THREAD_LEN = 80.0
TBAR_L = 64.0             # T-bar handle instead of a round knob: ~1.8x the torque of a 50 mm knob, 64 x 18 footprint (nests in the throat)
TBAR_W = 18.0
TBAR_H = 16.0
BALL_D = 14.0
BALL_NECK_D = 9.0         # >= 0.6 x BALL_D keeps the sphere underside printable
BALL_NECK_H = 2.0
PAD_D = 50.0
PAD_H = 11.5
PAD_SOCKET_CLR = 0.20
PAD_SLOTS = 6
PAD_SNAP_OVERLAP = 0.4    # per side; opening = BALL_D - 2*overlap (petal stress stays low)

# ---------------- small printed thumbscrews / nuts (ALL Tr8x2, one nut design) ----------------
TS_D = 8.0                # Tr8x2.5 thumbscrews: tilt lock, cradle retainer, slider lock
TS_P = 2.5
TS_CLR = 0.25             # radial thread clearance for the small threads (0.35 would eat the 2.5 pitch)
TS_HOLE = TS_D + 0.8      # clearance hole for a Tr8 shaft
# thumbscrew handles are small T-bars (more torque than a round knob, tiny plate footprint)
TS_TBAR_L = 40.0          # retain / lock screws: 40 x 12 x 10 bar
TS_TBAR_W = 12.0
TS_TBAR_H = 10.0
TS_TBAR_L_TILT = 50.0     # tilt screw: 50 x 14 x 12 bar (~1 N.m by hand -> ~300 N onto the Hirth teeth)
TS_TBAR_W_TILT = 14.0
TS_TBAR_H_TILT = 12.0
TS_LEN_TILT = 42.0        # thread lengths (tilt: Tr10, see TILT_*)
TS_LEN_RETAIN = 60.0      # through 40 head plate + 10 boss + ~9 into the cradle thread
TS_LEN_LOCK = 26.0
SQ_NUT = 16.0             # square nut 16 x 16 x 8 (x3)
SQ_NUT_T = 6.0            # 3 turns of Tr8x2 - plenty at 300 N
SQ_NUT_CLR = 0.30         # pocket clearance per side
TILT_D = 10.0             # Tr10x2.5 tilt thumbscrew (screw core carries the Hirth preload: FoS 4.5)
TILT_P = 2.5
TILT_CLR = 0.30
TILT_HOLE_NEAR = TILT_D + 0.8   # 10.8 through the knob-side ear and the tongue
TILT_HOLE_FAR = TILT_D + 0.6    # 10.6 in the far ear: guides the thread when unlocked
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
EAR_GAP = 20.0            # inner faces at +-10
EAR_W = 44.0              # along the fork x (phone direction); Hirth ring r 13.5..21 needs >= 44
TILT_AXIS_H = 26.0        # hinge axis above the cap top
EAR_TOP_R = 22.0          # semicircular ear top around the axis (ear height = 26 + 22)
FORK_ROT_DEG = 45.0       # fork rotated 45 deg vs the socket so the phone faces square to the desk edge
# Hirth-type positive tilt lock: radial teeth on the knob-side ear's inner face and on the tongue's near face.
# The tongue FLOATS in the ear gap (17 in 20) and is pulled onto the toothed ear by the screw + captured nut, so
# loosening half a turn lets the tongue slide 1.3 mm and the teeth disengage (stiff ears never need to flex).
HIRTH_N = 36              # true Hirth ring: tooth width = pitch at every radius -> zero rotational play; 10-degree tilt index
HIRTH_INCLUDED_DEG = 90.0 # 45-deg flanks: lift-off force = tangential force (a ~1 N.m T-bar gives ~300 N, bump needs ~150 N)
HIRTH_R0 = 12.0
HIRTH_R1 = 17.0
HIRTH_H1 = (math.pi * HIRTH_R1 / HIRTH_N)   # 1.48: tooth height at the outer radius (90 deg)
HIRTH_TRUNC = 0.3         # crest truncation = crest-to-root relief when the flanks touch (flanks carry, crests never bottom)
HIRTH_SINK = 0.2          # teeth sunk this far into the face (robust union)

# ---------------- carrier (tongue + head plate + index boss; prints on its back, boss up) ----------------
TONGUE_T = 16.0                  # floats in the 20 gap: 1.48 teeth engaged + 0.4 crest clearance leaves 2.1 free on the far side (> 1.48 + 0.3)
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
SPINE_LEN = 190.0         # lip outer face to top end: 8 lip + 165 phone + >=17 slider engagement
LIP_H = 8.0               # lip block behind the phone foot (y -8..0)
JAW_H = 22.0              # V-jaws rise this far above the rest plane (14 phone + 8)
JAW_INCLINE_DEG = 60.0    # jaw face angle to the rest plane: leans 22*tan(30) = 12.7 mm over the phone -> pinches any
                          # thickness 7..14 against the back, no rattle; in print the lip face is a 30-deg overhang
JAW_LEAN = JAW_H * math.tan(math.radians(90 - JAW_INCLINE_DEG))   # 12.7
PORT_CUT_W = 22.0         # through the whole lip, open to the phone side and the lip top (braided USB-C strain reliefs pass)
PAD_SQ = 40.0             # square back pad (boss socket + retaining thread), part of the spine
PAD_Y = 25.0              # pad centre above the lip's inner face
REST_Z = 20.0             # phone rest plane above the back face (= pad front = slider rest face)
CRADLE_SOCKET_DEPTH = BOSS_LEN
CRADLE_SOCKET_MOUTH = BOSS_TIP + 2 * (BOSS_LEN - BOSS_SEAT_GAP) * math.tan(math.radians(BOSS_TAPER_DEG))  # 19.74
CRADLE_THREAD_LEN = REST_Z - CRADLE_SOCKET_DEPTH     # 10 mm of Tr8 thread printed vertically

# ---------------- slider (top jaw; prints standing on its end = extrusion along the spine) ----------------
SLIDER_LEN = 22.0         # body length along the spine; the V-jaw leans a further 12.7 over the phone
SLIDER_SIDE_WALL = 5.0
SLIDER_BACK_WALL = 12.0          # houses the diamond nut pocket
SLIDER_FRONT_T = REST_Z - SPINE_T_CRADLE   # 8: front wall so the rest face is at REST_Z

# ---------------- plate layout (module, instance, x, y, rot) plate coords 0..250, footprint centred ----------------
PLATE_LAYOUT = [
    # (module, instance, x_centre, y_centre, rot_deg) — plate 0..250, footprints centred, 4 mm footprint gaps, 3 mm margin.
    ('clamp_body', 1, 53.5, 86.0, 0),          # x 3..104, y 3..169 (tower at low y, throat at y 73..143)
    ('clamp_screw', 1, 65.0, 86.6, 0),         # T-bar nested inside the clamp throat (4 mm from the pad rails)
    ('square_nut', 1, 41.0, 107.6, 0),         # nested inside the throat (Tr8, slider lock)
    ('square_nut_tilt', 1, 42.0, 128.6, 0),    # nested inside the throat (Tr10, tilt)
    ('nut_block', 1, 70.0, 114.6, 0),          # nested inside the throat
    ('pole_segment', 1, 133.0, 28.0, 0),
    ('pole_segment', 2, 133.0, 82.0, 0),
    ('pole_segment', 3, 133.0, 136.0, 0),
    ('head', 1, 194.0, 35.0, 0),
    ('carrier', 1, 204.0, 91.0, 0),
    ('slider', 1, 192.3, 142.2, 0),
    ('thumbscrew_tilt', 1, 28.0, 180.0, 0),
    ('thumbscrew_retain', 1, 77.0, 179.0, 0),
    ('thumbscrew_lock', 1, 121.0, 179.0, 0),
    ('cradle', 1, 98.0, 222.0, 90),
    ('swivel_pad', 1, 222.0, 222.0, 0),
]
