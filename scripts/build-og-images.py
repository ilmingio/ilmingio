#!/usr/bin/env python3
"""Draw a 1200×630 share image for each public page."""
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "images" / "og"
ICON = ROOT / "assets" / "images" / "favicon" / "icon-512.png"

CREAM = (250, 247, 242)
NAVY = (12, 24, 41)
EMERALD = (10, 107, 92)
GOLD = (201, 168, 76)
MUTED = (61, 79, 73)

CARDS = {
    "home.png": "The operating system\nfor Tahfiz institutes",
    "platform.png": "One Hifz workflow.\nOne institute platform.",
    "features.png": "Hifz desk, Hafazan\npractice, and the LMS",
    "present.png": "A ten-minute tour\nof ilming",
    "pricing-inr.png": "India pricing\nINR 50 per student",
    "pricing-aed.png": "UAE pricing\nAED 4 per student",
    "pricing-sar.png": "Saudi Arabia pricing\nSAR 4 per student",
    "pricing-gbp.png": "United Kingdom pricing\n£1 per student",
    "pricing-qar.png": "Qatar pricing\nQAR 4 per student",
    "pricing-kwd.png": "Kuwait pricing\nKWD 0.300 per student",
    "pricing-bhd.png": "Bahrain pricing\nBHD 0.400 per student",
    "pricing-omr.png": "Oman pricing\nOMR 0.400 per student",
    "pricing-usd.png": "International pricing\n$1 per student",
    "ai.png": "AI Hafazan practice.\nThe Ustadh decides.",
    "blog.png": "Insights for\nIslamic educators",
    "blog-madrassa.png": "Why your madrassa\nneeds an LMS",
    "blog-exams.png": "Secure online exams\nfor Islamic schools",
    "blog-ai-tools.png": "AI tools for Islamic\neducators",
    "blog-guardian.png": "How a guardian portal\nbuilds parent trust",
    "blog-digitising.png": "Digitising madrassas\nin the UK and UAE",
    "blog-whatsapp.png": "Why WhatsApp is not\nenough for Hifz",
    "about.png": "Why ilming exists",
    "contact.png": "Book a demo for\nyour institute",
    "tahfiz.png": "Tahfiz management\nsoftware",
    "privacy.png": "Privacy Policy",
    "terms.png": "Terms and Conditions",
    "security.png": "Security",
    "subprocessors.png": "Subprocessors",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_card(title: str) -> Image.Image:
    image = Image.new("RGB", (1200, 630), CREAM)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 16), fill=EMERALD)
    draw.rectangle((0, 620, 1200, 630), fill=GOLD)

    icon = Image.open(ICON).convert("RGBA").resize((112, 112), Image.Resampling.LANCZOS)
    image.paste(icon, (76, 96), icon)

    brand = font(28, bold=True)
    draw.text((208, 118), "ilming", font=brand, fill=EMERALD)
    kicker = font(22)
    draw.text((208, 158), "Operating system for Tahfiz institutes", font=kicker, fill=MUTED)

    title_font = font(68, bold=True)
    draw.multiline_text((76, 280), title, font=title_font, fill=NAVY, spacing=8)
    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, title in CARDS.items():
        card = draw_card(title)
        card.save(OUT / name, "PNG", optimize=True)
        print(f"og: {name}")
    shutil.copyfile(OUT / "home.png", OUT / "ilming-og.png")
    print("og: ilming-og.png")


if __name__ == "__main__":
    main()
