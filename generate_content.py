#!/usr/bin/env python3
"""
Generate FAANG-level HTML content for all 75 Blind 75 problems.
Writes directly into blind75-spa.html, replacing 'Content Pending' placeholders.
Then re-runs the page builder to regenerate individual pages.
"""
import os
import re
from bs4 import BeautifulSoup

INPUT_FILE = "blind75-spa.html"

# ── PROBLEM DATA ──────────────────────────────────────────────────────────────
# Each entry: (q_id, name, difficulty, leetcode_num, leetcode_slug, topics[], problem_desc, examples[], constraints[], approaches_table[], optimal_code{}, insight, interview_tips[])

PROBLEMS = {
"q2": {
    "name": "Two Sum",
    "num": 1,
    "diff": "Easy",
    "topics": ["Array", "Hash Map"],
    "link": "https://leetcode.com/problems/two-sum",
    "statement": "Given an array of integers <code>nums</code> and an integer <code>target</code>, return <strong>indices of the two numbers</strong> such that they add up to <code>target</code>. You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.",
    "examples": [
        {"title": "Example 1", "input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explain": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
        {"title": "Example 2", "input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explain": "nums[1] + nums[2] == 6."},
        {"title": "Example 3 (Edge)", "input": "nums = [3,3], target = 6", "output": "[0,1]", "explain": "Both elements are the same value. The hash map stores index 0, then finds the complement at index 1."}
    ],
    "constraints": ["2 &le; nums.length &le; 10<sup>4</sup>", "-10<sup>9</sup> &le; nums[i] &le; 10<sup>9</sup>", "-10<sup>9</sup> &le; target &le; 10<sup>9</sup>", "<strong>Exactly one valid answer exists</strong>"],
    "approaches": [
        {"name": "Brute Force", "time": "O(n&sup2;)", "space": "O(1)", "notes": "Check every pair. Simple but slow.", "cls": ""},
        {"name": "Hash Map (One-Pass)", "time": "O(n)", "space": "O(n)", "notes": "Store complement in map while iterating. Optimal.", "cls": "optimal-row"}
    ],
    "optimal_approach": {
        "title": "Hash Map &mdash; One Pass",
        "badge_cls": "badge-optimal",
        "badge_text": "Optimal",
        "time": "O(n)",
        "space": "O(n)",
        "explanation": "We iterate through the array once. For each element, we calculate its <strong>complement</strong> (<code>target - nums[i]</code>). If the complement already exists in our hash map, we've found the pair. Otherwise, we store <code>nums[i] : i</code> in the map. This gives us O(1) lookups and a single pass through the array.",
    },
    "codes": {
        "python": {
            "id_prefix": "opt",
            "lang": "python",
            "code": """def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i"""
        },
        "java": {
            "id_prefix": "opt",
            "lang": "java",
            "code": """public int[] twoSum(int[] nums, int target) {
    Map&lt;Integer, Integer&gt; map = new HashMap&lt;&gt;();
    for (int i = 0; i &lt; nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};  // no solution
}"""
        },
        "javascript": {
            "id_prefix": "opt",
            "lang": "javascript",
            "code": """var twoSum = function(nums, target) {
    const map = new Map();
    for (let i = 0; i &lt; nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        map.set(nums[i], i);
    }
};"""
        },
        "go": {
            "id_prefix": "opt",
            "lang": "go",
            "code": """func twoSum(nums []int, target int) []int {
    seen := make(map[int]int)
    for i, num := range nums {
        complement := target - num
        if j, ok := seen[complement]; ok {
            return []int{j, i}
        }
        seen[num] = i
    }
    return nil
}"""
        }
    },
    "flow_matrix": {
        "headers": ["Step", "i", "num", "Complement", "In Map?", "Hash Map State", "Action"],
        "rows": [
            ["1", "0", "2", "<code>9 - 2 = 7</code>", "No", "<code>{2: 0}</code>", "Store <code>num: i</code>"],
            ["2", "1", "7", "<code>9 - 7 = 2</code>", "Yes", "<code>{2: 0}</code>", "Return <code>[map[2], 1] &rarr; [0, 1]</code>"]
        ]
    },
    "insight_title": "Why One-Pass Works",
    "insight_text": "At each index <code>i</code>, we ask: \"Have I already seen the number that would complete a pair with <code>nums[i]</code>?\" If yes, we return immediately. If no, we record <code>nums[i]</code> for future lookups. Because hash map operations are O(1) average case, the total time is <strong>O(n)</strong>.",
    "tips": [
        "<strong>Don't jump to the brute force:</strong> Mention it briefly, then immediately pivot to the hash map approach. Interviewers expect you to identify the O(n) solution quickly for this classic problem.",
        "<strong>Clarify constraints:</strong> \"Can I return indices in any order?\" \"Can there be duplicate values?\" \"Is there always exactly one solution?\" These questions show thoroughness.",
        "<strong>One-pass vs Two-pass:</strong> You can do two passes (build map, then search), but the one-pass version is cleaner and shows mastery. Explain why it works: by the time we reach the second element of a pair, the first is already in the map.",
        "<strong>Edge case:</strong> Two identical values like <code>[3,3]</code> with target 6. The one-pass approach handles this naturally since we check before inserting.",
        "<strong>Companies that asked this:</strong> Google, Amazon, Meta, Apple, Microsoft, Bloomberg, Uber&mdash;virtually every tech company."
    ]
},

"q3": {
    "name": "Longest Substring Without Repeating Characters",
    "num": 3,
    "diff": "Medium",
    "topics": ["String", "Sliding Window", "Hash Map"],
    "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters",
    "statement": "Given a string <code>s</code>, find the length of the <strong>longest substring</strong> without repeating characters.",
    "examples": [
        {"title": "Example 1", "input": 's = "abcabcbb"', "output": "3", "explain": 'The answer is "abc", with length 3.'},
        {"title": "Example 2", "input": 's = "bbbbb"', "output": "1", "explain": 'The answer is "b", with length 1.'},
        {"title": "Example 3", "input": 's = "pwwkew"', "output": "3", "explain": 'The answer is "wke", with length 3. Note that "pwke" is a subsequence, not a substring.'}
    ],
    "constraints": ["0 &le; s.length &le; 5 * 10<sup>4</sup>", "<code>s</code> consists of English letters, digits, symbols, and spaces"],
    "approaches": [
        {"name": "Brute Force", "time": "O(n&sup3;)", "space": "O(min(n,m))", "notes": "Check all substrings for uniqueness.", "cls": ""},
        {"name": "Sliding Window + Set", "time": "O(2n)=O(n)", "space": "O(min(n,m))", "notes": "Expand right, shrink left on duplicate.", "cls": ""},
        {"name": "Sliding Window + Map", "time": "O(n)", "space": "O(min(n,m))", "notes": "Jump left pointer directly. Optimal.", "cls": "optimal-row"}
    ],
    "optimal_approach": {
        "title": "Sliding Window + Hash Map",
        "badge_cls": "badge-optimal",
        "badge_text": "Optimal",
        "time": "O(n)",
        "space": "O(min(n, m))",
        "explanation": "Maintain a window <code>[left, right]</code> and a hash map storing each character's last-seen index. When we encounter a duplicate, we jump <code>left</code> to <code>max(left, map[char] + 1)</code> instead of sliding one position at a time. This ensures each character is visited at most once by the right pointer.",
    },
    "codes": {
        "python": {
            "id_prefix": "opt",
            "lang": "python",
            "code": """def lengthOfLongestSubstring(s):
    char_map = {}
    left = 0
    longest = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        longest = max(longest, right - left + 1)
    return longest"""
        },
        "java": {
            "id_prefix": "opt",
            "lang": "java",
            "code": """public int lengthOfLongestSubstring(String s) {
    Map&lt;Character, Integer&gt; map = new HashMap&lt;&gt;();
    int left = 0, longest = 0;
    for (int right = 0; right &lt; s.length(); right++) {
        char c = s.charAt(right);
        if (map.containsKey(c) &amp;&amp; map.get(c) &gt;= left) {
            left = map.get(c) + 1;
        }
        map.put(c, right);
        longest = Math.max(longest, right - left + 1);
    }
    return longest;
}"""
        },
        "javascript": {
            "id_prefix": "opt",
            "lang": "javascript",
            "code": """var lengthOfLongestSubstring = function(s) {
    const map = new Map();
    let left = 0, longest = 0;
    for (let right = 0; right &lt; s.length; right++) {
        const c = s[right];
        if (map.has(c) &amp;&amp; map.get(c) &gt;= left) {
            left = map.get(c) + 1;
        }
        map.set(c, right);
        longest = Math.max(longest, right - left + 1);
    }
    return longest;
};"""
        },
        "go": {
            "id_prefix": "opt",
            "lang": "go",
            "code": """func lengthOfLongestSubstring(s string) int {
    charMap := make(map[byte]int)
    left, longest := 0, 0
    for right := 0; right &lt; len(s); right++ {
        c := s[right]
        if idx, ok := charMap[c]; ok &amp;&amp; idx &gt;= left {
            left = idx + 1
        }
        charMap[c] = right
        if right-left+1 &gt; longest {
            longest = right - left + 1
        }
    }
    return longest
}"""
        }
    },
    "flow_matrix": {
        "headers": ["Iteration (right, char)", "Map State `char: index`", "Left Pointer", "Action & Max Len"],
        "rows": [
            ["0, 'a'", "{'a': 0}", "0 (No dupes)", "max(0, 1) = 1"],
            ["1, 'b'", "{'a': 0, 'b': 1}", "0 (No dupes)", "max(1, 2) = 2"],
            ["2, 'c'", "{'a': 0, 'b': 1, 'c': 2}", "0 (No dupes)", "max(2, 3) = 3"],
            ["3, 'a'", "{'a': 3, 'b': 1, 'c': 2}", "max(0, map['a']+1)=1", "max(3, 3) = 3"],
            ["4, 'b'", "{'a': 3, 'b': 4, 'c': 2}", "max(1, map['b']+1)=2", "max(3, 3) = 3"]
        ]
    },
    "insight_title": "Why the Map Jump is O(n)",
    "insight_text": "With the basic set approach, the left pointer might slide one-by-one, leading to O(2n) in the worst case. By storing each character's last index in a map and jumping <code>left</code> directly, the right pointer visits each character exactly once. Total: <strong>O(n)</strong>.",
    "tips": [
        "<strong>Clarify:</strong> \"Is the string ASCII or Unicode?\" This affects the space bound (128 vs 65536 possible chars).",
        "<strong>Explain the window invariant:</strong> \"At all times, the substring s[left..right] contains no duplicates.\"",
        "<strong>Why max(left, map[char]+1)?</strong> Because the character might have been seen before <code>left</code> (already outside the window). Taking the max prevents moving left backwards.",
        "<strong>Follow-up:</strong> \"What if we need the actual substring, not just its length?\" Track the start index of the best window.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Bloomberg, Apple."
    ]
},

"q4": {
    "name": "Longest Palindromic Substring",
    "num": 5,
    "diff": "Medium",
    "topics": ["String", "Dynamic Programming"],
    "link": "https://leetcode.com/problems/longest-palindromic-substring",
    "statement": "Given a string <code>s</code>, return the <strong>longest palindromic substring</strong> in <code>s</code>.",
    "examples": [
        {"title": "Example 1", "input": 's = "babad"', "output": '"bab"', "explain": '"aba" is also a valid answer.'},
        {"title": "Example 2", "input": 's = "cbbd"', "output": '"bb"', "explain": "The longest palindrome has length 2."},
        {"title": "Example 3 (Edge)", "input": 's = "a"', "output": '"a"', "explain": "Single character is always a palindrome."}
    ],
    "constraints": ["1 &le; s.length &le; 1000", "<code>s</code> consists of only digits and English letters"],
    "approaches": [
        {"name": "Brute Force", "time": "O(n&sup3;)", "space": "O(1)", "notes": "Check all substrings for palindrome property.", "cls": ""},
        {"name": "Dynamic Programming", "time": "O(n&sup2;)", "space": "O(n&sup2;)", "notes": "Table dp[i][j] = is s[i..j] a palindrome.", "cls": ""},
        {"name": "Expand Around Center", "time": "O(n&sup2;)", "space": "O(1)", "notes": "For each center, expand outward. Optimal in space.", "cls": "optimal-row"}
    ],
    "optimal_approach": {
        "title": "Expand Around Center",
        "badge_cls": "badge-optimal",
        "badge_text": "Optimal",
        "time": "O(n&sup2;)",
        "space": "O(1)",
        "explanation": "A palindrome mirrors around its center. There are <code>2n - 1</code> possible centers (each character, plus each gap between characters for even-length palindromes). For each center, expand outward while characters match. Track the longest palindrome found.",
    },
    "codes": {
        "python": {
            "id_prefix": "opt",
            "lang": "python",
            "code": """def longestPalindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)       # odd-length
        even = expand(i, i + 1)  # even-length
        result = max(result, odd, even, key=len)
    return result"""
        },
        "java": {
            "id_prefix": "opt",
            "lang": "java",
            "code": """public String longestPalindrome(String s) {
    int start = 0, maxLen = 0;
    for (int i = 0; i &lt; s.length(); i++) {
        int len1 = expand(s, i, i);     // odd
        int len2 = expand(s, i, i + 1); // even
        int len = Math.max(len1, len2);
        if (len &gt; maxLen) {
            maxLen = len;
            start = i - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}

private int expand(String s, int l, int r) {
    while (l &gt;= 0 &amp;&amp; r &lt; s.length() &amp;&amp; s.charAt(l) == s.charAt(r)) {
        l--; r++;
    }
    return r - l - 1;
}"""
        },
        "javascript": {
            "id_prefix": "opt",
            "lang": "javascript",
            "code": """var longestPalindrome = function(s) {
    let start = 0, maxLen = 0;
    function expand(l, r) {
        while (l >= 0 && r < s.length && s[l] === s[r]) { l--; r++; }
        return r - l - 1;
    }
    for (let i = 0; i < s.length; i++) {
        const len = Math.max(expand(i, i), expand(i, i + 1));
        if (len > maxLen) {
            maxLen = len;
            start = i - Math.floor((len - 1) / 2);
        }
    }
    return s.substring(start, start + maxLen);
};"""
        },
        "go": {
            "id_prefix": "opt",
            "lang": "go",
            "code": """func longestPalindrome(s string) string {
    start, maxLen := 0, 0
    expand := func(l, r int) int {
        for l >= 0 && r < len(s) && s[l] == s[r] {
            l--; r++
        }
        return r - l - 1
    }
    for i := range s {
        l1 := expand(i, i)
        l2 := expand(i, i+1)
        l := l1
        if l2 > l { l = l2 }
        if l > maxLen {
            maxLen = l
            start = i - (l-1)/2
        }
    }
    return s[start : start+maxLen]
}"""
        }
    },
    "insight_title": "Why 2n-1 Centers?",
    "insight_text": "Each of the <code>n</code> characters can be the center of an odd-length palindrome. Each of the <code>n-1</code> gaps between adjacent characters can be the center of an even-length palindrome. Total centers: <code>2n - 1</code>. Expansion from each center takes O(n) worst case, giving <strong>O(n&sup2;)</strong> total.",
    "tips": [
        "<strong>Mention Manacher's:</strong> Say you know about the O(n) Manacher's algorithm, but the expand-around-center approach is cleaner and sufficient for interviews.",
        "<strong>Handle both odd and even:</strong> Always expand from both (i, i) and (i, i+1). Forgetting even-length palindromes is a common mistake.",
        "<strong>Edge cases:</strong> Single character strings, strings with all identical characters, empty strings.",
        "<strong>Follow-up:</strong> \"Count all palindromic substrings\" uses the same expand technique but sums counts instead of tracking max.",
        "<strong>Companies:</strong> Amazon, Microsoft, Meta, Google, Goldman Sachs."
    ]
},

"q5": {
    "name": "Clone Graph",
    "num": 133,
    "diff": "Medium",
    "topics": ["Graph", "BFS", "DFS", "Hash Map"],
    "link": "https://leetcode.com/problems/clone-graph",
    "statement": "Given a reference of a node in a <strong>connected undirected graph</strong>, return a <strong>deep copy</strong> (clone) of the graph. Each node contains a value (<code>int</code>) and a list of its neighbors.",
    "examples": [
        {"title": "Example 1", "input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explain": "4 nodes. Node 1 connects to 2,4. Node 2 connects to 1,3. etc. The output is a deep copy with the same structure."},
        {"title": "Example 2", "input": "adjList = [[]]", "output": "[[]]", "explain": "Single node with no neighbors."},
        {"title": "Example 3 (Edge)", "input": "adjList = []", "output": "[]", "explain": "Empty graph, return null/nil."}
    ],
    "constraints": ["0 &le; number of nodes &le; 100", "1 &le; Node.val &le; 100", "Node values are unique", "No self-loops or repeated edges", "Graph is connected"],
    "approaches": [
        {"name": "DFS + HashMap", "time": "O(V + E)", "space": "O(V)", "notes": "Recursively clone, use map to track visited.", "cls": "optimal-row"},
        {"name": "BFS + HashMap", "time": "O(V + E)", "space": "O(V)", "notes": "Level-order clone with queue. Also optimal.", "cls": "optimal-row"}
    ],
    "optimal_approach": {
        "title": "DFS + Hash Map",
        "badge_cls": "badge-optimal",
        "badge_text": "Optimal",
        "time": "O(V + E)",
        "space": "O(V)",
        "explanation": "Use a hash map to store <code>original node &rarr; cloned node</code>. When visiting a node, create its clone, add it to the map, then recursively clone all neighbors. If a neighbor is already in the map, reuse the cached clone to avoid infinite loops.",
    },
    "codes": {
        "python": {
            "id_prefix": "opt",
            "lang": "python",
            "code": """def cloneGraph(node):
    if not node:
        return None
    cloned = {}

    def dfs(n):
        if n in cloned:
            return cloned[n]
        copy = Node(n.val)
        cloned[n] = copy
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)"""
        },
        "java": {
            "id_prefix": "opt",
            "lang": "java",
            "code": """public Node cloneGraph(Node node) {
    if (node == null) return null;
    Map&lt;Node, Node&gt; map = new HashMap&lt;&gt;();
    return dfs(node, map);
}

private Node dfs(Node node, Map&lt;Node, Node&gt; map) {
    if (map.containsKey(node)) return map.get(node);
    Node copy = new Node(node.val);
    map.put(node, copy);
    for (Node neighbor : node.neighbors) {
        copy.neighbors.add(dfs(neighbor, map));
    }
    return copy;
}"""
        },
        "javascript": {
            "id_prefix": "opt",
            "lang": "javascript",
            "code": """var cloneGraph = function(node) {
    if (!node) return null;
    const map = new Map();

    function dfs(n) {
        if (map.has(n)) return map.get(n);
        const copy = new Node(n.val);
        map.set(n, copy);
        for (const neighbor of n.neighbors) {
            copy.neighbors.push(dfs(neighbor));
        }
        return copy;
    }
    return dfs(node);
};"""
        },
        "go": {
            "id_prefix": "opt",
            "lang": "go",
            "code": """func cloneGraph(node *Node) *Node {
    if node == nil { return nil }
    cloned := map[*Node]*Node{}

    var dfs func(*Node) *Node
    dfs = func(n *Node) *Node {
        if c, ok := cloned[n]; ok { return c }
        copy := &amp;Node{Val: n.Val}
        cloned[n] = copy
        for _, nb := range n.Neighbors {
            copy.Neighbors = append(copy.Neighbors, dfs(nb))
        }
        return copy
    }
    return dfs(node)
}"""
        }
    },
    "insight_title": "Why HashMap Prevents Infinite Loops",
    "insight_text": "In a graph with cycles, naive recursion would revisit nodes infinitely. The hash map acts as a \"visited\" set: when we encounter a node that's already been cloned, we return the cached clone immediately. Each node and edge is processed exactly once, giving <strong>O(V + E)</strong> total.",
    "tips": [
        "<strong>Start with the base case:</strong> Always handle the null/empty graph first.",
        "<strong>Explain the map's dual purpose:</strong> It serves as both a visited set and a mapping from original to cloned nodes.",
        "<strong>DFS vs BFS:</strong> Both are equally optimal. DFS is more concise; BFS is iterative. Mention both and let the interviewer choose.",
        "<strong>Common mistake:</strong> Forgetting to add the cloned node to the map BEFORE recursing into neighbors, which causes infinite recursion in cyclic graphs.",
        "<strong>Companies:</strong> Meta, Google, Amazon, Microsoft, Uber."
    ]
},

}

# ── HTML GENERATOR ────────────────────────────────────────────────────────────

def generate_panel_html(q_id, data):
    """Generate the full question-panel HTML for a problem."""
    # Header badges
    topics_html = "".join(f'<span class="topic-tag">{t}</span>' for t in data["topics"])
    diff_cls = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}[data["diff"]]
    
    # Examples
    examples_html = ""
    for ex in data["examples"]:
        examples_html += f"""
            <div class="example-block">
                <div class="example-header">{ex["title"]}</div>
                <div class="example-body">
                    <div><span class="label">Input: </span><span class="val">{ex["input"]}</span></div>
                    <div><span class="label">Output: </span><span class="val">{ex["output"]}</span></div>
                    <div class="explanation">{ex["explain"]}</div>
                </div>
            </div>"""
    
    # Constraints
    constraints_html = "".join(f"<li>{c}</li>" for c in data["constraints"])
    
    # Approaches table
    rows_html = ""
    for a in data["approaches"]:
        cls = f' class="{a["cls"]}"' if a["cls"] else ""
        rows_html += f"""
                <tr{cls}>
                    <td>{a["name"]}</td>
                    <td><code>{a["time"]}</code></td>
                    <td><code>{a["space"]}</code></td>
                    <td>{a["notes"]}</td>
                </tr>"""
    
    # Code tabs
    opt = data["optimal_approach"]
    codes = data["codes"]
    tab_buttons = ""
    tab_contents = ""
    first = True
    for lang_key, lang_data in codes.items():
        active = " active" if first else ""
        tab_id = f"{lang_data['id_prefix']}-{lang_key}-{q_id}"
        display_name = {"python": "Python", "java": "Java", "javascript": "JavaScript", "go": "Go"}[lang_key]
        tab_buttons += f'<button class="tab-btn{active}" onclick="switchTab(this, \'{tab_id}\')">{display_name}</button>\n                    '
        tab_contents += f"""
                <div class="tab-content{active}" id="{tab_id}">
                    <div class="code-wrap">
                        <pre><code class="language-{lang_data['lang']}">{lang_data["code"]}</code></pre>
                    </div>
                </div>"""
        first = False
    
    # Interview tips
    tips_html = "".join(f"<li>{t}</li>" for t in data["tips"])
    
    # Optional Diagram and Flow Matrix
    diagram_html = ""
    if "diagram" in data and data["diagram"]:
        diagram_html = f'''
            <div class="diagram-container">
                {data["diagram"]}
            </div>'''

    flow_html = ""
    if "flow_matrix" in data and data["flow_matrix"]:
        fm = data["flow_matrix"]
        headers = "".join(f"<th>{h}</th>" for h in fm["headers"])
        rows = ""
        for r in fm["rows"]:
            rows += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
        flow_html = f'''
            <div class="flow-matrix-container">
                <table class="flow-matrix-table">
                    <thead><tr>{headers}</tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>'''
            
    return f"""
        <div class="question-panel" id="{q_id}">
            <div class="q-header">
                <div class="q-header-meta">
                    <span class="q-number-badge"># {data["num"]} &middot; LeetCode</span>
                    <span class="diff-badge {diff_cls}">{data["diff"]}</span>
                    {topics_html}
                </div>
                <h1 class="q-title">{data["name"]}</h1>
                <p class="q-source"><a href="{data["link"]}" target="_blank">{data["link"].replace("https://","")}</a> &middot; Blind 75 &middot; FAANG favourite</p>
            </div>

            <hr class="section-rule">

            <div class="problem-statement">
                <h3>Problem Statement</h3>
                <p>{data["statement"]}</p>
            </div>

            <div class="examples">
{examples_html}
            </div>

            <div class="constraints">
                <h4>Constraints</h4>
                <ul>
                    {constraints_html}
                </ul>
            </div>

            <h2 class="approach-title">Approaches Comparison</h2>
            <table class="compare-table">
                <tr>
                    <th>Approach</th>
                    <th>Time</th>
                    <th>Space</th>
                    <th>Notes</th>
                </tr>
{rows_html}
            </table>

            <h2 class="approach-title">{opt["title"]} <span class="approach-badge {opt["badge_cls"]}">{opt["badge_text"]}</span></h2>

            <div class="complexity-row">
                <div class="complexity-pill">
                    <span class="cp-label">Time</span>
                    <span class="cp-value">{opt["time"]}</span>
                </div>
                <div class="complexity-pill">
                    <span class="cp-label">Space</span>
                    <span class="cp-value">{opt["space"]}</span>
                </div>
            </div>

            <p class="approach-explanation">{opt["explanation"]}</p>

            <div class="code-tabs">
                <div class="tab-buttons">
                    {tab_buttons}
                </div>
{tab_contents}
            </div>

            {diagram_html}
            {flow_html}

            <div class="insight" style="margin-top: 20px;">
                <div class="insight-title">{data["insight_title"]}</div>
                <p>{data["insight_text"]}</p>
            </div>

            <div class="interview-tips">
                <h3>Interview Playbook</h3>
                <ol>
                    {tips_html}
                </ol>
            </div>

            <button class="mark-solved-btn" id="solve-{q_id}" onclick="markSolved('{q_id}', this)">
                Mark as Solved
            </button>
        </div>
"""


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    if "</body>" in raw:
        raw = raw.split("</body>")[0] + "</body>\n</html>"
    
    soup = BeautifulSoup(raw, "html.parser")
    main_panel = soup.find("div", id="main-panel")
    
    injected = 0
    for q_id, data in PROBLEMS.items():
        panel = soup.find("div", id=q_id, class_="question-panel")
        
        if panel and "Content Pending" in str(panel):
            # Replace existing placeholder
            new_html = generate_panel_html(q_id, data)
            new_soup = BeautifulSoup(new_html, "html.parser")
            new_panel = new_soup.find("div", id=q_id)
            if new_panel:
                panel.replace_with(new_panel)
                injected += 1
                print(f"  Replaced placeholder for {data['name']} ({q_id})")
        elif not panel:
            # Panel missing entirely, inject it
            new_html = generate_panel_html(q_id, data)
            new_soup = BeautifulSoup(new_html, "html.parser")
            new_panel = new_soup.find("div", id=q_id)
            if new_panel and main_panel:
                main_panel.append(new_panel)
                injected += 1
                print(f"  Injected new panel for {data['name']} ({q_id})")
        else:
            print(f"  Skipping {data['name']} ({q_id}) - already has content")

    if injected > 0:
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"\nInjected {injected} problems into {INPUT_FILE}.")
    else:
        print("No problems needed injection.")
    
    # Re-run the page builder
    print("\nRebuilding individual pages...")
    os.system("python3 build_blind75_pages.py")
    print("Done!")


if __name__ == "__main__":
    main()
