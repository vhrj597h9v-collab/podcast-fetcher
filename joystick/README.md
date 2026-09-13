# 8 Button Joystick — parametric model, renders and STL

Thumb-operated joystick with eight 6×6×8 mm tactile push buttons wired to a
HiLetgo Pro Micro (ATmega32U4). Six buttons sit on a compact 58 × 37 × 34 mm
head that faces the user, tilted 10° down towards the thumb: a bottom row of
three on the flat face and a top row of three on an upper block that overhangs
the flat face, tipped 45° towards the user. Buttons are on a 16 mm pitch with
1 mm margins to the rounded edges. Two more buttons sit on a trigger bump under
the front of the head, facing down and forward for the index finger. Every edge
is rounded. Ergonomic curved grip, knurled collar, Ø72 mm base with four M4
countersunk mounting holes.

The Pro Micro sits in a pocket in the neck of the grip, directly under the head,
PCB parallel to the back, USB jack pointing down over the Ø12 mm cable channel.
Ribs behind the header plastic hold the board against the pocket's front wall.
One back plate covers the head opening and, with a tab, the neck pocket; both
sit flush in recesses on four M4 countersunk screws. Wires from all eight
switches run through the head cavity into the pocket.

All dimensions in millimetres. Z is up, −Y is towards the user.

## Files

| file | what it is |
| --- | --- |
| `build_joystick.py` | the parametric model — edit the constants at the top, re-run, re-slice |
| `out/joystick_body.stl` | head + grip + base, one print |
| `out/joystick_back_plate.stl` | 3 mm back plate: head cover plus neck tab, 4× M4 countersunk |
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
- solder switch leads to the header pins first, then drop the board into the neck pocket from the back
- the micro-USB plug is fed down the Ø12 channel from the pocket and exits the base groove at the back
- the build script asserts that the board envelope clears the body and the plate rails

## Printing

Body upright on its base, supports under the overhanging head and the trigger bump. Back plate flat.
Caps head-down. 0.2 mm layers, 3 walls, ~20 % infill; PETG or ABS for the grip.
