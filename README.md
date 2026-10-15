# Decorly — static blog scaffold

A complete static home-decor blog for the domain **decorly.homes** (not bought yet —
the site is fully working before the domain exists). Brand: *Decorly — Beautiful
homes on a renter's budget.*

**Stack:** Python 3 (stdlib only) + Markdown posts → static HTML. Zero hosting cost
via GitHub + Vercel. No build tools, no frameworks, no backend.

## What's inside

```
decorly/
├── build.py            # the site builder (run it after any content change)
├── config.py           # ← SITE_URL, AMAZON_TAG, contact email (change these)
├── markdown.py         # hand-rolled Markdown → HTML parser (stdlib only)
├── templates.py        # shared header/nav/footer, SEO head, JSON-LD helpers
├── style.css           # the entire design (copied to site/ on build)
├── posts/              # 8 launch posts (<slug>.md with frontmatter)
├── pages/              # about.md, privacy-policy.md
├── assets/<slug>/      # empty dirs awaiting real hero images
├── site/               # generated output (deploy this) — do not edit by hand
└── README.md
```

**Generated site (18 pages):** homepage, 8 posts, 3 Tier-1 category hubs
(`/small-spaces/`, `/rental-friendly/`, `/greenery-decor/`), 4 Tier-2 trend stubs
with "coming soon" + trend data, about, privacy policy, `sitemap.xml`,
`robots.txt`, `feed.xml` (RSS).

**SEO on every page:** keyword-targeted title + meta description, Open Graph +
Twitter cards, canonical URL, breadcrumb JSON-LD. Posts also get Article
(`BlogPosting`) JSON-LD and FAQ JSON-LD (auto-extracted from the FAQ section).

## Deploy — GitHub + Vercel (do this once)

1. **Commit & push**
   ```bash
   cd ~/workspace/decorly
   git init
   git add -A
   git commit -m "Decorly launch: 8 posts, scaffold v1"
   # create an empty repo named `decorly` on github.com (no README),
   # then:
   git remote add origin git@github.com:<your-username>/decorly.git
   git branch -M main
   git push -u origin main
   ```

2. **Connect Vercel**
   - vercel.com → Add New Project → import the `decorly` repo
   - Framework preset: **Other**. Build command: **empty** (leave blank).
   - Output directory: **`site`**
   - Deploy. You'll get a `decorly.vercel.app` URL — the site works fully on it.

3. **Buy the domain & point DNS** (after buying decorly.homes, ~$5/yr at Spaceship)
   - In Vercel: project → Settings → Domains → add `decorly.homes` and `www.decorly.homes`
   - Vercel shows the DNS records to add. At your registrar:
     - `A` record `@` → `76.76.21.21` (Vercel's IP — confirm the exact value Vercel shows)
     - `CNAME` record `www` → `cname.vercel-dns.com`
   - Wait for DNS to propagate (minutes to a few hours), Vercel auto-issues SSL.

4. **Set the Amazon tag** — in `config.py`, replace `AMAZON_TAG = "decorly-20"`
   with your real Amazon Associates tag after approval. Rebuild + push.

5. **Add real hero images** — each post page has an HTML comment
   `<!-- HERO IMAGE SLOT: /assets/<slug>/hero.jpg -->`. Generate or photograph a
   1200×630 JPG per post, save as `assets/<slug>/hero.jpg`, rebuild, push.
   (Also add it to the page's frontmatter later if you extend the builder to use it.)

## Publishing workflow (every new post)

1. Write `posts/<your-slug>.md`:
   ```markdown
   ---
   title: Your Keyword-First Title Here
   date: 2026-10-20
   category: small-spaces        # small-spaces | rental-friendly | greenery-decor
   tags: tag one, tag two
   description: One sentence, ~150 chars, keyword-rich.
   hero: hero-sage               # hero-terra|hero-sage|hero-gold|hero-clay|hero-moss|hero-umber|hero-blush|hero-olive
   motif: 🌿                     # emoji shown on the placeholder hero
   ---

   Intro paragraph...

   ## Section heading
   ...
   ## Frequently Asked Questions
   ### Question one?
   Answer...
   ```
   Affiliate links: write `https://www.amazon.com/s?k=...&tag={{AMAZON_TAG}}` —
   the builder substitutes your tag from `config.py`.
   Internal links: use root-relative paths like `[text](/other-post-slug/)`.
2. `python3 build.py --check` — builds into `site/`, verifies 0 broken internal
   links, and reports per-post word counts (aim 1,000+).
3. `git add -A && git commit -m "post: <slug>" && git push` — Vercel redeploys automatically.

## Changing the domain

One line in `config.py`: `SITE_URL = "https://decorly.homes"`. Rebuild, push.
Canonicals, sitemap, RSS, and OG tags all regenerate from it.

## Verification (last run: 2026-10-14)

- `python3 build.py --check`: **439 internal links, 0 broken**
- 8 posts, **10,628 total words** (1,231–1,495 each, all ≥ 1,000)
- 18 URLs in `sitemap.xml`; homepage lists all posts; hubs list correct posts
- FAQ JSON-LD present on all 8 posts; breadcrumb + article schema verified

## Still to do (owner)

- [ ] Buy decorly.homes; point DNS at Vercel (step 3 above)
- [ ] Apply for Amazon Associates; set real `AMAZON_TAG`
- [ ] Add 8 real hero images (`assets/<slug>/hero.jpg`)
- [ ] Set up Pinterest account + boards; pin plan is 2–3 fresh pins per post
- [ ] Optional: replace `hello@decorly.homes` contact email once mailbox exists
