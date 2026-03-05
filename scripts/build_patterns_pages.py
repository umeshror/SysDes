"""
build_patterns_pages.py
Generates 20 individual HTML pages for the Coding Patterns section.
Extracts content from pages/12-coding-interview-patterns.html
and produces patterns/01-sliding-window.html ... patterns/20-bit-manipulation.html
"""

import os
from bs4 import BeautifulSoup

SRC_FILE = "pages/12-coding-interview-patterns.html"
OUT_DIR  = "patterns"

PATTERNS = [
    (1,  "Sliding Window",             "sliding-window",             "cyan",    "#00e5ff", "Array",      "O(N)",       "O(K)"),
    (2,  "Two Pointers",               "two-pointers",                "violet",  "#b47fff", "Array",      "O(N)",       "O(1)"),
    (3,  "Fast & Slow Pointers",       "fast-slow-pointers",          "green",   "#00ff9f", "LinkedList", "O(N)",       "O(1)"),
    (4,  "Merge Intervals",            "merge-intervals",             "amber",   "#ffb700", "Array",      "O(N log N)", "O(N)"),
    (5,  "Cyclic Sort",                "cyclic-sort",                 "rose",    "#ff4d7d", "Array",      "O(N)",       "O(1)"),
    (6,  "In-place Reversal",          "in-place-reversal",           "sky",     "#4da8ff", "LinkedList", "O(N)",       "O(1)"),
    (7,  "Tree BFS",                   "tree-bfs",                    "teal",    "#00ffd5", "Tree",       "O(N)",       "O(W)"),
    (8,  "Tree DFS",                   "tree-dfs",                    "orange",  "#ff7340", "Tree",       "O(N)",       "O(H)"),
    (9,  "Two Heaps",                  "two-heaps",                   "lime",    "#b3ff4d", "Heap",       "O(N log N)", "O(N)"),
    (10, "Subsets",                    "subsets",                     "pink",    "#ff5df0", "Backtrack",  "O(N·2ᴺ)",   "O(2ᴺ)"),
    (11, "Modified Binary Search",     "modified-binary-search",      "cyan",    "#00e5ff", "Array",      "O(log N)",   "O(1)"),
    (12, "Top K Elements",             "top-k-elements",              "violet",  "#b47fff", "Heap",       "O(N log K)", "O(K)"),
    (13, "K-way Merge",                "k-way-merge",                 "green",   "#00ff9f", "Heap",       "O(N log K)", "O(K)"),
    (14, "Topological Sort",           "topological-sort",            "amber",   "#ffb700", "Graph",      "O(V+E)",     "O(V+E)"),
    (15, "Prefix Sum",                 "prefix-sum",                  "rose",    "#ff4d7d", "Array",      "O(1) query", "O(N)"),
    (16, "Monotonic Stack",            "monotonic-stack",             "sky",     "#4da8ff", "Stack",      "O(N)",       "O(N)"),
    (17, "Union Find",                 "union-find",                  "teal",    "#00ffd5", "Graph",      "O(α(N))",    "O(N)"),
    (18, "Dynamic Programming",        "dynamic-programming",         "orange",  "#ff7340", "DP",         "O(States)",  "O(States)"),
    (19, "Greedy",                     "greedy",                      "lime",    "#b3ff4d", "Greedy",     "O(N log N)", "O(1)"),
    (20, "Bit Manipulation",           "bit-manipulation",            "pink",    "#ff5df0", "Bits",       "O(1)",       "O(1)"),
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

# Python code snippets from coding-patterns-v2.jsx CODES dictionary
CODES = {
    1: r"""def sliding_window(nums, k):
  left, best, window = 0, 0, 0
  for right in range(len(nums)):
    window += nums[right]          # expand
    while window > k:              # shrink
      window -= nums[left]
      left += 1
    best = max(best, right-left+1) # record
  return best""",

    2: r"""def two_sum_sorted(arr, target):
  left, right = 0, len(arr)-1
  while left < right:
    s = arr[left] + arr[right]
    if s == target:  return [left, right]
    elif s < target: left += 1
    else:            right -= 1
  return [-1, -1]""",

    3: r"""def has_cycle(head):
  slow = fast = head
  while fast and fast.next:
    slow = slow.next       # ×1
    fast = fast.next.next  # ×2
    if slow == fast:
      return True  # cycle!
  return False""",

    4: r"""def merge(intervals):
  intervals.sort(key=lambda x: x[0])
  merged = [intervals[0]]
  for cur in intervals[1:]:
    if cur[0] <= merged[-1][1]:
      merged[-1][1] = max(merged[-1][1], cur[1])
    else:
      merged.append(cur)
  return merged""",

    5: r"""def cyclic_sort(nums):
  i = 0
  while i < len(nums):
    j = nums[i] - 1          # correct index
    if nums[i] != nums[j]:
      nums[i], nums[j] = nums[j], nums[i]
    else:
      i += 1
  return nums""",

    6: r"""def reverse_list(head):
  prev, curr = None, head
  while curr:
    nxt = curr.next  # save
    curr.next = prev # reverse
    prev = curr      # advance
    curr = nxt
  return prev        # new head""",

    7: r"""def bfs(root):
  queue, result = deque([root]), []
  while queue:
    level = []
    for _ in range(len(queue)):  # current level only
      node = queue.popleft()
      level.append(node.val)
      if node.left:  queue.append(node.left)
      if node.right: queue.append(node.right)
    result.append(level)
  return result""",

    8: r"""def dfs(node):
  if not node: return 0
  # pre-order: process node here
  left  = dfs(node.left)
  right = dfs(node.right)
  # post-order: combine results
  return 1 + max(left, right)""",

    9: r"""class MedianFinder:
  def __init__(self):
    self.lo = []  # max-heap (negate)
    self.hi = []  # min-heap
  def addNum(self, n):
    heappush(self.lo, -n)
    heappush(self.hi, -heappop(self.lo))
    if len(self.lo) < len(self.hi):
      heappush(self.lo, -heappop(self.hi))
  def findMedian(self):
    if len(self.lo) > len(self.hi):
      return -self.lo[0]
    return (-self.lo[0] + self.hi[0]) / 2""",

    10: r"""def subsets(nums):
  result = [[]]
  for n in nums:
    result += [s + [n] for s in result]
  return result

# backtracking variant:
def backtrack(start, path):
  result.append(path[:])
  for i in range(start, len(nums)):
    path.append(nums[i])
    backtrack(i+1, path)
    path.pop()""",

    11: r"""def search(nums, target):
  lo, hi = 0, len(nums)-1
  while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target:  return mid
    if nums[lo] <= nums[mid]:           # left sorted
      if nums[lo] <= target < nums[mid]: hi = mid-1
      else:                              lo = mid+1
    else:                               # right sorted
      if nums[mid] < target <= nums[hi]: lo = mid+1
      else:                              hi = mid-1
  return -1""",

    12: r"""def top_k(nums, k):
  heap = []
  for n in nums:
    heappush(heap, n)
    if len(heap) > k:
      heappop(heap)   # evict smallest
  return list(heap)  # k largest remain""",

    13: r"""def merge_k(lists):
  heap = []
  for i, lst in enumerate(lists):
    if lst: heappush(heap, (lst[0], i, 0))
  result = []
  while heap:
    val, i, j = heappop(heap)
    result.append(val)
    if j+1 < len(lists[i]):
      heappush(heap, (lists[i][j+1], i, j+1))
  return result""",

    14: r"""def topo_sort(V, edges):
  in_deg = {i:0 for i in range(V)}
  graph  = {i:[] for i in range(V)}
  for u,v in edges:
    graph[u].append(v); in_deg[v] += 1
  q = deque(k for k,d in in_deg.items() if d==0)
  order = []
  while q:
    u = q.popleft(); order.append(u)
    for v in graph[u]:
      in_deg[v] -= 1
      if in_deg[v] == 0: q.append(v)
  return order if len(order)==V else []""",

    15: r"""class PrefixSum:
  def __init__(self, nums):
    self.p = [0] * (len(nums)+1)
    for i,v in enumerate(nums):
      self.p[i+1] = self.p[i] + v
  def query(self, l, r):      # O(1)
    return self.p[r+1] - self.p[l]""",

    16: r"""def next_greater(nums):
  result = [-1] * len(nums)
  stack = []               # stores indices
  for i, v in enumerate(nums):
    while stack and nums[stack[-1]] < v:
      result[stack.pop()] = v  # found NGE!
    stack.append(i)
  return result""",

    17: r"""class UnionFind:
  def __init__(self, n):
    self.p, self.rank = list(range(n)), [1]*n
  def find(self, x):
    if self.p[x] != x:
      self.p[x] = self.find(self.p[x])  # compress
    return self.p[x]
  def union(self, x, y):
    rx, ry = self.find(x), self.find(y)
    if rx == ry: return False
    if self.rank[rx] < self.rank[ry]: rx,ry=ry,rx
    self.p[ry]=rx; self.rank[rx]+=1
    return True""",

    18: r"""# bottom-up DP template
def solve(n, cost):
  dp = [0] * (n+1)
  dp[0], dp[1] = cost[0], cost[1]
  for i in range(2, n):
    # state transition:
    dp[i] = cost[i] + min(dp[i-1], dp[i-2])
  return min(dp[-1], dp[-2])""",

    19: r"""def can_jump(nums):
  max_reach = 0
  for i, v in enumerate(nums):
    if i > max_reach: return False  # stuck
    max_reach = max(max_reach, i+v)
  return True

def jump_min(nums):
  jumps = reach = far = 0
  for i in range(len(nums)-1):
    far = max(far, i + nums[i])
    if i == reach:
      jumps += 1; reach = far
  return jumps""",

    20: r"""# XOR — find single number
def singleNumber(nums):
  r = 0
  for n in nums: r ^= n  # pairs cancel
  return r

# count set bits (Brian Kernighan)
def countBits(n):
  count = 0
  while n:
    n &= n-1  # drop lowest 1-bit
    count += 1
  return count

# check power of 2
def isPow2(n): return n>0 and (n & n-1)==0""",
}


def build_sidebar(patterns, current_num):
    items = []
    for p in patterns:
        num, name, slug = p[0], p[1], p[2]
        hex_color = p[4]
        num_str = str(num).zfill(2)
        fname   = f"{num_str}-{slug}.html"
        active  = " active" if num == current_num else ""
        mastered_dot = f'<span class="m-dot" id="m-dot-{num}"></span>'
        items.append(
            f'        <a href="{fname}" class="p-nav-item{active}" data-num="{num}">'
            f'<span class="p-num">{num}</span>'
            f'<span class="p-name">{name}</span>'
            f'{mastered_dot}'
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


def build_page(num, name, slug, color_name, hex_color, tag, time_c, space_c, patterns, content_html):
    idx      = num - 1
    prev_p   = patterns[idx - 1] if idx > 0 else None
    next_p   = patterns[idx + 1] if idx < len(patterns) - 1 else None
    prev_btn = (f'<a class="pnav-btn" href="{str(prev_p[0]).zfill(2)}-{prev_p[2]}.html">← {prev_p[1]}</a>') if prev_p else '<span></span>'
    next_btn = (f'<a class="pnav-btn" href="{str(next_p[0]).zfill(2)}-{next_p[2]}.html">{next_p[1]} →</a>') if next_p else '<span></span>'

    sidebar_html = build_sidebar(patterns, num)
    anim_fn      = ANIM_FN_MAP[num]
    img_name     = IMG_MAP[num]
    num_str      = str(num).zfill(2)
    code_snippet = CODES.get(num, "# No snippet available")
    # Escape for HTML embedding
    code_html    = code_snippet.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern {num}: {name} — Coding Interview Patterns</title>
    <meta name="description" content="Deep dive into the {name} pattern — visualized live with animation, Python code, and full editorial.">
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

        /* ── Sidebar */
        .patterns-sidebar {{
            width: var(--sidebar-w); min-width: var(--sidebar-w);
            background: var(--surface); border-right: 1px solid var(--border);
            position: fixed; top: 0; left: 0; height: 100vh;
            display: flex; flex-direction: column; overflow: hidden;
        }}
        .ps-header {{ padding: 20px 16px 14px; border-bottom: 1px solid var(--border); flex-shrink: 0; }}
        .ps-back-row {{ font-size: .75rem; margin-bottom: 10px; }}
        .ps-back-row .back-link {{ color: var(--muted); text-decoration: none; transition: color .2s; }}
        .ps-back-row .back-link:hover {{ color: var(--accent); }}
        .ps-title {{ font-size: 1rem; font-weight: 700; color: var(--accent); margin-bottom: 2px; }}
        .ps-sub {{ font-size: .72rem; color: var(--muted); }}
        .ps-list {{ flex: 1; overflow-y: auto; padding: 8px 0; }}
        .ps-list::-webkit-scrollbar {{ width: 3px; }}
        .ps-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
        .p-nav-item {{ display: flex; align-items: center; gap: 10px; padding: 8px 16px; font-size: .82rem; color: var(--muted); text-decoration: none; border-left: 3px solid transparent; transition: all .15s; }}
        .p-nav-item:hover {{ background: var(--card); color: var(--text); }}
        .p-nav-item.active {{ background: var(--card); border-left-color: var(--accent); color: var(--accent); }}
        .p-num {{ width: 20px; font-size: .7rem; font-weight: 700; color: var(--muted); flex-shrink: 0; }}
        .p-nav-item.active .p-num {{ color: var(--accent); }}
        .p-name {{ flex: 1; }}
        .m-dot {{ width: 6px; height: 6px; border-radius: 50%; background: transparent; flex-shrink: 0; transition: background .3s; }}
        .m-dot.done {{ background: #00ff9f; box-shadow: 0 0 4px #00ff9f; }}
        .ps-footer {{ padding: 14px 16px; border-top: 1px solid var(--border); flex-shrink: 0; }}
        .ps-progress-label {{ font-size: .75rem; color: var(--muted); margin-bottom: 6px; }}
        .ps-bar-wrap {{ background: var(--border); border-radius: 4px; height: 4px; }}
        .ps-bar-fill {{ background: var(--accent); height: 100%; border-radius: 4px; width: 0%; transition: width .4s; }}

        /* ── Main */
        .main-content {{ margin-left: var(--sidebar-w); flex: 1; max-width: 900px; padding: 48px 48px 80px; }}

        /* ── Pattern header */
        .pattern-header {{ margin-bottom: 32px; }}
        .pattern-badge {{ display: inline-flex; align-items: center; gap: 8px; background: var(--card); border: 1px solid var(--border); border-radius: 999px; padding: 4px 14px; font-size: .75rem; color: var(--muted); margin-bottom: 14px; }}
        .pattern-badge .dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 6px var(--accent); }}
        .pattern-title {{ font-size: 2.4rem; font-weight: 800; color: var(--text); line-height: 1.1; margin-bottom: 10px; }}
        .pattern-title span {{ color: var(--accent); }}

        /* ── Complexity / tag chips */
        .meta-chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px; }}
        .chip {{ font-family: monospace; font-size: .72rem; padding: 4px 10px; border-radius: 4px; border: 1px solid; letter-spacing: .4px; }}
        .chip-tag  {{ color: var(--accent); border-color: var(--accent); background: rgba(255,255,255,.03); }}
        .chip-time {{ color: #ffb700; border-color: #ffb70044; background: #ffb70008; }}
        .chip-space {{ color: #b47fff; border-color: #b47fff44; background: #b47fff08; }}

        /* ── Visualization card */
        .viz-card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 36px;
        }}
        /* tab bar */
        .viz-tabs {{
            display: flex;
            border-bottom: 1px solid var(--border);
            background: var(--surface);
        }}
        .viz-tab {{
            padding: 10px 20px;
            font-size: .72rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: monospace;
            color: var(--muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all .2s;
            background: none;
            border-top: none;
            border-left: none;
            border-right: none;
        }}
        .viz-tab.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
        /* tab panels */
        .viz-panel {{ display: none; padding: 24px; }}
        .viz-panel.active {{ display: block; }}

        /* anim panel inner */
        .anim-inner {{ }}

        /* code panel */
        .code-panel pre {{ margin: 0; font-size: .83rem; line-height: 1.75; border-radius: 8px; }}

        /* ── Infographic */
        .infographic-img {{ width: 100%; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 36px; }}

        /* ── Content */
        .pattern-content h2 {{ font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 36px 0 14px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
        .pattern-content h3 {{ font-size: 1.05rem; font-weight: 700; color: var(--accent); margin: 24px 0 8px; }}
        .pattern-content p {{ color: #8a9abf; margin-bottom: 12px; line-height: 1.8; }}
        .pattern-content ul, .pattern-content ol {{ margin: 8px 0 14px 22px; }}
        .pattern-content li {{ color: #8a9abf; margin-bottom: 6px; line-height: 1.7; }}
        .pattern-content li strong {{ color: var(--text); }}
        .pattern-content pre {{ background: #0d1117; border: 1px solid var(--border); border-radius: 8px; padding: 18px; overflow-x: auto; margin: 14px 0; }}
        .pattern-content code {{ font-family: 'Fira Code', monospace; font-size: .85rem; }}
        .pattern-content p code {{ background: var(--card); border: 1px solid var(--border); padding: 1px 5px; border-radius: 4px; font-size: .82rem; color: var(--accent); }}
        .callout {{ border-radius: 8px; padding: 16px 20px; margin: 16px 0; font-size: .88rem; border-left: 4px solid; }}
        .callout.info {{ background: #0e1a2e; border-color: #4da8ff; }}
        .callout.warn {{ background: #1a1200; border-color: #ffb700; }}
        .callout.tip  {{ background: #091a0e; border-color: #00ff9f; }}
        .callout-title {{ font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }}
        .callout.info .callout-title {{ color: #4da8ff; }}
        .callout.warn .callout-title {{ color: #ffb700; }}
        .callout.tip  .callout-title  {{ color: #00ff9f; }}
        .callout p {{ color: #8a9abf !important; margin: 0 !important; }}

        /* ── Mark mastered */
        .mark-btn {{ display: inline-flex; align-items: center; gap: 8px; background: var(--card); border: 1px solid var(--accent); color: var(--accent); padding: 12px 28px; border-radius: 8px; font-size: .9rem; font-weight: 600; cursor: pointer; margin-top: 40px; transition: all .2s; }}
        .mark-btn:hover {{ background: var(--accent); color: var(--bg); }}
        .mark-btn.mastered {{ background: var(--accent); color: var(--bg); }}

        /* ── Page nav */
        .page-nav {{ display: flex; justify-content: space-between; align-items: center; margin-top: 60px; padding-top: 24px; border-top: 1px solid var(--border); }}
        .pnav-btn {{ color: var(--muted); text-decoration: none; font-size: .85rem; padding: 8px 16px; border: 1px solid var(--border); border-radius: 6px; background: var(--card); transition: all .2s; }}
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
        <h1 class="pattern-title"><span>{name}</span></h1>
    </div>

    <!-- Complexity chips -->
    <div class="meta-chips">
        <span class="chip chip-tag">{tag}</span>
        <span class="chip chip-time">⏱ Time: {time_c}</span>
        <span class="chip chip-space">📦 Space: {space_c}</span>
    </div>

    <!-- Visualization + Code card -->
    <div class="viz-card">
        <div class="viz-tabs">
            <button class="viz-tab active" onclick="switchTab(this,'anim-panel-{num}')">▶ Animation</button>
            <button class="viz-tab" onclick="switchTab(this,'code-panel-{num}')">⌨ Python</button>
        </div>
        <div id="anim-panel-{num}" class="viz-panel active">
            <div class="anim-inner" id="anim-container" data-color="{hex_color}"></div>
        </div>
        <div id="code-panel-{num}" class="viz-panel code-panel">
            <pre><code class="language-python">{code_html}</code></pre>
        </div>
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

    // Tab switcher
    function switchTab(btn, panelId) {{
        btn.closest('.viz-card').querySelectorAll('.viz-tab').forEach(t => t.classList.remove('active'));
        btn.closest('.viz-card').querySelectorAll('.viz-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(panelId).classList.add('active');
    }}

    // Fire the animation
    new PatternAnimator('anim-container', {anim_fn}, 600);

    // Progress / mastered
    let mastered = JSON.parse(localStorage.getItem('patterns-mastered') || '[]');

    function updateProgress() {{
        const n = mastered.length;
        document.getElementById('solved-count').textContent = n;
        document.getElementById('progress-fill').style.width = (n / 20 * 100) + '%';
        mastered.forEach(s => {{
            const num = [{','.join(str(p[0]) + ': "' + p[2] + '"' for p in patterns)}][s] || null;
            // light up sidebar dots
        }});
    }}

    function markMastered(slug, btn) {{
        if (!mastered.includes(slug)) {{
            mastered.push(slug);
            localStorage.setItem('patterns-mastered', JSON.stringify(mastered));
        }}
        btn.textContent = '★ Mastered!';
        btn.classList.add('mastered');
        const item = document.querySelector('.p-nav-item.active');
        if (item) {{
            item.style.borderLeftColor = '#00ff9f';
            const dot = item.querySelector('.m-dot');
            if (dot) dot.classList.add('done');
        }}
        updateProgress();
    }}

    // Restore on load
    (function() {{
        const slugMap = {{{','.join('"' + p[2] + '": ' + str(p[0]) for p in patterns)}}};
        mastered.forEach(s => {{
            const n = slugMap[s];
            if (n) {{
                const dot = document.getElementById('m-dot-' + n);
                if (dot) dot.classList.add('done');
                const item = document.querySelector('.p-nav-item[data-num="' + n + '"]');
                if (item) item.style.borderLeftColor = '#00ff9f';
            }}
            if (s === '{slug}') {{
                const btn = document.getElementById('mark-btn');
                if (btn) {{ btn.textContent = '★ Mastered!'; btn.classList.add('mastered'); }}
            }}
        }});
        updateProgress();
    }})();
</script>
</body>
</html>
"""


def extract_pattern_content(soup, num):
    section = soup.find(id=f"p{num}")
    if not section:
        return f"<p>Content for pattern {num} will be added soon.</p>"
    return "".join(str(c) for c in section.children)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Parsing {SRC_FILE}...")
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for p in PATTERNS:
        num, name, slug, color_name, hex_color, tag, time_c, space_c = p
        content_html = extract_pattern_content(soup, num)
        page_html    = build_page(num, name, slug, color_name, hex_color, tag, time_c, space_c, PATTERNS, content_html)

        num_str  = str(num).zfill(2)
        out_path = os.path.join(OUT_DIR, f"{num_str}-{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  ✓ {out_path}")

    # redirect index.html
    first = PATTERNS[0]
    redirect = f"""<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="0; url=01-sliding-window.html"></head>
<body><p>Redirecting to <a href="01-sliding-window.html">{first[1]}</a>...</p></body>
</html>"""
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect)

    print(f"\n✅ Generated {len(PATTERNS)} pattern pages + index.html in {OUT_DIR}/")


if __name__ == "__main__":
    main()
