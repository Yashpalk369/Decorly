"""Decorly HTML templates. All pages share header/nav/footer and SEO head blocks."""
import html
import json
import os
import config

def esc(s):
    return html.escape(s or "", quote=True)

def head(title, description, path, og_type="website", extra_head=""):
    """Full <head> with SEO, OG, Twitter, canonical."""
    url = config.SITE_URL + path
    ga = ""
    if getattr(config, "GA_MEASUREMENT_ID", ""):
        mid = config.GA_MEASUREMENT_ID
        ga = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={mid}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{mid}');
</script>
"""
    return f"""{ga}<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:site_name" content="{esc(config.SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:type" content="{og_type}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<link rel="stylesheet" href="/style.css">
<link rel="icon" type="image/png" href="/assets/logo.png">
<link rel="apple-touch-icon" href="/assets/logo.png">
<link rel="alternate" type="application/rss+xml" title="{esc(config.SITE_NAME)} RSS" href="{esc(config.SITE_URL)}/feed.xml">
{extra_head}"""

def header(active=""):
    def link(path, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{path}"{cls}>{label}</a>'
    return f"""<header class="site-header"><nav class="nav" aria-label="Main navigation">
<a class="brand" href="/"><img class="brand-logo" src="/assets/logo.png" alt="Decorly logo" width="36" height="36">Decorly<small>{esc(config.TAGLINE)}</small></a>
<div class="nav-links">
{link("/", "Home", "home")}
{link("/small-spaces/", "Small Spaces", "small-spaces")}
{link("/rental-friendly/", "Rental-Friendly", "rental-friendly")}
{link("/greenery-decor/", "Plants & Greenery", "greenery-decor")}
{link("/about/", "About", "about")}
</div></nav></header>"""

def footer():
    return f"""<footer class="site-footer"><div class="footer-inner">
<div><div class="footer-brand"><img class="brand-logo" src="/assets/logo.png" alt="Decorly logo" width="30" height="30">Decorly</div>
<p style="font-size:14.5px;margin-top:10px;max-width:280px">{esc(config.TAGLINE)}. Practical, budget-first decorating ideas for renters and small-space dwellers.</p></div>
<div><h4>Browse</h4>
<a href="/small-spaces/">Small Space Decor</a>
<a href="/rental-friendly/">Rental-Friendly Decor</a>
<a href="/greenery-decor/">Plants &amp; Greenery</a>
<a href="/about/">About</a></div>
<div><h4>Site</h4>
<a href="/feed.xml">RSS Feed</a>
<a href="/privacy-policy/">Privacy Policy</a>
<a href="/sitemap.xml">Sitemap</a></div>
</div><div class="footer-bottom">
<span>&copy; 2026 {esc(config.SITE_NAME)}. All rights reserved.</span>
<span>Made for renters, by renters.</span>
</div></footer>"""

def page(title, description, path, body, active="", og_type="website", extra_head="", ld_blocks=None):
    """Assemble a complete HTML page."""
    ld = ""
    if ld_blocks:
        for block in ld_blocks:
            ld += '<script type="application/ld+json">\n' + json.dumps(block, indent=2) + "\n</script>\n"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, description, path, og_type, extra_head + ld)}
</head>
<body>
{header(active)}
<main>
{body}
</main>
{footer()}
</body>
</html>
"""

def breadcrumb_ld(crumbs):
    """crumbs: list of (name, path) — first is always Home."""
    items = []
    for i, (name, path) in enumerate(crumbs, start=1):
        items.append({"@type": "ListItem", "position": i,
                      "name": name, "item": config.SITE_URL + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": items}

def article_ld(post):
    """post: dict with title, description, date, slug."""
    return {"@context": "https://schema.org", "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["description"],
            "image": f"{config.SITE_URL}/assets/{post['slug']}/hero.jpg",
            "datePublished": post["date"],
            "dateModified": post["date"],
            "author": {"@type": "Organization", "name": config.SITE_NAME,
                       "url": config.SITE_URL},
            "publisher": {"@type": "Organization", "name": config.SITE_NAME,
                          "url": config.SITE_URL}}

def faq_ld(faq_items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faq_items]}

def hero_art(post, big=True):
    """Real hero <img> when assets/<slug>/hero.jpg exists (copied to site/ at build), else CSS placeholder."""
    slug = post["slug"]
    hero_src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", slug, "hero.jpg")
    if os.path.exists(hero_src):
        cls = "hero-img" if big else "thumb-img"
        return (f'<img class="{cls}" src="/assets/{esc(slug)}/hero.jpg" '
                f'alt="{esc(post["title"])}" loading="lazy">')
    theme = post.get("hero", "hero-terra")
    motif = post.get("motif", "🏠")
    title_html = f'<div class="hero-title">{esc(post["title"])}</div>' if big else ""
    return f"""<!-- HERO IMAGE SLOT: replace this entire div with <img src="/assets/{post['slug']}/hero.jpg" alt="..."> once the real hero image is ready -->
<div class="hero-art {esc(theme)}" role="img" aria-label="{esc(post['title'])}">
<span class="motif">{esc(motif)}</span>{title_html}
</div>"""

def post_card(post):
    return f"""<a class="post-card" href="/{post['slug']}/">
<div class="thumb">{hero_art(post, big=False)}</div>
<div class="body">
<span class="kicker">{esc(post['cat_name'])}</span>
<h3>{esc(post['title'])}</h3>
<p>{esc(post['description'])}</p>
<span class="date">{esc(post['date_pretty'])}</span>
</div></a>"""

def post_card_compact(post):
    """Pinterest-style card: image + kicker + title only, no paragraph."""
    return f"""<a class="post-card pin-card" href="/{post['slug']}/">
<div class="thumb">{hero_art(post, big=False)}</div>
<div class="body">
<span class="kicker">{esc(post['cat_name'])}</span>
<h3>{esc(post['title'])}</h3>
<span class="date">{esc(post['date_pretty'])}</span>
</div></a>"""

def cat_visual_card(slug, cat, img_slug, n):
    """Image-led category card: real photo with overlaid label."""
    return f"""<a class="cat-visual" href="/{slug}/">
<img src="/assets/{esc(img_slug)}/hero.jpg" alt="{esc(cat['name'])}" loading="lazy">
<span class="cat-visual-label"><strong>{esc(cat['name'])}</strong>
<em>{n} idea{'s' if n != 1 else ''} →</em></span></a>"""
