#!/usr/bin/env python3
"""Compose out/views/*.png into a spec sheet -> out/joystick_sheet.png"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "out", "views")
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
BG, LINE, FG, MUTED, DIM = "#151517", "#2e2e33", "#ececef", "#9a9aa2", "#f5f5f7"

W, H = 1600, 1800
sheet = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(sheet)
f = lambda size, bold=False: ImageFont.truetype(FONT_B if bold else FONT, size)


def panel(name, x, y, w, h, title, sub=None):
    img = Image.open(os.path.join(V, f"{name}.png")).convert("RGB")
    if img.size != (w, h):
        img = img.resize((w, h), Image.LANCZOS)
    sheet.paste(img, (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=LINE, width=2)
    d.text((x + 18, y + 14), title, fill=FG, font=f(22, True))
    if sub:
        d.text((x + 18, y + 44), sub, fill=MUTED, font=f(15))


def arrow_line(p0, p1, color=DIM, width=2, head=8):
    d.line([p0, p1], fill=color, width=width)
    import math
    for a, b in ((p0, p1), (p1, p0)):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for s in (+0.5, -0.5):
            d.line([b, (b[0] - head * math.cos(ang + s), b[1] - head * math.sin(ang + s))], fill=color, width=width)


def label(xy, text, size=16, anchor="mm", color=DIM):
    d.text(xy, text, fill=color, font=f(size), anchor=anchor)


# ---------------- layout ----------------
panel("hero", 0, 0, 600, 900, "8 BUTTON JOYSTICK")
d.text((18, 44), "TOP ROW TIPPED 45° TO THE THUMB", fill=MUTED, font=f(15))
d.text((18, 64), "BOTTOM ROW FLAT", fill=MUTED, font=f(15))

panel("front", 600, 0, 500, 450, "FRONT VIEW")
panel("top", 1100, 0, 500, 450, "TOP VIEW")
panel("left", 600, 450, 333, 450, "LEFT SIDE VIEW")
panel("right", 933, 450, 333, 450, "RIGHT SIDE VIEW")
panel("back", 1266, 450, 334, 450, "BACK VIEW")

panel("button", 0, 900, 500, 450, "BUTTON DETAIL")
panel("thumb", 500, 900, 600, 450, "THUMB SIDE VIEW", "top row overhangs the thumb")

# ---- dimensions: 100 mm on the front view (ortho: 500 px / 140 mm, target x=0,z=165) ----
import json, math
import numpy as np
meta = json.load(open(os.path.join(HERE, "out", "meta.json")))
T = np.array(meta["head_transform"])
ppm = 500 / 140.0
ox, oy = 600 + 250, 0 + 225
bx0, bx1 = ox - 50 * ppm, ox + 50 * ppm
top_px = oy - (max(T[2, 3] + T[2, 2] * 70 + T[2, 1] * 24, T[2, 3] + T[2, 2] * 70 + T[2, 1] * -48) + 6 - 165) * ppm
yd = top_px - 30
d.line([(bx0, top_px - 4), (bx0, yd - 8)], fill=MUTED, width=1)
d.line([(bx1, top_px - 4), (bx1, yd - 8)], fill=MUTED, width=1)
arrow_line((bx0, yd), (bx1, yd))
label((ox, yd - 16), "100 mm", 18)


# ---- left side view helpers (ortho: 333 px / 130 mm, target y=-20,z=140; screen right = -Y) ----
def left_view_px(local_yz):
    """head-local (y, z) -> pixel in the LEFT SIDE VIEW panel."""
    p = T @ np.array([0.0, local_yz[0], local_yz[1], 1.0])
    ppm = 333 / 130.0
    return (600 + 166.5 - (p[1] + 20) * ppm, 450 + 225 - (p[2] - 140) * ppm)


# 70 mm panel height, measured along the head behind the back face
a, b = left_view_px((24 + 10, 0)), left_view_px((24 + 10, 70))
a0, b0 = left_view_px((24 + 2, 0)), left_view_px((24 + 2, 70))
d.line([a0, (a[0] - 8 * (a[0] - a0[0]) / abs(a[0] - a0[0] + 1e-9), a[1])], fill=MUTED, width=1)
d.line([b0, (b[0] - 8 * (b[0] - b0[0]) / abs(b[0] - b0[0] + 1e-9), b[1])], fill=MUTED, width=1)
arrow_line(a, b)
label(((a[0] + b[0]) / 2 - 30, (a[1] + b[1]) / 2), "70 mm", 17, anchor="rm")

# 45 deg between the flat face and the overhanging top-row face
c = left_view_px((-24, 46))
up = left_view_px((-24, 46 + 30))
sl = left_view_px((-24 - 30 * 0.7071, 46 + 30 * 0.7071))
d.line([c, up], fill=MUTED, width=1)
d.line([c, sl], fill=MUTED, width=1)
r = 30
ang_up = math.degrees(math.atan2(up[1] - c[1], up[0] - c[0]))
ang_sl = math.degrees(math.atan2(sl[1] - c[1], sl[0] - c[0]))
lo, hi = sorted((ang_up, ang_sl))
if hi - lo > 180:
    lo, hi = hi, lo + 360
d.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r], lo, hi, fill=DIM, width=2)
mid = math.radians((lo + hi) / 2)
label((c[0] + (r + 22) * math.cos(mid), c[1] + (r + 22) * math.sin(mid)), "45°", 18)

# ---- button detail dims ----
label((250, 900 + 420), "Ø10 mm cap · 8 mm tall · Ø14 bezel · fits 6×6×8 mm tactile switch", 15, color=MUTED)

# ---- features panel ----
x, y = 1100, 900
d.rectangle([x, y, W - 1, y + 449], outline=LINE, width=2)
d.text((x + 18, y + 14), "FEATURES", fill=FG, font=f(22, True))
feat = [
    "8 momentary tactile push buttons (6×6×8 mm)",
    "Panel faces the user, tilted 10° down to the thumb",
    "Top row overhangs, tipped 45° towards the user",
    "Bottom row flat at 0° on the front face",
    "Ergonomic curved grip, rounded head (R6 edges)",
    "Designed for FDM printing, 3 mm shell walls",
    "M4 countersunk mounting: 4× base, 4× back plate",
    "100 × 70 mm button panel, Ø8 mm wiring channel",
    "Rear access plate on 4 M4 screw bosses",
]
for i, t in enumerate(feat):
    d.text((x + 24, y + 58 + i * 34), "•", fill=FG, font=f(17))
    d.text((x + 44, y + 58 + i * 34), t, fill=FG, font=f(17))
d.text((x + 18, y + 410), "Overall: 100 × 109 × 198 mm (base plate Ø72)", fill=MUTED, font=f(15))

# ---- exploded + parts panel ----
panel("exploded", 0, 1350, 700, 450, "EXPLODED VIEW", "back plate and caps lifted")
x, y = 700, 1350
d.rectangle([x, y, W - 1, y + 449], outline=LINE, width=2)
d.text((x + 18, y + 14), "PRINTABLE PARTS (STL)", fill=FG, font=f(22, True))
rows = [
    ("joystick_body.stl", "1×", "head + grip + base, one piece. Print upright on the base; supports under the head."),
    ("joystick_back_plate.stl", "1×", "84 × 54 × 3 mm, 4× M4 countersunk. Print flat."),
    ("joystick_button_cap.stl", "8×", "Ø10 × 8 mm head, Ø9.8 stem, Ø3.6 plunger socket. Print head down."),
    ("joystick_assembly.stl", "—", "everything assembled, preview only."),
]
yy = y + 60
for name, qty, desc in rows:
    d.text((x + 24, yy), name, fill=DIM, font=f(16, True))
    d.text((x + 260, yy), qty, fill=FG, font=f(16))
    d.text((x + 300, yy), desc, fill=MUTED, font=f(14))
    yy += 40
notes = [
    "Hardware: 8× 6×6×8 mm tactile switches, 8× M4×8 countersunk screws (4 base, 4 plate),",
    "M4 tap or heat-set inserts in the four Ø3.3 bosses, cable through the Ø8 grip channel.",
    "Suggested print: 0.2 mm layers, 3 walls, 20 % infill, PETG or ABS for the grip.",
    "Model source: build_joystick.py (parametric, trimesh + manifold). Edit, re-run, re-slice.",
]
for i, t in enumerate(notes):
    d.text((x + 24, yy + 16 + i * 26), t, fill=MUTED, font=f(14))

# outer grid lines
for xx in (600, 1100):
    d.line([(xx, 0), (xx, 900)], fill=LINE, width=2)

out = os.path.join(HERE, "out", "joystick_sheet.png")
sheet.save(out, optimize=True)
print("wrote", out)
