# Decorly affiliate backfill — today's 4 link-less posts — 16 Nov 2026

Source: weekly monetization check, Mon 16 Nov 2026 (reported in main chat
05:04 PKT): 43 of 143 posts carry no affiliate links, including 4 of that
day's 5 new posts. Verified independently in this run by scanning
posts/*.md for "amazon": 43 files with no mention, list at the end.

Pattern (established, user-approved 26 Oct 2026: "attach/link amazon
affiliate products in all articles"; same pattern used 26 Oct for 16 posts
and 4 Nov for 26 posts): add one "## Shop this look: ..." section of
5 Amazon search links (https://www.amazon.com/s?k=...&tag={{AMAZON_TAG}}),
inserted immediately before "## Frequently Asked Questions". Every product
below is named in the post's own text. The build auto-adds the affiliate
disclosure to every post page (build.py), so no disclosure text is needed
in the markdown. After editing: `python3 build.py --check`, verify 0
broken links and that the tag renders as thespicedspoo-20 on the 4 live
pages, then commit + push following the daily-publisher flow.

## 1. posts/christmas-morning-small-apartment-guide.md
Section title: `## Shop this look: Christmas morning basics`

- **Mini Christmas tree, 2–3 ft** — the right size for a side table, at eye level. [Shop mini Christmas trees](https://www.amazon.com/s?k=mini+christmas+tree+2+3+ft+tabletop&tag={{AMAZON_TAG}})
- **Battery-operated warm-white fairy lights, 50 count** — one short string makes a small tree glow. [Shop battery fairy lights](https://www.amazon.com/s?k=battery+operated+warm+white+fairy+lights+50&tag={{AMAZON_TAG}})
- **Removable adhesive hooks** — hang stockings with no holes in the wall. [Shop removable adhesive hooks](https://www.amazon.com/s?k=removable+adhesive+hooks+command+strips&tag={{AMAZON_TAG}})
- **Knitted Christmas stockings** — chunky, light, and easy to hang from a hook. [Shop knitted Christmas stockings](https://www.amazon.com/s?k=knitted+christmas+stockings+set&tag={{AMAZON_TAG}})
- **Flameless battery candles, set of 3** — flickering glow with no flame near wrapping paper. [Shop flameless battery candles](https://www.amazon.com/s?k=flameless+battery+candles+set+of+3+timer&tag={{AMAZON_TAG}})
- **Kraft wrapping paper with red twine** — a matching palette makes a small gift pile look generous. [Shop kraft wrapping paper](https://www.amazon.com/s?k=kraft+wrapping+paper+roll+red+twine&tag={{AMAZON_TAG}})

## 2. posts/host-christmas-eve-small-rental-guide.md
Section title: `## Shop this look: Christmas Eve hosting basics`

- **Flameless LED pillar candles** — candlelight with no flame near a tree or a guest's sleeve. [Shop flameless LED candles](https://www.amazon.com/s?k=flameless+led+pillar+candles+with+timer&tag={{AMAZON_TAG}})
- **Warm-white fairy lights** — one string along a shelf or window, overhead light off. [Shop warm white fairy lights](https://www.amazon.com/s?k=warm+white+fairy+lights+indoor&tag={{AMAZON_TAG}})
- **Slow cooker** — keeps the cocoa warm on the lowest heat all evening. [Shop slow cookers](https://www.amazon.com/s?k=slow+cooker+small&tag={{AMAZON_TAG}})
- **Christmas stockings** — one per guest, light enough for a removable hook. [Shop Christmas stockings](https://www.amazon.com/s?k=christmas+stockings+set+of+6&tag={{AMAZON_TAG}})
- **Floor cushions** — real seats for guests when the sofa runs out. [Shop floor cushions](https://www.amazon.com/s?k=floor+cushions+seating+set&tag={{AMAZON_TAG}})
- **Hot cocoa toppings set** — mini marshmallows, cinnamon, sprinkles and candy canes in one buy. [Shop hot cocoa toppings](https://www.amazon.com/s?k=hot+cocoa+toppings+marshmallows+cinnamon&tag={{AMAZON_TAG}})

## 3. posts/winter-succulent-care-ideas-small-apartments.md
Section title: `## Shop this look: winter succulent care basics`

- **Clip-on LED grow light** — the cheapest fix for short winter days. [Shop clip-on grow lights](https://www.amazon.com/s?k=clip+on+led+grow+light+indoor+plants&tag={{AMAZON_TAG}})
- **Terracotta pots with drainage holes** — breathable pots that dry out between waterings. [Shop terracotta pots with drainage](https://www.amazon.com/s?k=terracotta+pots+with+drainage+holes+set&tag={{AMAZON_TAG}})
- **Cactus and succulent soil mix** — gritty, fast-draining, rot-proof. [Shop succulent soil mix](https://www.amazon.com/s?k=cactus+succulent+soil+mix&tag={{AMAZON_TAG}})
- **Small watering can** — a tiny spout for a once-a-month soak. [Shop small watering cans](https://www.amazon.com/s?k=small+watering+can+indoor+plants&tag={{AMAZON_TAG}})
- **Tiered plant stand** — every pot gets its share of the brightest window. [Shop tiered plant stands](https://www.amazon.com/s?k=tiered+plant+stand+indoor+small&tag={{AMAZON_TAG}})

## 4. posts/keep-fiddle-leaf-fig-alive-winter-guide.md
Section title: `## Shop this look: fiddle leaf fig winter basics`

- **LED grow light bar** — ten to twelve hours of steady light on a timer. [Shop LED grow light bars](https://www.amazon.com/s?k=led+grow+light+bar+indoor+plants&tag={{AMAZON_TAG}})
- **Soil moisture meter** — about the price of a coffee, and it takes the guesswork out of watering. [Shop soil moisture meters](https://www.amazon.com/s?k=soil+moisture+meter+indoor+plants&tag={{AMAZON_TAG}})
- **Pebble tray** — raises humidity right around the plant, no humidifier needed. [Shop pebble trays for plants](https://www.amazon.com/s?k=pebble+tray+for+houseplants&tag={{AMAZON_TAG}})
- **Fine mist spray bottle** — morning misting that dries before nightfall. [Shop plant mist spray bottles](https://www.amazon.com/s?k=fine+mist+spray+bottle+plants&tag={{AMAZON_TAG}})
- **Small hygrometer** — tells you the actual humidity in the room. [Shop room hygrometers](https://www.amazon.com/s?k=small+room+hygrometer+indoor&tag={{AMAZON_TAG}})
- **Terracotta pot with drainage** — dries out faster than plastic or glazed ceramic in winter. [Shop terracotta pots with drainage](https://www.amazon.com/s?k=terracotta+pot+with+drainage+hole+large&tag={{AMAZON_TAG}})

## Remaining 39 link-less posts (same pattern, not drafted here)

afrohemian-living-room-ideas-small-apartments, christmas-countdown-ideas-rental-guide,
christmas-village-display-ideas-small-spaces, colourful-maximalist-small-apartment-ideas,
cozy-november-decor-small-apartments-ideas, decorate-rental-front-door-christmas-guide,
decorate-small-apartment-thanksgiving-guide, dopamine-decor-living-room-ideas-small-apartments,
dry-citrus-flowers-winter-decor-guide, eucalyptus-decor-winter-ideas,
fresh-evergreen-branch-decor-ideas-small-apartments, host-christmas-cookie-swap-small-rental-guide,
host-christmas-movie-night-small-rental, host-winter-dinner-party-small-rental-guide,
host-winter-games-night-small-rental-guide, keep-herbs-alive-indoors-winter-guide,
keep-norfolk-pine-alive-after-christmas-guide, make-dried-flower-wreath-winter-guide,
neo-deco-living-room-ideas-small-apartments, norfolk-pine-decor-ideas-christmas,
pearlescent-vase-styling-winter-greenery-ideas, pinecone-decor-ideas-winter-cost-almost-nothing,
protect-rental-floors-winter-salt-guide, renter-friendly-christmas-bedroom-decor-ideas,
renter-friendly-christmas-card-display-ideas, renter-friendly-christmas-decor-10-minutes-ideas,
renter-friendly-new-years-eve-table-decor-ideas, renter-friendly-winter-curtain-ideas-keep-heat-in,
renter-friendly-winter-lighting-ideas, rosemary-christmas-tree-grow-style-guide,
small-apartment-christmas-bookshelf-styling-ideas, small-apartment-christmas-without-tree-guide,
striped-ceiling-bedroom-rental-guide, style-air-plants-small-apartment-winter-guide,
winter-coffee-table-decor-ideas-small-apartments, winter-gallery-wall-small-apartment-guide,
winter-plant-shelf-display-ideas-small-apartments, winter-terrarium-ideas-small-apartments,
woven-basket-wall-trailing-plants-guide
