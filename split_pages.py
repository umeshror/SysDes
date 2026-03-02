"""
split_pages.py  –  accordion sidebar edition
Clicking a chapter header expands its sub-sections in-place in the sidebar.
"""
import re, os

SRC = "system-design-complete.html"
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
    {"file":"../case_studies/open-table.html","title":"Case Studies",
     "module":"Case Studies","icon":"📚","num":"12",
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
                # Same-page: JS-driven section switch
                active_cls = ' class="acc-sub-item active"' if sec_id == current_first_sec else ' class="acc-sub-item"'
                sub_items += f'              <div{active_cls} data-sec="{sec_id}">{label}</div>\n'
            else:
                # Cross-page: link to other page with hash to activate section
                sub_items += f'              <a class="acc-sub-item" href="{p["file"]}#{sec_id}">{label}</a>\n'

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

# ── Sidebar CSS ───────────────────────────────────────────────────────────────
SIDEBAR_CSS = """
  <style id="sidebar-improvements">
    .sidebar { width: 280px; }
    .main    { margin-left: 280px; }

    /* Header */
    .sidebar-header {
      background: linear-gradient(160deg,#1e1e3f 0%,#12122a 100%);
      border-bottom: 1px solid rgba(137,180,250,0.12);
    }
    .sidebar-header h1 { font-size:.9rem; color:#e2e8f9; letter-spacing:.3px; }
    .sidebar-header p  { font-size:.72rem; color:#6272a4; }

    .back-link {
      display:inline-flex; align-items:center; gap:6px;
      font-size:.75rem; color:#89b4fa; text-decoration:none;
      padding:4px 12px; border:1px solid rgba(137,180,250,.25);
      border-radius:20px; transition:all .2s;
    }
    .back-link:hover { background:rgba(137,180,250,.1); border-color:#89b4fa; }

    /* Accordion wrapper */
    .sidebar-accordion {
      overflow-y: auto;
      flex: 1;
      padding: 8px 0 24px;
    }

    /* Accordion chapter */
    .acc-chapter {
      border-bottom: 1px solid rgba(137,180,250,0.07);
    }
    .acc-chapter[open] { background: rgba(137,180,250,0.04); }

    /* Summary row = clickable chapter header */
    .acc-summary {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      cursor: pointer;
      list-style: none;
      user-select: none;
      transition: background 0.15s;
    }
    .acc-summary::-webkit-details-marker { display: none; }
    .acc-summary:hover { background: rgba(137,180,250,0.08); }
    .acc-chapter[open] > .acc-summary { background: rgba(137,180,250,0.1); }

    .chap-icon {
      font-size: 1rem;
      flex-shrink: 0;
      width: 24px;
      text-align: center;
    }
    .chap-text {
      display: flex;
      flex-direction: column;
      gap: 1px;
      flex: 1;
      min-width: 0;
    }
    .chap-num {
      font-size: .58rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .8px;
      color: #585b70;
    }
    .chap-label {
      font-size: .8rem;
      color: #a6adc8;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .acc-chapter[open] .chap-num   { color: #89b4fa; }
    .acc-chapter[open] .chap-label { color: #cdd6f4; font-weight: 600; }

    .chap-curr {
      font-size: .45rem;
      color: #89b4fa;
      flex-shrink: 0;
      animation: blink 2s infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }

    .acc-arrow {
      font-size: .85rem;
      color: #585b70;
      flex-shrink: 0;
      transition: transform 0.2s;
    }
    .acc-chapter[open] .acc-arrow { transform: rotate(90deg); color:#89b4fa; }

    /* Sub-items panel */
    .acc-sub {
      padding: 2px 0 6px 0;
      animation: slideDown .18s ease;
    }
    @keyframes slideDown {
      from { opacity:0; transform:translateY(-6px); }
      to   { opacity:1; transform:translateY(0); }
    }

    .acc-sub-item {
      display: block;
      padding: 7px 14px 7px 48px;
      font-size: .78rem;
      color: #7f849c;
      cursor: pointer;
      border-left: 2px solid transparent;
      text-decoration: none;
      transition: all 0.14s;
      line-height: 1.35;
    }
    .acc-sub-item:hover {
      color: #cdd6f4;
      background: rgba(137,180,250,0.07);
      border-left-color: rgba(137,180,250,.4);
    }
    .acc-sub-item.active {
      color: #cdd6f4;
      background: rgba(137,180,250,0.12);
      border-left-color: #89b4fa;
      font-weight: 600;
    }

    /* Page nav */
    .page-nav {
      display:flex; justify-content:space-between; align-items:center;
      padding:28px 40px 48px; border-top:1px solid #e0e4f0;
      margin-top:24px; gap:12px;
    }
    .page-nav-btn {
      display:inline-flex; align-items:center; gap:8px;
      padding:10px 22px; background:#1a1a2e; color:#cdd6f4;
      border-radius:8px; text-decoration:none; font-size:.84rem;
      font-weight:600; transition:all .18s;
      border:1px solid rgba(137,180,250,.15);
    }
    .page-nav-btn:hover {
      background:#313244; border-color:rgba(137,180,250,.35);
      transform:translateY(-1px); box-shadow:0 4px 12px rgba(0,0,0,.2);
    }
    .page-nav-btn.home { background:linear-gradient(135deg,#1e3a5f,#162d48); }
    .page-nav-btn.home:hover { background:linear-gradient(135deg,#264a78,#1e3a5f); }

    @media (max-width:768px) { .sidebar{width:100%} .main{margin-left:0} }

    /* ── Mermaid diagram consistency ── */
    .mermaid {
      background: transparent !important;
      padding: 0 !important;
    }
    .mermaid svg {
      background: transparent !important;
      max-width: 100%;
    }
    /* Override Mermaid's internal background rect (dark in state/sequence diagrams) */
    .mermaid svg > rect:first-child,
    .mermaid svg > g:first-child > rect:first-child {
      fill: transparent !important;
      stroke: none !important;
    }
    /* State diagram node styling */
    .mermaid .state-note rect,
    .mermaid .note rect { fill: #fffbdd !important; stroke: #e6d87a !important; }
    /* Ensure subgraph labels are readable */
    .mermaid .cluster rect { fill: #f1f5f9 !important; stroke: #cbd5e1 !important; }
    .mermaid .cluster text { fill: #475569 !important; }
    /* Entity / node labels */
    .mermaid .label { color: #1e293b !important; }
    .mermaid .nodeLabel { color: #1e293b !important; }
    .mermaid .edgeLabel { background: #fff !important; color: #475569 !important; }
  </style>
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
  <link rel="stylesheet" href="../styles.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  {SHARED_STYLE}
{SIDEBAR_CSS}
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
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'default',
      themeVariables: {{
        primaryColor: '#e8f4fd',
        primaryTextColor: '#1e293b',
        primaryBorderColor: '#93c5fd',
        lineColor: '#64748b',
        secondaryColor: '#f0fdf4',
        tertiaryColor: '#faf5ff',
        background: '#ffffff',
        mainBkg: '#f8fafc',
        nodeBorder: '#cbd5e1',
        clusterBkg: '#f1f5f9',
        titleColor: '#1e293b',
        edgeLabelBackground: '#ffffff',
        attributeBackgroundColorEven: '#f8fafc',
        attributeBackgroundColorOdd: '#f1f5f9'
      }},
      flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
      sequence: {{ useMaxWidth: true }},
      stateDiagram: {{ useMaxWidth: true }},
      securityLevel: 'loose'
    }});

    // ── Section switching (same-page nav items only) ──
    const pageSections = document.querySelectorAll('.section');
    const subItems     = document.querySelectorAll('.acc-sub-item[data-sec]');
    const pb           = document.getElementById('pb');

    function showSection(id) {{
      pageSections.forEach(s => s.classList.remove('active'));
      subItems.forEach(n => n.classList.remove('active'));
      const target = document.getElementById(id);
      if (target) {{
        target.classList.add('active');
        const diags = target.querySelectorAll('.mermaid:not([data-processed])');
        if (diags.length) mermaid.run({{ nodes: diags }});
        // Scroll content area to top, NOT the whole window
        const main = document.querySelector('.main');
        if (main) main.scrollTo(0, 0);
      }}
      const item = document.querySelector(`.acc-sub-item[data-sec="${{id}}"]`);
      if (item) item.classList.add('active');
      updateProgress(id);
    }}

    function updateProgress(activeId) {{
      const ids = Array.from(subItems).map(n => n.dataset.sec);
      const idx = ids.indexOf(activeId);
      const pct = idx >= 0 ? Math.round(((idx + 1) / ids.length) * 100) : 0;
      pb.style.width = pct + '%';
    }}

    subItems.forEach(item => {{
      item.addEventListener('click', () => {{
        if (item.dataset.sec) showSection(item.dataset.sec);
      }});
    }});

    // On load: check URL hash for deep link from another page
    const hash = window.location.hash.slice(1);
    if (hash && document.getElementById(hash)) {{
      showSection(hash);
    }} else if (subItems.length) {{
      showSection(subItems[0].dataset.sec);
    }}

    // Scroll progress
    const mainEl = document.querySelector('.main');
    if (mainEl) {{
      mainEl.style.overflowY = 'auto';
      mainEl.style.height = '100vh';
      mainEl.addEventListener('scroll', () => {{
        const scrolled = mainEl.scrollTop + mainEl.clientHeight;
        const total = mainEl.scrollHeight;
        if (total > 0) pb.style.width = Math.min(100, Math.round((scrolled / total) * 100)) + '%';
      }});
    }}

    const bttBtn = document.getElementById('back-to-top');
    (mainEl || window).addEventListener('scroll', () => {{
      const top = mainEl ? mainEl.scrollTop : window.scrollY;
      bttBtn.classList.toggle('visible', top > 500);
    }});
    bttBtn.addEventListener('click', () => {{
      if (mainEl) mainEl.scrollTo({{top:0,behavior:'smooth'}});
      else window.scrollTo({{top:0,behavior:'smooth'}});
    }});
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
