# Scripts — Pipeline Reference

This folder contains all code-generation scripts for the site. **Always run commands from the project root**, not from inside this folder.

---

## 🏗️ Site Architecture

```
system-design-complete.html   ← source of truth (monolith)
        │
        ▼  python3 scripts/split_pages.py
pages/*.html                  ← generated system design chapter pages
case_studies/*.html           ← generated case study pages

scripts/items.json            ← Blind 75 problem manifest  
        │
        ▼  python3 scripts/build_blind75_pages.py
blind75/*.html                ← generated Blind 75 problem pages

scripts/top150_items.json     ← Top Interview 150 manifest (from LeetCode API)
        │
        ▼  python3 scripts/build_top150_pages.py
top150/*.html                 ← generated Top 150 problem pages
```

---

## 📋 Active Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `split_pages.py` | Rebuild all system design pages from the monolith | `python3 scripts/split_pages.py` |
| `build_blind75_pages.py` | Generate individual Blind 75 HTML pages | `python3 scripts/build_blind75_pages.py` |
| `build_top150_pages.py` | Generate individual Top 150 HTML pages | `python3 scripts/build_top150_pages.py` |
| `fetch_top150.py` | Re-fetch Top 150 problem list from LeetCode API | `python3 scripts/fetch_top150.py` |
| `shared_generator.py` | HTML injection engine for Blind 75 content | *imported by batch scripts* |
| `run_all_batches.py` | Run all Blind 75 content batches to inject into SPA | `python3 scripts/run_all_batches.py` |
| `generate_all_problems.py` | Generate Blind 75 content via Gemini API | `GOOGLE_API_KEY=... python3 scripts/generate_all_problems.py` |
| `generate_content.py` | Hardcoded Blind 75 problem data (no API needed) | *imported by run_all_batches.py* |
| `generate_top150_content.py` | Generate Top 150 content via Gemini API | `GOOGLE_API_KEY=... python3 scripts/generate_top150_content.py` |
| `replace_blind75_nav.py` | One-time nav fix for Blind 75 pages | run once if nav breaks |
| `inject_pattern_details.py` | Injects content into coding pattern pages | run once per pattern |
| `validate_monolith.py` | Validates the monolith has all 38 sections | `python3 scripts/validate_monolith.py` |

## 📦 Blind 75 Content Batches

These files hold the pre-authored problem data injected by `shared_generator.py`:
- `batch2_content.py` — problems in batch 2
- `batch3_content.py` — problems in batch 3
- `batch6_content.py` — problems in batch 6
- `batch7_content.py` — problems in batch 7
- `batch8_content.py` — problems in batch 8
- `batch9_content.py` — problems in batch 9

## 📁 Data Files

| File | Description |
|------|-------------|
| `items.json` | Blind 75 sidebar manifest |
| `top150_items.json` | Top Interview 150 problem list (fetched from LeetCode) |
| `templates/top150_template.html` | HTML shell template for Top 150 pages |

## 🚀 Quickstart (also see root Makefile)

```bash
# Rebuild everything after editing system-design-complete.html
make site

# Add new Blind 75 problem content
# Edit a batch*_content.py file, then:
python3 scripts/run_all_batches.py
python3 scripts/build_blind75_pages.py

# Regenerate Top 150 from scratch  
python3 scripts/fetch_top150.py
python3 scripts/build_top150_pages.py
```
