"""Printed-thread generator for CadQuery (trapezoidal / ACME-like profile) tuned for FDM PETG.

Conventions: axis = +Z, thread starts at z=0.  All dimensions in mm.

    external_thread(major_d, pitch, length)            -> complete threaded rod section (core + ridge),
                                                          crest chamfered (lead-in) at both ends.
    internal_thread_cutter(major_d, pitch, length, c)  -> solid to SUBTRACT from a nut body occupying
                                                          z in [0, length]; mates with the external thread
                                                          of the same (major_d, pitch) with radial/flank
                                                          clearance c.

OCCT robustness rule learned the hard way: a helical sweep must be TRIMMED (intersect with a cylinder)
to the exact z-extent of the body it is fused with; if the ridge overhangs the body's top face the
boolean silently drops one operand.  Every public function here obeys that.
"""
from __future__ import annotations

import math
import cadquery as cq

DEPTH_FRACTION = 0.45        # thread depth / pitch (ACME = 0.5; a bit shallower prints stronger crests)
FLANK_HALF_ANGLE_DEG = 15.0  # 30 deg included angle, ACME-like
CREST_FRACTION = 0.25        # crest flat width / pitch (bolt).  Root flat = crest + 2*depth*tan(flank)
                             # (0.25 balances bolt and nut ridge widths once the nut is grown by the clearance)
ROOT_SINK = 0.30             # how far the ridge root is buried inside the core (avoids coincident faces)


def thread_depth(pitch: float) -> float:
    return DEPTH_FRACTION * pitch


def minor_diameter(major_d: float, pitch: float) -> float:
    return major_d - 2.0 * thread_depth(pitch)


def spec(major_d: float, pitch: float, clearance: float) -> dict:
    """Numbers worth printing in a spec table."""
    h = thread_depth(pitch)
    tan_f = math.tan(math.radians(FLANK_HALF_ANGLE_DEG))
    bolt_crest = CREST_FRACTION * pitch
    bolt_root = bolt_crest + 2 * h * tan_f
    return dict(
        major_d=major_d, minor_d=major_d - 2 * h, pitch=pitch, depth=h,
        bolt_crest_w=bolt_crest, bolt_root_w=bolt_root,
        bolt_groove_at_root=pitch - bolt_root,
        nut_major_d=major_d + 2 * clearance, nut_minor_d=major_d - 2 * h + 2 * clearance,
        nut_ridge_w_at_crest=pitch - bolt_root - 2 * clearance,
        radial_clearance=clearance, axial_backlash=2 * clearance,
    )


def _ridge(major_d: float, pitch: float, z0: float, z1: float, grow: float = 0.0,
           left_hand: bool = False) -> cq.Workplane:
    """Helical ridge (no core) trimmed EXACTLY to z in [z0, z1].  `grow` enlarges it radially and
    axially (used to build the nut cutter with clearance)."""
    h = thread_depth(pitch)
    r_major = major_d / 2.0 + grow
    r_minor = r_major - h
    r_root = r_minor - ROOT_SINK
    tan_f = math.tan(math.radians(FLANK_HALF_ANGLE_DEG))
    w_crest = CREST_FRACTION * pitch + 2.0 * grow
    w_root = w_crest + 2.0 * (h + ROOT_SINK) * tan_f
    if w_root >= pitch - 0.05:
        raise ValueError(f"thread profile too wide for pitch: root {w_root:.2f} >= pitch {pitch}")
    span = z1 - z0
    # overshoot one pitch each side so the helix start/end caps are fully outside the trim window
    helix = cq.Wire.makeHelix(pitch=pitch, height=span + 2 * pitch, radius=r_root, lefthand=left_hand)
    pts = [(r_root, -w_root / 2.0), (r_major, -w_crest / 2.0), (r_major, w_crest / 2.0), (r_root, w_root / 2.0)]
    ridge = (cq.Workplane("XZ").polyline(pts).close()
             .sweep(cq.Workplane(obj=helix), isFrenet=True)
             .translate((0, 0, z0 - pitch)))
    trim = cq.Workplane("XY").circle(r_major + 1.0).extrude(span).translate((0, 0, z0))
    return ridge.intersect(trim)


def external_thread(major_d: float, pitch: float, length: float, chamfer: float | None = None,
                    left_hand: bool = False) -> cq.Workplane:
    """Threaded rod section z in [0, length]: core + ridge, crests chamfered (lead-in) at both ends.

    The core deliberately overshoots the ridge by 0.5 mm at both ends (OCCT fuses reliably when the
    ridge is strictly inside the core's z-range); the result is then trimmed to [0, length]."""
    h = thread_depth(pitch)
    r_major = major_d / 2.0
    r_minor = r_major - h
    if chamfer is None:
        chamfer = h
    ridge = _ridge(major_d, pitch, 0.0, length, 0.0, left_hand)
    core = cq.Workplane("XY").circle(r_minor + 0.001).extrude(length + 1.0).translate((0, 0, -0.5))
    rod = core.union(ridge)
    env = cq.Workplane("XY").circle(r_major + 0.02).extrude(length)
    if chamfer > 0:
        env = env.faces(">Z").chamfer(chamfer).faces("<Z").chamfer(chamfer)
    return rod.intersect(env)


def internal_thread_cutter(major_d: float, pitch: float, length: float, clearance: float = 0.35,
                           left_hand: bool = False, run_out: float | None = None) -> cq.Workplane:
    """Solid to SUBTRACT from a nut body that occupies z in [0, length].
    Extends `run_out` (default one pitch) beyond both faces so the thread runs fully through.
    The bore overshoots the ridge by 0.5 mm (same OCCT robustness rule as external_thread)."""
    if run_out is None:
        run_out = pitch
    h = thread_depth(pitch)
    r_major = major_d / 2.0 + clearance
    r_minor = r_major - h
    z0, z1 = -run_out, length + run_out
    ridge = _ridge(major_d, pitch, z0, z1, clearance, left_hand)
    bore = cq.Workplane("XY").circle(r_minor + 0.001).extrude(z1 - z0 + 1.0).translate((0, 0, z0 - 0.5))
    return bore.union(ridge)


def nut_entry_chamfer_cutter(major_d: float, pitch: float, clearance: float, depth: float | None = None) -> cq.Workplane:
    """Cone to subtract at a nut face (z=0 face, opening downward) for an easy thread start.
    Translate/rotate it yourself to the other face if needed."""
    h = thread_depth(pitch)
    if depth is None:
        depth = h
    r_nut_major = major_d / 2.0 + clearance
    r_nut_minor = r_nut_major - h
    cone = cq.Solid.makeCone(r_nut_major + depth, r_nut_minor - 0.01, depth + 0.01, pnt=cq.Vector(0, 0, -0.01))
    return cq.Workplane(obj=cone)
