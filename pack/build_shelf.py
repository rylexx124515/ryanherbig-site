#!/usr/bin/env python3
"""The pack shelf image on the home page: the six reel posters as phone cards on a light ground,
alternating offsets, soft shadow. Written to assets/img/pack-shelf.jpg (1600 x 900).

Reads the posters from pack/assets/posters/ in the order the pack page lists the reels, so run
it after the posters change. Run: ../../.venv/bin/python build_shelf.py (needs Pillow)
"""
import pathlib
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
POSTERS = HERE / "assets" / "posters"
OUT = HERE.parent / "assets" / "img" / "pack-shelf.jpg"
ORDER = ["V5", "V4", "V2", "V3", "V1"]      # same order as the pack page

W, H = 1600, 900
CW, CH = 236, 420                                  # one phone card
GAP = 30
RADIUS = 14
ground = Image.new("RGB", (W, H), (244, 244, 246))

total = len(ORDER) * CW + (len(ORDER) - 1) * GAP
x = (W - total) // 2
for i, key in enumerate(ORDER):
    y = (H - CH) // 2 + (-32 if i % 2 == 0 else 32)
    card = Image.open(POSTERS / f"{key}.jpg").convert("RGB").resize((CW, CH), Image.LANCZOS)
    mask = Image.new("L", (CW, CH), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, CW - 1, CH - 1), RADIUS, fill=255)
    # shadow: a blurred dark rounded rect, offset down
    sh = Image.new("RGBA", (CW + 80, CH + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 52, 40 + CW, 52 + CH), RADIUS, fill=(20, 24, 40, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    ground.paste(sh, (x - 40, y - 40), sh)
    ground.paste(card, (x, y), mask)
    x += CW + GAP

OUT.parent.mkdir(parents=True, exist_ok=True)
ground.save(OUT, quality=86, optimize=True, progressive=True)
print("wrote", OUT, ground.size)
