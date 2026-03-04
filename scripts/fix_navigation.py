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
    {"file":"../case_studies/open-table.html","title":"Case Studies",
     "module":"Case Studies","icon":"📚","num":"13",
     "sections":["case-opentable"],"nav":[("case-opentable","Design OpenTable (Deep Dive)")]},
]

def generate_sidebar(current_file):
    html = '<div class="sidebar-accordion">\n'
    for p in PAGES:
        # Normalize paths for comparison
        target_file = p["file"].split("/")[-1]
        this_file = current_file.split("/")[-1]
        
        is_cur = target_file == this_file
        open_attr = ' open' if is_cur else ''
        cur_badge = '<span class="chap-curr">●</span>' if is_cur else ''
        
        sub_items = ""
        for sec_id, label in p["nav"]:
            if is_cur:
                # We assume the first section is active by default for sidebar highlighting
                is_first = p["nav"][0][0] == sec_id
                active_cls = ' class="acc-sub-item active"' if is_first else ' class="acc-sub-item"'
                sub_items += f'              <div{active_cls} data-sec="{sec_id}">{label}</div>\n'
            else:
                # Need to handle path depth
                href = p["file"] if current_file.startswith("pages") else p["file"].replace("../", "")
                if current_file.startswith("case_studies") and not p["file"].startswith("../"):
                    href = "../pages/" + p["file"]
                
                # Special case for case studies link from within case studies
                if current_file.startswith("case_studies") and p["file"].startswith("../case_studies"):
                    href = p["file"].split("/")[-1]

                sub_items += f'              <a class="acc-sub-item" href="{href}#{sec_id}">{label}</a>\n'

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
    html += '      </div>'
    return html

def fix_file(filepath):
    print(f"Fixing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    sidebar_html = generate_sidebar(filepath)
    content = re.sub(r'<div class="sidebar-accordion">.*?</div>\s*</nav>', sidebar_html + '\n    </nav>', content, flags=re.DOTALL)

    # 2. Update Page Nav (Prev/Next)
    filename = filepath.split("/")[-1]
    current_idx = -1
    for i, p in enumerate(PAGES):
        if p["file"].split("/")[-1] == filename:
            current_idx = i
            break
    
    if current_idx != -1:
        prev_p = PAGES[current_idx-1] if current_idx > 0 else None
        next_p = PAGES[current_idx+1] if current_idx < len(PAGES)-1 else None
        
        # Helper to fix links based on depth
        def fix_link(link):
            if not link: return ""
            if filepath.startswith("pages"):
                return link # already relative or starts with ../case_studies
            if filepath.startswith("case_studies"):
                if link.startswith("../case_studies"): return link.split("/")[-1]
                return "../pages/" + link
            return link

        prev_link = fix_link(prev_p["file"]) if prev_p else ""
        next_link = fix_link(next_p["file"]) if next_p else ""
        home_link = fix_link("01-introduction.html")

        prev_btn = f'<a class="page-nav-btn" href="{prev_link}">&#8592; {prev_p["module"]}</a>' if prev_p else '<span></span>'
        next_btn = f'<a class="page-nav-btn" href="{next_link}">{next_p["module"]} &#8594;</a>' if next_p else '<span></span>'
        
        new_nav = f"""      <div class="page-nav">
        {prev_btn}
        <a class="page-nav-btn home" href="{home_link}">&#9776; All Topics</a>
        {next_btn}
      </div>"""
        
        content = re.sub(r'<div class="page-nav">.*?</div>', new_nav, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Fix all pages in pages/
    for f in os.listdir("pages"):
        if f.endswith(".html"):
            fix_file(os.path.join("pages", f))
    
    # Fix open-table.html in case_studies/
    fix_file("case_studies/open-table.html")
    print("Navigation unified!")
