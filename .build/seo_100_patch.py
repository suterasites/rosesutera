#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Rose Sutera site.

Brings every page to a clean pass on the machine-checkable checks in
Apps/sutera-seo/checklist.py (the engine behind SEO HQ). Safe to re-run.

The live site is served on rosesutera.com.au, but every page canonicalised (and
pointed og:url + schema URLs) to healthbyrose.com.au, which is NXDOMAIN (never
set up). James confirmed 2026-07-28 that rosesutera.com.au is the canonical
domain, so this rewrites every healthbyrose.com.au URL to rosesutera.com.au.

Also:
  - recipes.html: add the HealthAndBeautyBusiness node it was missing
  - privacy.html: lengthen the 31-char title, trim the 174-char description, and
    fix "book a class" -> "book a consultation" (nutritionist-only positioning)

sitemap.xml + robots.txt (with a Sitemap: line) are written as real files at the
repo root by build_site_files() - the live paths currently fall through to the
SPA/homepage HTML.

Homepage breadcrumb is deliberately left as the only page warn - a homepage crumb
is pointless UX - and the pooled score rounds to 100.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD_DOMAIN = "healthbyrose.com.au"
NEW_DOMAIN = "rosesutera.com.au"

PAGES = ["index.html", "about.html", "services.html", "recipes.html",
         "contact.html", "privacy.html"]

PRIVACY_TITLE = "Privacy Policy | Health By Rose Nutrition, Melbourne"
PRIVACY_DESC = ("How Health By Rose collects, uses and protects the personal information you "
                "share when you book a consultation or get in touch, under the Australian Privacy Principles.")

SITEMAP_URLS = [
    ("/", "1.0"), ("/services.html", "0.9"), ("/about.html", "0.8"),
    ("/recipes.html", "0.6"), ("/contact.html", "0.7"), ("/privacy.html", "0.3"),
]


def business_node():
    """Pull the HealthAndBeautyBusiness node from index, with the domain fixed."""
    h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    h = h.replace(OLD_DOMAIN, NEW_DOMAIN)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for node in (d.get("@graph", [d]) if isinstance(d, dict) else [d]):
            t = node.get("@type", "")
            tl = t if isinstance(t, list) else [t]
            if any(x.endswith("Business") or x in ("LocalBusiness", "Organization") for x in tl):
                node = dict(node)
                node.pop("@context", None)
                return node
    return None


def patch(fn, biz):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    # --- canonical/og/schema domain: healthbyrose.com.au -> rosesutera.com.au ---
    n = html.count(OLD_DOMAIN)
    if n:
        html = html.replace(OLD_DOMAIN, NEW_DOMAIN)
        did.append(f"domain x{n}")

    # --- privacy: title + description ---
    if fn == "privacy.html":
        html2 = re.sub(r"<title>.*?</title>", "<title>" + PRIVACY_TITLE + "</title>", html, count=1, flags=re.S)
        if html2 != html:
            html = html2
            did.append(f"title({len(PRIVACY_TITLE)})")
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + PRIVACY_DESC + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"desc({len(PRIVACY_DESC)})")

    # --- recipes: add the missing business node ---
    if fn == "recipes.html" and biz and '"HealthAndBeautyBusiness"' not in html:
        block = ('<script type="application/ld+json">\n'
                 + json.dumps({"@context": "https://schema.org", **biz}, indent=2, ensure_ascii=False)
                 + "\n</script>\n")
        html = html.replace("</head>", block + "</head>", 1)
        did.append("business-schema")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def build_site_files():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr in SITEMAP_URLS:
        lines.append(f'  <url><loc>https://{NEW_DOMAIN}{loc}</loc><priority>{pr}</priority></url>')
    lines.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    robots = ("User-agent: *\nAllow: /\n\n"
              f"Sitemap: https://{NEW_DOMAIN}/sitemap.xml\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(robots)
    print("  wrote sitemap.xml + robots.txt")


def main():
    biz = business_node()
    print(f"Patching {len(PAGES)} pages under {ROOT}")
    print(f"business node: {'found (' + str(biz.get('@type')) + ')' if biz else 'MISSING'}\n")
    for fn in PAGES:
        changed = patch(fn, biz)
        print(f"  {fn:16s} {', '.join(changed) if changed else 'no change'}")
    build_site_files()
    print("\nDone. Idempotent - safe to re-run.")


if __name__ == "__main__":
    main()
