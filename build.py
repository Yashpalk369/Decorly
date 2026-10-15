#!/usr/bin/env python3
"""Decorly static site builder.

Reads Markdown posts from posts/<slug>.md (frontmatter: title, date, category,
tags, description, hero, motif) and static pages from pages/<slug>.md, then
renders a complete static site into site/:

  site/index.html                  homepage (latest posts + category cards)
  site/<slug>/index.html           one page per post
  site/<category>/index.html       Tier-1 category hubs
  site/<trend>/index.html          Tier-2 trend stubs ("coming soon")
  site/about/index.html            about page
  site/privacy-policy/index.html   privacy policy (needed for ad networks)
  site/sitemap.xml, site/robots.txt, site/feed.xml, site/style.css

Usage:
  python3 build.py          build the site
  python3 build.py --check   build + verify internal links + report word counts

Idempotent: wipes and regenerates site/ on every run.
"""
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime

import config
import templates as T
from markdown import parse as md_parse, word_count

BASE = Path(__file__).resolve().parent
POSTS_DIR = BASE / "posts"
PAGES_DIR = BASE / "pages"
SITE = BASE / "site"

# ---- taxonomy ----
CATEGORIES = {
    "small-spaces": {
        "name": "Small Space Decor",
        "motif": "🏠",
        "title": "Small Space Decor Ideas — Budget Apartment & Bedroom Styling | Decorly",
        "description": "Budget-friendly small space decor ideas: small bedroom makeovers under $100, studio apartment layouts, and storage hacks for tiny living rooms.",
    },
    "rental-friendly": {
        "name": "Rental-Friendly Decor",
        "motif": "🔑",
        "title": "Rental-Friendly Decor Ideas — No-Drill, No-Damage Upgrades | Decorly",
        "description": "Renter-friendly decor upgrades that don't risk your deposit: no-drill wall decor, temporary wallpaper, and kitchen upgrades with zero renovation.",
    },
    "greenery-decor": {
        "name": "Plants & Greenery",
        "motif": "🌿",
        "title": "Indoor Plant Decor Ideas — Bedroom Styling & Low-Light Plants | Decorly",
        "description": "Biophilic decor ideas: bedroom plant styling, low-light indoor plants for dark apartments, and greenery that thrives on a budget.",
    },
}

# Tier-2 trends (Pinterest Predicts 2026) — stub hubs until posts exist.
# ---- frontmatter ----

def read_md(path):
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip().lower()] = v.strip().strip('"').strip("'")
            body = text[end + 4:].lstrip("\n")
    # placeholders
    body = body.replace("{{AMAZON_TAG}}", config.AMAZON_TAG)
    body = body.replace("{{SITE_URL}}", config.SITE_URL)
    return fm, body

def pretty_date(datestr):
    try:
        d = datetime.strptime(datestr, "%Y-%m-%d")
    except ValueError:
        d = datetime.now()
    return d.strftime("%B %-d, %Y"), d

# ---- page builders ----

def build_post(post):
    body_html, faq_items = md_parse(post["body"])
    ld = [T.breadcrumb_ld([("Home", "/"),
                           (post["cat_name"], f"/{post['category']}/"),
                           (post["title"], f"/{post['slug']}/")]),
          T.article_ld(post)]
    if faq_items:
        ld.append(T.faq_ld(faq_items))

    # related posts: same category first, then others
    related = [p for p in ALL_POSTS if p["slug"] != post["slug"]
               and p["category"] == post["category"]]
    related += [p for p in ALL_POSTS if p["slug"] != post["slug"]
                and p["category"] != post["category"]]
    related = related[:3]
    keep = ('<div class="keep-reading"><h2>Keep reading</h2><ul>' +
            "".join(f'<li><a href="/{p["slug"]}/">{T.esc(p["title"])}</a></li>'
                    for p in related) + "</ul></div>")

    disclosure = ('<div class="disclosure"><strong>Affiliate disclosure:</strong> '
                  "Decorly is reader-supported. When you buy through links on "
                  "this page we may earn an affiliate commission at no extra cost to you.</div>")

    body = f"""<article>
<div class="article-head">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo;
<a href="/{post['category']}/">{T.esc(post['cat_name'])}</a> &rsaquo; {T.esc(post['title'])}</nav>
<h1>{T.esc(post['title'])}</h1>
<div class="article-meta">
<a class="kicker" href="/{post['category']}/">{T.esc(post['cat_name'])}</a>
<span>{post['date_pretty']}</span><span>·</span><span>{post['words']:,} words</span>
</div>
<p class="article-dek">{T.esc(post['description'])}</p>
</div>
<div class="article-hero">{T.hero_art(post, big=True)}</div>
<div class="article-body">
{body_html}
{disclosure}
{keep}
</div></article>"""
    return T.page(post["title"] + " | " + config.SITE_NAME,
                  post["description"], f"/{post['slug']}/", body,
                  active=post["category"], og_type="article", ld_blocks=ld)

def build_hub(slug, cat):
    posts = [p for p in ALL_POSTS if p["category"] == slug]
    cards = "\n".join(T.post_card(p) for p in posts)
    body = f"""<div class="wrap"><div class="section">
<div class="section-head"><h2><span style="font-size:30px">{cat['motif']}</span> {T.esc(cat['name'])}</h2></div>
<p style="color:var(--muted);max-width:680px;margin-bottom:28px">{T.esc(cat['description'])}</p>
<div class="post-grid">{cards}</div>
</div></div>"""
    ld = [T.breadcrumb_ld([("Home", "/"), (cat["name"], f"/{slug}/")])]
    return T.page(cat["title"], cat["description"], f"/{slug}/", body,
                  active=slug, ld_blocks=ld)

def build_home():
    latest = ALL_POSTS[:6]
    cards = "\n".join(T.post_card_compact(p) for p in latest)
    # representative real photo per category (hero images, verified to exist)
    cat_img = {
        "small-spaces": "15-small-bedroom-ideas-under-100",
        "rental-friendly": "no-drill-wall-decor-renters",
        "greenery-decor": "bedroom-plant-styling-ideas",
    }
    cat_cards = []
    for slug, cat in CATEGORIES.items():
        n = len([p for p in ALL_POSTS if p["category"] == slug])
        cat_cards.append(T.cat_visual_card(slug, cat, cat_img[slug], n))
    body = f"""<div class="hero"><div class="hero-inner">
<p class="hero-eyebrow">Budget decor for renters &amp; small spaces</p>
<h1>Beautiful homes on a <em>renter's budget</em></h1>
<p>Practical, budget-first decorating ideas for small spaces, rentals, and plant lovers. No renovation required.</p>
<a class="hero-cta" href="#latest">Explore the latest ideas ↓</a>
</div></div>
<div class="wrap">
<div class="section"><div class="section-head"><h2>Start with your space</h2></div>
<div class="cat-visual-grid">{"".join(cat_cards)}</div></div>
<div class="section" id="latest"><div class="section-head"><h2>Latest ideas</h2><a href="/feed.xml">Follow via RSS →</a></div>
<div class="post-grid pin-grid">{cards}</div></div>
</div>"""
    ld = [T.breadcrumb_ld([("Home", "/")]),
          {"@context": "https://schema.org", "@type": "WebSite",
           "name": config.SITE_NAME, "url": config.SITE_URL,
           "description": config.TAGLINE}]
    return T.page(f"{config.SITE_NAME} — {config.TAGLINE}",
                  "Budget-friendly home decor ideas for renters and small-space dwellers: small bedroom makeovers, no-drill upgrades, temporary wallpaper, and indoor plant styling.",
                  "/", body, active="home", ld_blocks=ld)

def build_static_page(slug, fm, body_html):
    body = f"""<div class="wrap"><div class="section" style="max-width:var(--read)">
<h1 style="margin-bottom:20px">{T.esc(fm['title'])}</h1>
<div class="article-body" style="padding:0;max-width:none">{body_html}</div>
</div></div>"""
    ld = [T.breadcrumb_ld([("Home", "/"), (fm["title"], f"/{slug}/")])]
    return T.page(fm["title"] + " | " + config.SITE_NAME,
                  fm.get("description", config.TAGLINE), f"/{slug}/", body,
                  active=slug, ld_blocks=ld)

# ---- feeds ----

def build_sitemap(urls):
    items = "\n".join(
        f'  <url><loc>{config.SITE_URL}{u}</loc><lastmod>{d}</lastmod></url>'
        for u, d in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""

def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {config.SITE_URL}/sitemap.xml
"""

def build_feed(posts):
    items = []
    for p in posts:
        pub = format_datetime(p["dt"].replace(tzinfo=timezone.utc))
        items.append(f"""<item>
<title>{T.esc(p['title'])}</title>
<link>{config.SITE_URL}/{p['slug']}/</link>
<guid>{config.SITE_URL}/{p['slug']}/</guid>
<pubDate>{pub}</pubDate>
<description>{T.esc(p['description'])}</description>
</item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{T.esc(config.SITE_NAME)} — {T.esc(config.TAGLINE)}</title>
<link>{config.SITE_URL}/</link>
<description>Budget-friendly home decor ideas for renters and small-space dwellers.</description>
{''.join(items)}
</channel>
</rss>
"""

# ---- link check ----

def check_links():
    """Verify every internal href/src in site/ resolves to a generated file."""
    pages = {}
    for f in SITE.rglob("*.html"):
        rel = f.relative_to(SITE).as_posix()
        if rel == "index.html":
            url = "/"
        elif rel.endswith("/index.html"):
            url = "/" + rel[:-len("index.html")]
        else:
            url = "/" + rel
        pages[url] = f
    static = {"/style.css": SITE / "style.css", "/feed.xml": SITE / "feed.xml",
              "/sitemap.xml": SITE / "sitemap.xml", "/robots.txt": SITE / "robots.txt"}
    errors = []
    checked = 0
    for url, f in pages.items():
        html_text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'''(?:href|src)="([^"]+)"''', html_text):
            link = m.group(1)
            if link.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            checked += 1
            target = link.split("#")[0].split("?")[0] or "/"
            if target in pages or target in static:
                continue
            # allow asset dirs (hero images land here later)
            if target.startswith("/assets/"):
                continue
            errors.append(f"{url} -> {link}")
    print(f"link check: {checked} internal links checked, {len(errors)} broken")
    for e in errors:
        print("  BROKEN:", e)
    return not errors

# ---- main ----

ALL_POSTS = []

def main():
    global ALL_POSTS
    # load posts
    for path in sorted(POSTS_DIR.glob("*.md")):
        fm, body = read_md(path)
        slug = path.stem
        date_pretty, dt = pretty_date(fm.get("date", "2026-10-14"))
        cat = fm.get("category", "")
        ALL_POSTS.append({
            "slug": slug, "title": fm.get("title", slug),
            "date": fm.get("date", "2026-10-14"),
            "date_pretty": date_pretty, "dt": dt,
            "category": cat, "cat_name": CATEGORIES.get(cat, {}).get("name", cat),
            "tags": [t.strip() for t in fm.get("tags", "").split(",") if t.strip()],
            "description": fm.get("description", ""),
            "hero": fm.get("hero", "hero-terra"),
            "motif": fm.get("motif", "🏠"),
            "body": body, "words": word_count(body),
        })
    ALL_POSTS.sort(key=lambda p: p["date"], reverse=True)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    urls = []  # (path, lastmod)
    def write(path, content):
        full = SITE / path.lstrip("/")
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")

    # posts
    for p in ALL_POSTS:
        write(f"/{p['slug']}/index.html", build_post(p))
        urls.append((f"/{p['slug']}/", p["date"]))
        print(f"  post: /{p['slug']}/  ({p['words']:,} words)")
    # homepage
    write("/index.html", build_home()); urls.append(("/", ALL_POSTS[0]["date"] if ALL_POSTS else "2026-10-14"))
    # category hubs
    for slug, cat in CATEGORIES.items():
        write(f"/{slug}/index.html", build_hub(slug, cat))
        urls.append((f"/{slug}/", "2026-10-14"))
    # static pages
    for path in sorted(PAGES_DIR.glob("*.md")):
        fm, body = read_md(path)
        body_html, _ = md_parse(body)
        write(f"/{path.stem}/index.html", build_static_page(path.stem, fm, body_html))
        urls.append((f"/{path.stem}/", fm.get("date", "2026-10-14")))
    # feeds & meta
    write("/sitemap.xml", build_sitemap(urls))
    write("/robots.txt", build_robots())
    write("/feed.xml", build_feed(ALL_POSTS))
    shutil.copy(BASE / "style.css", SITE / "style.css")
    # hero images: assets/<slug>/hero.jpg -> site/assets/<slug>/hero.jpg
    assets_dir = BASE / "assets"
    if assets_dir.is_dir():
        for d in sorted(assets_dir.iterdir()):
            if not d.is_dir():
                continue
            for asset in sorted(d.glob("*.jpg")):
                dest = SITE / "assets" / d.name / asset.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(asset, dest)
                print(f"  asset: /assets/{d.name}/{asset.name}")
    logo = BASE / "assets" / "logo.png"
    if logo.is_file():
        dest = SITE / "assets" / "logo.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(logo, dest)
        print("  logo: /assets/logo.png")
    print(f"built {len(urls)} pages -> {SITE}")

    if "--check" in sys.argv:
        ok = check_links()
        total_words = sum(p["words"] for p in ALL_POSTS)
        print(f"posts: {len(ALL_POSTS)}, total words: {total_words:,}")
        for p in ALL_POSTS:
            flag = "OK " if p["words"] >= 1000 else "SHORT"
            print(f"  [{flag}] {p['slug']}: {p['words']:,} words")
        sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
