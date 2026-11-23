#!/usr/bin/env python3
"""Decorly pin builder, style v2 (sample).

Differences vs build-decorly-pin.py (v1):
- Slimmer bottom band (photo 1000x1080, band 420px) so the photo dominates.
- Short on-image title only (no SEO keyword tail), set larger (72px).
- Gold hook badge top-left on the photo (e.g. UNDER $25, RENTAL-FRIENDLY).
- Branding pulled up directly under the title instead of the very bottom.
- Optional tighter zoom crop (default 0.85 of source width) so the subject
  fills the frame.

Usage:
    python3 build-decorly-pin-v2.py --image <photo> --title "<short title>" \
        --badge "RENTAL-FRIENDLY" --output <out.jpg>
"""
import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
IMG_H = 1080
BURG_DEEP = (103, 34, 47)   # #67222f
BURG = (142, 47, 63)        # #8e2f3f
CREAM = (250, 243, 230)     # #faf3e6
GOLD = (217, 164, 65)       # #d9a441

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-SemiBold.ttf")
SERIF_R = os.path.join(FONT_DIR, "NotoSerif-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")

BRAND = "decorly.homes"


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


def make_pin(img_path, title, badge, out_path, zoom=0.85):
    img = Image.open(img_path).convert("RGB")
    # tighter crop: keep the central `zoom` fraction of the width, full height,
    # so the subject fills the frame more than a plain center cover-fit.
    zw = int(img.width * zoom)
    x0 = (img.width - zw) // 2
    img = img.crop((x0, 0, x0 + zw, img.height))
    r = max(W / img.width, IMG_H / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - W) // 2
    y = (img.height - IMG_H) // 2
    img = img.crop((x, y, x + W, y + IMG_H))

    canvas = Image.new("RGB", (W, H), BURG_DEEP)
    canvas.paste(img, (0, 0))

    # burgundy gradient band (slimmer than v1)
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

    # gold hook badge, top-left on the photo
    if badge:
        try:
            bf_badge = ImageFont.truetype(SANS_B, 30)
        except OSError:
            bf_badge = ImageFont.truetype(SERIF_B, 30)
        pad_x, pad_y = 28, 14
        tw = d.textlength(badge, font=bf_badge)
        bx, by = 36, 36
        d.rounded_rectangle(
            [bx, by, bx + tw + pad_x * 2, by + 30 + pad_y * 2],
            radius=28, fill=GOLD,
        )
        d.text((bx + pad_x, by + pad_y - 2), badge, font=bf_badge, fill=BURG_DEEP)

    # short title, larger type; shrink until it fits 4 lines so the
    # branding below never gets clipped off the bottom of the band
    # (a 5-line title at 72px overflows the 420px band and loses it).
    size = 72
    while True:
        font = ImageFont.truetype(SERIF_B, size)
        lines = wrap(d, title, font, W - 120)
        if len(lines) <= 4 or size <= 52:
            break
        size -= 4
    line_h = size + 16
    total = len(lines) * line_h
    brand_h = 44
    ty = IMG_H + (H - IMG_H - total - brand_h) // 2
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((W - tw) / 2, ty), ln, font=font, fill=CREAM)
        ty += line_h

    # branding directly under the title, bold
    bf = ImageFont.truetype(SERIF_B, 32)
    bw = d.textlength(BRAND, font=bf)
    d.text(((W - bw) / 2, ty + 8), BRAND, font=bf, fill=GOLD)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    canvas.save(out_path, quality=92)
    print(f"saved {out_path} ({len(lines)} title lines, badge={badge!r})")


def main():
    ap = argparse.ArgumentParser(description="Build Decorly branded pins, style v2.")
    ap.add_argument("--image", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--badge", default="")
    ap.add_argument("--output", required=True)
    ap.add_argument("--zoom", type=float, default=0.85)
    args = ap.parse_args()
    make_pin(args.image, args.title, args.badge, args.output, args.zoom)


if __name__ == "__main__":
    main()
