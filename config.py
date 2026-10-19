# Decorly site configuration.
# Change these values — everything else (canonicals, sitemap, feed, OG tags)
# is generated from them by build.py.

SITE_URL = "https://decorly.homes"   # no trailing slash; update after the domain is bought & pointed at Vercel
SITE_NAME = "Decorly"
TAGLINE = "Beautiful homes on a renter's budget"
AUTHOR = "Decorly"

# Amazon Associates tracking ID. Replace with the real tag once approved.
# Used in posts via {{AMAZON_TAG}} placeholders.
AMAZON_TAG = "decorly-20"

# Google Analytics 4 measurement ID. Injected as the gtag.js snippet on every page.
GA_MEASUREMENT_ID = "G-FKL6VMXCF0"

# Google Search Console site verification token. Injected as a meta tag on every page.
GOOGLE_SITE_VERIFICATION = "3SxmeiBROAdRg73C_AbsxRRHnRD4V0wNvtrJRBfiIzc"

# Contact shown on about/privacy pages (replace with a real one before launch).
CONTACT_EMAIL = "hello@decorly.homes"

# Email newsletter signup.
# Human step: create the provider account first (recommend Buttondown — simple,
# cheap, API-friendly), then paste its subscribe form action URL below.
# While empty, the signup forms on the homepage and post pages render with a
# clearly-marked placeholder action that stores nothing.
EMAIL_PROVIDER = ""
EMAIL_FORM_ACTION = ""
