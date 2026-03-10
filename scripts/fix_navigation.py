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
     "module":"System Designs","icon":"📚","num":None,
     "sections":["case-urlshortener"],"nav":[
         ("case-urlshortener","URL Shortening Platform"),
         ("case-urlshortener-1","1. Executive Summary"),
         ("case-urlshortener-2","2. Problem Definition"),
         ("case-urlshortener-3","3. Capacity Planning"),
         ("case-urlshortener-4","4. Data Model"),
         ("case-urlshortener-5","5. High-Level Architecture"),
         ("case-urlshortener-6","6. Write Path"),
         ("case-urlshortener-7","7. Short Code Gen"),
         ("case-urlshortener-8","8. Read Path"),
         ("case-urlshortener-9","9. DB Selection"),
         ("case-urlshortener-10","10. Multi-Region"),
         ("case-urlshortener-11","11. Analytics Pipeline"),
         ("case-urlshortener-12","12. Abuse Prevention"),
         ("case-urlshortener-13","13. Failure Handling"),
         ("case-urlshortener-14","14. Observability"),
         ("case-urlshortener-15","15. Operations"),
         ("case-urlshortener-16","16. Future Evolution"),
         ("case-urlshortener-17","17. Key Decisions"),
         ("case-urlshortener-18","18. Viral URLs")
     ]},
    {"file":"../case_studies/open-table.html","title":"Design OpenTable",
     "module":"System Designs","icon":"🍴","num":None,
     "sections":["case-opentable"],"nav":[
         ("case-opentable","Design OpenTable (Deep Dive)")]},
]

def get_relative_path(target_path, current_filepath):
    if not target_path: return ""
    current_dir = os.path.dirname(filepath)
    if current_dir == "pages": return target_path
    if current_dir == "case_studies":
        if target_path.startswith("../case_studies/"):
            return target_path.split("/")[-1]
        return "../pages/" + target_path
    return target_path

def generate_sidebar(current_filepath, filter_module=None):
    current_filename = current_filepath.split("/")[-1]
    html_lines = ['<div class="sidebar-accordion">']
    
    # 1. Group pages by module
    modules = {}
    for p in PAGES:
        m_name = p["module"]
        if m_name not in modules:
            modules[m_name] = {"icon": p["icon"], "num": p["num"], "pages": []}
        modules[m_name]["pages"].append(p)

    # 2. Add Internals Section (only if not restricted by filter_module or if it's the active page)
    # We find the active page first
    active_page = next((p for p in PAGES if p["file"].split("/")[-1] == current_filename), None)
    
    # 3. Generate Modules
    for m_name, meta in modules.items():
        if filter_module and m_name != filter_module:
            continue
            
        has_active = any(p["file"].split("/")[-1] == current_filename for p in meta["pages"])
        open_attr = ' open' if has_active else ''
        
        # Chapter numbering logic
        num_span = f'<span class="chap-num">Chapter {meta["num"]}</span>' if meta["num"] else ''
        
        html_lines.append(f'        <details class="acc-chapter"{open_attr}>')
        html_lines.append(f'          <summary class="acc-summary">')
        html_lines.append(f'            <span class="chap-icon">{meta["icon"]}</span>')
        html_lines.append(f'            <span class="chap-text">')
        if num_span: html_lines.append(f'              {num_span}')
        html_lines.append(f'              <span class="chap-label">{m_name}</span>')
        html_lines.append(f'            </span>')
        if has_active: html_lines.append(f'            <span class="chap-curr">●</span>')
        html_lines.append(f'            <span class="acc-arrow">›</span>')
        html_lines.append(f'          </summary>')
        
        html_lines.append('          <div class="acc-sub">')
        for p in meta["pages"]:
            is_p_active = p["file"].split("/")[-1] == current_filename
            base_href = get_relative_path(p["file"], current_filepath)
            
            # Sub-items logic: If page is active, we list its sections inside the module? 
            # Or just the page link? The user's edit showed sub-items for active pages.
            for sec_id, label in p["nav"]:
                html_lines.append(f'            <a class="acc-sub-item" href="{base_href}#{sec_id}" data-sec="{sec_id}">{label}</a>')
        html_lines.append('          </div>')
        html_lines.append('        </details>')

    # 4. Add "Internals" Section for active page TOC
    if active_page:
        html_lines.append(f'        <details class="acc-chapter" open>')
        html_lines.append(f'          <summary class="acc-summary">')
        html_lines.append(f'            <span class="chap-icon">📋</span>')
        html_lines.append(f'            <span class="chap-text">')
        html_lines.append(f'              <span class="chap-label">Internals</span>')
        html_lines.append(f'            </span>')
        html_lines.append(f'            <span class="acc-arrow">›</span>')
        html_lines.append(f'          </summary>')
        html_lines.append('          <div class="acc-sub">')
        for sec_id, label in active_page["nav"]:
             html_lines.append(f'             <a class="acc-sub-item internal-link" href="#{sec_id}">{label}</a>')
        html_lines.append('          </div>')
        html_lines.append('        </details>')

    html_lines.append('      </div>')
    return "\n".join(html_lines)

def generate_nav_footer(current_filepath):
    filename = current_filepath.split("/")[-1]
    current_idx = next((i for i, p in enumerate(PAGES) if p["file"].split("/")[-1] == filename), -1)
    if current_idx == -1: return ""
    prev_p = PAGES[current_idx - 1] if current_idx > 0 else None
    next_p = PAGES[current_idx + 1] if current_idx < len(PAGES) - 1 else None
    prev_link = get_relative_path(prev_p["file"], current_filepath) if prev_p else ""
    next_link = get_relative_path(next_p["file"], current_filepath) if next_p else ""
    home_link = get_relative_path("01-introduction.html", current_filepath)
    prev_btn = f'<a class="page-nav-btn" href="{prev_link}">&#8592; {prev_p["module"]}</a>' if prev_p else '<span></span>'
    next_btn = f'<a class="page-nav-btn" href="{next_link}">{next_p["module"]} &#8594;</a>' if next_p else '<span></span>'
    return f"""      <div class="page-nav">
        {prev_btn}
        <a class="page-nav-btn home" href="{home_link}">&#9776; All Topics</a>
        {next_btn}
      </div>"""

def fix_file(fpath):
    print(f"Fixing {fpath}...")
    global filepath # Hack to make get_relative_path find it
    filepath = fpath
    filter_module = "System Designs" if fpath.startswith("case_studies") else None
    with open(fpath, 'r', encoding='utf-8') as f: content = f.read()
    sidebar_html = generate_sidebar(fpath, filter_module=filter_module)
    content = re.sub(r'<div class="sidebar-accordion">.*?</div>\s*</nav>', f'{sidebar_html}\n    </nav>', content, flags=re.DOTALL)
    nav_footer_html = generate_nav_footer(fpath)
    if nav_footer_html: content = re.sub(r'<div class="page-nav">.*?</div>', nav_footer_html, content, flags=re.DOTALL)
    with open(fpath, 'w', encoding='utf-8') as f: f.write(content)

if __name__ == "__main__":
    if os.path.exists("pages"):
        for f in os.listdir("pages"):
            if f.endswith(".html"): fix_file(os.path.join("pages", f))
    if os.path.exists("case_studies"):
        for f in os.listdir("case_studies"):
            if f.endswith(".html") and not f.startswith("index"): fix_file(os.path.join("case_studies", f))
    print("Navigation overhaul complete!")
