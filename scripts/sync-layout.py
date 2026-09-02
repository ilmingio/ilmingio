#!/usr/bin/env python3
"""Sync unified site header and footer across all marketing pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_VER = "20260815"
SW_VER = "20260815"

PAGES = [
    ("index.html", "assets/", False),
    ("404.html", "/assets/", False),
    ("platform/index.html", "../assets/", False),
    ("features/index.html", "../assets/", False),
    ("pricing/index.html", "../assets/", False),
    ("pricing/usd/index.html", "../../assets/", False),
    ("about/index.html", "../assets/", False),
    ("contact/index.html", "../assets/", False),
    ("ai/index.html", "../assets/", False),
    ("privacy-policy/index.html", "../assets/", False),
    ("terms-and-conditions/index.html", "../assets/", False),
    ("blog/index.html", "../assets/", False),
    ("blog/why-your-madrassa-needs-an-lms/index.html", "../../assets/", False),
    ("blog/secure-online-exams-for-islamic-schools/index.html", "../../assets/", False),
    ("blog/ai-tools-for-islamic-educators/index.html", "../../assets/", False),
    ("blog/guardian-portal-build-parent-trust/index.html", "../../assets/", False),
    ("blog/digitising-madrassas-in-uk-and-uae/index.html", "../../assets/", False),
]


def js_prefix(asset_prefix: str) -> str:
    if asset_prefix.startswith("/"):
        return "/assets/js/"
    return asset_prefix.replace("assets/", "assets/js/")


def pwa_head_block(ap: str) -> str:
    return f"""    <link rel="icon" href="{ap}images/favicon/favicon.svg" type="image/svg+xml" />
    <link rel="icon" href="{ap}images/favicon/favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" sizes="32x32" href="{ap}images/favicon/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="{ap}images/favicon/favicon-16x16.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="{ap}images/favicon/apple-touch-icon.png" />
    <link rel="manifest" href="{ap}images/favicon/site.webmanifest" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="ilming" />
    <meta name="mobile-web-app-capable" content="yes" />"""


PWA_HEAD_PAT = re.compile(
    r'<link rel="icon" href="[^"]*favicon\.svg"[^>]*/>\s*'
    r'(?:<link rel="icon"[^>]*/>\s*)*'
    r'(?:<link rel="apple-touch-icon"[^>]*/>\s*)?'
    r'(?:<link rel="manifest"[^>]*/>\s*)?'
    r'(?:<meta name="apple-mobile-web-app-capable"[^>]*/>\s*)?'
    r'(?:<meta name="apple-mobile-web-app-title"[^>]*/>\s*)?'
    r'(?:<meta name="mobile-web-app-capable"[^>]*/>\s*)?',
    re.DOTALL,
)


def sync_pwa_head(text: str, asset_prefix: str) -> str:
    block = pwa_head_block(asset_prefix)
    if PWA_HEAD_PAT.search(text):
        return PWA_HEAD_PAT.sub(block, text, count=1)
    insert_before = re.search(r'\s*<link rel="preconnect"', text)
    if insert_before:
        return text[: insert_before.start()] + "\n" + block + text[insert_before.start() :]
    insert_before = re.search(r'\s*<link rel="stylesheet"', text)
    if insert_before:
        return text[: insert_before.start()] + "\n" + block + text[insert_before.start() :]
    print("warn: could not insert PWA head block")
    return text


def header_block(ap: str, noscript: bool) -> str:
    ns = ""
    if noscript:
        ns = (
            '    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-W6FCQMT3" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
        )
    return f"""{ns}    <div class="scroll-indicator" id="scrollIndicator"></div>

    <div class="site-announcement" id="siteAnnouncement" role="region" aria-label="Announcement">
      <div class="site-announcement__inner">
        <p class="site-announcement__text">
          <strong>Virtual Ustadh</strong> + full Islamic LMS — Tahfiz · Hifz · Academy · UK · UAE · India · GCC
        </p>
        <a href="/contact/" class="site-announcement__link">Book a demo</a>
        <button type="button" class="site-announcement__dismiss" id="announceDismiss" aria-label="Dismiss announcement">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
      </div>
    </div>

    <header class="site-nav" id="navbar">
      <div class="nav-inner">
        <a href="/" class="brand">
          <img src="{ap}images/logo/ilming_icon-mark.svg?v=20260902" alt="" class="brand__icon brand__icon--mark" width="44" height="44" aria-hidden="true" />
          <span class="brand__lockup">
            <span class="brand__name">ilming</span>
            <span class="brand__tagline">Islamic LMS Platform</span>
          </span>
        </a>
        <ul class="nav-links nav-desktop-only">
          <li><a href="/platform/">Platform</a></li>
          <li><a href="/features/">Features</a></li>
          <li><a href="/ai/">AI</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
        <div class="nav-actions nav-desktop-only">
          <a href="/login" class="nav-btn nav-btn-outline" data-app-link="/login">Log in</a>
          <a href="/contact/" class="nav-btn nav-btn-primary">Book a demo</a>
        </div>
        <button type="button" class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav">
          <svg class="menu-toggle__icon menu-toggle__icon--open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
          <svg class="menu-toggle__icon menu-toggle__icon--close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
      </div>
    </header>
    <button type="button" class="mobile-nav-backdrop" id="navBackdrop" aria-label="Close menu" tabindex="-1"></button>
    <nav class="mobile-nav" id="mobileNav" aria-label="Main menu">
      <span class="mobile-nav__label">Menu</span>
      <a href="/platform/">Platform</a>
      <a href="/features/">Features</a>
      <a href="/ai/">AI</a>
      <a href="/pricing/">Pricing</a>
      <a href="/blog/">Blog</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/login" class="nav-btn nav-btn-outline" data-app-link="/login">Log in</a>
      <a href="/contact/" class="nav-btn nav-btn-primary">Book a demo</a>
    </nav>"""


def footer_block(ap: str, compact_cta: bool) -> str:
    cta_title = "Questions about your institute?" if compact_cta else "Ready to modernise your institute?"
    cta_sub = "Book a demo or start a 14-day pilot — we'll set up your admin account."
    return f"""    <footer class="site-footer">
      <div class="footer-cta">
        <div class="container footer-cta__inner">
          <div class="footer-cta__copy">
            <h3>{cta_title}</h3>
            <p>{cta_sub}</p>
          </div>
          <div class="footer-cta__actions">
            <a href="/contact/" class="cta-button gold">Book a demo</a>
            <a href="/pricing/" class="cta-button secondary footer-cta__secondary">View pricing</a>
          </div>
        </div>
      </div>
      <div class="footer-main">
        <div class="footer-grid">
          <div class="footer-brand">
            <a href="/" class="brand brand--footer">
              <img src="{ap}images/logo/ilming_icon.svg?v=20260902" alt="" class="brand__icon" width="44" height="44" aria-hidden="true" />
              <span class="brand__lockup">
                <span class="brand__name">ilming</span>
                <span class="brand__tagline">Islamic LMS Platform</span>
              </span>
            </a>
            <p>
              AI-powered Quran learning and Islamic LMS for Tahfiz institutes, madrassas, and
              Islamic schools — Hifz tracking, Virtual Ustadh, exams, fees, and guardian visibility.
            </p>
            <div class="footer-regions" aria-label="Regions served">
              <span class="footer-region">UK</span>
              <span class="footer-region">UAE</span>
              <span class="footer-region">India</span>
              <span class="footer-region">GCC</span>
            </div>
            <p class="footer-tagline">ilming.io — Islamic learning software</p>
          </div>
          <div class="footer-col">
            <h4>Product</h4>
            <ul>
              <li><a href="/platform/">Platform</a></li>
              <li><a href="/features/">Features</a></li>
              <li><a href="/ai/">AI &amp; Virtual Ustadh</a></li>
              <li><a href="/present/">Product tour</a></li>
              <li><a href="/demo-platform/">Demo guide</a></li>
              <li><a href="/pricing/">Pricing</a></li>
              <li><a href="/login" data-app-link="/login">Log in</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Company</h4>
            <ul>
              <li><a href="/about/">About</a></li>
              <li><a href="/contact/">Contact</a></li>
              <li><a href="/verify" data-app-link="/verify">Verify certificate</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Resources</h4>
            <ul>
              <li><a href="/blog/">Blog</a></li>
              <li><a href="/blog/why-your-madrassa-needs-an-lms/">Madrassa LMS guide</a></li>
              <li><a href="/blog/secure-online-exams-for-islamic-schools/">Exam security</a></li>
              <li><a href="/ai/">AI for educators</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Legal</h4>
            <ul>
              <li><a href="/privacy-policy/">Privacy policy</a></li>
              <li><a href="/terms-and-conditions/">Terms &amp; conditions</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© <span id="footerYear">2026</span> ilming. All rights reserved.</p>
          <p class="footer-note">ilming.io is an Islamic LMS software platform — not affiliated with third-party stationery brands.</p>
        </div>
      </div>
    </footer>"""


def scripts_block(ap: str, analytics: bool = True) -> str:
    jp = js_prefix(ap)
    lines = [
        f'    <script src="{jp}config.js"></script>',
        f'    <script src="{jp}site.js?v={CSS_VER}"></script>',
    ]
    if analytics:
        lines.append(f'    <script src="{jp}analytics.js"></script>')
    return "\n".join(lines)


def strip_dup_noscript(text: str) -> str:
    ns = re.compile(
        r"\s*<noscript>\s*<iframe src=\"https://www.googletagmanager.com/ns.html[^>]*>\s*</iframe>\s*</noscript>",
        re.I,
    )
    matches = list(ns.finditer(text))
    if len(matches) <= 1:
        return text
    for m in reversed(matches[1:]):
        text = text[: m.start()] + text[m.end() :]
    return text


def sync_file(rel: str, asset_prefix: str, is_home: bool) -> None:
    path = ROOT / rel
    if not path.exists():
        print(f"skip (missing): {rel}")
        return
    text = path.read_text(encoding="utf-8")
    text = strip_dup_noscript(text)
    noscript = "noscript" in text and rel != "404.html"

    # Replace header + any duplicated mobile nav blocks after it
    header_pat = re.compile(
        r"(?:<div class=\"scroll-indicator\".*?</header>|<header class=\"site-nav\".*?</header>)"
        r"(?:\s*<button type=\"button\" class=\"mobile-nav-backdrop\".*?</button>"
        r"\s*<nav class=\"mobile-nav\".*?</nav>)+",
        re.DOTALL,
    )
    if not header_pat.search(text):
        # 404 has no header yet
        if rel == "404.html":
            text = text.replace(
                "<body>",
                "<body>\n" + header_block(asset_prefix, False),
            )
        else:
            print(f"warn: no header match in {rel}")
    else:
        text = header_pat.sub(header_block(asset_prefix, False), text, count=1)

    # Replace footer
    footer_pat = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.DOTALL)
    if footer_pat.search(text):
        text = footer_pat.sub(footer_block(asset_prefix, is_home), text, count=1)
    elif rel == "404.html":
        text = text.replace(
            "</section>",
            "</section>\n\n" + footer_block(asset_prefix, False),
            1,
        )

    # Normalize PWA icon/manifest tags
    text = sync_pwa_head(text, asset_prefix)

    # Update CSS version
    text = re.sub(r"site\.css\?v=[\w.]+", f"site.css?v={CSS_VER}", text)
    text = re.sub(r"site\.js\?v=[\w.]+", f"site.js?v={CSS_VER}", text)

    # Normalize script block before </body>
    script_pat = re.compile(
        r"\s*<script src=\"[^\"]*config\.js\"></script>.*?(\s*</body>)",
        re.DOTALL,
    )
    analytics = "analytics.js" in text or rel != "404.html"
    if script_pat.search(text):
        text = script_pat.sub("\n" + scripts_block(asset_prefix, analytics) + r"\1", text)

    path.write_text(text, encoding="utf-8")
    print(f"updated: {rel}")


def main() -> None:
    for rel, ap, _ in PAGES:
        sync_file(rel, ap, rel == "index.html")
    print("done.")


if __name__ == "__main__":
    main()
