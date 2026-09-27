#!/usr/bin/env python3
"""Build every part of the iPhone desk mount, export individual STLs, compose the one-plate STL,
and validate (watertight, envelope, gaps).

    python3 build.py            # build everything -> ../stl/
    python3 build.py clamp_body # build one part only (module name under parts/)

Each module in parts/ exposes build() -> cq.Workplane in PRINT orientation with its lowest point at
z = 0 and its footprint centred on the origin.  params.PLATE_LAYOUT lists (module, instance, x, y, rot_deg).
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import time

import cadquery as cq
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params  # noqa: E402
from lib import validate as V  # noqa: E402

STL_DIR = os.path.normpath(os.path.join(HERE, '..', 'stl'))
EXPORT_TOL = 0.02
EXPORT_ANG = 0.15


def build_part(module_name: str) -> cq.Workplane:
    mod = importlib.import_module(f'parts.{module_name}')
    wp = mod.build()
    # normalise: lowest point at z=0, XY centred on bounding-box centre
    bb = wp.val().BoundingBox()
    wp = wp.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))
    return wp


def export(wp: cq.Workplane, path: str) -> trimesh.Trimesh:
    """Tessellate with OCCT, then clean with trimesh (merge vertices, drop degenerate triangles that OCCT
    emits at sphere poles) and re-save as binary STL."""
    cq.exporters.export(wp, path, tolerance=EXPORT_TOL, angularTolerance=EXPORT_ANG)
    m = trimesh.load(path, force='mesh', process=True, validate=True)
    m.export(path)
    return m


def main(only: str | None = None) -> int:
    os.makedirs(STL_DIR, exist_ok=True)
    modules = sorted({m for (m, *_rest) in params.PLATE_LAYOUT})
    if only:
        modules = [only]
    built: dict[str, cq.Workplane] = {}
    reports = []
    ok = True
    for m in modules:
        t = time.time()
        wp = build_part(m)
        built[m] = wp
        path = os.path.join(STL_DIR, f'{m}.stl')
        mesh = export(wp, path)
        rep = V.mesh_report(mesh, m)
        rep['build_s'] = round(time.time() - t, 1)
        rep['bed_contact_mm2'] = round(V.bed_contact_area(mesh), 1)
        reports.append(rep)
        flag = 'OK ' if rep['watertight'] and rep['bodies'] == 1 else 'BAD'
        if flag == 'BAD':
            ok = False
        print(f"[{flag}] {m:18s} {rep['size_x']:6.1f} x {rep['size_y']:6.1f} x {rep['size_z']:6.1f} mm  "
              f"vol {rep['volume_mm3']/1000:7.1f} cm3  faces {rep['faces']:6d}  bodies {rep['bodies']}  {rep['build_s']}s")
    if only:
        return 0 if ok else 1

    # compose plate
    placed = []
    scene_meshes = []
    for (m, inst, x, y, rot) in params.PLATE_LAYOUT:
        wp = built[m].rotate((0, 0, 0), (0, 0, 1), rot).translate((x, y, 0))
        path = os.path.join(STL_DIR, f'_tmp_{m}_{inst}.stl')
        mesh = export(wp, path)
        os.remove(path)
        placed.append((f'{m}#{inst}', mesh))
        scene_meshes.append(mesh)
    problems = V.check_plate(placed)
    plate = trimesh.util.concatenate(scene_meshes)
    plate_path = os.path.join(STL_DIR, 'ALL_PARTS_ONE_PLATE.stl')
    plate.export(plate_path)
    ext = plate.bounds[1] - plate.bounds[0]
    print(f"\nPlate: {len(placed)} bodies, envelope {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"total {plate.volume/1000:.1f} cm3 (~{plate.volume/1000*1.27:.0f} g PETG solid; less with infill)")
    for p in problems:
        print('  PROBLEM:', p)
        ok = False
    if not problems:
        print(f'  plate layout OK: inside {V.PLATE_XY:.0f}x{V.PLATE_XY:.0f}, all footprint gaps >= {V.MIN_GAP:.0f} mm, all parts on the bed')
    with open(os.path.join(STL_DIR, 'build_report.json'), 'w') as f:
        json.dump(dict(parts=reports, plate_problems=problems,
                       plate_envelope=[float(v) for v in ext]), f, indent=1)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
