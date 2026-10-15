#!/usr/bin/env python3
"""Build Decorly Pinterest pins (1000x1500) from real post photos.

Layout (adapted from the approved Design B grammar):
  real photo top (1000x940), dark warm band bottom (1000x560) with
  huge cream serif title, small cream category pill on the photo,
  terracotta decorly.homes branding at the bottom of the band.
Two pins per post: pin 1 = hero + exact title, pin 2 = idea photo + keyword variant.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 1500
PHOTO_H = 940
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

CREAM = (250, 246, 240)
PILL = (255, 250, 240)
DARK = (46, 42, 37)          # site ink
TERRA = (194, 109, 75)       # brand terracotta

BASE = os.path.expanduser("~/workspace/decorly")
PINS_DIR = os.path.join(BASE, "pins")
os.makedirs(PINS_DIR, exist_ok=True)

def cover_crop(img, w, h):
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def wrap_title(draw, title, font, max_w):
    words = title.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def fit_font(draw, title, max_w, start, max_lines=3, min_size=52):
    size = start
    while size > min_size:
        f = ImageFont.truetype(SERIF_BOLD, size)
        if len(wrap_title(draw, title, f, max_w)) <= max_lines:
            return f
        size -= 6
    return ImageFont.truetype(SERIF_BOLD, min_size)

def build_pin(photo_path, title, pill, out_path):
    photo = Image.open(photo_path).convert("RGB")
    photo = cover_crop(photo, W, PHOTO_H)
    photo = photo.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=3))

    base = Image.new("RGB", (W, H), DARK)
    base.paste(photo, (0, 0))
    d = ImageDraw.Draw(base)

    # small cream category pill on the photo, top-center
    bf = ImageFont.truetype(SERIF_BOLD, 28)
    tw = d.textlength(pill, font=bf)
    bx0, by0 = (W - tw) / 2 - 56, 64
    bx1, by1 = (W + tw) / 2 + 56, 64 + 28 + 40
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=34, fill=PILL)
    d.text((W / 2, (by0 + by1) / 2), pill, font=bf, fill=DARK, anchor="mm")

    # huge cream title centered in the band
    tf = fit_font(d, title, 880, 112)
    lines = wrap_title(d, title, tf, 880)
    lh = int(tf.size * 1.18)
    band_h = H - PHOTO_H
    y = PHOTO_H + (band_h - lh * len(lines)) / 2 - 20
    for ln in lines:
        d.text((W / 2, y + lh / 2), ln, font=tf, fill=CREAM, anchor="mm")
        y += lh

    # terracotta branding at the very bottom
    brf = ImageFont.truetype(SERIF_BOLD, 38)
    d.text((W / 2, H - 48), "decorly.homes", font=brf, fill=TERRA, anchor="mm")

    base.save(out_path, "JPEG", quality=92)
    return out_path

# (slug, pin-1 title, pin-2 title, pin-2 description seed, pill label)
POSTS = [
    ("15-small-bedroom-ideas-under-100",
     "15 Small Bedroom Ideas Under $100 That Look Expensive",
     "Small Bedroom Ideas on a Budget: 15 Cheap Ways to Look Luxe",
     "SMALL SPACES"),
    ("afrohemian-decor-finds-under-25",
     "9 Afrohemian Decor Finds Under $25 for Small Apartments",
     "Afrohemian Bedroom Decor: 9 Affordable Finds Under $25",
     "SMALL SPACES"),
    ("bedroom-plant-styling-ideas",
     "12 Bedroom Plant Styling Ideas That Turn Any Room Into a Green Retreat",
     "Bedroom Plants Decor: 12 Styling Ideas for a Green Retreat",
     "GREENERY"),
    ("halloween-rental-decor-guide",
     "How to Decorate Your Rental for Halloween on a $50 Budget",
     "Rental Halloween Decorations: $50 Budget Ideas (No Damage)",
     "RENTAL-FRIENDLY"),
    ("low-light-indoor-plants-dark-apartments",
     "10 Low-Light Indoor Plants That Thrive in Dark Apartments",
     "Best Indoor Plants for Dark Apartments: 10 Low-Light Picks",
     "GREENERY"),
    ("no-drill-wall-decor-renters",
     "12 No-Drill Wall Decor Ideas for Renters (Zero Holes, Full Style)",
     "Renter Friendly Wall Decor: 12 No-Drill Ideas, Zero Holes",
     "RENTAL-FRIENDLY"),
    ("renter-friendly-kitchen-upgrades",
     "10 Renter-Friendly Kitchen Upgrades (No Renovation Needed)",
     "Apartment Kitchen Ideas: 10 Renter Upgrades Without Renovation",
     "RENTAL-FRIENDLY"),
    ("small-living-room-storage-hacks",
     "14 Small Living Room Storage Hacks That Don't Look Like Storage",
     "Small Living Room Storage Ideas: 14 Hidden Hacks",
     "SMALL SPACES"),
    ("studio-apartment-layout-ideas",
     "Studio Apartment Layout Ideas That Actually Work (7 Floor Plans)",
     "Studio Apartment Layouts: 7 Floor Plans That Actually Work",
     "SMALL SPACES"),
    ("temporary-wallpaper-renters",
     "Temporary Wallpaper Ideas for Renters: 9 Patterns That Peel Off Clean",
     "Peel and Stick Wallpaper for Renters: 9 Patterns, Zero Damage",
     "RENTAL-FRIENDLY"),
]

def main():
    manifest = []
    ok, fail = 0, []
    for slug, t1, t2, pill in POSTS:
        adir = os.path.join(BASE, "assets", slug)
        p1 = os.path.join(adir, "hero.jpg")
        # second pin: a mid-list idea photo for visual variety
        ideas = sorted(f for f in os.listdir(adir) if f.startswith("idea-") and f.endswith(".jpg"))
        p2 = os.path.join(adir, ideas[len(ideas) // 2])
        for i, (photo, title) in enumerate([(p1, t1), (p2, t2)], start=1):
            out = os.path.join(PINS_DIR, f"{slug}-pin{i}.jpg")
            try:
                assert len(title) <= 100, f"title too long ({len(title)}): {title}"
                build_pin(photo, title, pill, out)
                manifest.append({"slug": slug, "pin": i, "file": out,
                                 "title": title, "pill": pill,
                                 "url": f"https://decorly.homes/{slug}/"})
                ok += 1
                print("OK", os.path.basename(out))
            except Exception as e:
                fail.append((slug, i, str(e)))
                print("FAIL", slug, i, e)
    json.dump(manifest, open(os.path.join(PINS_DIR, "manifest.json"), "w"), indent=1)
    print(f"\n{ok} pins built, {len(fail)} failed")
    if fail:
        sys.exit(1)

if __name__ == "__main__":
    main()
