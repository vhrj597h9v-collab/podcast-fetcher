# 8 Button Joystick — parametric model, renders and STL

Thumb-operated joystick head with eight 6×6×8 mm tactile push buttons wired to
a HiLetgo Pro Micro (ATmega32U4) that lives inside the head. The 92 × 60 mm
button panel faces the user and is tilted 10° down towards the thumb; the bottom
row of four buttons sits on the flat face, the top row on an upper block that
overhangs the flat face and is tipped 45° towards the user. Every edge is
rounded. Ergonomic curved grip, knurled collar, Ø72 mm base with four M4
countersunk mounting holes.

The head is 36 mm deep, sized around the board stack: 3 mm wall, 6 mm switch
body and legs, 7 mm wiring gap, 3 mm USB jack, 1.6 mm PCB, 12 mm pin and wiring
space, 3 mm plate. The board slides into edge grooves on two rails printed on
the back plate (pins towards the plate), and the plate carries it into the
head. The micro-USB jack points down at the Ø12 mm channel through the shaft,
which passes a standard micro-USB plug and exits through a groove across the
underside of the base.

All dimensions in millimetres. Z is up, −Y is towards the user.

## Files

| file | what it is |
| --- | --- |
| `build_joystick.py` | the parametric model — edit the constants at the top, re-run, re-slice |
| `out/joystick_body.stl` | head + grip + base, one print |
| `out/joystick_back_plate.stl` | 76 × 44 × 3 mm rear access plate with Pro Micro rails, 4× M4 countersunk |
| `out/pro_micro_mockup.stl` | board envelope (PCB, USB jack, headers, pins) for fit checks — not printed |
| `out/joystick_button_cap.stl` | one Ø10 × 8 mm cap with a Ø3.6 plunger socket — print 8 |
| `out/joystick_assembly.stl` | everything assembled, preview only |
| `out/joystick_sheet.png` | multi-view spec sheet (front / top / sides / back / details / exploded) |
| `out/joystick_viewer.html` | self-contained interactive viewer: orbit, engineering views, exploded, wireframe |
| `out/views/*.png` | the individual renders |
| `out/meta.json` | head transform and button positions, used by the sheet annotations |

## Regenerating

```bash
pip install trimesh manifold3d shapely numpy pillow
python3 build_joystick.py        # STLs + scene.json + meta.json
python3 make_viewer.py           # out/joystick_viewer.html
node render_views.js             # out/views/*.png (needs Playwright + Chromium;
                                 #   THREE_JS=/path/three.min.js serves three.js offline)
python3 make_sheet.py            # out/joystick_sheet.png
```

## Hardware

- 1× HiLetgo Pro Micro, ATmega32U4, 33 × 18 mm, micro-USB
- 8× 6×6×8 mm tactile switches (seat in the 6.8 mm square pockets behind each Ø10.6 hole)
- 8× M4×8 countersunk screws — 4 for the base, 4 for the back plate
- M4 tap or heat-set inserts in the four Ø3.3 bosses behind the back plate
- solder switch leads straight to the header pins: there is 12 mm behind the board, which is not enough for Dupont housings
- the micro-USB plug is fed down the Ø12 channel from the head and exits the base groove at the back
- the build script asserts that the board envelope clears the body and the plate rails

## Printing

Body upright on its base, supports under the overhanging head. Back plate flat, rails up.
Caps head-down. 0.2 mm layers, 3 walls, ~20 % infill; PETG or ABS for the grip.
