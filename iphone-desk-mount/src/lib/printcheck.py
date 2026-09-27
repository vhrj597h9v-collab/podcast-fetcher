"""FDM printability analysis of a mesh in its print orientation (z up, bed at z = min z).

overhang_report(mesh) -> dict with the area of downward-facing surface whose overhang exceeds the limit,
grouped by z-band, so bridges/ceilings can be located.  Overhang angle convention: 0 deg = vertical wall,
90 deg = horizontal ceiling.  Faces on the bed are ignored.
"""
from __future__ import annotations

import numpy as np
import trimesh

MAX_OVERHANG_DEG = 50.0


def overhang_report(m: trimesh.Trimesh, max_deg: float = MAX_OVERHANG_DEG, band: float = 2.0) -> dict:
    n = m.face_normals
    down = n[:, 2] < -1e-6
    # overhang angle from vertical: angle between the normal and the horizontal plane, for downward normals
    ang = np.degrees(np.arcsin(np.clip(-n[:, 2], 0, 1)))  # 0 = wall, 90 = ceiling
    z0 = m.bounds[0][2]
    centroids = m.triangles_center
    on_bed = np.all(np.abs(m.triangles[:, :, 2] - z0) < 0.05, axis=1)
    bad = down & (ang > max_deg) & ~on_bed
    ceilings = down & (ang > 85) & ~on_bed
    rep = dict(total_bad_area_mm2=float(m.area_faces[bad].sum()),
               ceiling_area_mm2=float(m.area_faces[ceilings].sum()),
               bands=[])
    if bad.any():
        zs = centroids[bad, 2]
        for zb in np.arange(np.floor(zs.min() / band) * band, zs.max() + band, band):
            sel = bad & (centroids[:, 2] >= zb) & (centroids[:, 2] < zb + band)
            if not sel.any():
                continue
            pts = m.triangles[sel].reshape(-1, 3)
            ext = pts.max(axis=0) - pts.min(axis=0)
            rep['bands'].append(dict(z=float(zb), area_mm2=float(m.area_faces[sel].sum()),
                                     max_angle=float(ang[sel].max()),
                                     span_x=float(ext[0]), span_y=float(ext[1])))
    return rep


def summarize(rep: dict, name: str = '') -> str:
    lines = [f"{name}: overhang>limit area {rep['total_bad_area_mm2']:.0f} mm2, of which ceilings {rep['ceiling_area_mm2']:.0f} mm2"]
    for b in rep['bands'][:12]:
        lines.append(f"   z~{b['z']:6.1f}: {b['area_mm2']:7.1f} mm2  max {b['max_angle']:4.0f} deg  span {b['span_x']:.0f} x {b['span_y']:.0f}")
    if len(rep['bands']) > 12:
        lines.append(f"   ... {len(rep['bands']) - 12} more bands")
    return '\n'.join(lines)
