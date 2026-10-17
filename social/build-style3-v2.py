#!/usr/bin/env python3
"""Style 3 v2: burgundy top band, rich title (italic gold accent + underline),
photo below, CREAM footer with burgundy brand text."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
BURG_DEEP = (103, 34, 47)
BURG = (142, 47, 63)
CREAM = (250, 243, 230)
GOLD = (240, 199, 110)  # champagne gold — brighter for text on burgundy

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-SemiBold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
DISPLAY_I = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-BlackItalic.ttf"

def cover_fit(path, w, h):
    img = Image.open(path).convert("RGB")
    r = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def layout_runs(d, segments, max_w):
    words = []
    for text, font, fill, accent in segments:
        for w_ in text.split():
            words.append((w_, font, fill, accent,
                          d.textlength(w_ + " ", font=font),
                          d.textlength(w_, font=font)))
    lines, cur, cur_w = [], [], 0
    for item in words:
        if cur and cur_w + item[4] > max_w:
            lines.append(cur); cur, cur_w = [], 0
        cur.append(item); cur_w += item[4]
    if cur:
        lines.append(cur)
    return lines

def style_topband_v2(img_path, eyebrow, segments, out):
    BAND, FOOT = 600, 96
    canvas = Image.new("RGB", (W, H), BURG_DEEP)
    d = ImageDraw.Draw(canvas)
    for i in range(BAND):
        t = i / BAND
        d.line([(0, i), (W, i)],
               fill=tuple(int(BURG[c] + (BURG_DEEP[c] - BURG[c]) * t) for c in range(3)))
    d = ImageDraw.Draw(canvas)

    # eyebrow, letterspaced gold
    f_eye = ImageFont.truetype(SERIF_R, 30)
    eb = " ".join(list(eyebrow.upper()))
    bw = d.textlength(eb, font=f_eye)
    d.text(((W - bw) / 2, 52), eb, font=f_eye, fill=GOLD)

    f_main = ImageFont.truetype(SERIF_B, 58)
    f_acc = ImageFont.truetype(DISPLAY_I, 66)
    segs = [(t, f_main if s == "m" else f_acc,
             CREAM if s == "m" else GOLD, s == "a") for t, s in segments]
    lines = layout_runs(d, segs, W - 150)
    lh = 82
    ty = 130 + (BAND - 130 - len(lines) * lh) // 2
    for line in lines:
        total = sum(w[4] for w in line)
        x = (W - total) / 2
        # x position of each word
        xs, cx = [], x
        for w_ in line:
            xs.append(cx); cx += w_[4]
        # cream highlighter behind consecutive accent words
        i = 0
        while i < len(line):
            if line[i][3]:
                j = i
                while j < len(line) and line[j][3]:
                    j += 1
                x0 = xs[i] - 10
                x1 = xs[j - 1] + line[j - 1][5] + 10
                # sharp selection-style block, tight like highlighted text
                d.rectangle([x0, ty - 6, x1, ty + 74], fill=CREAM)
                i = j
            else:
                i += 1
        # words on top — accent words in burgundy
        cx = x
        for w_, font, fill, accent, adv, bare in line:
            d.text((cx, ty), w_, font=font, fill=BURG_DEEP if accent else fill)
            cx += adv
        ty += lh

    photo = cover_fit(img_path, W, H - BAND - FOOT)
    canvas.paste(photo, (0, BAND))

    # cream footer, burgundy brand
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, H - FOOT, W, H], fill=CREAM)
    f_brand = ImageFont.truetype(SERIF_B, 34)
    brand = "decorly.homes"
    bw = d.textlength(brand, font=f_brand)
    d.text(((W - bw) / 2, H - FOOT + (FOOT - 40) // 2), brand, font=f_brand, fill=BURG_DEEP)
    canvas.save(out, quality=92); print("saved", out)

JOBS = [
    ("assets/halloween-rental-decor-guide/hero.jpg", "SEASONAL DECOR",
     [("How to Decorate Your Rental for Halloween on a ", "m"), ("$50 Budget", "a")],
     "social/samples/style3v2-topband-halloween.jpg"),
    ("assets/afrohemian-decor-finds-under-25/hero.jpg", "DECOR FINDS",
     [("9 Afrohemian Decor Finds ", "m"), ("Under $25", "a")],
     "social/samples/style3v2-topband-afrohemian.jpg"),
    ("assets/bedroom-plant-styling-ideas/hero.jpg", "PLANT STYLING",
     [("12 Bedroom Plant Styling Ideas That Turn Any Room Into a ", "m"), ("Green Retreat", "a")],
     "social/samples/style3v2-topband-bedroom-plants.jpg"),
]

if __name__ == "__main__":
    for img_p, eyebrow, segs, out in JOBS:
        style_topband_v2(img_p, eyebrow, segs, out)
