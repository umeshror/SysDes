import os
import re
from bs4 import BeautifulSoup

INPUT_FILE = "blind75-spa.html"
OUT_DIR = "blind75"

os.makedirs(OUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

# Strip any junk appended after the closing script/body tag
if "</body>" in raw:
    raw = raw.split("</body>")[0] + "</body>\n</html>"

soup = BeautifulSoup(raw, "html.parser")

sidebar = soup.find("div", id="sidebar-list")
q_items = sidebar.find_all("div", class_="q-item")

questions = []
for item in q_items:
    q_id = item.get("data-q")
    q_num = item.find("span", class_="q-num").text.strip()
    q_name = item.find("span", class_="q-name").text.strip()
    q_diff_span = item.find("span", class_="q-diff")
    q_diff_class = " ".join(q_diff_span.get("class", []))
    q_diff_text = q_diff_span.text.strip()

    slug = re.sub(r"[^a-z0-9]+", "-", q_name.lower()).strip("-")
    filename = f"{str(q_num).zfill(2)}-{slug}.html"
    
    questions.append({
        "id": q_id,
        "num": q_num,
        "name": q_name,
        "diff_class": q_diff_class,
        "diff_text": q_diff_text,
        "file": filename
    })

head_split = raw.split('<nav class="sidebar">')
head_html = head_split[0]

import re as _re
script_match = _re.search(r'(\s*<script>)', raw)
if script_match:
    script_html = raw[script_match.start():]
else:
    raise RuntimeError("Could not find <script> tag in source HTML")
script_html = script_html.replace(
    'function showQ(qId, item) {',
    'function showQ(qId, item) {\n            return; // disabled in multi-page\n'
)

def build_sidebar_html(current_q_id):
    html = """    <nav class="sidebar">
        <div class="sidebar-header">
            <a href="../index.html">← Back to Home</a>
            <h1>Blind 75</h1>
            <p>Essential LeetCode patterns</p>
        </div>

        <div class="sidebar-search">
            <input type="text" id="q-search" placeholder="Search questions…" oninput="filterQuestions(this.value)">
        </div>

        <div class="sidebar-scroll" id="sidebar-list">
            <div class="category-section">
                <div class="category-label">All Questions</div>\n"""
                
    for q in questions:
        active_cls = " active" if q["id"] == current_q_id else ""
        html += f"""                <a href="{q['file']}" class="q-item{active_cls}" data-q="{q['id']}" style="text-decoration:none;">
                    <span class="q-num">{q['num']}</span>
                    <span class="q-check"></span>
                    <span class="q-name">{q['name']}</span>
                    <span class="{q['diff_class']}">{q['diff_text']}</span>
                </a>\n"""
                
    html += """            </div>
        </div>

        <div class="progress-footer">
            <div class="progress-label"><span id="solved-count">0</span> / 75 solved</div>
            <div class="progress-bar-wrap">
                <div class="progress-bar-fill" id="progress-fill"></div>
            </div>
        </div>
    </nav>\n"""
    return html

panels = {}
for q in questions:
    panel_node = soup.find("div", id=q['id'], class_="question-panel")
    if panel_node:
        # We must add the 'active' class so it's visible natively on page load
        classes = panel_node.get("class", [])
        if "active" not in classes:
            classes.append("active")
        panel_node["class"] = classes
        
        # We need to make sure we serialize correctly without getting other siblings
        panels[q['id']] = str(panel_node)
    else:
        panels[q['id']] = f'<div class="question-panel active" id="{q["id"]}"><h2>Content Pending</h2></div>'

for q in questions:
    sidebar_html = build_sidebar_html(q["id"])
    main_html = f"""    <div class="main" id="main-panel">\n{panels.get(q['id'], '')}\n    </div>\n"""
    
    full_html = head_html + sidebar_html + main_html + script_html
    
    out_path = os.path.join(OUT_DIR, q["file"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

if questions:
    first_file = questions[0]["file"]
    redirect_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={first_file}">
</head>
<body>
    <p>Redirecting to <a href="{first_file}">{questions[0]["name"]}</a>...</p>
</body>
</html>'''
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect_html)

print("Regeneration complete matching exact IDs.")
