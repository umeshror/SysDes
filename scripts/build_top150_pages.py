import os
import json
from collections import defaultdict

ITEMS_FILE = "scripts/top150_items.json"
TEMPLATE_FILE = "scripts/templates/top150_template.html"
OUT_DIR = "top150"

def build_sidebar(items, current_id):
    # Group items by category
    categories = defaultdict(list)
    for item in items:
        categories[item["category"]].append(item)
        
    html = []
    html.append('    <nav class="sidebar">')
    html.append('        <div class="sidebar-header">')
    html.append('            <a href="../index.html">← Back to Home</a>')
    html.append('            <h1>Top Interview 150</h1>')
    html.append('            <p>Essential LeetCode patterns</p>')
    html.append('        </div>')
    html.append('        <div class="sidebar-search">')
    html.append('            <input type="text" id="q-search" placeholder="Search questions…" oninput="filterQuestions(this.value)">')
    html.append('        </div>')
    html.append('        <div class="sidebar-scroll" id="sidebar-list">')
    
    for cat_name, cat_items in categories.items():
        # Check if the current item is in this category to expand it
        is_expanded = any(i["data_q"] == current_id for i in cat_items)
        exp_cls = " expanded" if is_expanded else ""
        
        html.append(f'            <div class="nav-module{exp_cls}">')
        html.append(f'                <div class="nav-module-title">{cat_name}</div>')
        for q in cat_items:
            active_cls = " active" if q["data_q"] == current_id else ""
            html.append(f'                <a href="{q["href"]}" class="q-item{active_cls}" data-q="{q["data_q"]}" style="text-decoration:none;">')
            html.append(f'                    {q["inner"]}')
            html.append('                </a>')
        html.append('            </div>')
        
    html.append('        </div>')
    
    html.append('        <div class="progress-footer">')
    html.append(f'            <div class="progress-label"><span id="solved-count">0</span> / {len(items)} solved</div>')
    html.append('            <div class="progress-bar-wrap">')
    html.append('                <div class="progress-bar-fill" id="progress-fill"></div>')
    html.append('            </div>')
    html.append('        </div>')
    html.append('    </nav>')
    
    return "\n".join(html)

def build_main_content(item):
    html = f"""
        <div class="question-panel active" id="{item["data_q"]}">
            <div class="q-header">
                <div class="q-header-meta">
                    <span class="q-number-badge"># {item["num"]} &middot; LeetCode</span>
                    <span class="diff-badge diff-{item["diff"].lower()}">{item["diff"]}</span>
                    <span class="topic-tag">{item["category"]}</span>
                </div>
                <h1 class="q-title">{item["name"]}</h1>
                <p class="q-source"><a href="https://leetcode.com/problems/{item["slug"]}/" target="_blank">leetcode.com/problems/{item["slug"]}</a> &middot; Top Interview 150</p>
            </div>
            <hr class="section-rule">
            
            <div class="warn-box" style="margin-top: 40px; text-align: center; padding: 60px 20px;">
                <h2 style="margin-bottom: 20px; color: #a6adc8;">Content Pending</h2>
                <p style="color: #6c7086;">The FAANG-level breakdown for this problem is currently being generated.</p>
                <p style="color: #6c7086; margin-top: 10px;">Check back later for detailed optimal solutions, complexity analysis, and interview tips.</p>
            </div>
            
            <button class="mark-solved-btn" id="solve-{item['data_q']}" onclick="markSolved('{item['data_q']}',this)" style="margin-top: 60px;">Mark as Solved</button>
        </div>
    """
    return html

def build_nav(current_idx, items):
    prev_q = items[current_idx-1] if current_idx > 0 else None
    next_q = items[current_idx+1] if current_idx < len(items)-1 else None
    
    prev_btn = f'<a class="page-nav-btn" href="{prev_q["href"]}">&#8592; {prev_q["name"]}</a>' if prev_q else '<span></span>'
    next_btn = f'<a class="page-nav-btn" href="{next_q["href"]}">{next_q["name"]} &#8594;</a>' if next_q else '<span></span>'
    
    html = f'''
        <div class="page-nav" style="max-width: 960px; margin: 40px auto 0; padding: 20px 48px;">
            {prev_btn}
            <a class="page-nav-btn home" href="../index.html">&#9776; Back to Portfolio</a>
            {next_btn}
        </div>'''
    return html

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    with open(ITEMS_FILE, "r") as f:
        data = json.load(f)
    items = data["items"]
    
    with open(TEMPLATE_FILE, "r") as f:
        template = f.read()
        
    for i, item in enumerate(items):
        sidebar_html = build_sidebar(items, item["data_q"])
        main_html = build_main_content(item)
        nav_html = build_nav(i, items)
        
        # Inject into template
        page_html = template.replace('<!-- {{SIDEBAR_HTML}} -->', sidebar_html)
        page_html = page_html.replace('<!-- {{MAIN_CONTENT}} -->', main_html)
        page_html = page_html.replace('<!-- {{PAGE_NAV}} -->', nav_html)
        
        # Save file
        out_path = os.path.join(OUT_DIR, item["href"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
            
    # Write redirect index.html
    if items:
        first_file = items[0]["href"]
        redirect_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={first_file}">
</head>
<body>
    <p>Redirecting to <a href="{first_file}">{items[0]["name"]}</a>...</p>
</body>
</html>'''
        with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(redirect_html)

    print(f"Successfully generated {len(items)} HTML pages in {OUT_DIR}/")

if __name__ == "__main__":
    main()
