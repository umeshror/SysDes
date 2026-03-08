# SysDes — Interview-Ready Design Guide & Coding Playbook

A static portfolio site and interactive interview prep platform combining:
- **System Design Playbook** — 12 chapters, 180+ topics, case studies
- **Blind 75** — 75 level coding problems with optimal solutions (Python/Java/Go)
- **Top Interview 150** — All 150 LeetCode top interview problems
- **20 Coding Patterns** — Animated visualizations + editorial deep-dives

---

## 🏗️ Architecture

```
SysDes/
├── index.html                       # Portfolio homepage + hub
│
├── pages/                           # System Design chapters (auto-generated)
│   ├── 01-introduction.html
│   ├── 02-core-concepts.html
│   └── ...12 chapters + case studies
│
├── blind75/                         # Blind 75 coding problems (auto-generated)
│   ├── index.html                   # Redirects to first problem
│   ├── question.css                 # Shared CSS for all problem pages  
│   └── 01-*.html ... 75-*.html
│
├── top150/                          # Top Interview 150 (auto-generated)
│   ├── index.html
│   └── 001-*.html ... 150-*.html
│
├── patterns/                        # 20 Coding Pattern deep-dives
│   ├── 01-sliding-window.html
│   └── ...20 patterns
│
├── case_studies/                    # Extended case studies
│   └── open-table.html
│
├── assets/
│   ├── css/                         # Shared stylesheets
│   │   ├── design-tokens.css        # Brand colours, typography tokens
│   │   └── styles.css               # System Design pages CSS
│   ├── js/                          # Shared JS
│   │   ├── system-design-common.js  # Sidebar, accordion, progress bar
│   │   └── pattern-animations.js    # Canvas-based pattern animations
│   └── patterns/                    # Infographic PNGs for each pattern
│
├── scripts/                         # All code generators (see scripts/README.md)
│   ├── split_pages.py               # ← Rebuild system design pages
│   ├── build_blind75_pages.py       # ← Rebuild Blind 75 pages
│   ├── build_top150_pages.py        # ← Rebuild Top 150 pages
│   └── README.md                    # Full pipeline reference
│
└── system-design-complete.html      # ⚠️ SOURCE OF TRUTH — edit here, then run make site
```

---

## 🚀 Getting Started

```bash
# Install Python deps
pip install beautifulsoup4 requests google-generativeai

# Rebuild everything
make site

# Serve locally (Python built-in server)
make serve
# Then open http://localhost:8080
```

---

## 🔧 Common Workflows

### After editing the System Design content:
```bash
# Edit system-design-complete.html, then regenerate pages:
make site
```

### Add a new Blind 75 problem with full content:
```bash
# 1. Add problem data to a batch*_content.py file
# 2. Run the injector
python3 scripts/run_all_batches.py
# 3. Rebuild individual pages
python3 scripts/build_blind75_pages.py
```

### Generate Top 150 content via AI:
```bash
export GOOGLE_API_KEY="your-key-here"
python3 scripts/generate_top150_content.py
python3 scripts/build_top150_pages.py
```

### Refresh Top 150 problem list from LeetCode:
```bash
python3 scripts/fetch_top150.py   # updates scripts/top150_items.json
python3 scripts/build_top150_pages.py
```

### Validate the system design monolith:
```bash
python3 scripts/validate_monolith.py
```

---

## 📐 Design Tokens

All sections share CSS custom properties from `assets/css/design-tokens.css`:

| Token | Value | Usage |
|-------|-------|-------|
| `--dt-accent` | `#00ffd5` | Cyan — active states, badges |
| `--dt-bg` | `#03050d` | Deep navy — page background |
| `--dt-surface` | `#070c1a` | Sidebar background |
| `--dt-card` | `#0b1120` | Card / panel background |
| `--dt-border` | `#131d35` | Borders, dividers |
| `--dt-text` | `#c8d4f0` | Primary text |
| `--dt-muted` | `#3a4a70` | Secondary / placeholder text |
| `--dt-font` | `'Inter', system-ui, sans-serif` | Brand font |

---

## 🏃 Make Targets

| Target | Description |
|--------|-------------|
| `make site` | Rebuild all system design pages from the monolith |
| `make blind75` | Rebuild all Blind 75 problem pages |
| `make top150` | Rebuild all Top 150 problem pages |
| `make serve` | Start local HTTP server on port 8080 |
| `make validate` | Validate the monolith has all sections |
| `make clean` | Remove Python `__pycache__` dirs |

---

## 🌐 Live Site
Deployed to GitHub Pages via the `refactor-inline-css` branch.
