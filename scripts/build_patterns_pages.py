"""
build_patterns_pages.py
Generates 20 individual HTML pages for the Coding Patterns section.
Extracts content from pages/12-coding-interview-patterns.html
and produces patterns/01-sliding-window.html ... patterns/20-bit-manipulation.html
"""

import os
import re
from bs4 import BeautifulSoup

SRC_FILE = "pages/12-coding-interview-patterns.html"
OUT_DIR  = "patterns"

PATTERNS = [
    (1,  "Sliding Window",             "sliding-window",             "cyan",    "#00e5ff"),
    (2,  "Two Pointers",               "two-pointers",                "violet",  "#b47fff"),
    (3,  "Fast & Slow Pointers",       "fast-slow-pointers",          "green",   "#00ff9f"),
    (4,  "Merge Intervals",            "merge-intervals",             "amber",   "#ffb700"),
    (5,  "Cyclic Sort",                "cyclic-sort",                 "rose",    "#ff4d7d"),
    (6,  "In-place Reversal",          "in-place-reversal",           "sky",     "#4da8ff"),
    (7,  "Tree BFS",                   "tree-bfs",                    "teal",    "#00ffd5"),
    (8,  "Tree DFS",                   "tree-dfs",                    "orange",  "#ff7340"),
    (9,  "Two Heaps",                  "two-heaps",                   "lime",    "#b3ff4d"),
    (10, "Subsets",                    "subsets",                     "pink",    "#ff5df0"),
    (11, "Modified Binary Search",     "modified-binary-search",      "cyan",    "#00e5ff"),
    (12, "Top K Elements",             "top-k-elements",              "violet",  "#b47fff"),
    (13, "K-way Merge",                "k-way-merge",                 "green",   "#00ff9f"),
    (14, "Topological Sort",           "topological-sort",            "amber",   "#ffb700"),
    (15, "Prefix Sum",                 "prefix-sum",                  "rose",    "#ff4d7d"),
    (16, "Monotonic Stack",            "monotonic-stack",             "sky",     "#4da8ff"),
    (17, "Union Find",                 "union-find",                  "teal",    "#00ffd5"),
    (18, "Dynamic Programming",        "dynamic-programming",         "orange",  "#ff7340"),
    (19, "Greedy",                     "greedy",                      "lime",    "#b3ff4d"),
    (20, "Bit Manipulation",           "bit-manipulation",            "pink",    "#ff5df0"),
]

ANIM_FN_MAP = {
    1:  "renderSlidingWindow",
    2:  "renderTwoPointers",
    3:  "renderFastSlow",
    4:  "renderMergeIntervals",
    5:  "renderCyclicSort",
    6:  "renderInPlaceReversal",
    7:  "renderTreeBFS",
    8:  "renderTreeDFS",
    9:  "renderTwoHeaps",
    10: "renderSubsets",
    11: "renderBinarySearch",
    12: "renderTopK",
    13: "renderKWayMerge",
    14: "renderTopoSort",
    15: "renderPrefixSum",
    16: "renderMonotonicStack",
    17: "renderUnionFind",
    18: "renderDP",
    19: "renderGreedy",
    20: "renderBitManip",
}

IMG_MAP = {
    1:  "p1-sliding-window.png",
    2:  "p2-two-pointers.png",
    3:  "p3-fast-slow-pointers.png",
    4:  "p4-merge-intervals.png",
    5:  "p5-cyclic-sort.png",
    6:  "p6-linked-list-reversal.png",
    7:  "p7-tree-bfs.png",
    8:  "p8-tree-dfs.png",
    9:  "p9-two-heaps.png",
    10: "p10-subsets.png",
    11: "p11-binary-search.png",
    12: "p12-top-k-elements.png",
    13: "p13-k-way-merge.png",
    14: "p14-topological-sort.png",
    15: "p15-prefix-sum.png",
    16: "p16-monotonic-stack.png",
    17: "p17-union-find.png",
    18: "p18-dynamic-programming.png",
    19: "p19-greedy.png",
    20: "p20-bit-manipulation.png",
}


def build_sidebar(patterns, current_num):
    items = []
    for num, name, slug, _, color in patterns:
        num_str = str(num).zfill(2)
        fname = f"{num_str}-{slug}.html"
        active = " active" if num == current_num else ""
        items.append(
            f'        <a href="{fname}" class="p-nav-item{active}" data-num="{num}">'
            f'<span class="p-num">{num}</span>'
            f'<span class="p-name">{name}</span>'
            f'</a>'
        )
    items_html = "\n".join(items)
    return f"""    <nav class="patterns-sidebar">
        <div class="ps-header">
            <div class="ps-back-row">
                <a href="../index.html" class="back-link">← Home</a>
                &nbsp;|&nbsp;
                <a href="../blind75/index.html" class="back-link">Blind 75</a>
                &nbsp;|&nbsp;
                <a href="../top150/index.html" class="back-link">Top 150</a>
            </div>
            <h1 class="ps-title">Coding Patterns</h1>
            <p class="ps-sub">20 Mastery Blueprints</p>
        </div>
        <div class="ps-list">
{items_html}
        </div>
        <div class="ps-footer">
            <div class="ps-progress-label"><span id="solved-count">0</span> / 20 mastered</div>
            <div class="ps-bar-wrap"><div class="ps-bar-fill" id="progress-fill"></div></div>
        </div>
    </nav>"""


def build_page(num, name, slug, color_name, hex_color, patterns, content_html):
    """Build a full standalone HTML page for a single pattern."""
    idx = num - 1
    prev_p = patterns[idx - 1] if idx > 0 else None
    next_p = patterns[idx + 1] if idx < len(patterns) - 1 else None

    prev_btn = (f'<a class="pnav-btn" href="{str(prev_p[0]).zfill(2)}-{prev_p[2]}.html">'
                f'← {prev_p[1]}</a>') if prev_p else '<span></span>'
    next_btn = (f'<a class="pnav-btn" href="{str(next_p[0]).zfill(2)}-{next_p[2]}.html">'
                f'{next_p[1]} →</a>') if next_p else '<span></span>'

    sidebar_html = build_sidebar(patterns, num)
    anim_fn      = ANIM_FN_MAP[num]
    img_name     = IMG_MAP[num]
    num_str      = str(num).zfill(2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern {num}: {name} — Coding Interview Patterns</title>
    <meta name="description" content="Deep dive into the {name} pattern — when to use it, complexity analysis, LeetCode problems, and animated visualizations.">

    <!-- Highlight.js -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <style>
        :root {{
            --accent: {hex_color};
            --bg: #03050d;
            --surface: #070c1a;
            --card: #0b1120;
            --border: #131d35;
            --text: #c8d4f0;
            --muted: #3a4a70;
            --sidebar-w: 280px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); display: flex; min-height: 100vh; }}

        /* ── Sidebar ─────────────────────────────────── */
        .patterns-sidebar {{
            width: var(--sidebar-w);
            min-width: var(--sidebar-w);
            background: var(--surface);
            border-right: 1px solid var(--border);
            position: fixed;
            top: 0; left: 0;
            height: 100vh;
            display: flex; flex-direction: column;
            overflow: hidden;
        }}
        .ps-header {{
            padding: 20px 16px 14px;
            border-bottom: 1px solid var(--border);
            background: var(--surface);
            flex-shrink: 0;
        }}
        .ps-back-row {{ font-size: 0.75rem; margin-bottom: 10px; }}
        .ps-back-row .back-link {{ color: var(--muted); text-decoration: none; transition: color .2s; }}
        .ps-back-row .back-link:hover {{ color: var(--accent); }}
        .ps-title {{ font-size: 1rem; font-weight: 700; color: var(--accent); margin-bottom: 2px; }}
        .ps-sub {{ font-size: 0.72rem; color: var(--muted); }}

        .ps-list {{
            flex: 1;
            overflow-y: auto;
            padding: 8px 0;
        }}
        .ps-list::-webkit-scrollbar {{ width: 4px; }}
        .ps-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

        .p-nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 16px;
            font-size: 0.82rem;
            color: var(--muted);
            text-decoration: none;
            border-left: 3px solid transparent;
            transition: all .15s;
        }}
        .p-nav-item:hover {{ background: var(--card); color: var(--text); }}
        .p-nav-item.active {{ background: #0b1120; border-left-color: var(--accent); color: var(--accent); }}
        .p-num {{ width: 20px; font-size: 0.7rem; font-weight: 700; color: var(--muted); flex-shrink: 0; }}
        .p-nav-item.active .p-num {{ color: var(--accent); }}

        .ps-footer {{
            padding: 14px 16px;
            border-top: 1px solid var(--border);
            flex-shrink: 0;
        }}
        .ps-progress-label {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 6px; }}
        .ps-bar-wrap {{ background: var(--border); border-radius: 4px; height: 4px; }}
        .ps-bar-fill {{ background: var(--accent); height: 100%; border-radius: 4px; width: 0%; transition: width .4s; }}

        /* ── Main ─────────────────────────────────────── */
        .main-content {{
            margin-left: var(--sidebar-w);
            flex: 1;
            max-width: 900px;
            padding: 48px 48px 80px;
        }}

        /* ── Pattern header ───────────────────────────── */
        .pattern-header {{
            margin-bottom: 36px;
        }}
        .pattern-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 4px 14px;
            font-size: 0.75rem;
            color: var(--muted);
            margin-bottom: 16px;
        }}
        .pattern-badge .dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 6px var(--accent); }}
        .pattern-title {{
            font-size: 2.4rem;
            font-weight: 800;
            color: var(--text);
            line-height: 1.1;
            margin-bottom: 12px;
        }}
        .pattern-title span {{ color: var(--accent); }}
        .pattern-meta {{ font-size: 0.85rem; color: var(--muted); }}

        /* ── Animation card ───────────────────────────── */
        .anim-card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 36px;
        }}
        .anim-label {{
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--muted);
            margin-bottom: 12px;
        }}
        #anim-container {{ }}

        /* ── Infographic ─────────────────────────────── */
        .infographic-img {{
            width: 100%;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 36px;
        }}

        /* ── Section content ─────────────────────────── */
        .pattern-content h2 {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text);
            margin: 36px 0 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }}
        .pattern-content h3 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--accent);
            margin: 24px 0 8px;
        }}
        .pattern-content p {{ color: #8a9abf; margin-bottom: 12px; line-height: 1.8; }}
        .pattern-content ul, .pattern-content ol {{ margin: 8px 0 14px 22px; }}
        .pattern-content li {{ color: #8a9abf; margin-bottom: 6px; line-height: 1.7; }}
        .pattern-content li strong {{ color: var(--text); }}
        .pattern-content pre {{ background: #0d1117; border: 1px solid var(--border); border-radius: 8px; padding: 18px; overflow-x: auto; margin: 14px 0; }}
        .pattern-content code {{ font-family: 'Fira Code', monospace; font-size: 0.85rem; }}
        .pattern-content p code {{ background: var(--card); border: 1px solid var(--border); padding: 1px 5px; border-radius: 4px; font-size: 0.82rem; color: var(--accent); }}

        .callout {{
            border-radius: 8px;
            padding: 16px 20px;
            margin: 16px 0;
            font-size: 0.88rem;
            border-left: 4px solid;
        }}
        .callout.info {{ background: #0e1a2e; border-color: #4da8ff; }}
        .callout.warn {{ background: #1a1200; border-color: #ffb700; }}
        .callout.tip  {{ background: #091a0e; border-color: #00ff9f; }}
        .callout-title {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }}
        .callout.info .callout-title {{ color: #4da8ff; }}
        .callout.warn .callout-title {{ color: #ffb700; }}
        .callout.tip  .callout-title  {{ color: #00ff9f; }}
        .callout p {{ color: #8a9abf !important; margin: 0 !important; }}

        /* ── Mark mastered ────────────────────────────── */
        .mark-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--card);
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 12px 28px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            margin-top: 40px;
            transition: all .2s;
        }}
        .mark-btn:hover {{ background: var(--accent); color: var(--bg); }}
        .mark-btn.mastered {{ background: var(--accent); color: var(--bg); }}

        /* ── Page nav ────────────────────────────────── */
        .page-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 60px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
        }}
        .pnav-btn {{
            color: var(--muted);
            text-decoration: none;
            font-size: 0.85rem;
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--card);
            transition: all .2s;
        }}
        .pnav-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
    </style>
</head>
<body>

{sidebar_html}

<main class="main-content">
    <!-- Header -->
    <div class="pattern-header">
        <div class="pattern-badge">
            <div class="dot"></div>
            Pattern {num_str} of 20
        </div>
        <h1 class="pattern-title">
            <span>{name}</span>
        </h1>
        <p class="pattern-meta">A fundamental algorithmic blueprint used across FAANG interviews.</p>
    </div>

    <!-- Live Animation -->
    <div class="anim-card">
        <div class="anim-label">Live Visualization</div>
        <div id="anim-container" data-color="{hex_color}"></div>
    </div>

    <!-- Infographic -->
    <img src="../assets/patterns/{img_name}" alt="{name} pattern infographic" class="infographic-img"
         onerror="this.style.display='none'">

    <!-- Main Content -->
    <div class="pattern-content">
        {content_html}
    </div>

    <!-- Mark as Mastered -->
    <button class="mark-btn" id="mark-btn" onclick="markMastered('{slug}', this)">
        ✓ Mark as Mastered
    </button>

    <!-- Page Nav -->
    <div class="page-nav">
        {prev_btn}
        <a href="../index.html" class="pnav-btn">⌂ Portfolio</a>
        {next_btn}
    </div>
</main>

<script src="../assets/js/pattern-animations.js"></script>
<script>
    hljs.highlightAll();

    // Fire the animation for this pattern
    new PatternAnimator('anim-container', {anim_fn}, 600);

    // Progress / Mastered tracking
    let mastered = JSON.parse(localStorage.getItem('patterns-mastered') || '[]');

    function markMastered(slug, btn) {{
        if (!mastered.includes(slug)) {{
            mastered.push(slug);
            localStorage.setItem('patterns-mastered', JSON.stringify(mastered));
        }}
        btn.textContent = '★ Mastered!';
        btn.classList.add('mastered');
        const item = document.querySelector('.p-nav-item.active');
        if (item) item.style.borderLeftColor = '#00ff9f';
        updateProgress();
    }}

    function updateProgress() {{
        const n = mastered.length;
        document.getElementById('solved-count').textContent = n;
        document.getElementById('progress-fill').style.width = (n / 20 * 100) + '%';
    }}

    // Restore mastered state on load
    mastered.forEach(slug => {{
        if (slug === '{slug}') {{
            const btn = document.getElementById('mark-btn');
            if (btn) {{ btn.textContent = '★ Mastered!'; btn.classList.add('mastered'); }}
        }}
    }});
    updateProgress();
</script>
</body>
</html>
"""


def extract_pattern_content(soup, num):
    """Find and extract the HTML content for pattern pN from the SPA."""
    section = soup.find(id=f"p{num}")
    if not section:
        return f"<p>Content for pattern {num} will be added soon.</p>"
    # Return inner HTML of the found section, dropping the outer section wrapper
    return "".join(str(c) for c in section.children)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Parsing {SRC_FILE}...")
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for num, name, slug, color_name, hex_color in PATTERNS:
        content_html = extract_pattern_content(soup, num)
        page_html = build_page(num, name, slug, color_name, hex_color, PATTERNS, content_html)

        num_str = str(num).zfill(2)
        out_path = os.path.join(OUT_DIR, f"{num_str}-{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  ✓ {out_path}")

    # Write redirect index.html
    first_num, first_name, first_slug, _, _ = PATTERNS[0]
    redirect = f"""<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="0; url=01-sliding-window.html"></head>
<body><p>Redirecting to <a href="01-sliding-window.html">{first_name}</a>...</p></body>
</html>"""
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect)

    print(f"\n✅ Generated {len(PATTERNS)} pattern pages + index.html in {OUT_DIR}/")


if __name__ == "__main__":
    main()
