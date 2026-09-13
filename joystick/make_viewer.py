#!/usr/bin/env python3
"""Inline out/scene.json into viewer_template.html -> out/joystick_viewer.html (self-contained)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "viewer_template.html"), encoding="utf-8").read()
scene = open(os.path.join(HERE, "out", "scene.json"), encoding="utf-8").read()
html = tpl.replace("/*__SCENE__*/null", scene, 1)
out = os.path.join(HERE, "out", "joystick_viewer.html")
open(out, "w", encoding="utf-8").write(html)
print(f"wrote {out} ({len(html) / 1e6:.1f} MB)")
