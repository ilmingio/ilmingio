#!/usr/bin/env python3
"""Inject Open Graph, Twitter Card, canonical, and JSON-LD across marketing pages."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ilming.io"
OG_IMAGE = f"{SITE}/assets/images/og/ilming-og.png"
LOGO = f"{SITE}/assets/images/logo/ilming_logo.svg"

# rel path -> SEO config (title/description for OG when not parsed from page)
PAGE_SEO = {
    "index.html": {
        "url": f"{SITE}/",
        "og_title": "ilming — Islamic LMS for Madrassas, Schools & Institutes",
        "schemas": ["organization", "software", "website"],
    },
    "404.html": {
        "url": f"{SITE}/404.html",
        "og_title": "Page not found — ilming",
        "description": "This page has moved or no longer exists on ilming.io.",
        "robots": "noindex, follow",
        "schemas": [],
    },
    "platform/index.html": {
        "url": f"{SITE}/platform/",
        "og_title": "Platform — ilming Islamic LMS",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Platform", None)],
    },
    "features/index.html": {
        "url": f"{SITE}/features/",
        "og_title": "Features — ilming Islamic LMS",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Features", None)],
    },
    "pricing/index.html": {
        "url": f"{SITE}/pricing/",
        "og_title": "Pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Pricing", None)],
    },
    "about/index.html": {
        "url": f"{SITE}/about/",
        "og_title": "About ilming — Islamic LMS for Madrassas & Schools",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("About", None)],
    },
    "contact/index.html": {
        "url": f"{SITE}/contact/",
        "og_title": "Contact ilming — Demo & sales for Islamic institutes",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Contact", None)],
    },
    "ai/index.html": {
        "url": f"{SITE}/ai/",
        "og_title": "Virtual Ustadh & ilming AI — Quran Practice for Institutes",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("AI", None)],
    },
    "blog/index.html": {
        "url": f"{SITE}/blog/",
        "og_title": "Blog — ilming Islamic LMS Insights",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Blog", None)],
    },
    "privacy-policy/index.html": {
        "url": f"{SITE}/privacy-policy/",
        "og_title": "Privacy Policy — ilming Islamic LMS",
        "description": "How ilming collects, uses, and protects data for madrassas, Islamic schools, and learning institutes using the LMS platform.",
        "schemas": [],
    },
    "terms-and-conditions/index.html": {
        "url": f"{SITE}/terms-and-conditions/",
        "og_title": "Terms & Conditions — ilming Islamic LMS",
        "description": "Terms of service for institutes using ilming — the Islamic LMS platform at ilming.io for madrassas, schools, and learning centres.",
        "schemas": [],
    },
    "blog/why-your-madrassa-needs-an-lms/index.html": {
        "url": f"{SITE}/blog/why-your-madrassa-needs-an-lms/",
        "og_title": "Why your madrassa needs an LMS in 2026",
        "og_type": "article",
        "published": "2026-05-15",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("Why your madrassa needs an LMS", None),
        ],
    },
    "blog/secure-online-exams-for-islamic-schools/index.html": {
        "url": f"{SITE}/blog/secure-online-exams-for-islamic-schools/",
        "og_title": "Secure online exams for Islamic schools",
        "og_type": "article",
        "published": "2026-05-08",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("Secure online exams", None),
        ],
    },
    "blog/ai-tools-for-islamic-educators/index.html": {
        "url": f"{SITE}/blog/ai-tools-for-islamic-educators/",
        "og_title": "AI tools for Islamic educators — used responsibly",
        "og_type": "article",
        "published": "2026-04-28",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("AI for Islamic educators", None),
        ],
    },
    "blog/guardian-portal-build-parent-trust/index.html": {
        "url": f"{SITE}/blog/guardian-portal-build-parent-trust/",
        "og_title": "How a guardian portal builds parent trust",
        "og_type": "article",
        "published": "2026-04-12",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("Guardian portal & parent trust", None),
        ],
    },
    "blog/digitising-madrassas-in-uk-and-uae/index.html": {
        "url": f"{SITE}/blog/digitising-madrassas-in-uk-and-uae/",
        "og_title": "Digitising madrassas in the UK and UAE",
        "og_type": "article",
        "published": "2026-03-22",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("Digitising madrassas UK & UAE", None),
        ],
    },
}


def parse_title(text: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", text, re.I)
    return html.unescape(m.group(1).strip()) if m else "ilming"


def parse_description(text: str) -> str:
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', text, re.I | re.S)
    if m:
        return html.unescape(m.group(1).strip())
    m = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        text.replace("\n", " "),
        re.I,
    )
    return html.unescape(m.group(1).strip()) if m else ""


def org_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "ilming",
        "url": SITE,
        "logo": LOGO,
        "description": "Advanced Islamic Learning Management System for madrassas, schools, and learning institutes.",
        "areaServed": ["GB", "AE", "IN", "SA", "QA", "KW", "BH", "OM"],
    }


def software_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "ilming",
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Web",
        "url": SITE,
        "description": "Islamic LMS for madrassas and schools — secure exams, fees, guardian portal, live classes, and optional AI.",
        "offers": {
            "@type": "Offer",
            "price": "999",
            "priceCurrency": "INR",
            "description": "Plans from Basic; 14-day trial available",
        },
        "provider": {"@type": "Organization", "name": "ilming", "url": SITE},
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "ilming",
        "url": SITE,
        "description": "Islamic LMS platform for madrassas, schools, and learning institutes.",
        "publisher": {"@type": "Organization", "name": "ilming"},
    }


def article_schema(cfg: dict, title: str, description: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": cfg.get("og_title", title),
        "description": description,
        "datePublished": cfg.get("published", "2026-01-01"),
        "dateModified": cfg.get("published", "2026-01-01"),
        "author": {"@type": "Organization", "name": "ilming", "url": SITE},
        "publisher": {
            "@type": "Organization",
            "name": "ilming",
            "logo": {"@type": "ImageObject", "url": LOGO},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": cfg["url"]},
        "image": OG_IMAGE,
    }


def breadcrumb_schema(items: list) -> dict:
    elements = []
    for i, (name, url) in enumerate(items, start=1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if url:
            item["item"] = url
        elements.append(item)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }


def build_json_ld(cfg: dict, title: str, description: str) -> str:
    blocks = []
    for kind in cfg.get("schemas", []):
        if kind == "organization":
            blocks.append(org_schema())
        elif kind == "software":
            blocks.append(software_schema())
        elif kind == "website":
            blocks.append(website_schema())
        elif kind == "article":
            blocks.append(article_schema(cfg, title, description))
        elif kind == "breadcrumb" and cfg.get("breadcrumb"):
            blocks.append(breadcrumb_schema(cfg["breadcrumb"]))
    if not blocks:
        return ""
    lines = []
    for block in blocks:
        lines.append(
            '    <script type="application/ld+json">'
            + json.dumps(block, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )
    return "\n".join(lines)


def seo_block(cfg: dict, title: str, description: str) -> str:
    url = cfg["url"]
    og_title = cfg.get("og_title", title)
    og_type = cfg.get("og_type", "website")
    robots = cfg.get("robots", "index, follow")
    desc = cfg.get("description") or description
    if not desc and cfg.get("description"):
        desc = cfg["description"]

    lines = [
        f'    <meta name="robots" content="{robots}" />',
        f'    <link rel="canonical" href="{url}" />',
        f'    <meta property="og:site_name" content="ilming" />',
        f'    <meta property="og:locale" content="en_GB" />',
        f'    <meta property="og:type" content="{og_type}" />',
        f'    <meta property="og:url" content="{url}" />',
        f'    <meta property="og:title" content="{html.escape(og_title, quote=True)}" />',
        f'    <meta property="og:description" content="{html.escape(desc, quote=True)}" />',
        f'    <meta property="og:image" content="{OG_IMAGE}" />',
        f'    <meta property="og:image:width" content="1200" />',
        f'    <meta property="og:image:height" content="630" />',
        f'    <meta property="og:image:alt" content="ilming — Islamic LMS for madrassas, schools and institutes" />',
        '    <meta name="twitter:card" content="summary_large_image" />',
        f'    <meta name="twitter:title" content="{html.escape(og_title, quote=True)}" />',
        f'    <meta name="twitter:description" content="{html.escape(desc, quote=True)}" />',
        f'    <meta name="twitter:image" content="{OG_IMAGE}" />',
    ]
    if og_type == "article" and cfg.get("published"):
        lines.append(
            f'    <meta property="article:published_time" content="{cfg["published"]}" />'
        )
        lines.append('    <meta property="article:author" content="ilming" />')

    json_ld = build_json_ld(cfg, title, desc)
    if json_ld:
        lines.append(json_ld)
    return "\n".join(lines)


def sync_file(rel: str, cfg: dict) -> None:
    path = ROOT / rel
    if not path.exists():
        print(f"skip: {rel}")
        return
    text = path.read_text(encoding="utf-8")
    title = parse_title(text)
    description = parse_description(text)
    if cfg.get("description") and not description:
        description = cfg["description"]
        if 'name="description"' not in text:
            text = re.sub(
                r"(<title>[^<]+</title>)",
                r'\1\n    <meta name="description" content="'
                + html.escape(description, quote=True)
                + '" />',
                text,
                count=1,
            )

    block = seo_block(cfg, title, description)

    # Remove existing SEO injection (robots through json-ld, og, twitter, duplicate canonical)
    text = re.sub(r"\n?\s*<meta name=\"robots\"[^>]*>", "", text)
    text = re.sub(r"\n?\s*<link rel=\"canonical\"[^>]*>", "", text)
    text = re.sub(
        r"\n?\s*<meta(?:\s[^>]*?(?:property=\"og:[^\"]+\"|name=\"twitter:[^\"]+\"|property=\"article:[^\"]+\"|name=\"article:[^\"]+\"))[^>]*/>",
        "",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(
        r"\n?\s*<script type=\"application/ld\+json\">.*?</script>",
        "",
        text,
        flags=re.DOTALL,
    )

    # Insert after description meta (or after title if no description)
    desc_pat = re.compile(
        r'(<meta\s+name="description"\s+content="[^"]*"\s*/>)',
        re.I | re.S,
    )
    if desc_pat.search(text):
        text = desc_pat.sub(r"\1\n" + block, text, count=1)
    else:
        # 404 — insert after title
        text = re.sub(
            r"(<title>[^<]+</title>)",
            r"\1\n" + block,
            text,
            count=1,
        )
        if 'name="description"' not in text and cfg.get("description"):
            text = re.sub(
                r"(<meta name=\"theme-color\"[^>]*/>)",
                rf'\1\n    <meta name="description" content="{html.escape(cfg["description"], quote=True)}" />',
                text,
                count=1,
            )

    path.write_text(text, encoding="utf-8")
    print(f"seo: {rel}")


def update_robots() -> None:
    content = """User-agent: *
Allow: /
Disallow: /_legacy/

Sitemap: https://ilming.io/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(content, encoding="utf-8")
    print("updated: robots.txt")


def update_sitemap() -> None:
    urls = [
        (f"{SITE}/", "weekly", "1.0", "2026-06-01"),
        (f"{SITE}/platform/", "monthly", "0.9", "2026-06-01"),
        (f"{SITE}/features/", "monthly", "0.9", "2026-06-01"),
        (f"{SITE}/ai/", "monthly", "0.85", "2026-06-01"),
        (f"{SITE}/pricing/", "monthly", "0.9", "2026-06-01"),
        (f"{SITE}/blog/", "weekly", "0.8", "2026-06-01"),
        (f"{SITE}/blog/why-your-madrassa-needs-an-lms/", "monthly", "0.7", "2026-05-15"),
        (f"{SITE}/blog/secure-online-exams-for-islamic-schools/", "monthly", "0.7", "2026-05-08"),
        (f"{SITE}/blog/ai-tools-for-islamic-educators/", "monthly", "0.7", "2026-04-28"),
        (f"{SITE}/blog/guardian-portal-build-parent-trust/", "monthly", "0.7", "2026-04-12"),
        (f"{SITE}/blog/digitising-madrassas-in-uk-and-uae/", "monthly", "0.7", "2026-03-22"),
        (f"{SITE}/about/", "monthly", "0.7", "2026-06-01"),
        (f"{SITE}/contact/", "monthly", "0.8", "2026-06-01"),
        (f"{SITE}/privacy-policy/", "yearly", "0.3", "2026-05-01"),
        (f"{SITE}/terms-and-conditions/", "yearly", "0.3", "2026-05-01"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, pri, mod in urls:
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>"
        )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("updated: sitemap.xml")


def main() -> None:
    for rel, cfg in PAGE_SEO.items():
        sync_file(rel, cfg)
    update_robots()
    update_sitemap()
    print("done.")


if __name__ == "__main__":
    main()
