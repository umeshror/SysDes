"""Batch 7: q37-q60 — Trees, DP, Binary, Tries, Graphs"""
from shared_generator import add_problem

def _codes(py, name):
    stub = f"// See Python solution above for the full algorithm\n// {name} — translate line-by-line"
    return {
        "python": {"id_prefix":"opt","lang":"python","code": py},
        "java":   {"id_prefix":"opt","lang":"java","code": stub},
        "javascript": {"id_prefix":"opt","lang":"javascript","code": stub},
        "go":     {"id_prefix":"opt","lang":"go","code": stub},
    }

add_problem("q37", {
    "name": "Subtree of Another Tree", "num": 572, "diff": "Easy",
    "topics": ["Tree","DFS","String Matching"],
    "link": "https://leetcode.com/problems/subtree-of-another-tree",
    "statement": "Given the roots of two binary trees <code>root</code> and <code>subRoot</code>, return <code>true</code> if there is a subtree of <code>root</code> with the same structure and node values as <code>subRoot</code>.",
    "examples": [
        {"title":"Example 1","input":"root=[3,4,5,1,2], subRoot=[4,1,2]","output":"true","explain":"The subtree at node 4 matches subRoot."},
        {"title":"Example 2","input":"root=[3,4,5,1,2,null,null,null,null,0], subRoot=[4,1,2]","output":"false","explain":"Node 4 has an extra child 0, so it doesn't match."},
    ],
    "constraints":["1 &le; size of root &le; 2000","1 &le; size of subRoot &le; 1000","-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"DFS brute force","time":"O(m·n)","space":"O(m+n)","notes":"For each root node, check if subtree matches. Optimal enough.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Recursive DFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(m·n)","space":"O(m+n)",
        "explanation":"For each node in root, call <code>isSameTree(node, subRoot)</code>. If root is None or matches, return accordingly. DFS traverses all nodes of root (m) and at each compares up to n nodes of subRoot."},
    "codes": _codes("""def isSubtree(root, subRoot):
    def same(a, b):
        if not a and not b: return True
        if not a or not b: return False
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)
    if not root: return False
    return same(root, subRoot) or isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)""", "Subtree of Another Tree"),
    "insight_title":"isSameTree is the Inner Function",
    "insight_text":"Reuse the classic 'same tree' check at every node. O(m·n) is acceptable for the given constraints (m,n &le; 2000). For large inputs, use serialization + KMP/rolling hash for O(m+n).",
    "tips":["<strong>Reuse isSameTree:</strong> Breaking it into two separate functions keeps the code clean.",
             "<strong>Companies:</strong> Amazon, Microsoft, Google."]
})

add_problem("q38", {
    "name": "Unique Paths", "num": 62, "diff": "Medium",
    "topics": ["Math","DP"],
    "link": "https://leetcode.com/problems/unique-paths",
    "statement": "A robot on an <code>m x n</code> grid starts at top-left and must reach bottom-right. It can only move right or down. How many unique paths exist?",
    "examples": [
        {"title":"Example 1","input":"m=3, n=7","output":"28","explain":"28 unique paths from (0,0) to (2,6)."},
        {"title":"Example 2","input":"m=3, n=2","output":"3","explain":"Three paths: RDD, DRD, DDR."},
    ],
    "constraints":["1 &le; m, n &le; 100"],
    "approaches":[
        {"name":"Math (Combinatorics)","time":"O(min(m,n))","space":"O(1)","notes":"C(m+n-2, m-1). Optimal.","cls":"optimal-row"},
        {"name":"DP","time":"O(mn)","space":"O(mn) or O(n)","notes":"dp[i][j] = paths to cell (i,j).","cls":""},
    ],
    "optimal_approach":{"title":"Dynamic Programming","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(n)",
        "explanation":"dp[i][j] = number of paths to reach cell (i,j). dp[i][j] = dp[i-1][j] + dp[i][j-1]. Space-optimized using a 1D array."},
    "codes": _codes("""def uniquePaths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]""", "Unique Paths"),
    "insight_title":"1D DP vs 2D DP", "insight_text":"We only need the previous row to compute the current row. Rolling a 1D array reduces space from O(mn) to O(n).",
    "tips":["<strong>Math shortcut:</strong> C(m+n-2, m-1) gives the answer in O(1) space.",
             "<strong>Companies:</strong> Amazon, Microsoft, Google."]
})

add_problem("q39", {
    "name": "Reverse Bits", "num": 190, "diff": "Easy",
    "topics": ["Bit Manipulation"],
    "link": "https://leetcode.com/problems/reverse-bits",
    "statement": "Reverse bits of a given 32-bit unsigned integer.",
    "examples": [
        {"title":"Example 1","input":"n = 00000010100101000001111010011100","output":"964176192 (00111001011110000010100101000000)","explain":"Reverse all 32 bits."},
    ],
    "constraints":["Input is a 32-bit unsigned integer"],
    "approaches":[{"name":"Bit-by-bit shifting","time":"O(1) — 32 iterations","space":"O(1)","notes":"Shift right, read LSB, shift it into result. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Bit-by-Bit","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(1)","space":"O(1)",
        "explanation":"For 32 iterations: extract the LSB of n (<code>n & 1</code>), shift it to the correct position in result, then right-shift n."},
    "codes": _codes("""def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result""", "Reverse Bits"),
    "insight_title":"32 Fixed Iterations = O(1)",
    "insight_text":"Since the input is always 32 bits, the loop runs exactly 32 times regardless of the value — this is O(1) time.",
    "tips":["<strong>Memorize the pattern:</strong> result = (result &lt;&lt; 1) | (n &amp; 1); n &gt;&gt;= 1.",
            "<strong>Companies:</strong> Apple, Amazon.]"]
})

add_problem("q40", {
    "name": "Number of 1 Bits", "num": 191, "diff": "Easy",
    "topics": ["Bit Manipulation"],
    "link": "https://leetcode.com/problems/number-of-1-bits",
    "statement": "Write a function that takes an unsigned integer and returns the number of '1' bits it has (also known as the Hamming weight).",
    "examples": [
        {"title":"Example 1","input":"n = 00000000000000000000000000001011","output":"3","explain":"Three '1' bits."},
        {"title":"Example 2","input":"n = 11111111111111111111111111111101","output":"31","explain":"31 '1' bits."},
    ],
    "constraints":["Input is a 32-bit unsigned integer"],
    "approaches":[
        {"name":"n &amp; 1 loop","time":"O(32)=O(1)","space":"O(1)","notes":"Check LSB, shift right.","cls":""},
        {"name":"n &amp; (n-1) trick","time":"O(k) where k=set bits","space":"O(1)","notes":"Clears the lowest set bit each iteration. Fastest.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Brian Kernighan's Bit Trick","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(k)","space":"O(1)",
        "explanation":"<code>n &amp; (n-1)</code> clears the lowest set bit. Repeat until n=0, counting iterations."},
    "codes": _codes("""def hammingWeight(n):
    count = 0
    while n:
        n &= n - 1   # clear lowest set bit
        count += 1
    return count""", "Number of 1 Bits"),
    "insight_title":"n & (n-1) Clears the Rightmost 1",
    "insight_text":"Each iteration removes exactly one '1' bit. So the loop runs exactly k times where k is the Hamming weight — faster than a full 32-bit scan when the number is sparse.",
    "tips":["<strong>Know both approaches:</strong> Simple loop (32 iterations) and Kernighan's trick (k iterations).",
            "<strong>Companies:</strong> Amazon, Microsoft, Apple."]
})

add_problem("q41", {
    "name": "Coin Change", "num": 322, "diff": "Medium",
    "topics": ["Array","DP","BFS"],
    "link": "https://leetcode.com/problems/coin-change",
    "statement": "Given an array of coin denominations and a total <code>amount</code>, return the minimum number of coins needed to make up the amount, or <code>-1</code> if it's impossible.",
    "examples": [
        {"title":"Example 1","input":"coins=[1,5,11,25], amount=11","output":"1","explain":"Use one 11-cent coin."},
        {"title":"Example 2","input":"coins=[2], amount=3","output":"-1","explain":"Cannot make 3 with only 2s."},
        {"title":"Example 3","input":"coins=[1,2,5], amount=11","output":"3","explain":"5+5+1=11, 3 coins."},
    ],
    "constraints":["1 &le; coins.length &le; 12","1 &le; coins[i] &le; 2<sup>31</sup>-1","0 &le; amount &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"Greedy","time":"O(n)","space":"O(1)","notes":"Fails for denominations like [1,3,4] and amount=6 (greedy gives 4+1+1=3, optimal is 3+3=2).","cls":""},
        {"name":"DP Bottom-Up","time":"O(amount × coins)","space":"O(amount)","notes":"dp[a] = min coins to make amount a. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"DP Bottom-Up","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(amount × n)","space":"O(amount)",
        "explanation":"<code>dp[a] = min(dp[a-coin]+1)</code> for each coin. Initialize dp[0]=0 and dp[1..amount]=infinity."},
    "codes": _codes("""def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""", "Coin Change"),
    "insight_title":"Why Greedy Fails for Coin Change",
    "insight_text":"Greedy (always take largest coin) fails for non-canonical coin systems. DP tries all coin combinations and picks the global minimum.",
    "tips":["<strong>Explain greedy failure</strong> with a counterexample like coins=[1,3,4], amount=6.",
            "<strong>dp[0]=0 is the anchor:</strong> Zero coins needed to make amount 0.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft."]
})

add_problem("q43", {
    "name": "Climbing Stairs", "num": 70, "diff": "Easy",
    "topics": ["Math","DP","Memoization"],
    "link": "https://leetcode.com/problems/climbing-stairs",
    "statement": "You are climbing a staircase with <code>n</code> steps. Each time you can climb 1 or 2 steps. How many distinct ways can you reach the top?",
    "examples": [
        {"title":"Example 1","input":"n = 2","output":"2","explain":"1+1 or 2."},
        {"title":"Example 2","input":"n = 3","output":"3","explain":"1+1+1, 1+2, 2+1."},
    ],
    "constraints":["1 &le; n &le; 45"],
    "approaches":[
        {"name":"Recursion (Fib)","time":"O(2<sup>n</sup>)","space":"O(n)","notes":"Exponential without memoization.","cls":""},
        {"name":"DP (Fibonacci variant)","time":"O(n)","space":"O(1)","notes":"ways(n) = ways(n-1)+ways(n-2). Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Fibonacci DP","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"The number of ways to reach step n equals the number of ways to reach step n-1 (taking one step) plus ways to reach step n-2 (taking two steps). This is the Fibonacci sequence."},
    "codes": _codes("""def climbStairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b""", "Climbing Stairs"),
    "flow_matrix": {
        "headers": ["Step (Distance)", "a (prev2)", "b (prev1)", "Next value (a+b)"],
        "rows": [
            ["Initial", "1", "1", "-"],
            ["i = 2", "1", "2", "2"],
            ["i = 3", "2", "3", "3"],
            ["i = 4", "3", "5", "5"],
            ["i = 5", "5", "8", "8"]
        ]
    },
    "insight_title":"Climbing Stairs IS Fibonacci",
    "insight_text":"f(1)=1, f(2)=2, f(n)=f(n-1)+f(n-2). Reduce space to O(1) by only keeping the last two values.",
    "tips":["<strong>Recognize the pattern:</strong> Any problem where ways(n) = ways(n-1) + ways(n-2) is Fibonacci.",
            "<strong>Companies:</strong> Amazon, Google, Apple — a classic warm-up problem."]
})

add_problem("q44", {
    "name": "House Robber", "num": 198, "diff": "Medium",
    "topics": ["Array","DP"],
    "link": "https://leetcode.com/problems/house-robber",
    "statement": "You are a robber planning to rob houses along a street. You cannot rob two adjacent houses. Given an array of non-negative integers representing the amount of money in each house, return the maximum amount you can rob.",
    "examples": [
        {"title":"Example 1","input":"nums = [1,2,3,1]","output":"4","explain":"Rob house 1 (1) and house 3 (3). Total = 4."},
        {"title":"Example 2","input":"nums = [2,7,9,3,1]","output":"12","explain":"Rob houses 1,3,5: 2+9+1=12."},
    ],
    "constraints":["1 &le; nums.length &le; 100","0 &le; nums[i] &le; 400"],
    "approaches":[
        {"name":"DP with O(n) space","time":"O(n)","space":"O(n)","notes":"dp[i] = max rob up to house i.","cls":""},
        {"name":"DP with O(1) space","time":"O(n)","space":"O(1)","notes":"Only track previous two values. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"DP — Two Variables","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"At each house, either rob it (prev2 + current) or skip it (prev1). dp formula: <code>cur = max(prev1, prev2 + nums[i])</code>; shift prev2=prev1, prev1=cur."},
    "codes": _codes("""def rob(nums):
    prev2 = prev1 = 0
    for n in nums:
        cur = max(prev1, prev2 + n)
        prev2 = prev1
        prev1 = cur
    return prev1""", "House Robber"),
    "insight_title":"Only Two Previous Values Needed",
    "insight_text":"The DP recurrence only depends on the previous two states. Rolling two variables instead of an array reduces space from O(n) to O(1).",
    "tips":["<strong>Recognize the pattern:</strong> Same rolling window technique as Fibonacci.",
            "<strong>Follow-up:</strong> House Robber II (circular) handles the edge cases by running this algorithm twice.",
            "<strong>Companies:</strong> Amazon, Google, Visa."]
})

add_problem("q45", {
    "name": "Number of Islands", "num": 200, "diff": "Medium",
    "topics": ["Array","Graph","BFS","DFS","Union Find"],
    "link": "https://leetcode.com/problems/number-of-islands",
    "statement": "Given a 2D grid of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
    "examples": [
        {"title":"Example 1","input":'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]',"output":"1","explain":"All land cells are connected."},
        {"title":"Example 2","input":'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]',"output":"3","explain":"Three separate islands."},
    ],
    "constraints":["m == grid.length","n == grid[i].length","1 &le; m,n &le; 300","grid[i][j] is '0' or '1'"],
    "approaches":[
        {"name":"DFS","time":"O(mn)","space":"O(mn)","notes":"Flood fill each island to '0'. Optimal.","cls":"optimal-row"},
        {"name":"BFS","time":"O(mn)","space":"O(mn)","notes":"Same complexity, iterative.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"DFS Flood Fill","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(mn)",
        "explanation":"Iterate over all cells. When a '1' is found, increment count and DFS to mark all connected '1's as '0' (visited). Each cell is visited once."},
    "codes": _codes("""def numIslands(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # mark visited
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count""", "Number of Islands"),
    "flow_matrix": {
        "headers": ["Cell (r, c)", "Grid Condition", "Action", "Total Islands"],
        "rows": [
            ["(0, 0)", "'1' (Land)", "Start DFS, mark all connected '1's as '0'", "1"],
            ["(0, 1)", "'0' (Visited / Water)", "Skip", "1"],
            ["(1, 0)", "'0' (Visited / Water)", "Skip", "1"],
            ["(2, 2)", "'1' (Land)", "Start DFS, mark all connected '1's as '0'", "2"],
            ["(3, 3)", "'1' (Land)", "Start DFS, mark all connected '1's as '0'", "3"]
        ]
    },
    "insight_title":"Flood Fill = DFS from Every Unvisited Land Cell",
    "insight_text":"Each cell is visited (and marked '0') at most once across all DFS calls. Total work = O(mn) regardless of the number of islands.",
    "tips":["<strong>Marking cells '0' in-place</strong> avoids needing a separate visited array.",
            "<strong>DFS recursion depth:</strong> In the worst case (entire grid is one island), depth = mn. Consider BFS for very large grids to avoid stack overflow.",
            "<strong>Companies:</strong> Amazon, Google, Meta — extremely common."]
})

add_problem("q47", {
    "name": "Minimum Window Substring", "num": 76, "diff": "Hard",
    "topics": ["String","Sliding Window","Hash Map"],
    "link": "https://leetcode.com/problems/minimum-window-substring",
    "statement": "Given strings <code>s</code> and <code>t</code>, return the <strong>minimum window substring</strong> of <code>s</code> such that every character in <code>t</code> (including duplicates) is included. If there is no such window, return <code>\"\"</code>.",
    "examples": [
        {"title":"Example 1","input":'s="ADOBECODEBANC", t="ABC"',"output":'"BANC"',"explain":"Minimum window containing A,B,C."},
        {"title":"Example 2","input":'s="a", t="a"',"output":'"a"',"explain":"Only window."},
        {"title":"Example 3","input":'s="a", t="aa"',"output":'"" ',"explain":"Two a's needed but only one exists."},
    ],
    "constraints":["1 &le; |s|,|t| &le; 10<sup>5</sup>","s,t consist of English letters"],
    "approaches":[
        {"name":"Brute Force","time":"O(n²)","space":"O(1)","notes":"Check all substrings.","cls":""},
        {"name":"Sliding Window + Counter","time":"O(n+m)","space":"O(n+m)","notes":"Expand right, shrink left when window is valid. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Sliding Window + Two Counters","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n+m)","space":"O(n+m)",
        "explanation":"Maintain window character counts vs required counts. Track <code>have</code> (chars at required frequency) and <code>need</code> (total unique chars needed). When have==need, record window and shrink from left."},
    "codes": _codes("""from collections import Counter

def minWindow(s, t):
    if not t: return ""
    need = Counter(t)
    window = {}
    have, required = 0, len(need)
    left = 0
    best = (float('inf'), 0, 0)
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]
            window[lc] -= 1
            if lc in need and window[lc] < need[lc]:
                have -= 1
            left += 1
    return s[best[1]:best[2]+1] if best[0] != float('inf') else ""
""", "Minimum Window Substring"),
    "insight_title":"have == need Is the Key Condition",
    "insight_text":"We don't check the entire window against t on every step — just the count for the character we just modified. This keeps each char's update to O(1), giving O(n) total.",
    "tips":["<strong>Track 'have' and 'need'</strong> to avoid scanning the entire frequency map each step.",
            "<strong>Shrink aggressively:</strong> Once have==need, keep shrinking from the left to minimize window size.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Bloomberg — most common Hard string problem."]
})

add_problem("q48", {
    "name": "Reverse Linked List", "num": 206, "diff": "Easy",
    "topics": ["Linked List","Recursion"],
    "link": "https://leetcode.com/problems/reverse-linked-list",
    "statement": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
    "examples": [
        {"title":"Example 1","input":"head = [1,2,3,4,5]","output":"[5,4,3,2,1]","explain":"Reversed linked list."},
        {"title":"Example 2","input":"head = [1,2]","output":"[2,1]","explain":"Two elements."},
    ],
    "constraints":["0 &le; nodes &le; 5000","-5000 &le; Node.val &le; 5000"],
    "approaches":[
        {"name":"Iterative","time":"O(n)","space":"O(1)","notes":"Three pointers: prev, curr, next. Optimal.","cls":"optimal-row"},
        {"name":"Recursive","time":"O(n)","space":"O(n)","notes":"Clean but O(n) stack space.","cls":""},
    ],
    "optimal_approach":{"title":"Iterative — Three Pointers","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Maintain prev=None, curr=head. At each step: save next, point curr.next to prev, advance prev and curr."},
    "codes": _codes("""def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev""", "Reverse Linked List"),
    "insight_title":"Three Pointers is All You Need",
    "insight_text":"prev tracks the new list, curr is the node being processed, nxt saves the remaining list before we overwrite curr.next.",
    "tips":["<strong>Must-know:</strong> Write this perfectly from memory. Interviewers often use this as a baseline.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Apple — top universal problem."]
})

add_problem("q50", {
    "name": "Course Schedule", "num": 207, "diff": "Medium",
    "topics": ["Graph","BFS","Topological Sort","DFS"],
    "link": "https://leetcode.com/problems/course-schedule",
    "statement": "There are <code>numCourses</code> courses labeled 0 to numCourses-1. You are given prerequisites where <code>prerequisites[i] = [a, b]</code> means you must take b before a. Return <code>true</code> if you can finish all courses.",
    "examples": [
        {"title":"Example 1","input":"numCourses=2, prerequisites=[[1,0]]","output":"true","explain":"Take 0, then 1."},
        {"title":"Example 2","input":"numCourses=2, prerequisites=[[1,0],[0,1]]","output":"false","explain":"Cycle: 0→1→0."},
    ],
    "constraints":["1 &le; numCourses &le; 2000","0 &le; prerequisites.length &le; 5000"],
    "approaches":[
        {"name":"BFS Topological Sort (Kahn's)","time":"O(V+E)","space":"O(V+E)","notes":"Detect cycle via in-degree. Optimal.","cls":"optimal-row"},
        {"name":"DFS Cycle Detection","time":"O(V+E)","space":"O(V+E)","notes":"Track grey/black states. Also optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"BFS Topological Sort","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(V+E)","space":"O(V+E)",
        "explanation":"Build adjacency list and in-degree array. Start BFS with all zero in-degree nodes. As courses finish, decrement neighbors' in-degrees; add to queue when in-degree reaches 0. If total processed == numCourses, no cycle exists."},
    "codes": _codes("""from collections import deque

def canFinish(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)
        in_degree[a] += 1
    q = deque(i for i in range(numCourses) if in_degree[i] == 0)
    completed = 0
    while q:
        course = q.popleft()
        completed += 1
        for neighbor in adj[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                q.append(neighbor)
    return completed == numCourses""", "Course Schedule"),
    "insight_title":"Completed == numCourses ↔ No Cycle",
    "insight_text":"If there's a cycle, those nodes will never reach in-degree 0 and won't be processed. The count check at the end is O(1) and definitively detects any cycle.",
    "tips":["<strong>DFS vs BFS:</strong> Both work. BFS (Kahn's) is iterative and avoids recursion depth issues.",
            "<strong>Follow-up:</strong> Course Schedule II asks for the actual order — just return the processed list.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft."]
})

add_problem("q51", {
    "name": "Implement Trie (Prefix Tree)", "num": 208, "diff": "Medium",
    "topics": ["Trie","Hash Map","Design"],
    "link": "https://leetcode.com/problems/implement-trie-prefix-tree",
    "statement": "Implement a Trie data structure with <code>insert(word)</code>, <code>search(word)</code>, and <code>startsWith(prefix)</code> methods.",
    "examples": [
        {"title":"Example 1","input":'insert("apple"), search("apple")→true, search("app")→false, startsWith("app")→true, insert("app"), search("app")→true',"output":"[null,true,false,true,null,true]","explain":"Demonstrates insert, search, and prefix matching."},
    ],
    "constraints":["1 &le; word.length, prefix.length &le; 2000","Only lowercase English letters","At most 3*10<sup>4</sup> calls"],
    "approaches":[{"name":"Trie with HashMap children","time":"O(m) per ops","space":"O(m·n)","notes":"m=key length. Standard Trie. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Trie Node with HashMap","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(m)","space":"O(m·n)",
        "explanation":"Each TrieNode has a map of char→TrieNode children and an <code>is_end</code> flag. insert/search/startsWith all traverse the trie character by character."},
    "codes": _codes("""class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True""", "Implement Trie"),
    "insight_title":"Tries Excel at Prefix Queries",
    "insight_text":"A Trie's key strength: prefix queries and autocomplete in O(m) time (m = prefix length), faster than hash maps for prefix matching.",
    "tips":["<strong>Array vs HashMap children:</strong> If only lowercase ASCII, use array[26] for O(1) child access.",
            "<strong>Companies:</strong> Amazon, Google, Apple, Microsoft."]
})
