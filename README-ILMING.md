# ilming marketing site (ilming.io)

Static marketing website for **ilming** — an advanced Islamic Learning Management System (LMS) for madrassas, schools, and learning institutes (UK, UAE, India & GCC).

## Site map

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/platform/` | Platform overview (pillars, roles, onboarding) |
| `/features/` | Full module list |
| `/pricing/` | Plans, comparison table, pricing FAQ |
| `/ai/` | Optional AI tools (beta) for educators |
| `/blog/` | Blog — LMS guides & insights |
| `/about/` | Vision, purpose, focus areas |
| `/contact/` | Contact / demo form |
| `/present/` | **Client product tour** — 10 visual slides for a short meeting |
| `/demo-platform/` | **Platform flow charts & demo guide** (architecture, Tahfiz flow, credentials) |
| `/docs/PLATFORM-ARCHITECTURE.md` | Technical reference (Markdown) |
| `/privacy-policy/` | Privacy |
| `/terms-and-conditions/` | Terms |

Also: `404.html`, `robots.txt`, `sitemap.xml`, `_redirects` for legacy URLs.

## Positioning

- **Product:** Islamic LMS software at ilming.io — not stationery or e-commerce
- **Audience:** Tahfiz institutes, madrassas, Islamic schools, hifz/weekend programmes
- **Surfaces:** Web CRM (`app.ilming.io`) · student iOS/Android app · guardian portal
- **Regions:** UK, UAE, India, GCC

## Local preview

```bash
cd ilming
python3 -m http.server 8000
```

Open http://localhost:8000

With LMS app (login/register links):

```bash
cd ../Ilming-crm && pnpm dev   # :3000
cd ../Ilming-api && pnpm dev   # :8080 (required)
```

`assets/js/config.js` uses `http://localhost:3000` for app links when hostname is localhost.

## Design system

| Token | Hex | Use |
|-------|-----|-----|
| Emerald primary | `#0a6b5c` | Buttons, links, accents |
| Gold accent | `#c9a84c` | Badges, highlights, CTAs |
| Navy | `#0c1829` | Hero, footer, headings |
| Cream | `#faf7f2` | Section backgrounds |

Fonts: **Cormorant Garamond** (display) + **Plus Jakarta Sans** (body)  
CSS: `assets/css/site.css`  
Logo tagline: *Islamic LMS Platform*

## CTAs

| Audience | Action | Destination |
|----------|--------|-------------|
| Institute admin | Book a demo / Request pilot | `/contact/` |
| Existing admin | Log in | app `/login` |
| Student | Student enroll | app `/register` |

## SEO

- **Sitemap:** `sitemap.xml` (with `lastmod` dates)
- **Robots:** `robots.txt` — blocks `/_legacy/` from crawlers
- **Social preview:** `assets/images/og/ilming-og.png` (1200×630)
- **Structured data:** JSON-LD on homepage (Organization, SoftwareApplication, WebSite), blog posts (Article), inner pages (BreadcrumbList)

Re-apply SEO tags after copy changes:

```bash
python3 scripts/sync-seo.py
python3 scripts/sync-layout.py   # nav + footer
```

After deploy, submit `https://ilming.io/sitemap.xml` in [Google Search Console](https://search.google.com/search-console).

## Full stack (local)

```bash
# Terminal 1 — marketing site (this folder)
cd ilming && python3 -m http.server 8000

# Terminal 2 — LMS app
cd ../Ilming-crm && pnpm dev          # :3000

# Terminal 3 — API
cd ../Ilming-api && pnpm dev          # :8080
```

See `../Ilming-crm/README.md` and `../Ilming-api/README.md` for full setup.

## Deploy

1. Publish **ilming/** root to ilming.io hosting.
2. Point DNS; enable `_redirects` on Netlify/Cloudflare.
3. Host **Ilming-crm** on app.ilming.io.
4. Host **Ilming-api** on api.ilming.io.

## Legacy

Old tuition template (~800 pages): `_legacy/content/` — not deployed.
