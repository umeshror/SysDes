import os
import re

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
     "sections":["patterns"],"nav":[("patterns","14 Essential Patterns")]},
    {"file":"../case_studies/url-shortener.html","title":"Global URL Shortener",
     "module":"Case Studies","icon":"📚","num":"13",
     "sections":["case-urlshortener"],"nav":[
         ("case-urlshortener","URL Shortening Platform")]},
    {"file":"../case_studies/open-table.html","title":"Design OpenTable",
     "module":"Case Studies","icon":"🍴","num":"14",
     "sections":["case-opentable"],"nav":[
         ("case-opentable","Design OpenTable (Deep Dive)")]},
]

def get_relative_path(target_path, current_filepath):
    """
    Resolves the relative path between the current file and the target page.
    Assumes standard SysDes structure: /pages/ and /case_studies/
    """
    if not target_path: return ""
    
    current_dir = os.path.dirname(current_filepath)
    
    if current_dir == "pages":
        return target_path # target is already relative to pages/ or is ../case_studies/...
    
    if current_dir == "case_studies":
        if target_path.startswith("../case_studies/"):
            return target_path.split("/")[-1] # "url-shortener.html"
        return "../pages/" + target_path # "../pages/01-intro.html"
        
    return target_path

def generate_sidebar(current_filepath, filter_module=None):
    """Generates the sidebar accordion HTML."""
    html_lines = ['<div class="sidebar-accordion">']
    
    for p in PAGES:
        # 1. Filtering
        if filter_module and p["module"] != filter_module:
            continue

        # 2. State checks
        target_filename = p["file"].split("/")[-1]
        current_filename = current_filepath.split("/")[-1]
        is_cur = target_filename == current_filename
        
        open_attr = ' open' if is_cur else ''
        cur_badge = '<span class="chap-curr">●</span>' if is_cur else ''
        base_href = get_relative_path(p["file"], current_filepath)
        
        # 3. Sub-items Link construction
        sub_items_html = ""
        for sec_id, label in p["nav"]:
            sub_items_html += f'              <a class="acc-sub-item" href="{base_href}#{sec_id}" data-sec="{sec_id}">{label}</a>\n'

        # 4. Assemble Details/Summary
        html_lines.append(f"""        <details class="acc-chapter"{open_attr}>
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
{sub_items_html}          </div>
        </details>""")
        
    html_lines.append('      </div>')
    return "\n".join(html_lines)

def generate_nav_footer(current_filepath):
    """Generates the Prev / All Topics / Next navigation footer."""
    filename = current_filepath.split("/")[-1]
    
    # Find current page in sequence
    current_idx = next((i for i, p in enumerate(PAGES) if p["file"].split("/")[-1] == filename), -1)
    if current_idx == -1: return ""

    prev_p = PAGES[current_idx - 1] if current_idx > 0 else None
    next_p = PAGES[current_idx + 1] if current_idx < len(PAGES) - 1 else None
    
    # Path resolution
    prev_link = get_relative_path(prev_p["file"], current_filepath) if prev_p else ""
    next_link = get_relative_path(next_p["file"], current_filepath) if next_p else ""
    home_link = get_relative_path("01-introduction.html", current_filepath)
    
    # Template construction
    prev_btn = f'<a class="page-nav-btn" href="{prev_link}">&#8592; {prev_p["module"]}</a>' if prev_p else '<span></span>'
    next_btn = f'<a class="page-nav-btn" href="{next_link}">{next_p["module"]} &#8594;</a>' if next_p else '<span></span>'
    
    return f"""      <div class="page-nav">
        {prev_btn}
        <a class="page-nav-btn home" href="{home_link}">&#9776; All Topics</a>
        {next_btn}
      </div>"""

def fix_file(filepath):
    """Processes a single HTML file to inject navigation components."""
    print(f"Fixing {filepath}...")
    
    filter_module = "Case Studies" if filepath.startswith("case_studies") else None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    sidebar_html = generate_sidebar(filepath, filter_module=filter_module)
    content = re.sub(r'<div class="sidebar-accordion">.*?</div>\s*</nav>', 
                     f'{sidebar_html}\n    </nav>', content, flags=re.DOTALL)

    # 2. Update Nav Footer
    nav_footer_html = generate_nav_footer(filepath)
    if nav_footer_html:
        content = re.sub(r'<div class="page-nav">.*?</div>', nav_footer_html, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # 1. Sync Pages
    if os.path.exists("pages"):
        for f in os.listdir("pages"):
            if f.endswith(".html"):
                fix_file(os.path.join("pages", f))
    
    # 2. Sync Case Studies
    if os.path.exists("case_studies"):
        for f in os.listdir("case_studies"):
            # Skip indices or non-article files if necessary, but here we fix specifically requested ones
            if f in ["url-shortener.html", "open-table.html"]:
                fix_file(os.path.join("case_studies", f))

    print("Navigation unified and refactored!")
