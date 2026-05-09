# CLAUDE.md - Health By Rose

## Business Context

**Business Name:** Health By Rose
**Owner:** Rose Sutera (James's mum)
**Email:** rosesutera680@gmail.com
**Phone:** 0419 554 640 (tel: +61419554640)
**Location:** West Melbourne / Altona, VIC, Australia
**Service modes:** In-person (West Melbourne, Altona) and Zoom (Australia-wide)
**Domain:** healthbyrose.com.au

### About
- Qualified nutritionist and aerobics instructor
- Lifelong passion for health and fitness, traces back to school sport (netball, softball)
- Personal training: cycling, running, weights
- Philosophy: "you are what you eat" + balance. Real wellness is the sweet spot between nourishing food and active movement
- Tone: warm, practical, encouraging, never preachy

### Specialties
- Weight loss
- Gut health
- Sleep, stress and anxiety
- Hormonal health

### Services and pricing
- **Initial consultation** - 60 minutes, $175. Full case history and initial health assessment. Baseline analysis of current health status.
- **Return consultation** - 30 minutes, $85. Discussion of personalised treatment plan and goals.

### Site content focus
- Practical tips
- Recipes
- Fitness routines
- Mindset guidance

---

## Design Direction

Warm modern wellness. Confident, not clinical. Photo-led when assets land.

**Palette**
- Terracotta accent: `#C66B4A`
- Warm cream background: `#FAF6F0`
- Deep charcoal text: `#2A2825`
- Soft sage secondary: `#A8B5A0`
- Subtle stone for cards: `#F0EBE3`

**Type**
- Display: Fraunces (serif), tight tracking on large headings
- Body: Inter (sans), generous line-height

---

## Tech and Output Rules
- Static HTML/CSS/JS (matches Neil Sutera site pattern)
- Tailwind CSS via CDN, custom brand colors via `tailwind.config`
- Single file per page, styles inline
- Placeholder images via `https://placehold.co/WIDTHxHEIGHT` until real photos arrive
- Mobile-first, sticky bottom CTA bar on mobile (Call + Book)
- No em dashes anywhere - use hyphens, commas, or periods

## On-Page SEO
- Read `SEO_brief/on-page-seo.md` at project root before generating any new page. Every applicable item must be satisfied.
- Schema: LocalBusiness or HealthAndBeautyBusiness, Person (Rose, with credentials), Service (per consult), BreadcrumbList per page, Organization site-wide
- Title 50-60 chars, meta 150-160 chars, primary keyword early
- Click-to-call phone in header on every viewport (do not hide on mobile)

## Multi-Page Consistency
- Navbar identical across all pages. Update everywhere if changed.
- Footer identical across all pages. Update everywhere if changed.
- Internal links must point to actual existing pages.

## Pages
- [x] index.html - homepage
- [x] about.html
- [x] services.html
- [x] recipes.html (coming-soon page; blog index when posts land)
- [x] contact.html

## Image policy
- No image placeholders anywhere on the site. Hero, about, and journal sections use typographic / coloured-block design instead.
- When real photos are supplied, swap into:
  - index.html hero right column (replace quote card)
  - index.html about section (replace credentials card)
  - index.html journal cards (replace gradient panels)
  - about.html hero / story sections

## Forms
- Formspree endpoint placeholder: `https://formspree.io/f/REPLACE_ME` (swap when James creates the form)

## Deployment
- Repo and Cloudflare Pages project to be set up when site is ready for first deploy
- Auto-deploy to GitHub + Cloudflare Pages on every change once live (per global Sutera Sites rule)
