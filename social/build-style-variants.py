#!/usr/bin/env python3
"""Three alternate Decorly pin styles, all in brand colors."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
BURG_DEEP = (103, 34, 47)
BURG = (142, 47, 63)
CREAM = (250, 243, 230)
GOLD = (217, 164, 65)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"

def cover_fit(path, w, h):
    img = Image.open(path).convert("RGB")
    r = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines

def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius, fill=255)
    out = Image.new("RGB", img.size, (0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out

# ---- Style 1: full-bleed cover, title over a solid burgundy scrim ----
def style_cover(img_path, title, out):
    img = cover_fit(img_path, W, H).convert("RGBA")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(SERIF_B, 72)
    lines = wrap(d, title, font, W - 140)
    lh = 88
    ty = H - 160 - len(lines) * lh
    # solid burgundy scrim behind title + pill so text never fights the photo
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rectangle([0, ty - 70, W, H], fill=(103, 34, 47, 205))
    img = Image.alpha_composite(img, scrim).convert("RGB")

    d = ImageDraw.Draw(img)
    for ln in lines:
        d.text((70, ty), ln, font=font, fill=CREAM)
        ty += lh
    # website pill below title: cream badge, burgundy bold text
    f_brand = ImageFont.truetype(SERIF_B, 40)
    brand = "decorly.homes"
    bw = d.textlength(brand, font=f_brand)
    px, py, pad = (W - bw) / 2, ty + 28, 30
    d.rounded_rectangle([px - pad, py - 14, px + bw + pad, py + 58],
                        34, fill=CREAM)
    d.text((px, py), brand, font=f_brand, fill=BURG_DEEP)
    img.save(out, quality=92); print("saved", out)

# ---- Style 2: cream editorial, framed photo, burgundy type ----
def style_editorial(img_path, title, out):
    canvas = Image.new("RGB", (W, H), CREAM)
    photo = rounded(cover_fit(img_path, 880, 880), 36)
    canvas.paste(photo, (60, 60))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(SERIF_B, 58)
    lines = wrap(d, title, font, W - 160)
    lh = 74
    ty = 1020
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((W - tw) / 2, ty), ln, font=font, fill=BURG_DEEP)
        ty += lh
    # gold rule
    ry = ty + 30
    d.line([(W/2 - 60, ry), (W/2 + 60, ry)], fill=GOLD, width=4)
    f_brand = ImageFont.truetype(SERIF_R, 32)
    brand = "decorly.homes"
    bw = d.textlength(brand, font=f_brand)
    d.text(((W - bw) / 2, ry + 26), brand, font=f_brand, fill=BURG)
    canvas.save(out, quality=92); print("saved", out)

# ---- Style 3: burgundy top band, photo below, gold footer ----
def style_topband(img_path, title, out):
    BAND = 560
    canvas = Image.new("RGB", (W, H), BURG_DEEP)
    d = ImageDraw.Draw(canvas)
    for i in range(BAND):
        t = i / BAND
        d.line([(0, i), (W, i)],
               fill=tuple(int(BURG[c] + (BURG_DEEP[c] - BURG[c]) * t) for c in range(3)))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(SERIF_B, 60)
    lines = wrap(d, title, font, W - 140)
    lh = 76
    ty = (BAND - len(lines) * lh) // 2
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((W - tw) / 2, ty), ln, font=font, fill=CREAM)
        ty += lh
    photo = cover_fit(img_path, W, H - BAND - 90)
    canvas.paste(photo, (0, BAND))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, H - 90, W, H], fill=GOLD)
    f_brand = ImageFont.truetype(SERIF_B, 34)
    brand = "decorly.homes"
    bw = d.textlength(brand, font=f_brand)
    d.text(((W - bw) / 2, H - 90 + (90 - 34) // 2 - 4), brand, font=f_brand, fill=BURG_DEEP)
    canvas.save(out, quality=92); print("saved", out)

JOBS = [
    ("assets/halloween-rental-decor-guide/hero.jpg",
     "How to Decorate Your Rental for Halloween on a $50 Budget"),
    ("assets/afrohemian-decor-finds-under-25/hero.jpg",
     "9 Afrohemian Decor Finds Under $25"),
    ("assets/bedroom-plant-styling-ideas/hero.jpg",
     "12 Bedroom Plant Styling Ideas That Turn Any Room Into a Green Retreat"),
]
NAMES = ["halloween", "afrohemian", "bedroom-plants"]

if __name__ == "__main__":
    import os
    os.makedirs("social/samples", exist_ok=True)
    for (img_p, title), name in zip(JOBS, NAMES):
        style_cover(img_p, title, f"social/samples/style1-cover-{name}.jpg")
        style_editorial(img_p, title, f"social/samples/style2-editorial-{name}.jpg")
        style_topband(img_p, title, f"social/samples/style3-topband-{name}.jpg")
