# iPhone desk mount — articulated, fully 3D-printed, one Bambu Lab P1S plate, PETG

A rigid, clamp-on, **articulated** iPhone arm: a desk clamp, a lower arm, a positively locked **elbow**, an upper
segment and a tilting head with a V-jaw cradle. Straight up it puts the phone centre **628 mm (24.7 in)** above the
desk; bent 90° at the elbow it holds the phone about 280 mm high and 350 mm out from the elbow, and every angle in
between in 9° steps. It clamps desks **5–53 mm (up to 2.1 in)** thick, holds any iPhone with or without a case
(64–86 mm wide, 7–14 mm thick, up to 165 mm long) in portrait or landscape, and prints as **18 parts in one job on a
256 × 256 mm plate** with **no supports and no hardware**: every screw, nut and joint is printed.

- `stl/ALL_PARTS_ONE_PLATE.stl` — the whole kit laid out on the plate (242 × 244 mm footprint, tallest part 245 mm).
- `stl/<part>.stl` — each part alone, already in its print orientation (Z up, sitting on Z = 0).
- `stl/ASSEMBLED_PREVIEW.stl` — the parts composed straight-up on a 30 mm desk, for viewing only
  (`assembled_preview.png` and `plate_preview.png` are renders of the assembly and the plate).
- `src/` — CadQuery source that generates everything (`python3 build.py`), plus `check_assembly.py`, which places the
  exported STLs in their mating positions and measures every clearance and interference.

## How it moves and why it stays put

| joint | mechanism | positions |
|---|---|---|
| clamp → lower arm | 2.5° square **taper wedge**, self-locking, zero play | 4 orientations (90° steps) |
| **elbow** (lower arm → upper segment) | 40-tooth **Hirth coupling** clamped by a Tr16 screw with a 60 mm T-bar: the toothed tongue is pulled onto the toothed ear, so it locks positively with zero rotational play; loosen ¾ turn, the tongue floats 3 mm off the teeth, swing, retighten | 9° steps through 360° (practically −90° … +90°) |
| upper segment → head | taper wedge | 4 orientations |
| head tilt | 30-tooth Hirth coupling, Tr10 screw with a 50 mm T-bar | 12° steps |
| cradle on the head | 5° tapered square boss preloaded by a Tr10 retaining screw | portrait / landscape, either way up |
| phone in the cradle | two 60° V-jaws pinch it against the back plate; friction-locked top jaw | continuous |

Nothing in the load path is a friction lock except the top jaw on the cradle spine, and the phone weighs 2.5 N.

## Stiffness and strength

| item | value |
|---|---|
| arm sections | 50 × 50 mm square tube, 3 mm walls, I ≈ 204 000 mm⁴ |
| elbow | Hirth ring r 20–30 mm; a 1.5 N·m T-bar gives ≈ 440 N preload → ≈ 11 N·m holding moment against ≈ 8 N·m from a 20 N bump at the phone with the arm straight up |
| tilt | Hirth ring r 14–20 mm; ≈ 300 N preload → ≈ 5 N·m against ≈ 2 N·m from the same bump |
| clamp | one-piece C-body, 26 mm spine × 110 mm wide, contact frame with rails 102 mm apart, screw at mid-pad; printed Tr16×3 screw with a 60 mm T-bar |
| pole stress for a 20 N sideways bump at the phone, straight up | ≈ 2 MPa; factor of safety > 12 against PETG layer strength |

Tighten the clamp to 1.5–2 N·m (a firm two-finger pull on each end of the T-bar): pry-off capacity is preload ×
37.5 mm, so 1.5 N·m gives ≈ 16 N·m against ≈ 14 N·m for the 20 N bump. Everyday loads are 30 times smaller. Retighten
once after 24 h; PETG settles.

## Parts (18 bodies)

| qty | part | print orientation (as laid out) | notes |
|---|---|---|---|
| 1 | `arm_lower` | standing on its taper | diamond taper into the clamp, twist to a square tube, elbow fork with the Hirth ring |
| 1 | `elbow_tongue` | standing on its spigot tip | tongue with the mating ring and a slot for the elbow nut; spigot for the segment. Print with a 3 mm brim |
| 1 | `elbow_screw`, `elbow_nut` | T-bar down / flat | Tr16×3, 25 mm square nut |
| 1 | `pole_segment` | standing, socket mouth on the bed | 240 mm; knock slot for releasing a stuck spigot |
| 1 | `clamp_body` | on its side | diamond pole socket with a release hole, nut-block pocket, pad contact frame |
| 1 | `nut_block`, `clamp_screw`, `swivel_pad` | flat / T-bar down / face down | Tr16×3, 12 mm ball, six-petal snap pad |
| 1 | `head` | standing, socket down | fork with the tilt Hirth ring |
| 1 | `carrier` | on its back, boss up | tilt tongue (true half-round end, tilts to ±90°), captured nut, square index boss |
| 1 | `cradle` | flat, back down | 198 mm spine, V-lip with 22 mm port cut-out, boss socket, hopper and Tr10 thread |
| 1 | `slider` | standing on its jaw end | top V-jaw; channel body rides under the phone |
| 3 | `thumbscrew_tilt` (Tr10), `thumbscrew_retain` (Tr10), `thumbscrew_lock` (Tr8) | T-bar down | 50 × 14 and 38 × 12 T-bars |
| 2 | `square_nut_tilt` (18 mm, Tr10), `square_nut` (16 mm, Tr8) | flat | live inside the carrier tongue and the slider |

Estimated printed mass: about **1284 g of PETG with 4 walls and 20 % infill**, or ≈ 1761 g with 6 walls and 30 %.
Expect a 45–60 hour job; the individual STLs let you split it into two jobs if you prefer.

## Print settings (PETG, 0.4 mm nozzle)

- 0.2 mm layers, **4 walls**, 4 top/bottom layers, 15–25 % gyroid infill; **6 walls + 30 %** on `clamp_body`,
  `arm_lower` and `head` for the stiffest result.
- **No supports.** Every overhang is ≤ 50°, every internal ceiling ≤ 20 mm, every horizontal hole has a 45° gable.
- Print all objects at once (normal by-layer mode, not "by object"): parts are 4 mm apart. Brims off, except a
  3 mm brim on `elbow_tongue` (121 mm tall on a 30 mm base) and optionally on `arm_lower` and `pole_segment`.
- Elephant-foot compensation 0.15 mm; every sliding fit and wedge mouth has its own chamfer on the bed face.
- Threads: 60° flanks, so they print without support; slow the outer walls on threaded parts (≤ 60 mm/s), enable
  wipe-on-retract, keep PETG ≤ 240 °C to limit stringing across the wedge flats.

## Assembly

1. **Clamp.** Slide the `nut_block` into the bottom-jaw pocket from the side. Screw the `clamp_screw` up through the
   jaw into it, ball first. Press the `swivel_pad` onto the ball until it snaps.
2. **Lower arm.** Push the `arm_lower` taper into the diamond socket on the clamp, corner first, until it wedges. The
   fork on top ends up with its axis parallel to the desk edge, so the arm swings toward and away from you. To
   release it later, push a 5 mm rod through the hole in the tower against the base.
3. **Elbow.** Drop the `elbow_nut` into the slot in the `elbow_tongue` (rounded end) and hold it there while you put
   the tongue between the fork ears, toothed face toward the toothed ear. Run the `elbow_screw` through the toothed
   ear, the tongue and out through the far ear; tighten. To move the elbow: loosen ¾ turn, swing to the next notch,
   tighten hard (1.5 N·m).
4. **Segment and head.** Push the `pole_segment` socket onto the elbow spigot, then the `head` onto the segment.
   A firm shove seats each wedge; a 1–7 mm gap remains at the shoulder because the wedge, not the shoulder, carries
   the load. Release with a twist-and-pull, or a rod through the knock slot against the spigot tip.
5. **Tilt.** Slide the `square_nut_tilt` into the carrier tongue from its rounded end until it sits on the axis. Put
   the tongue between the head ears, toothed face toward the toothed ear, and run `thumbscrew_tilt` through.
6. **Cradle.** Put the `cradle` over the carrier's square boss (four positions), then run `thumbscrew_retain` through
   the carrier from behind into the thread in the cradle's back pad and snug it.
7. **Slider.** Drop the `square_nut` into the slider's back-wall pocket from the inside, thread `thumbscrew_lock` in
   until its tip is flush, and slide the slider onto the cradle spine from the top end, jaw wall outward.
8. **Use.** Clamp to the desk (tighten hard, retighten after a day). Set the phone's bottom edge in the V-lip, slide
   the top jaw down until both V faces pinch the phone, lock the thumbscrew. Set the elbow and tilt, lock both.

## Engineering notes

- **Wedges.** ±0.15 mm of printer error moves a 2.5° seat by ±3.4 mm; every socket has 5–14 mm of spare depth so
  nothing bottoms out. If a joint seats with its shoulder touching, scale that spigot's XY by 0.995 in the slicer.
- **Hirth couplings.** True Hirth geometry: tooth width equals the pitch at every radius, 90° included angle, 0.3 mm
  crest relief, so the flanks carry and the rings self-centre. Each tongue floats in its fork and is pulled onto the
  toothed ear by a screw and a nut captured inside the tongue; loosening lets it slide clear of the teeth.
- **Printed threads.** 60° flanks, depth 0.35 p, bolt crest 0.15 p; radial clearance 0.35 mm on Tr16×3, 0.30 on
  Tr10×2.5, 0.25 on Tr8×2.5. Every screw is preloaded, so backlash never appears as play.
- **Verified fits** (`src/check_assembly.py`): 0.000 mm interference at every wedge seat with the predicted
  0.044 mm gap per 1 mm of lift; both Hirth couplings flank-to-flank when locked (0.10 mm) and ≥ 0.49 mm clear when
  unlocked; 0.30 mm on the nut block, slider, tilt nut and elbow nut; 0.18 mm around the ball; 30 mm of slider on the
  spine with a 165 × 14 mm phone.
- **Printability check** (`src/lib/printcheck.py`): the only surfaces steeper than 50° are the 45° hopper corners
  (small patches at 54°) and the ≤ 12 mm flats at the tops of gabled holes and hoppers.

## Regenerating

```bash
pip install cadquery trimesh numpy shapely rtree networkx
cd iphone-desk-mount/src
python3 build.py            # all parts -> ../stl, plate STL, validation (watertight, envelope, gaps, bed contact)
python3 check_assembly.py   # clearance report + height stack-up
```
All dimensions live in `src/params.py` (desk opening, arm size, elbow, phone range, plate layout).
