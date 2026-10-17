#!/usr/bin/env python3
"""Sample Decorly branded pins: real photo top, burgundy band + cream serif title."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 1500
IMG_H = 940
BURG_DEEP = (103, 34, 47)
BURG = (142, 47, 63)
CREAM = (250, 243, 230)
GOLD = (217, 164, 65)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines

def make_pin(img_path, title, out_path):
    img = Image.open(img_path).convert("RGB")
    # cover-fit to 1000x940
    r = max(W / img.width, IMG_H / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - W) // 2; y = (img.height - IMG_H) // 2
    img = img.crop((x, y, x + W, y + IMG_H))

    canvas = Image.new("RGB", (W, H), BURG_DEEP)
    canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    # subtle gradient on band
    band = Image.new("RGB", (W, H - IMG_H))
    bd = ImageDraw.Draw(band)
    for i in range(H - IMG_H):
        t = i / (H - IMG_H)
        bd.line([(0, i), (W, i)],
                fill=tuple(int(BURG_DEEP[c] + (BURG[c] - BURG_DEEP[c]) * t) for c in range(3)))
    canvas.paste(band, (0, IMG_H))

    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(SERIF_B, 62)
    lines = wrap(d, title, font, W - 120)
    line_h = 78
    total = len(lines) * line_h
    ty = IMG_H + (H - IMG_H - total) // 2 - 20
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((W - tw) / 2, ty), ln, font=font, fill=CREAM)
        ty += line_h

    bf = ImageFont.truetype(SERIF_R, 34)
    brand = "decorly.homes"
    bw = d.textlength(brand, font=bf)
    d.text(((W - bw) / 2, H - 78), brand, font=bf, fill=GOLD)
    canvas.save(out_path, quality=92)
    print("saved", out_path)

JOBS = [
    ("assets/halloween-rental-decor-guide/hero.jpg",
     "How to Decorate Your Rental for Halloween on a $50 Budget",
     "social/samples/pin-halloween-rental-50.jpg"),
    ("assets/afrohemian-decor-finds-under-25/hero.jpg",
     "9 Afrohemian Decor Finds Under $25",
     "social/samples/pin-afrohemian-under-25.jpg"),
    ("assets/bedroom-plant-styling-ideas/hero.jpg",
     "12 Bedroom Plant Styling Ideas That Turn Any Room Into a Green Retreat",
     "social/samples/pin-bedroom-plants.jpg"),
]

if __name__ == "__main__":
    import os
    os.makedirs("social/samples", exist_ok=True)
    for img_p, title, out in JOBS:
        make_pin(img_p, title, out)
