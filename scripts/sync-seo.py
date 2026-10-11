#!/usr/bin/env python3
"""Inject Open Graph, Twitter Card, canonical, and JSON-LD across marketing pages."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.ilming.io"
OG_IMAGE = f"{SITE}/assets/images/og/ilming-og.png"
LOGO = f"{SITE}/assets/images/favicon/apple-touch-icon.png"
OG_ALT = "ilming — operating system for Tahfiz institutes"
TWITTER = "@ilming_io"

HREFLANG = [
    ("en-IN", f"{SITE}/pricing/"),
    ("en-AE", f"{SITE}/pricing/aed/"),
    ("en-SA", f"{SITE}/pricing/sar/"),
    ("en-GB", f"{SITE}/pricing/gbp/"),
    ("en-QA", f"{SITE}/pricing/qar/"),
    ("en-KW", f"{SITE}/pricing/kwd/"),
    ("en-BH", f"{SITE}/pricing/bhd/"),
    ("en-OM", f"{SITE}/pricing/omr/"),
    ("en", f"{SITE}/pricing/usd/"),
    ("x-default", f"{SITE}/pricing/usd/"),
]

# Open Graph locale for each pricing URL. Generic English uses en_US.
OG_LOCALE = {
    "en-IN": "en_IN",
    "en-AE": "en_AE",
    "en-SA": "en_SA",
    "en-GB": "en_GB",
    "en-QA": "en_QA",
    "en-KW": "en_KW",
    "en-BH": "en_BH",
    "en-OM": "en_OM",
    "en": "en_US",
}

# rel path -> SEO config (title/description for OG when not parsed from page)
PAGE_SEO = {
    "index.html": {
        "url": f"{SITE}/",
        "og_title": "ilming — The operating system for Tahfiz institutes",
        "schemas": ["organization", "software", "website"],
    },
    "404.html": {
        "url": f"{SITE}/404.html",
        "og_title": "Page not found — ilming",
        "description": "This page has moved or no longer exists on ilming.io.",
        "robots": "noindex, nofollow",
        "schemas": [],
    },
    "platform/index.html": {
        "url": f"{SITE}/platform/",
        "og_title": "Platform — Tahfiz LMS and web Hafazan practice | ilming",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Platform", None)],
    },
    "features/index.html": {
        "url": f"{SITE}/features/",
        "og_title": "Features — Hifz desk, Hafazan practice, and LMS | ilming",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Features", None)],
    },
    "pricing/index.html": {
        "url": f"{SITE}/pricing/",
        "og_title": "India pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [("Home", SITE + "/"), ("Pricing", None)],
        "locale": "en_IN",
        "hreflang": True,
        "price": "50",
        "currency": "INR",
        "image": "pricing-inr.png",
        "image_alt": "ilming India pricing — INR 50 per active student",
    },
    "pricing/usd/index.html": {
        "url": f"{SITE}/pricing/usd/",
        "og_title": "International pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("International plans", None),
        ],
        "locale": "en_US",
        "hreflang": True,
        "price": "1",
        "currency": "USD",
        "image": "pricing-usd.png",
        "image_alt": "ilming international pricing — $1 per active student",
    },
    "pricing/gbp/index.html": {
        "url": f"{SITE}/pricing/gbp/",
        "og_title": "United Kingdom pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("United Kingdom plans", None),
        ],
        "locale": "en_GB",
        "hreflang": True,
        "price": "1",
        "currency": "GBP",
        "image": "pricing-gbp.png",
        "image_alt": "ilming United Kingdom pricing — £1 per active student",
    },
    "pricing/aed/index.html": {
        "url": f"{SITE}/pricing/aed/",
        "og_title": "UAE pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("UAE plans", None),
        ],
        "locale": "en_AE",
        "hreflang": True,
        "price": "4",
        "currency": "AED",
        "image": "pricing-aed.png",
        "image_alt": "ilming UAE pricing — AED 4 per active student",
    },
    "pricing/sar/index.html": {
        "url": f"{SITE}/pricing/sar/",
        "og_title": "Saudi Arabia pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("Saudi Arabia plans", None),
        ],
        "locale": "en_SA",
        "hreflang": True,
        "price": "4",
        "currency": "SAR",
        "image": "pricing-sar.png",
        "image_alt": "ilming Saudi Arabia pricing — SAR 4 per active student",
    },
    "pricing/qar/index.html": {
        "url": f"{SITE}/pricing/qar/",
        "og_title": "Qatar pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("Qatar plans", None),
        ],
        "locale": "en_QA",
        "hreflang": True,
        "price": "4",
        "currency": "QAR",
        "image": "pricing-qar.png",
        "image_alt": "ilming Qatar pricing — QAR 4 per active student",
    },
    "pricing/kwd/index.html": {
        "url": f"{SITE}/pricing/kwd/",
        "og_title": "Kuwait pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("Kuwait plans", None),
        ],
        "locale": "en_KW",
        "hreflang": True,
        "price": "0.300",
        "currency": "KWD",
        "image": "pricing-kwd.png",
        "image_alt": "ilming Kuwait pricing — KWD 0.300 per active student",
    },
    "pricing/bhd/index.html": {
        "url": f"{SITE}/pricing/bhd/",
        "og_title": "Bahrain pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("Bahrain plans", None),
        ],
        "locale": "en_BH",
        "hreflang": True,
        "price": "0.400",
        "currency": "BHD",
        "image": "pricing-bhd.png",
        "image_alt": "ilming Bahrain pricing — BHD 0.400 per active student",
    },
    "pricing/omr/index.html": {
        "url": f"{SITE}/pricing/omr/",
        "og_title": "Oman pricing — ilming Islamic LMS",
        "schemas": ["breadcrumb", "offer"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Pricing", SITE + "/pricing/"),
            ("Oman plans", None),
        ],
        "locale": "en_OM",
        "hreflang": True,
        "price": "0.400",
        "currency": "OMR",
        "image": "pricing-omr.png",
        "image_alt": "ilming Oman pricing — OMR 0.400 per active student",
    },
    "about/index.html": {
        "url": f"{SITE}/about/",
        "og_title": "About ilming — Operating system for Tahfiz institutes",
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
        "og_title": "AI Hafazan Teacher for Tahfiz institutes | ilming",
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
    "security/index.html": {
        "url": f"{SITE}/security/",
        "og_title": "Security — ilming",
        "description": "How ilming separates institutes, stores recitation audio, backs up data, and handles exam checks.",
        "schemas": [],
    },
    "subprocessors/index.html": {
        "url": f"{SITE}/subprocessors/",
        "og_title": "Subprocessors — ilming",
        "description": "Providers ilming uses for hosting, payments, email, notifications, transcription, and the talking-face add-on.",
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
    "blog/why-whatsapp-is-not-enough-for-hifz/index.html": {
        "url": f"{SITE}/blog/why-whatsapp-is-not-enough-for-hifz/",
        "og_title": "Why WhatsApp is not enough for Hifz management",
        "og_type": "article",
        "published": "2026-09-30",
        "schemas": ["article", "breadcrumb"],
        "breadcrumb": [
            ("Home", SITE + "/"),
            ("Blog", SITE + "/blog/"),
            ("Why WhatsApp is not enough for Hifz", None),
        ],
    },
    "present/index.html": {
        "url": f"{SITE}/present/",
        "og_title": "Product tour — Hifz desk and Hafazan practice | ilming",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Product tour", None)],
    },
    "tahfiz-management-software/index.html": {
        "url": f"{SITE}/tahfiz-management-software/",
        "og_title": "Tahfiz management software — ilming",
        "schemas": ["breadcrumb"],
        "breadcrumb": [("Home", SITE + "/"), ("Tahfiz management software", None)],
    },
}

# rel path -> og file name. ilming-og.png stays the brand fallback.
OG_FILES = {
    "index.html": "home.png",
    "404.html": "home.png",
    "platform/index.html": "platform.png",
    "features/index.html": "features.png",
    "pricing/index.html": "pricing-inr.png",
    "pricing/usd/index.html": "pricing-usd.png",
    "pricing/gbp/index.html": "pricing-gbp.png",
    "pricing/aed/index.html": "pricing-aed.png",
    "pricing/sar/index.html": "pricing-sar.png",
    "pricing/qar/index.html": "pricing-qar.png",
    "pricing/kwd/index.html": "pricing-kwd.png",
    "pricing/bhd/index.html": "pricing-bhd.png",
    "pricing/omr/index.html": "pricing-omr.png",
    "about/index.html": "about.png",
    "contact/index.html": "contact.png",
    "ai/index.html": "ai.png",
    "blog/index.html": "blog.png",
    "privacy-policy/index.html": "privacy.png",
    "terms-and-conditions/index.html": "terms.png",
    "security/index.html": "security.png",
    "subprocessors/index.html": "subprocessors.png",
    "blog/why-your-madrassa-needs-an-lms/index.html": "blog-madrassa.png",
    "blog/secure-online-exams-for-islamic-schools/index.html": "blog-exams.png",
    "blog/ai-tools-for-islamic-educators/index.html": "blog-ai-tools.png",
    "blog/guardian-portal-build-parent-trust/index.html": "blog-guardian.png",
    "blog/digitising-madrassas-in-uk-and-uae/index.html": "blog-digitising.png",
    "blog/why-whatsapp-is-not-enough-for-hifz/index.html": "blog-whatsapp.png",
    "present/index.html": "present.png",
    "tahfiz-management-software/index.html": "tahfiz.png",
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
        "@id": f"{SITE}/#organization",
        "name": "ilming",
        "url": f"{SITE}/",
        "logo": {
            "@type": "ImageObject",
            "url": LOGO,
            "width": 180,
            "height": 180,
        },
        "description": "Operating system for Tahfiz institutes, madrassas, and Islamic schools.",
        "areaServed": ["GB", "AE", "IN", "SA", "QA", "KW", "BH", "OM"],
        "sameAs": [
            "https://www.instagram.com/ilming.io/",
            "https://www.facebook.com/profile.php?id=61595146591176",
            "https://x.com/ilming_io",
            "https://www.linkedin.com/in/ilming-io/",
            "https://www.youtube.com/@ilming-io",
        ],
    }


def software_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "ilming",
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Web, iOS, Android",
        "url": f"{SITE}/",
        "description": "Tahfiz institute platform. Native iOS and Android apps for institute, teacher, student, and guardian. AI Hafazan practice on the web. Teacher approval stays with the Ustadh.",
        "offers": [
            {
                "@type": "Offer",
                "name": "India Circle",
                "price": "50",
                "priceCurrency": "INR",
                "url": f"{SITE}/pricing/",
                "description": "₹50 per active student per month in India after a 30-day trial for 10 students.",
            },
            {
                "@type": "Offer",
                "name": "International Circle",
                "price": "1",
                "priceCurrency": "USD",
                "url": f"{SITE}/pricing/usd/",
                "description": "$1 per active student per month internationally after a 30-day trial for 10 students.",
            },
        ],
        "provider": {"@id": f"{SITE}/#organization"},
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "ilming",
        "url": f"{SITE}/",
        "description": "Operating system for Tahfiz institutes, madrassas, and Islamic schools.",
        "publisher": {"@id": f"{SITE}/#organization"},
    }


def article_schema(cfg: dict, title: str, description: str, image: str) -> dict:
    published = cfg.get("published", "2026-01-01")
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": cfg.get("og_title", title),
        "description": description,
        "datePublished": published,
        "dateModified": published,
        "author": {"@type": "Organization", "name": "ilming", "url": f"{SITE}/"},
        "publisher": {
            "@type": "Organization",
            "name": "ilming",
            "logo": {
                "@type": "ImageObject",
                "url": LOGO,
                "width": 180,
                "height": 180,
            },
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": cfg["url"]},
        "image": image,
    }


def offer_schema(cfg: dict, description: str, image: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "ilming Circle",
        "description": description,
        "image": image,
        "brand": {"@type": "Brand", "name": "ilming"},
        "offers": {
            "@type": "Offer",
            "price": cfg["price"],
            "priceCurrency": cfg["currency"],
            "url": cfg["url"],
            "availability": "https://schema.org/InStock",
            "description": description,
        },
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


def build_json_ld(cfg: dict, title: str, description: str, image: str) -> str:
    blocks = []
    for kind in cfg.get("schemas", []):
        if kind == "organization":
            blocks.append(org_schema())
        elif kind == "software":
            blocks.append(software_schema())
        elif kind == "website":
            blocks.append(website_schema())
        elif kind == "article":
            blocks.append(article_schema(cfg, title, description, image))
        elif kind == "offer":
            blocks.append(offer_schema(cfg, description, image))
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


def image_url(rel: str, cfg: dict) -> str:
    name = cfg.get("image") or OG_FILES[rel]
    return f"{SITE}/assets/images/og/{name}"


def hreflang_html() -> str:
    return "\n".join(
        f'    <link rel="alternate" href="{href}" hreflang="{lang}" />'
        for lang, href in HREFLANG
    )


def seo_block(rel: str, cfg: dict, title: str, description: str, faqs: list) -> str:
    url = cfg["url"]
    og_title = cfg.get("og_title", title)
    og_type = cfg.get("og_type", "website")
    robots = cfg.get("robots", "index, follow")
    desc = cfg.get("description") or description
    image = image_url(rel, cfg)
    alt = cfg.get("image_alt") or og_title
    locale = cfg.get("locale", "en_GB")

    lines = [
        f'    <meta name="robots" content="{robots}" />',
        f'    <link rel="canonical" href="{url}" />',
        f'    <meta property="og:site_name" content="ilming" />',
        f'    <meta property="og:locale" content="{locale}" />',
        f'    <meta property="og:type" content="{og_type}" />',
        f'    <meta property="og:url" content="{url}" />',
        f'    <meta property="og:title" content="{html.escape(og_title, quote=True)}" />',
        f'    <meta property="og:description" content="{html.escape(desc, quote=True)}" />',
        f'    <meta property="og:image" content="{image}" />',
        f'    <meta property="og:image:width" content="1200" />',
        f'    <meta property="og:image:height" content="630" />',
        f'    <meta property="og:image:alt" content="{html.escape(alt, quote=True)}" />',
        '    <meta name="twitter:card" content="summary_large_image" />',
        f'    <meta name="twitter:site" content="{TWITTER}" />',
        f'    <meta name="twitter:title" content="{html.escape(og_title, quote=True)}" />',
        f'    <meta name="twitter:description" content="{html.escape(desc, quote=True)}" />',
        f'    <meta name="twitter:image" content="{image}" />',
    ]
    if cfg.get("hreflang"):
        for lang, _href in HREFLANG:
            alt_locale = OG_LOCALE.get(lang)
            if alt_locale and alt_locale != locale:
                lines.append(f'    <meta property="og:locale:alternate" content="{alt_locale}" />')
    if og_type == "article" and cfg.get("published"):
        lines.append(
            f'    <meta property="article:published_time" content="{cfg["published"]}" />'
        )
        lines.append('    <meta property="article:author" content="ilming" />')

    json_ld = build_json_ld(cfg, title, desc, image)
    if json_ld:
        lines.append(json_ld)
    for raw in faqs:
        lines.append('    <script type="application/ld+json">' + raw + "</script>")
    if cfg.get("hreflang"):
        lines.append(hreflang_html())
    return "\n".join(lines)


def extract_faqs(text: str) -> list:
    faqs = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if data.get("@type") == "FAQPage":
            faqs.append(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    return faqs


def sync_file(rel: str, cfg: dict) -> None:
    path = ROOT / rel
    if not path.exists():
        print(f"skip: {rel}")
        return
    text = path.read_text(encoding="utf-8")
    title = parse_title(text)
    description = parse_description(text)
    faqs = extract_faqs(text)
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

    block = seo_block(rel, cfg, title, description, faqs)

    # Remove existing SEO injection. FAQ markup is reattached from `faqs`.
    text = re.sub(r"\n?\s*<meta name=\"robots\"[^>]*>", "", text)
    text = re.sub(r"\n?\s*<link rel=\"canonical\"[^>]*>", "", text)
    text = re.sub(r'\n?\s*<link rel="alternate" href="[^"]+" hreflang="[^"]+"\s*/>', "", text)
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
Disallow: /demo-platform/

Sitemap: https://www.ilming.io/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(content, encoding="utf-8")
    print("updated: robots.txt")


SITE_LASTMOD = "2026-10-11"


def hreflang_xml() -> str:
    return "".join(
        f'<xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>'
        for lang, href in HREFLANG
    )


def update_sitemap() -> None:
    pricing_urls = {href for _lang, href in HREFLANG if _lang != "x-default"}
    urls = [
        (f"{SITE}/", "weekly", "1.0", SITE_LASTMOD),
        (f"{SITE}/platform/", "monthly", "0.9", SITE_LASTMOD),
        (f"{SITE}/features/", "monthly", "0.9", SITE_LASTMOD),
        (f"{SITE}/present/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/", "monthly", "0.9", SITE_LASTMOD),
        (f"{SITE}/pricing/usd/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/gbp/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/aed/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/sar/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/qar/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/kwd/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/bhd/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/pricing/omr/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/ai/", "monthly", "0.85", SITE_LASTMOD),
        (f"{SITE}/blog/", "weekly", "0.8", SITE_LASTMOD),
        (f"{SITE}/blog/why-your-madrassa-needs-an-lms/", "monthly", "0.7", "2026-05-15"),
        (f"{SITE}/blog/secure-online-exams-for-islamic-schools/", "monthly", "0.7", "2026-05-08"),
        (f"{SITE}/blog/ai-tools-for-islamic-educators/", "monthly", "0.7", "2026-04-28"),
        (f"{SITE}/blog/guardian-portal-build-parent-trust/", "monthly", "0.7", "2026-04-12"),
        (f"{SITE}/blog/digitising-madrassas-in-uk-and-uae/", "monthly", "0.7", "2026-03-22"),
        (f"{SITE}/about/", "monthly", "0.7", SITE_LASTMOD),
        (f"{SITE}/contact/", "monthly", "0.8", SITE_LASTMOD),
        (f"{SITE}/tahfiz-management-software/", "monthly", "0.9", SITE_LASTMOD),
        (f"{SITE}/blog/why-whatsapp-is-not-enough-for-hifz/", "monthly", "0.7", "2026-09-30"),
        (f"{SITE}/privacy-policy/", "yearly", "0.3", SITE_LASTMOD),
        (f"{SITE}/terms-and-conditions/", "yearly", "0.3", SITE_LASTMOD),
        (f"{SITE}/security/", "yearly", "0.4", SITE_LASTMOD),
        (f"{SITE}/subprocessors/", "yearly", "0.4", SITE_LASTMOD),
    ]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    alternates = hreflang_xml()
    for loc, freq, pri, mod in urls:
        extra = alternates if loc in pricing_urls else ""
        lines.append(
            f"  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority>{extra}</url>"
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
