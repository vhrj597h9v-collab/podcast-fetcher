"""Assembled-fit checks between two meshes using surface sampling + signed distance (trimesh + rtree)."""
from __future__ import annotations

import numpy as np
import trimesh


def clearance_report(inner: trimesh.Trimesh, outer: trimesh.Trimesh, samples: int = 6000, seed: int = 0) -> dict:
    """Sample points on `inner`'s surface and measure signed distance to `outer`'s surface.
    Positive = point is inside `outer` solid  (trimesh convention: signed_distance > 0 inside).
    For a male part sitting inside a female cavity we expect points OUTSIDE the female solid, i.e. negative
    signed distance whose magnitude is the local gap.  Returns min gap, interference depth, stats."""
    rng = np.random.default_rng(seed)
    pts, _ = trimesh.sample.sample_surface(inner, samples, seed=seed)
    sd = trimesh.proximity.signed_distance(outer, pts)   # >0 inside outer
    interfering = sd > 1e-3
    return dict(
        samples=int(len(pts)),
        max_interference_mm=float(sd.max()) if interfering.any() else 0.0,
        interfering_fraction=float(interfering.mean()),
        min_gap_mm=float(-sd[~interfering].max()) if (~interfering).any() else None,
        median_gap_mm=float(np.median(-sd[~interfering])) if (~interfering).any() else None,
    )


def solid_contains_points(mesh: trimesh.Trimesh, pts: np.ndarray) -> np.ndarray:
    return mesh.contains(pts)
