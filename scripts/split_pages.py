"""
split_pages.py  –  accordion sidebar edition
Clicking a chapter header expands its sub-sections in-place in the sidebar.
"""
import re, os

# Calculate the root directory as the parent of this script's directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT_DIR, "system-design-complete.html")
OUT_DIR = "pages"
os.makedirs(OUT_DIR, exist_ok=True)

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

style_m = re.search(r"<style>(.*?)</style>", raw, re.DOTALL)
SHARED_STYLE = style_m.group(0) if style_m else ""

def extract_sections(html_text):
    sections = {}
    pattern = re.compile(r'<div class="section[^"]*"\s+id="([^"]+)"', re.DOTALL)
    for m in pattern.finditer(html_text):
        sec_id = m.group(1); start = m.start(); depth = 0; i = start
        while i < len(html_text):
            if html_text[i:i+4] == "<div":  depth += 1; i += 4
            elif html_text[i:i+6] == "</div>":
                depth -= 1; i += 6
                if depth == 0:
                    content = html_text[start:i]
                    if sec_id in sections:
                        sections["db-federation"] = content.replace(f'id="{sec_id}"', 'id="db-federation"', 1)
                    else:
                        sections[sec_id] = content
                    break
            else: i += 1
    if "disaster-recovery" in sections:
        sections["deployments"] = sections["disaster-recovery"]
    return sections

sections = extract_sections(raw)
print(f"Found {len(sections)} sections.")

PAGES = [
    {"file":"01-introduction.html","title":"Introduction to System Design",
     "module":"Introduction to SDI","icon":"🚀","num":"01",
     "sections":["intro"],"nav":[("intro","The SDI Process")]},
    {"file":"02-core-concepts.html","title":"Core Concepts & Basics",
     "module":"Glossary of Basics","icon":"📖","num":"02",
     "sections":["core","cap","pacelc","hashing"],
     "nav":[("core","Core Characteristics"),("cap","CAP & PACELC Theorems"),
            ("pacelc","PACELC In Depth"),("hashing","Consistent Hashing")]},
    {"file":"03-tradeoffs.html","title":"System Design Trade-offs",
     "module":"Trade-offs","icon":"⚖️","num":"03",
     "sections":["tradeoffs"],"nav":[("tradeoffs","Topic-by-Topic Trade-offs")]},
    {"file":"04-networking.html","title":"Networking Fundamentals",
     "module":"Networking","icon":"🌐","num":"04",
     "sections":["networking","proxy"],
     "nav":[("networking","OSI, TCP/UDP, HTTP, DNS"),("proxy","Proxy & Reverse Proxy")]},
    {"file":"05-infrastructure.html","title":"Infrastructure",
     "module":"Infrastructure","icon":"🏗️","num":"05",
     "sections":["lb","caching","cdn","storage"],
     "nav":[("lb","Load Balancing & Algorithms"),("caching","Caching Strategies"),
            ("cdn","CDN & Distributed Cache"),("storage","Storage Systems")]},
    {"file":"06-api-communication.html","title":"API & Communication",
     "module":"API & Communication","icon":"🔌","num":"06",
     "sections":["api-design","api-infra","api-auth","realtime","async"],
     "nav":[("api-design","API Design (REST, GraphQL, gRPC)"),
            ("api-infra","API Gateway & Rate Limiting"),
            ("api-auth","Authentication & Authorization"),
            ("realtime","Real-Time Communication"),
            ("async","Async Messaging (Queues, Pub/Sub)")]},
    {"file":"07-architecture.html","title":"Architecture Patterns",
     "module":"Architecture","icon":"🏛️","num":"07",
     "sections":["arch-patterns","microservices","containers"],
     "nav":[("arch-patterns","Architectural Patterns"),
            ("microservices","Microservices & Service Mesh"),
            ("containers","Containers & Orchestration")]},
    {"file":"08-data-layer.html","title":"Data Layer",
     "module":"Data Layer","icon":"🗄️","num":"08",
     "sections":["db-types","db-internals","db-scaling"],
     "nav":[("db-types","Database Types"),("db-internals","Database Internals"),
            ("db-scaling","Database Scaling")]},
    {"file":"09-distributed-systems.html","title":"Distributed Systems",
     "module":"Distributed Systems","icon":"🕸️","num":"09",
     "sections":["db-federation","dist-fundamentals","time-ordering",
                 "consensus","dist-tx","data-structures","big-data"],
     "nav":[("db-federation","Database Federation"),
            ("dist-fundamentals","Challenges & Failures"),
            ("time-ordering","Time, Ordering & Clocks"),
            ("consensus","Consensus & Coordination"),
            ("dist-tx","Distributed Transactions"),
            ("data-structures","Design Data Structures"),
            ("big-data","Big Data & Stream Processing")]},
    {"file":"10-search-operations.html","title":"Search, Operations & Security",
     "module":"Search, Ops & Security","icon":"🔍","num":"10",
     "sections":["search","disaster-recovery","observability","security"],
     "nav":[("search","FTS, Inverted Index, Ranking"),
            ("disaster-recovery","Disaster Recovery & Deployments"),
            ("observability","Logs, Metrics, Tracing"),
            ("security","Encryption, IAM, Zero Trust")]},
    {"file":"11-interview-framework.html","title":"Interview Framework",
     "module":"Interview Framework","icon":"🎯","num":"11",
     "sections":["framework"],"nav":[("framework","The 4-Step SDI Framework")]},
    {"file":"12-coding-interview-patterns.html","title":"Coding Interview Patterns",
     "module":"Coding Patterns","icon":"🧩","num":"12",
     "sections":["patterns"],"nav":[("patterns","20 Essential Patterns")]},
    {"file":"../case_studies/open-table.html","title":"Case Studies",
     "module":"Case Studies","icon":"📚","num":"13",
     "sections":["case-opentable"],"nav":[("case-opentable","Design OpenTable (Deep Dive)")]},
]

# ── Accordion sidebar HTML ────────────────────────────────────────────────────
def accordion_sidebar(current_file, current_first_sec):
    html = ""
    for p in PAGES:
        is_cur = p["file"] == current_file
        open_attr = ' open' if is_cur else ''
        cur_badge = '<span class="chap-curr">●</span>' if is_cur else ''

        # Build sub-items
        sub_items = ""
        for sec_id, label in p["nav"]:
            if is_cur:
                active_cls = ' class="acc-sub-item active"' if sec_id == current_first_sec else ' class="acc-sub-item"'
                sub_items += f'              <div{active_cls} data-sec="{sec_id}">{label}</div>\n'
            else:
                # Cross-page: link to other page with hash to activate section
                target_link = p["file"]
                if current_file.startswith("../") and not target_link.startswith("../"):
                    # Current is in case_studies, target is in pages
                    target_link = "../pages/" + target_link
                elif not current_file.startswith("../") and target_link.startswith("../"):
                    # Current is in pages, target is in case_studies (already has ../)
                    pass 
                
                sub_items += f'              <a class="acc-sub-item" href="{target_link}#{sec_id}">{label}</a>\n'

        html += f"""        <details class="acc-chapter"{open_attr}>
          <summary class="acc-summary">
            <span class="chap-icon">{p['icon']}</span>
            <span class="chap-text">
              <span class="chap-num">Chapter {p['num']}</span>
              <span class="chap-label">{p['module']}</span>
            </span>
            {cur_badge}
            <span class="acc-arrow">›</span>
          </summary>
          <div class="acc-sub">
{sub_items}          </div>
        </details>\n"""
    return html

# Central CSS/JS links
COMMON_ASSETS = """
  <link rel="stylesheet" href="../assets/css/system-design-common.css">
  <script defer src="../assets/js/system-design-common.js"></script>
"""

def fix_section_class(content, sec_id, is_first):
    css_class = "section active" if is_first else "section"
    return re.sub(
        r'<div class="section[^"]*"\s+id="'+re.escape(sec_id)+'"',
        f'<div class="{css_class}" id="{sec_id}"',
        content, count=1
    )

# ── Build all pages ───────────────────────────────────────────────────────────
for idx, page in enumerate(PAGES):
    # Remove the manual skip for Chapter 12 so it gets the correct sidebar
        
    prev_page = PAGES[idx-1]["file"] if idx > 0 else None
    next_page = PAGES[idx+1]["file"] if idx < len(PAGES)-1 else None

    first_sec = page["nav"][0][0] if page["nav"] else ""

    accordion_html = accordion_sidebar(page["file"], first_sec)

    sections_html = ""
    first = True
    for sec_id in page["sections"]:
        if sec_id not in sections:
            print(f"  WARNING: '{sec_id}' not found")
            continue
        content = fix_section_class(sections[sec_id], sec_id, first)
        sections_html += content + "\n\n"
        first = False

    is_case_study = page["file"].startswith("../case_studies")
    def format_link(link):
        if not link: return ""
        if is_case_study and not link.startswith("../"):
            return "../pages/" + link
        return link

    prev_link = format_link(prev_page)
    next_link = format_link(next_page)
    all_topics_link = format_link("01-introduction.html")

    prev_btn = (f'<a class="page-nav-btn" href="{prev_link}">&#8592; {PAGES[idx-1]["module"]}</a>'
                if prev_page else '<span></span>')
    next_btn = (f'<a class="page-nav-btn" href="{next_link}">{PAGES[idx+1]["module"]} &#8594;</a>'
                if next_page else '<span></span>')

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="System Design Reference — {page['title']}">
  <title>{page['icon']} {page['title']} — System Design Fundamentals</title>
  <link rel="stylesheet" href="../assets/css/styles.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  {SHARED_STYLE}
  {COMMON_ASSETS}
  {'<script defer src="../assets/js/pattern-animations.js"></script>' if "12-coding-interview-patterns" in page["file"] else ''}
</head>
<body>
  <div class="layout">

    <nav class="sidebar" style="display:flex;flex-direction:column">
      <div class="sidebar-header">
        <div style="margin-bottom:14px">
          <a href="../index.html" class="back-link">&#8592; Back to Home</a>
        </div>
        <h1>System Design Fundamentals</h1>
        <p>180+ topics &nbsp;|&nbsp; Complete Reference</p>
      </div>

      <div class="sidebar-accordion">
{accordion_html}      </div>
    </nav>

    <div class="main">
      <div class="progress-bar-wrap"><div class="progress-bar" id="pb"></div></div>

{sections_html}
      <div class="page-nav">
        {prev_btn}
        <a class="page-nav-btn home" href="{all_topics_link}">&#9776; All Topics</a>
        {next_btn}
      </div>
    </div>
  </div>

  <button id="back-to-top" title="Back to top" aria-label="Back to top">&#8593;</button>

  <script>
    if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose'
        }});
    }}
  </script>
</body>
</html>
"""
    out_path = os.path.join(OUT_DIR, page["file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    sz = round(os.path.getsize(out_path) / 1024)
    print(f"  {page['icon']} {out_path}  ({sz} KB)")

print("\n✅ Accordion sidebar done!")
