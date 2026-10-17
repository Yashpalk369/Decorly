#!/usr/bin/env python3
"""Reusable Decorly branded static pin builder.

1000x1500 pin: real post photo on top (1000x940), burgundy gradient band
at bottom with the post title in large cream serif, small gold
"decorly.homes" branding at the very bottom.

No AI-generated imagery — pass real post photos from ~/workspace/decorly/assets/.

Usage:
    python3 build-decorly-pin.py --image <photo> --title "<title>" --output <out.jpg>
    python3 build-decorly-pin.py --jobs jobs.json   # [{"image","title","output"}, ...]

Pinterest SEO rule enforced: title must be <= 100 chars (warns otherwise).
"""
import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
IMG_H = 940
BURG_DEEP = (103, 34, 47)   # #67222f
BURG = (142, 47, 63)        # #8e2f3f
CREAM = (250, 243, 230)     # #faf3e6
GOLD = (217, 164, 65)       # #d9a441

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-SemiBold.ttf")
SERIF_R = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")

BRAND = "decorly.homes"
MAX_TITLE = 100


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def make_pin(img_path, title, out_path):
    if len(title) > MAX_TITLE:
        print(f"WARNING: title is {len(title)} chars (> {MAX_TITLE}): {title!r}",
              file=sys.stderr)

    img = Image.open(img_path).convert("RGB")
    # cover-fit to 1000x940
    r = max(W / img.width, IMG_H / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - W) // 2
    y = (img.height - IMG_H) // 2
    img = img.crop((x, y, x + W, y + IMG_H))

    canvas = Image.new("RGB", (W, H), BURG_DEEP)
    canvas.paste(img, (0, 0))

    # burgundy gradient band
    band = Image.new("RGB", (W, H - IMG_H))
    bd = ImageDraw.Draw(band)
    for i in range(H - IMG_H):
        t = i / (H - IMG_H)
        bd.line(
            [(0, i), (W, i)],
            fill=tuple(int(BURG_DEEP[c] + (BURG[c] - BURG_DEEP[c]) * t) for c in range(3)),
        )
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
    bw = d.textlength(BRAND, font=bf)
    d.text(((W - bw) / 2, H - 78), BRAND, font=bf, fill=GOLD)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    canvas.save(out_path, quality=92)
    print(f"saved {out_path}  ({len(lines)} title lines, {len(title)} chars)")


def main():
    ap = argparse.ArgumentParser(description="Build Decorly branded 1000x1500 pins.")
    ap.add_argument("--image", help="source photo (real post photo only)")
    ap.add_argument("--title", help="pin title, <= 100 chars, keyword-rich")
    ap.add_argument("--output", help="output JPG path")
    ap.add_argument("--jobs", help="JSON file with list of {image, title, output}")
    args = ap.parse_args()

    if args.jobs:
        with open(args.jobs) as f:
            jobs = json.load(f)
        for j in jobs:
            make_pin(j["image"], j["title"], j["output"])
    elif args.image and args.title and args.output:
        make_pin(args.image, args.title, args.output)
    else:
        ap.error("need --image/--title/--output or --jobs")


if __name__ == "__main__":
    main()
