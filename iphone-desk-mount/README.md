# iPhone desk mount — fully 3D-printed, one Bambu Lab P1S plate, PETG

A rigid clamp-on iPhone stand that puts the phone **up to 709 mm (27.9 in) above the desk**, clamps desks
**5–57 mm (up to 2.2 in)** thick, holds any iPhone with or without a case (64–86 mm wide, 7–14 mm thick) in portrait
or landscape with a positively locked tilt, and prints as **16 parts in one job on a 256 × 256 mm plate** with **no
supports and no hardware**: every screw, nut and joint is printed.

- `stl/ALL_PARTS_ONE_PLATE.stl` — the whole kit laid out on the plate (244 × 244 mm footprint, tallest part 225 mm).
- `stl/<part>.stl` — each part alone, already in its print orientation (Z up, sitting on Z = 0).
- `src/` — CadQuery source that generates everything (`python3 build.py`), plus `check_assembly.py`, which places the
  exported STLs in their mating positions and measures every clearance and interference.

## Why it is stiff and not wobbly

| item | value |
|---|---|
| pole | 50 × 50 mm square tube, 3 mm walls, I ≈ 204 000 mm⁴; three identical 225 mm segments |
| pole joints | 2.5°/side square **taper wedges**, self-locking and self-centring: zero play, tightened by the weight above them. The same wedge joins pole→pole, pole→head and pole→clamp |
| tip stiffness (bare pole, 20 N at the phone centre 709 mm up) | ≈ 4.6 N/mm; assembled with clamp, joints and head ≈ 3.3 N/mm (target ≥ 3), first mode ≈ 12 Hz |
| stress at the pole root for a 20 N sideways bump at the phone | 1.9 MPa; factor of safety > 13 even against PETG's layer-adhesion strength |
| clamp | one-piece C-body, 26 mm spine × 110 mm wide, two 8 mm contact rails 102 mm apart, screw at mid-pad; printed Tr16×3 screw with a 64 mm T-bar |
| tilt lock | 36-tooth **Hirth coupling** (10° steps), positive lock, zero play; Tr10 thumbscrew with a 50 mm T-bar |
| phone grip | two 60° V-jaws pinch the phone against the back plate whatever its thickness: nothing rattles |

A slip-fit joint with 0.3 mm clearance over 50 mm would let the phone move about 5 mm per joint. Every joint here is a
wedge or a preloaded toothed coupling, and nothing relies on a clearance fit for rigidity.

## Parts (16 bodies)

| qty | part | print orientation (as laid out) | notes |
|---|---|---|---|
| 3 | `pole_segment` | standing, socket mouth on the bed, spigot up | identical; the bottom 55 mm also has an external taper that plugs into the clamp; 6 mm knock hole for releasing a stuck joint |
| 1 | `clamp_body` | on its side | diamond (45°) pole socket, pocket for the nut block, two desk rails |
| 1 | `nut_block` | flat | Tr16×3 nut, slides into the bottom-jaw pocket |
| 1 | `clamp_screw` | standing on its T-bar | Tr16×3, 80 mm thread, ball tip |
| 1 | `swivel_pad` | flat face down | snaps onto the ball (six flex petals) |
| 1 | `head` | standing, socket down | fork rotated 45° so the phone faces the desk edge squarely; Hirth ring on one ear |
| 1 | `carrier` | on its back, boss up | tilt tongue with the mating Hirth ring and a captured nut; square index boss for portrait/landscape |
| 1 | `cradle` | flat, back down | 12 mm spine, V-lip with 22 mm port cut-out, boss socket, retaining thread |
| 1 | `slider` | standing on its end | top V-jaw; friction-locked by a thumbscrew |
| 1 | `thumbscrew_tilt` | standing on its T-bar | Tr10×2.5, 50 × 14 T-bar |
| 2 | `thumbscrew_retain`, `thumbscrew_lock` | standing on the T-bar | Tr8×2.5, 40 × 12 T-bar |
| 1 | `square_nut_tilt` | flat | 18 mm square, Tr10×2.5, lives inside the carrier tongue |
| 1 | `square_nut` | flat | 16 mm square, Tr8×2.5, lives inside the slider |

Solid volume of the kit is 2.17 L. Sliced with 4 walls and 15–25 % infill expect roughly **1.2–1.4 kg of PETG**; the
clamp body is about 450–600 g of that and the three pole segments about 200 g each (they are almost all wall). Plan on
a fresh 1 kg spool plus a partial, or print the plate as two jobs.

## Print settings (PETG, 0.4 mm nozzle)

- 0.2 mm layers, **4 walls**, 4 top/bottom layers, 15–25 % gyroid infill. Use **6 walls + 30 %** on `clamp_body` and
  `head` for the stiffest result.
- **No supports.** Every overhang is ≤ 50°, every internal ceiling ≤ 20 mm; thread flanks are self-supporting.
- Print all objects at once (normal by-layer mode, not "by object"): parts are 4 mm apart on this plate. Brims off, or
  ≤ 1.5 mm; a 3 mm brim on the three pole segments only (225 mm tall on a 50 mm base) is cheap insurance on a drafty
  printer.
- Elephant-foot compensation 0.15 mm. Every mating surface that touches the bed already has a 1 mm chamfer, so a little
  elephant foot does not change how the wedges seat.
- Slow the outer walls on threaded parts (≤ 60 mm/s); keep part cooling at 50–80 %.

## Assembly

1. **Clamp.** Slide the `nut_block` into the bottom-jaw pocket from the side (the pocket is open toward the side face
   and the desk). Screw the `clamp_screw` up through the jaw into the nut block, ball first. Press the `swivel_pad`
   onto the ball until it snaps.
2. **Pole.** Push a segment into the diamond socket on the clamp, corner first: the pole runs at 45° to the desk edge
   on purpose. Push the next segment's socket down over the spigot until it wedges, then the third. A firm shove seats
   each wedge; a 1–7 mm gap remains between the shoulder and the socket mouth because the wedge, not the shoulder,
   carries the load. To separate, pull with a twist, or push a 5 mm rod through the knock hole against the spigot tip.
3. **Head.** Push the `head` onto the top spigot. Its fork is already turned so the phone faces the desk edge.
4. **Tilt.** Slide the `square_nut_tilt` into the slot in the carrier tongue from the rounded end until it sits on the
   hinge axis. Put the tongue between the ears with its toothed face toward the toothed ear, and run
   `thumbscrew_tilt` through the toothed ear, the tongue and out through the far ear. Tightening pulls the tongue
   onto the teeth; to change the angle, loosen three quarters of a turn, nod to the next notch, retighten.
5. **Cradle.** Put the `cradle` over the carrier's square boss (four positions: portrait or landscape, either way up),
   then run `thumbscrew_retain` through the carrier from behind into the thread in the cradle's back pad. Snug it and
   the boss wedge seats: the cradle becomes one piece with the carrier.
6. **Slider.** Drop the `square_nut` into the slider's back-wall pocket from the inside, thread `thumbscrew_lock` in
   until its tip is flush, and slide the slider onto the cradle spine from the top end, V-jaw toward the phone.
7. **Clamp it.** Open the throat, hook the pad over the desk edge (the pole ends up 25 mm inboard of the edge) and
   tighten the T-bar hard: 1.5–2 N·m, which is a firm two-finger pull on each end. Retighten once after 24 h (PETG
   settles). Set the phone's bottom edge in the V-lip, slide the top jaw down until both V faces pinch the phone
   against the back, and lock the thumbscrew.

Height options: use one, two or three segments; the phone centre sits at about 350, 530 or 709 mm above the desk.

## Engineering notes

- **Wedge seat sensitivity.** ±0.15 mm of printer error moves a 2.5° wedge seat by ±3.4 mm; sockets are 60 mm deep for
  50 mm spigots and the clamp socket 56 mm deep for a 55 mm taper, so nothing bottoms out. If a joint seats with its
  shoulder touching the mouth, scale that spigot's XY by 0.995 in the slicer or sand its flats.
- **Clamp preload.** A printed Tr16×3 delivers about 290 N per N·m once ball friction is counted. Pry-off capacity is
  preload × 37.5 mm (screw to either pad edge): a 20 N bump at the phone needs about 14.4 N·m, so tighten to ≥ 1.5 N·m
  (≈ 16.5 N·m capacity) and preferably 2 N·m (≈ 22 N·m). Everyday loads are 30× smaller than that bump.
- **Tilt lock.** The Hirth teeth are radial wedges whose width equals the pitch at every radius, with 0.3 mm crest
  relief, so the flanks carry and the rings self-centre. The tongue floats 2.5 mm in the ear gap and is pulled onto
  the toothed ear by the screw and a nut captured inside the tongue: 300 N from the T-bar against a lift-off demand of
  about 150 N at the 20 N bump. No friction lock is involved.
- **Printed threads.** Trapezoidal, 30° included angle, depth 0.45 p, bolt crest 0.25 p; radial clearance 0.35 mm on
  Tr16×3, 0.30 on Tr10×2.5, 0.25 on Tr8×2.5 (about ±0.3–0.45 mm axial backlash, irrelevant because every screw is
  preloaded).
- **Verified fits** (`src/check_assembly.py`, run on the exported STLs): 0.000 mm interference at every wedge seat
  with the predicted 0.044 mm gap per 1 mm of lift; 0.30 mm on the nut block, slider and tilt nut; 0.18 mm around the
  ball; the Hirth rings interlock flank-to-flank when locked and clear by 0.33 mm when unlocked.
- **Printability check** (`src/lib/printcheck.py`): the only surfaces steeper than 50° are thread flanks, the corners
  of 45° internal hoppers (small patches at 54°) and hole roofs ≤ 19 mm with 45° gables.

## Regenerating

```bash
pip install cadquery trimesh numpy shapely rtree networkx
cd iphone-desk-mount/src
python3 build.py            # all parts -> ../stl, plate STL, validation (watertight, envelope, gaps, bed contact)
python3 check_assembly.py   # clearance report + height stack-up
```
All dimensions live in `src/params.py` (desk opening, pole size, phone range, plate layout).
