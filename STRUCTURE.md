# ILMING Static Website – Folder Structure

## Target Structure

```
ilming/
├── index.html                 # Homepage
├── README.md
├── README-ILMING.md
├── STRUCTURE.md
│
├── assets/                    # All static assets (unified)
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript
│   ├── images/                # Icons, logos, UI images
│   ├── fonts/                 # Web fonts
│   ├── video/                 # Video files
│   └── media/                 # Content media (achievement, blog, program, etc.)
│       ├── achievement/
│       ├── blog/
│       ├── program/
│       ├── slider/
│       ├── testimonial/
│       └── ...
│
├── about/                     # About Us
├── blogs/                     # Blog posts + categories
│   ├── index.html
│   ├── category/              # Blog categories (merged from blog/category)
│   └── [post-slug]/
├── boards/                    # Education boards (CBSE, ICSE, etc.)
│   ├── cbse/
│   ├── icse/
│   ├── igcse/
│   └── state/
├── clubs/                     # Academic clubs
├── contact/                   # Contact & Become a Tutor
├── countries/                 # Country-specific pages
├── courses/                   # Academic courses (LKG, UKG, Montessori, etc.)
├── downloads/                 # Downloadable resources
├── language-courses/          # Language learning
├── location/                  # Location pages (online tuition by city)
├── news/                      # News & events
├── nonacademics/              # Non-academic index
├── nonacademic-courses/       # Skill courses (Vedic Math, Robotics, etc.)
├── privacy-policy/
├── smartest/                  # Mock tests
├── subject/                   # Subject tuition pages
├── terms-and-conditions/
├── testimonials/
└── tools/                     # Calculators (CGPA, grade conversion)
```

## Path Conventions

| Old Path           | New Path        |
|--------------------|-----------------|
| `static/web/css/`  | `assets/css/`   |
| `static/web/js/`   | `assets/js/`    |
| `static/web/images/` | `assets/images/` |
| `static/web/fonts/`  | `assets/fonts/`  |
| `static/web/video/`  | `assets/video/`  |
| `media/`           | `assets/media/`  |
| `blog/category/`   | `blogs/category/` |
| `board/`           | `boards/` (merged) |

## Naming Rules

- **Lowercase with hyphens**: `drawing-course` not `drawing-Course`
- **Plural for indexes**: `blogs`, `boards`, `courses`, `tools`
- **Consistent slugs**: kebab-case for URLs
- **No spaces in filenames**: use hyphens (e.g. `board-exam-2026-cbse.html`)

## Fixes Applied

- `malayalam-tution` → `malayalam-tuition` (typo)
- `Online-montessori-*` → `online-montessori-*` (lowercase)
- `drawing-Course` → `drawing-course`
- Removed `courses/Foundation-French` (redirect duplicate)
- Renamed files with spaces to kebab-case
- Added `.gitignore` for .DS_Store, etc.

## Removed (after migration)

- `cdn-cgi/` – Cloudflare email-decode script; removed (script refs stripped from HTML)
- `blog/` – merged into `blogs/category/`
- `board/` – merged into `boards/`
- `static/` – contents moved to `assets/`
- `media/` – contents moved to `assets/media/`
