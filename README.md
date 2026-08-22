# ilming marketing site (ilming.io)

Static marketing website for **ilming** — an Islamic Learning Management System for Tahfiz institutes, madrassas, and Islamic schools (UK, UAE, India & GCC).

## Site map

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/platform/` | Platform overview |
| `/features/` | Full module list |
| `/pricing/` | India INR plans |
| `/pricing/usd/` | International USD plans (LMS + Quran AI) |
| `/ai/` | Virtual Ustadh & AI tools |
| `/blog/` | Blog |
| `/about/` | Vision and purpose |
| `/contact/` | Demo / contact form |
| `/present/` | 10-minute product tour |
| `/demo-platform/` | Internal demo guide (noindex) |
| `/privacy-policy/` | Privacy |
| `/terms-and-conditions/` | Terms |

Also: `404.html`, `robots.txt`, `sitemap.xml`, `_redirects` (legacy tuition URLs), `_headers`.

## Local preview

```bash
python3 -m http.server 8000
```

Open http://localhost:8000

App login/register links resolve to `http://localhost:3000` when the hostname is localhost (`assets/js/config.js`).

## Design

| Token | Hex | Use |
|-------|-----|-----|
| Emerald | `#0a6b5c` | Buttons, links, accents |
| Gold | `#c9a84c` | Badges, highlights, CTAs |
| Navy | `#0c1829` | Hero, footer, headings |
| Cream | `#faf7f2` | Section backgrounds |

Fonts: **Cormorant Garamond** (display) + **Plus Jakarta Sans** (body)  
CSS: `assets/css/site.css`

## SEO & layout sync

After copy or nav changes:

```bash
python3 scripts/sync-seo.py
python3 scripts/sync-layout.py
```

Submit `https://ilming.io/sitemap.xml` in [Google Search Console](https://search.google.com/search-console) after deploy.

## Deploy

Publish this folder root to ilming.io (Netlify / Cloudflare Pages). `_redirects` and `_headers` are picked up automatically.

LMS app: `app.ilming.io` · API: `api.ilming.io`
