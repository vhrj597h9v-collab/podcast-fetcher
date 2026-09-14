# Joystick project brief

Status as of 2026-09-14. Everything below lives in this folder; the model is fully
parametric, so any dimension is a constant at the top of `build_joystick.py`.

## What we set out to build

A 3D-printable thumb-operated button joystick, starting from a spec-sheet render
of an 8-button head (100 × 70 mm box, top row tilted 45°, bottom row flat,
6×6×8 mm tactile switches, M4 countersunk mounting, ergonomic grip). The goal was
a render to review, then STL files to print.

## How the design evolved

1. **First pass.** Faithful to the spec sheet: a 100 × 70 mm box on top of the
   grip with the buttons facing the ceiling. Rejected: with the hand on the
   shaft, the thumb can't reach buttons that face up.
2. **Head rotated to face the user.** The panel now stands vertical, facing the
   hand, and is tilted a further 10° down toward the thumb. All edges rounded
   (R5) for comfort. The top row was first put on a chamfer leaning back, which
   was the wrong way round.
3. **Top row tipped toward the user.** The top row sits on an upper block that
   overhangs the flat face, its face tipped 45° down toward the thumb. This is
   the layout that stuck.
4. **Pro Micro integration.** The controller is a HiLetgo Pro Micro (ATmega32U4,
   33 × 18 mm, micro-USB on a short edge). First it was carried on rails on the
   back plate inside the head, which forced the head to stay 60 mm tall.
   The USB cable channel through the shaft was widened to Ø12 mm so a micro-USB
   plug can pass, exiting through a groove across the underside of the base.
5. **Compaction to six buttons.** Buttons reduced to 3 + 3 on a 16 mm pitch with
   1 mm margins to the rounded edges, head shrunk to 58 × 37 × 34 mm. The board
   moved out of the head into a pocket in the neck of the grip, directly under
   the head, jack pointing down over the cable channel. One back plate covers the
   head opening and, with a tab, the neck pocket.
6. **Trigger buttons tried and removed.** Two index-finger buttons on a bump under
   the head were built, judged ugly, and removed. The design is six buttons.
7. **Mesh cleanup.** The exported body was six touching shells rather than one
   solid because bezels and ledges only touched the shell face-to-face. Those
   features now overlap by 1 mm and a finalize step quantises to float32 and
   merges vertices before the watertight and single-body assertions, so the
   files on disk are exactly what was checked. 3MF exports were added.

## Final design

| item | value |
| --- | --- |
| head | 58 × 37 × 34 mm, plus 14 mm overhang for the top row |
| buttons | 6, Ø10 × 8 mm caps on Ø14 bezels, 16 mm pitch |
| panel | faces the user, tilted 10° down; top row face tipped 45° toward the user |
| grip | curved sweep, elliptical section, knurled collar, Ø72 base with 4× M4 countersunk |
| controller | Pro Micro in the neck pocket, ribs behind the headers locate it |
| cable | Ø12 channel from the pocket through the base, groove out the back |
| access | one 3 mm back plate (head cover + neck tab), 4× M4 countersunk into Ø3.3 bosses |
| walls | 3 mm shell; switch pockets 6.8 mm square behind Ø10.6 holes |
| overall | 72 × 88 × 165 mm |

## Files

| file | purpose |
| --- | --- |
| `build_joystick.py` | parametric model; regenerates every STL/3MF, `scene.json`, `meta.json` and asserts the board fits |
| `out/joystick_body.stl` / `.3mf` | head + grip + base, print 1 upright with supports under the head |
| `out/joystick_back_plate.stl` / `.3mf` | back plate with neck tab, print 1 flat |
| `out/joystick_button_cap.stl` / `.3mf` | button cap, print 6 head down |
| `out/joystick_parts.zip` | the three STLs zipped for uploads that reject STL |
| `out/pro_micro_mockup.stl` | board envelope for fit checks, not printed |
| `out/joystick_assembly.stl` | everything assembled, preview only |
| `out/joystick_sheet.png` | multi-view spec sheet |
| `out/joystick_viewer.html` | self-contained interactive 3D viewer |
| `viewer_template.html`, `make_viewer.py` | viewer source and the inliner |
| `render_views.js`, `make_sheet.py` | headless renders and the sheet composer |
| `README.md` | hardware, wiring, regeneration and print notes |

Interactive viewer (published): https://claude.ai/code/artifact/08a7ab1f-80dc-480e-8465-0a4ac5d8041b

## Print settings

- Printer: Bambu Lab P1S. Body is 165 mm tall and fits.
- Body: 0.2 mm layers, 3 walls, 20 % infill, tree supports. Supports must reach
  the overhanging top row but should not fill the neck pocket; paint a blocker
  over the pocket opening if they do.
- Back plate and caps: no supports, flat side down. PETG or ABS for the grip.

## Getting files to the printer

- Bambu Handy on this phone cannot import local files: it is absent from the iOS
  share sheet, and its Files page only lists the SD card and cloud history.
- MakerWorld's upload page greys out STL/3MF in the iOS picker; the zip in
  `out/` gets past that, but publishing there makes the model public and a raw
  upload has no print profile.
- The reliable route is Bambu Studio on a computer, once. After that, re-prints
  are a "Print again" in Handy.

## Hardware and assembly

- 1× HiLetgo Pro Micro, 6× 6×6×8 mm tactile switches, 8× M4×8 countersunk screws
  (4 base, 4 plate), M4 tap or heat-set inserts in the four bosses.
- Solder switch leads to the header pins first, drop the board into the neck
  pocket from the back, feed the micro-USB plug down the channel, fit the plate.

## Open items

- Print and check the fit: board in the pocket, caps on the switch plungers,
  plate flush in its recess.
- Firmware for the Pro Micro (HID gamepad, 6 inputs) has not been written yet.
- The bezel could drop to Ø12 for a 14 mm pitch if the buttons should be tighter.
