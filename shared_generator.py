"""
shared_generator.py
Shared HTML-generation engine for Blind 75 content batches.
All batch files import add_problem() from here.
Run run_all_batches.py to apply everything.
"""
import os, re
from bs4 import BeautifulSoup

INPUT_FILE = os.path.join(os.path.dirname(__file__), "blind75-spa.html")
_PROBLEMS = {}  # populated by add_problem()

def add_problem(q_id, data):
    _PROBLEMS[q_id] = data

def _generate_panel_html(q_id, d):
    topics_html = "".join(f'<span class="topic-tag">{t}</span>' for t in d["topics"])
    diff_cls = {"Easy":"easy","Medium":"medium","Hard":"hard"}[d["diff"]]
    examples_html = "".join(f"""
            <div class="example-block">
                <div class="example-header">{ex["title"]}</div>
                <div class="example-body">
                    <div><span class="label">Input: </span><span class="val">{ex["input"]}</span></div>
                    <div><span class="label">Output: </span><span class="val">{ex["output"]}</span></div>
                    <div class="explanation">{ex["explain"]}</div>
                </div>
            </div>""" for ex in d["examples"])
    constraints_html = "".join(f"<li>{c}</li>" for c in d["constraints"])
    rows_html = "".join(f"""
                <tr{' class="'+a.get("cls", "")+'"' if a.get("cls") else ""}>
                    <td>{a["name"]}</td><td><code>{a["time"]}</code></td>
                    <td><code>{a["space"]}</code></td><td>{a["notes"]}</td>
                </tr>""" for a in d["approaches"])
    opt = d["optimal_approach"]
    
    # Generate tabs for optimal approach
    tab_buttons, tab_contents = "", ""
    first = True
    names_map = {"python":"Python","java":"Java","javascript":"JavaScript","go":"Go"}
    for lk, ld in d["codes"].items():
        act = " active" if first else ""
        tid = f"{ld['id_prefix']}-{lk}-{q_id}"
        tab_buttons += f"""<button class="tab-btn{act}" onclick="switchTab(this, '{tid}')">{names_map[lk]}</button>
                    """
        tab_contents += f"""
                <div class="tab-content{act}" id="{tid}">
                    <div class="code-wrap"><pre><code class="language-{ld['lang']}">{ld['code']}</code></pre></div>
                </div>"""
        first = False

    # Generate multi-approach sections
    approaches_sections = ""
    for i, a in enumerate(d["approaches"], 1):
        is_optimal = "optimal" in a.get("cls", "").lower() or a["name"] == opt.get("title") or i == len(d["approaches"])
        
        if is_optimal:
            # Render optimal block with code
            approaches_sections += f"""
            <h2 class="approach-title">Approach {i} — {opt.get("title", a["name"])} <span class="approach-badge {opt.get("badge_cls", "badge-optimal")}">{opt.get("badge_text", "Optimal")}</span></h2>
            <div class="complexity-row">
                <div class="complexity-pill"><span class="cp-label">Time</span><span class="cp-value">{opt.get("time", a["time"])}</span></div>
                <div class="complexity-pill"><span class="cp-label">Space</span><span class="cp-value">{opt.get("space", a["space"])}</span></div>
            </div>
            <p class="approach-explanation">{opt.get("explanation", a["notes"])}</p>
            <div class="code-tabs">
                <div class="tab-buttons">{tab_buttons}</div>
                {tab_contents}
            </div>"""
        else:
            # Render suboptimal block with warn box
            approaches_sections += f"""
            <h2 class="approach-title">Approach {i} — {a['name']} <span class="approach-badge badge-better">{a['time']}</span></h2>
            <div class="complexity-row">
                <div class="complexity-pill"><span class="cp-label">Time</span><span class="cp-value">{a['time']}</span></div>
                <div class="complexity-pill"><span class="cp-label">Space</span><span class="cp-value">{a['space']}</span></div>
            </div>
            <p class="approach-explanation">{a['notes']}</p>
            <div class="warn-box">
                <div class="warn-box-title">⚠ Interviewer will push back</div>
                <p>This is a valid stepping-stone answer. But the problem requires better optimization. Always start by acknowledging this brute force/suboptimal time complexity before moving to the optimal solution.</p>
            </div>"""

    tips_html = "".join(f"<li>{t}</li>" for t in d["tips"])
    return f"""
        <div class="question-panel" id="{q_id}">
            <div class="q-header">
                <div class="q-header-meta">
                    <span class="q-number-badge"># {d["num"]} &middot; LeetCode</span>
                    <span class="diff-badge {diff_cls}">{d["diff"]}</span>
                    {topics_html}
                </div>
                <h1 class="q-title">{d["name"]}</h1>
                <p class="q-source"><a href="{d.get("link", "")}" target="_blank">{d.get("link", "").replace("https://","")}</a> &middot; Blind 75 &middot; FAANG favourite</p>
            </div>
            <hr class="section-rule">
            <div class="problem-statement"><h3>Problem Statement</h3><div class="statement-content">{d["statement"]}</div></div>
            <div class="examples">{examples_html}</div>
            <div class="constraints"><h4>Constraints</h4><ul>{constraints_html}</ul></div>
            
            <h2 class="approach-title">Approaches Comparison</h2>
            <table class="compare-table">
                <tr><th>Approach</th><th>Time</th><th>Space</th><th>Notes</th></tr>
                {rows_html}
            </table>
            
            {approaches_sections}
            <div class="insight" style="margin-top:20px;">
                <div class="insight-title">{d["insight_title"]}</div>
                <p>{d["insight_text"]}</p>
            </div>
            <div class="interview-tips">
                <h3>Interview Playbook</h3>
                <ol>{tips_html}</ol>
            </div>
            <button class="mark-solved-btn" id="solve-{q_id}" onclick="markSolved('{q_id}',this)">Mark as Solved</button>
        </div>
"""

def run_injection():
    with open(INPUT_FILE,"r",encoding="utf-8") as f:
        raw = f.read()
    if "</body>" in raw:
        raw = raw.split("</body>")[0]+"</body>\n</html>"
    soup = BeautifulSoup(raw,"html.parser")
    main_panel = soup.find("div",id="main-panel")
    injected = 0
    for q_id, data in _PROBLEMS.items():
        panel = soup.find("div",id=q_id,class_="question-panel")
        if panel and "Content Pending" not in str(panel):
            print(f"  Skipping {data['name']} — already has content")
            continue
        new_html = _generate_panel_html(q_id, data)
        new_node = BeautifulSoup(new_html,"html.parser").find("div",id=q_id)
        if not new_node:
            print(f"  WARNING: Could not generate panel for {data['name']}")
            continue
        if panel:
            panel.replace_with(new_node)
        elif main_panel:
            main_panel.append(new_node)
        else:
            print(f"  ERROR: No main-panel found, cannot inject {data['name']}")
            continue
        injected += 1
        print(f"  Injected {data['name']} ({q_id})")
    if injected:
        with open(INPUT_FILE,"w",encoding="utf-8") as f:
            f.write(str(soup))
        print(f"\n{injected} problems written to {INPUT_FILE}")
    return injected
