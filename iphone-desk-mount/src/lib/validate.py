"""Mesh / plate validation helpers (trimesh based)."""
from __future__ import annotations

import itertools
import numpy as np
import trimesh

PLATE_XY = 250.0      # usable envelope (P1S is 256 x 256)
PLATE_Z = 245.0       # usable height (P1S is 256)
MIN_GAP = 4.0         # between parts (footprint to footprint)
EDGE_MARGIN = 3.0     # from envelope edge


def load(path: str) -> trimesh.Trimesh:
    m = trimesh.load(path, force='mesh')
    return m


def mesh_report(m: trimesh.Trimesh, name: str = '') -> dict:
    ext = m.bounds[1] - m.bounds[0]
    rep = dict(name=name, watertight=bool(m.is_watertight), winding_consistent=bool(m.is_winding_consistent),
               volume_mm3=float(m.volume), faces=int(len(m.faces)), bodies=int(m.body_count),
               size_x=float(ext[0]), size_y=float(ext[1]), size_z=float(ext[2]),
               min_z=float(m.bounds[0][2]))
    return rep


def footprint_polygon(m: trimesh.Trimesh):
    """2D footprint (shapely polygon) of the mesh projected onto the bed, via the convex hull of each
    connected slice... we use the exact projection so C-shaped parts can nest other parts."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    tris = m.triangles[:, :, :2]
    polys = []
    for t in tris:
        p = Polygon(t)
        if p.is_valid and p.area > 1e-6:
            polys.append(p)
    return unary_union(polys).buffer(0)


def check_plate(placed: list[tuple[str, trimesh.Trimesh]], plate_xy: float = PLATE_XY, plate_z: float = PLATE_Z,
                min_gap: float = MIN_GAP, edge_margin: float = EDGE_MARGIN) -> list[str]:
    """placed: (name, mesh already translated into plate coordinates, plate spans [0,plate_xy]^2, z>=0).
    Returns a list of problems (empty == OK).  Gaps are measured between exact 2D footprints, so parts may
    nest inside another part's concavity (e.g. the clamp throat)."""
    problems = []
    foots = []
    for name, m in placed:
        lo, hi = m.bounds
        if lo[0] < edge_margin - 1e-6 or lo[1] < edge_margin - 1e-6 or hi[0] > plate_xy - edge_margin + 1e-6 or hi[1] > plate_xy - edge_margin + 1e-6:
            problems.append(f"{name}: outside XY envelope {lo[:2].round(1)}..{hi[:2].round(1)}")
        if hi[2] > plate_z:
            problems.append(f"{name}: too tall {hi[2]:.1f} > {plate_z}")
        if abs(lo[2]) > 0.05:
            problems.append(f"{name}: does not sit on the plate (min z = {lo[2]:.2f})")
        foots.append((name, footprint_polygon(m)))
    for (n1, p1), (n2, p2) in itertools.combinations(foots, 2):
        d = p1.distance(p2)
        if d < min_gap - 0.05:   # tessellation slack
            problems.append(f"{n1} <-> {n2}: footprint gap {d:.1f} < {min_gap}")
    return problems


def bed_contact_area(m: trimesh.Trimesh, tol: float = 0.05) -> float:
    """Area of faces lying on z = min z (first layer footprint)."""
    z0 = m.bounds[0][2]
    fz = m.triangles[:, :, 2]
    on_bed = np.all(np.abs(fz - z0) < tol, axis=1)
    return float(m.area_faces[on_bed].sum())
