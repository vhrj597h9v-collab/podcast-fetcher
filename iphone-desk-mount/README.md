# iPhone desk mount — fully 3D-printed, one Bambu Lab P1S plate, PETG

A rigid, clamp-on iPhone stand that reaches **24 in+ (≈ 709 mm to the phone centre)** above the desk, clamps desks
**5–55 mm (up to 2.16 in)** thick, holds any iPhone with or without a case (64–86 mm wide, 7–14 mm thick) in portrait or
landscape with a lockable tilt, and prints as **17 parts in one job on a 256 × 256 mm plate** with **no supports and no
hardware** — every screw, nut and joint is printed.

- `stl/ALL_PARTS_ONE_PLATE.stl` — the whole kit laid out on the plate (243 × 240 mm footprint, tallest part 225 mm).
- `stl/<part>.stl` — each part alone, already in its print orientation (Z up, sitting on Z = 0).
- `src/` — the CadQuery source that generates everything (`python3 build.py`), plus `check_assembly.py`, which places
  the exported STLs in their mating positions and measures every clearance.

## Why it is stiff (and not wobbly)

| item | value |
|---|---|
| pole | 50 × 50 mm square tube, 3 mm walls, I = 208 500 mm⁴ |
| bare tip stiffness at 610 mm | 5.2 N/mm (target ≥ 3 N/mm assembled) |
| first natural frequency (phone + head on the pole) | ≈ 16 Hz bare, > 10 Hz assembled |
| stress at the pole base for a 20 N sideways bump at the phone | 1.5 MPa — factor of safety > 15 even against PETG's layer-adhesion strength |
| joints | 2.5°/side square **taper wedges**: self-centring, zero play, tightened by the weight above them; the same wedge joins pole → pole, pole → head and pole → clamp |
| clamp | one-piece C-body, 22 mm spine × 90 mm wide, 75 mm desk pad; a printed Tr16×3 screw gives ≈ 400 N at 1 N·m hand torque, ≈ 2.5× what a 20 N bump at the top needs to pry the pad off |

A slip-fit joint with 0.3 mm clearance over 50 mm would let the tip move ~5 mm per joint; that is why every joint here is a
wedge, and why nothing in this design relies on a clearance fit for rigidity.

## Parts (17 bodies)

| qty | part | print orientation (as laid out) | notes |
|---|---|---|---|
| 3 | `pole_segment` | standing, socket mouth on the bed, spigot up | identical; the bottom 55 mm also has an external taper that plugs into the clamp |
| 1 | `clamp_body` | on its side | diamond (45°) pole socket, pocket for the nut block |
| 1 | `nut_block` | flat | Tr16×3 nut, slides into the bottom-jaw pocket |
| 1 | `clamp_screw` | standing on its knob | Tr16×3, 80 mm thread, ball tip |
| 1 | `swivel_pad` | flat face down | snaps onto the ball |
| 1 | `head` | standing, socket down | fork is rotated 45° so the phone faces the desk edge squarely |
| 1 | `carrier` | on its back, boss up | tilt tongue + square index boss (portrait / landscape) |
| 1 | `cradle` | flat, back down | bottom lip with port cut-out, boss socket, retaining thread |
| 1 | `slider` | standing on its end | top jaw; friction-locked by a thumbscrew |
| 3 | `thumbscrew_tilt` / `_retain` / `_lock` | standing on the knob | all Tr8×2.5 |
| 3 | `square_nut` | flat | 16 mm square, Tr8×2.5 |

Solid volume of the whole kit is 1.84 L; sliced with 4 walls and 15–25 % infill expect roughly 1.1–1.3 kg of PETG
(the pole segments are wall-dominated at ≈ 220 g each). Use a fresh 1 kg spool plus a partial, or split the plate STL
into two jobs if you prefer.

## Print settings (PETG, 0.4 mm nozzle)

- 0.2 mm layers, **4 walls**, 3 top/bottom layers, 15–25 % gyroid infill; **6 walls + 30 %** for `clamp_body` and `head`
  if you want the very stiffest result.
- No supports. Every overhang is ≤ 50°, every internal ceiling ≤ 20 mm; thread flanks are self-supporting.
- Brim 5 mm on the three pole segments (225 mm tall on a 50 mm base) — optional on the P1S textured plate, cheap insurance.
- Elephant-foot compensation 0.15 mm (Bambu Studio default 0.15 is fine). Every mating fit that touches the bed
  already has a 1 mm chamfer, so a little elephant foot does not change how the wedges seat.
- Slow the outer wall on the threads (≤ 60 mm/s) and use a 0.2 mm "seam: aligned" setting; keep part cooling at
  50–80 % for PETG bridges.
- Print all parts in one job as laid out in `ALL_PARTS_ONE_PLATE.stl`, or import the individual STLs and let the
  slicer arrange them — they are already in the correct orientation.

## Assembly

1. **Clamp.** Slide the `nut_block` into the bottom-jaw pocket from the side (it is open toward the side face and the
   desk). Screw the `clamp_screw` up through the jaw's hole into the nut block, ball first. Press the `swivel_pad` onto
   the ball until it snaps.
2. **Pole.** Push segment 1 (any segment) into the diamond socket on top of the clamp, corner-first (the pole runs at
   45° to the desk edge — this is intentional). Push segment 2's socket down over segment 1's spigot until it wedges;
   then segment 3. A firm shove seats each wedge; there should be a 1–7 mm gap between the shoulder and the socket
   mouth — the wedge, not the shoulder, carries the load. To separate, twist and pull.
3. **Head.** Push the `head` onto the top spigot. Its fork is already turned so the phone faces the desk edge.
4. **Tilt.** Put the `square_nut` into the diamond pocket on the thick ear. Slide the `carrier` tongue between the
   ears, rings toward the ears, and run `thumbscrew_tilt` through the thin ear, the tongue and into the nut.
5. **Cradle.** Put the `cradle` over the carrier's square boss (4 positions: portrait or landscape, either way up),
   then run `thumbscrew_retain` through the carrier from behind into the thread inside the cradle's back pad. Snug it:
   the boss wedge seats and the cradle becomes one piece with the carrier.
6. **Slider.** Drop a `square_nut` into the slider's back-wall pocket from the inside, thread `thumbscrew_lock` into it
   until the tip is flush, slide the slider onto the cradle spine from the top end, hook facing the phone.
7. **Clamp it.** Open the throat, hook the pad over the desk edge (the pole ends up 25 mm inboard of the edge), tighten
   the knob hard by hand (≈ 1 N·m). Set the phone on the lip, slide the top jaw down onto it and lock the thumbscrew.
   Tilt, then lock the tilt knob.

Height options: use one, two or three segments — the phone centre sits at ≈ 350, 530 or 709 mm above the desk.

## Engineering notes

- Wedge seat sensitivity: ±0.15 mm of printer error moves the seat depth ±3.4 mm; sockets are 60 mm deep for 50 mm
  spigots and the clamp socket 56 mm deep for a 55 mm taper, so nothing bottoms out. If a joint seats with the
  shoulder touching the mouth (no gap), scale the spigot's outer XY by 0.995 in the slicer or sand the spigot flats.
- Printed threads: trapezoidal, 30° included angle, depth 0.45 p, bolt crest 0.25 p; radial clearance 0.35 mm on
  Tr16×3 and 0.25 mm on Tr8×2.5 (≈ ±0.4 / ±0.3 mm axial backlash, irrelevant because every screw is preloaded).
- Tilt lock is a friction lock on two raised rings (r 9–17 mm) clamped by a 30 mm knob: ≈ 1–2 N·m holding moment vs
  0.21 N·m from the phone. Hard bumps can still nod the phone — retighten; nothing breaks.
- Every mating pair has been checked numerically (`src/check_assembly.py`): 0.000 mm interference at nominal wedge
  seat, 0.30 mm on the nut block and slider, 0.10 mm at the tilt rings, 0.19 mm around the ball.

## Regenerating

```bash
pip install cadquery trimesh numpy shapely rtree networkx
cd iphone-desk-mount/src
python3 build.py            # all parts -> ../stl, plate STL, validation
python3 check_assembly.py   # clearance report + height stack-up
```
All dimensions live in `src/params.py` (desk opening, pole size, phone range, plate layout).
