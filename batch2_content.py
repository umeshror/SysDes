"""Batch 2 problems: q6 Graph Valid Tree through q12 3Sum"""
from shared_generator import add_problem

add_problem("q6", {
    "name": "Graph Valid Tree",
    "num": 261,
    "diff": "Medium",
    "topics": ["Graph", "Union Find", "DFS"],
    "link": "https://leetcode.com/problems/graph-valid-tree",
    "statement": "Given <code>n</code> nodes labeled <code>0</code> to <code>n-1</code> and a list of undirected edges, return <code>true</code> if these edges form a <strong>valid tree</strong>. A valid tree has exactly <code>n-1</code> edges and is fully connected with no cycles.",
    "examples": [
        {"title": "Example 1", "input": "n=5, edges=[[0,1],[0,2],[0,3],[1,4]]", "output": "true", "explain": "4 edges for 5 nodes, fully connected, no cycle."},
        {"title": "Example 2", "input": "n=5, edges=[[0,1],[1,2],[2,3],[1,3],[1,4]]", "output": "false", "explain": "Contains a cycle: 1-2-3-1."},
    ],
    "constraints": ["1 &le; n &le; 2000", "0 &le; edges.length &le; 5000", "edges[i].length == 2", "No self-loops or duplicate edges"],
    "approaches": [
        {"name": "DFS Cycle Detection", "time": "O(V+E)", "space": "O(V+E)", "notes": "Build adjacency list, DFS checking for back edges.", "cls": ""},
        {"name": "Union Find", "time": "O(E &alpha;(n))", "space": "O(V)", "notes": "Union edges; if both nodes already connected, cycle found. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Union Find",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(E &alpha;(n))", "space": "O(V)",
        "explanation": "Two conditions must be true for a valid tree: (1) exactly n-1 edges, (2) no cycle. Use Union-Find: for each edge, if both endpoints already share a root, a cycle exists. Afterwards verify all nodes are connected by checking a single root.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def validTree(n, edges):
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return False
        parent[pu] = pv
    return True"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public boolean validTree(int n, int[][] edges) {
    if (edges.length != n - 1) return false;
    int[] parent = new int[n];
    for (int i = 0; i &lt; n; i++) parent[i] = i;

    for (int[] e : edges) {
        int pu = find(parent, e[0]);
        int pv = find(parent, e[1]);
        if (pu == pv) return false;
        parent[pu] = pv;
    }
    return true;
}
int find(int[] p, int x) {
    while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; }
    return x;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var validTree = function(n, edges) {
    if (edges.length !== n - 1) return false;
    const parent = Array.from({length:n},(_,i)=>i);
    const find = x => { while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x];} return x; };
    for (const [u,v] of edges) {
        const [pu,pv]=[find(u),find(v)];
        if (pu===pv) return false;
        parent[pu]=pv;
    }
    return true;
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func validTree(n int, edges [][]int) bool {
    if len(edges) != n-1 { return false }
    parent := make([]int, n)
    for i := range parent { parent[i] = i }
    var find func(int) int
    find = func(x int) int {
        for parent[x] != x { parent[x]=parent[parent[x]]; x=parent[x] }
        return x
    }
    for _, e := range edges {
        pu, pv := find(e[0]), find(e[1])
        if pu == pv { return false }
        parent[pu] = pv
    }
    return true
}"""},
    },
    "insight_title": "Valid Tree = n-1 Edges + No Cycle",
    "insight_text": "Any connected graph with n nodes and n-1 edges is a tree. Checking edge count first is O(1) and eliminates many invalid cases before running Union-Find.",
    "tips": [
        "<strong>State the two conditions upfront:</strong> n-1 edges AND fully connected (no cycles). This shows structural thinking.",
        "<strong>DFS vs Union-Find:</strong> Both work. Union-Find is more elegant and slightly faster with path compression.",
        "<strong>Edge count check first:</strong> If edges.length != n-1, return false immediately without traversal.",
        "<strong>Companies:</strong> Google, LinkedIn, Meta, Amazon.",
    ]
})

add_problem("q7", {
    "name": "Palindromic Substrings",
    "num": 647,
    "diff": "Medium",
    "topics": ["String", "Dynamic Programming"],
    "link": "https://leetcode.com/problems/palindromic-substrings",
    "statement": "Given a string <code>s</code>, return the <strong>number of palindromic substrings</strong> in it. A string is a palindrome when it reads the same backward as forward.",
    "examples": [
        {"title": "Example 1", "input": 's = "abc"', "output": "3", "explain": '"a", "b", "c" are palindromes.'},
        {"title": "Example 2", "input": 's = "aaa"', "output": "6", "explain": '"a","a","a","aa","aa","aaa" are 6 palindromes.'},
    ],
    "constraints": ["1 &le; s.length &le; 1000", "<code>s</code> consists of lowercase English letters"],
    "approaches": [
        {"name": "Brute Force", "time": "O(n&sup3;)", "space": "O(1)", "notes": "Check every substring.", "cls": ""},
        {"name": "Expand Around Center", "time": "O(n&sup2;)", "space": "O(1)", "notes": "Count palindromes by expanding from each center. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Expand Around Center",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n&sup2;)", "space": "O(1)",
        "explanation": "For each of the 2n-1 centers (characters and gaps between them), expand outward while the characters match, counting each valid palindrome. This is identical in structure to #647 but counts instead of tracks maximum length.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def countSubstrings(s):
    count = 0
    def expand(l, r):
        nonlocal count
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
    for i in range(len(s)):
        expand(i, i)      # odd-length
        expand(i, i + 1)  # even-length
    return count"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public int countSubstrings(String s) {
    int count = 0;
    for (int i = 0; i &lt; s.length(); i++) {
        count += expand(s, i, i);
        count += expand(s, i, i + 1);
    }
    return count;
}
int expand(String s, int l, int r) {
    int c = 0;
    while (l &gt;= 0 &amp;&amp; r &lt; s.length() &amp;&amp; s.charAt(l)==s.charAt(r)) {
        c++; l--; r++;
    }
    return c;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var countSubstrings = function(s) {
    let count = 0;
    const expand = (l, r) => {
        while (l >= 0 && r < s.length && s[l] === s[r]) { count++; l--; r++; }
    };
    for (let i = 0; i < s.length; i++) {
        expand(i, i); expand(i, i + 1);
    }
    return count;
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func countSubstrings(s string) int {
    count := 0
    expand := func(l, r int) {
        for l >= 0 && r < len(s) && s[l] == s[r] {
            count++; l--; r++
        }
    }
    for i := range s {
        expand(i, i); expand(i, i+1)
    }
    return count
}"""},
    },
    "insight_title": "Same Technique as Longest Palindromic Substring",
    "insight_text": "Both problems use expand-around-center. Here, each successful expansion increments the count. 2n-1 centers, O(n) expansion each = <strong>O(n&sup2;)</strong> total.",
    "tips": [
        "<strong>Don't forget even-length palindromes</strong> — expand from (i, i+1) gaps.",
        "<strong>Relate to #5:</strong> If the interviewer asks about Longest Palindromic Substring next, explain it uses the same technique but tracks max length.",
        "<strong>Companies:</strong> Amazon, Microsoft, Google.",
    ]
})

add_problem("q8", {
    "name": "Container With Most Water",
    "num": 11,
    "diff": "Medium",
    "topics": ["Array", "Two Pointers", "Greedy"],
    "link": "https://leetcode.com/problems/container-with-most-water",
    "statement": "Given an integer array <code>height</code> of length <code>n</code>, there are <code>n</code> vertical lines drawn at each index. Find two lines that together with the x-axis form a container that holds the <strong>most water</strong>. Return the <strong>maximum amount of water</strong> the container can store.",
    "examples": [
        {"title": "Example 1", "input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49", "explain": "Lines at index 1 (height=8) and index 8 (height=7). Water = min(8,7) * (8-1) = 7*7 = 49."},
        {"title": "Example 2", "input": "height = [1,1]", "output": "1", "explain": "Only two lines, area = min(1,1) * 1 = 1."},
    ],
    "constraints": ["n == height.length", "2 &le; n &le; 10<sup>5</sup>", "0 &le; height[i] &le; 10<sup>4</sup>"],
    "approaches": [
        {"name": "Brute Force", "time": "O(n&sup2;)", "space": "O(1)", "notes": "Check all pairs of lines.", "cls": ""},
        {"name": "Two Pointers", "time": "O(n)", "space": "O(1)", "notes": "Move the shorter pointer inward. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Two Pointers",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n)", "space": "O(1)",
        "explanation": "Start with pointers at both ends (maximum width). At each step, compute the area and update the max. Move the pointer pointing to the <strong>shorter line</strong> inward — moving the taller line can never increase the area (width decreases, height is still limited by the short line).",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, max = 0;
    while (left &lt; right) {
        max = Math.max(max, Math.min(height[left], height[right]) * (right - left));
        if (height[left] &lt; height[right]) left++;
        else right--;
    }
    return max;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var maxArea = function(height) {
    let left = 0, right = height.length - 1, max = 0;
    while (left < right) {
        max = Math.max(max, Math.min(height[left], height[right]) * (right - left));
        if (height[left] < height[right]) left++;
        else right--;
    }
    return max;
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func maxArea(height []int) int {
    left, right, max := 0, len(height)-1, 0
    for left < right {
        h := height[left]
        if height[right] < h { h = height[right] }
        if area := h * (right - left); area > max { max = area }
        if height[left] < height[right] { left++ } else { right-- }
    }
    return max
}"""},
    },
    "insight_title": "Why Move the Shorter Pointer?",
    "insight_text": "The current area is bounded by <code>min(h[left], h[right])</code>. If we move the taller pointer, the width decreases AND the bottleneck height stays the same or worsens. Moving the shorter pointer is the only way to potentially increase the min height. This greedy choice provably covers all candidates.",
    "tips": [
        "<strong>Key insight:</strong> Area = min(heights) * width. Moving the taller bar can never help — the bottleneck is the shorter bar.",
        "<strong>Prove the greedy:</strong> When we discard a configuration (by moving a pointer), argue that we're not missing any better solution.",
        "<strong>Don't confuse with Trapping Rain Water</strong> (#42) which requires a different DP/stack approach.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Bloomberg.",
    ]
})

add_problem("q9", {
    "name": "Word Break",
    "num": 139,
    "diff": "Medium",
    "topics": ["String", "Dynamic Programming", "Trie"],
    "link": "https://leetcode.com/problems/word-break",
    "statement": "Given a string <code>s</code> and a dictionary of strings <code>wordDict</code>, return <code>true</code> if <code>s</code> can be segmented into a space-separated sequence of one or more dictionary words.",
    "examples": [
        {"title": "Example 1", "input": 's = "leetcode", wordDict = ["leet","code"]', "output": "true", "explain": '"leetcode" = "leet" + "code".'},
        {"title": "Example 2", "input": 's = "applepenapple", wordDict = ["apple","pen"]', "output": "true", "explain": '"applepenapple" = "apple"+"pen"+"apple". Words can be reused.'},
        {"title": "Example 3", "input": 's = "catsandog", wordDict = ["cats","dog","sand","and","cat"]', "output": "false", "explain": "Cannot be segmented into dictionary words."},
    ],
    "constraints": ["1 &le; s.length &le; 300", "1 &le; wordDict.length &le; 1000", "1 &le; wordDict[i].length &le; 20", "s and wordDict[i] consist of lowercase letters", "All wordDict strings are unique"],
    "approaches": [
        {"name": "Brute Force (Recursion)", "time": "O(2<sup>n</sup>)", "space": "O(n)", "notes": "Try all cuts; exponential without memoization.", "cls": ""},
        {"name": "DP Bottom-Up", "time": "O(n<sup>2</sup>&middot;m)", "space": "O(n)", "notes": "dp[i] = can s[0..i] be segmented. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Dynamic Programming",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n&sup2; &middot; m)", "space": "O(n)",
        "explanation": "<code>dp[i]</code> means the first <code>i</code> characters of <code>s</code> can be segmented. For each position, look back from all <code>j &lt; i</code>: if <code>dp[j]</code> is true and <code>s[j:i]</code> is in the word set, set <code>dp[i] = true</code>.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True       # empty string is always valid

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public boolean wordBreak(String s, List&lt;String&gt; wordDict) {
    Set&lt;String&gt; set = new HashSet&lt;&gt;(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i &lt;= n; i++) {
        for (int j = 0; j &lt; i; j++) {
            if (dp[j] &amp;&amp; set.contains(s.substring(j, i))) {
                dp[i] = true; break;
            }
        }
    }
    return dp[n];
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var wordBreak = function(s, wordDict) {
    const set = new Set(wordDict);
    const n = s.length;
    const dp = Array(n + 1).fill(false);
    dp[0] = true;
    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            if (dp[j] && set.has(s.slice(j, i))) { dp[i] = true; break; }
        }
    }
    return dp[n];
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func wordBreak(s string, wordDict []string) bool {
    set := map[string]bool{}
    for _, w := range wordDict { set[w] = true }
    n := len(s)
    dp := make([]bool, n+1)
    dp[0] = true
    for i := 1; i &lt;= n; i++ {
        for j := 0; j &lt; i; j++ {
            if dp[j] &amp;&amp; set[s[j:i]] { dp[i] = true; break }
        }
    }
    return dp[n]
}"""},
    },
    "insight_title": "dp[0] = true is the Anchor",
    "insight_text": "The base case <code>dp[0] = true</code> means an empty prefix is trivially segmentable. Every dp[i] is built on top of this: if some earlier position j is true and s[j:i] is a word, then i is reachable.",
    "tips": [
        "<strong>Use a set for O(1) word lookup</strong> — converting wordDict to a set reduces the inner loop from O(m*len) to O(len).",
        "<strong>dp[0] = true:</strong> This base case trips people up. Explain it means ''we start before the string with a valid empty segmentation''.",
        "<strong>Optimisation:</strong> Only check substrings whose length &le; max word length in the dictionary.",
        "<strong>Follow-up:</strong> \"Return all ways to segment\" — use memoized recursion and backtracking.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Bloomberg, Uber.",
    ]
})

add_problem("q10", {
    "name": "Linked List Cycle",
    "num": 141,
    "diff": "Easy",
    "topics": ["Linked List", "Two Pointers"],
    "link": "https://leetcode.com/problems/linked-list-cycle",
    "statement": "Given <code>head</code>, the head of a linked list, determine if the linked list has a <strong>cycle</strong> in it. Return <code>true</code> if there is a cycle, otherwise return <code>false</code>.",
    "examples": [
        {"title": "Example 1", "input": "head = [3,2,0,-4], pos = 1", "output": "true", "explain": "Tail connects back to the node at index 1, creating a cycle."},
        {"title": "Example 2", "input": "head = [1,2], pos = 0", "output": "true", "explain": "Tail connects back to head."},
        {"title": "Example 3", "input": "head = [1], pos = -1", "output": "false", "explain": "No cycle."},
    ],
    "constraints": ["0 &le; number of nodes &le; 10<sup>4</sup>", "-10<sup>5</sup> &le; Node.val &le; 10<sup>5</sup>"],
    "approaches": [
        {"name": "Hash Set", "time": "O(n)", "space": "O(n)", "notes": "Store visited nodes; if revisited, cycle exists.", "cls": ""},
        {"name": "Floyd's Tortoise and Hare", "time": "O(n)", "space": "O(1)", "notes": "Fast pointer laps slow pointer inside cycle. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Floyd's Cycle Detection (Tortoise &amp; Hare)",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n)", "space": "O(1)",
        "explanation": "Maintain two pointers: <code>slow</code> moves one step, <code>fast</code> moves two steps. If there's no cycle, fast reaches null. If there's a cycle, fast will eventually lap slow and they'll meet inside the cycle.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null &amp;&amp; fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var hasCycle = function(head) {
    let slow = head, fast = head;
    while (fast && fast.next) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow === fast) return true;
    }
    return false;
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func hasCycle(head *ListNode) bool {
    slow, fast := head, head
    for fast != nil &amp;&amp; fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
        if slow == fast { return true }
    }
    return false
}"""},
    },
    "insight_title": "Why Do They Always Meet?",
    "insight_text": "If a cycle exists of length L, once both pointers enter the cycle, the fast pointer gains 1 step per iteration. It catches up to slow in at most L iterations — they're guaranteed to meet inside the cycle.",
    "tips": [
        "<strong>Know Floyd's by heart:</strong> This is a fundamental algorithm. Be able to write it from memory and explain why it works.",
        "<strong>Guard: fast and fast.next:</strong> Check both to avoid null pointer errors on even-length lists.",
        "<strong>Follow-up:</strong> \"Find the start of the cycle\" — after meeting, reset one pointer to head, advance both one step at a time; they meet at the cycle start (LeetCode #142).",
        "<strong>Companies:</strong> Amazon, Google, Meta, Apple, Bloomberg.",
    ]
})

add_problem("q11", {
    "name": "Missing Number",
    "num": 268,
    "diff": "Easy",
    "topics": ["Array", "Math", "Bit Manipulation"],
    "link": "https://leetcode.com/problems/missing-number",
    "statement": "Given an array <code>nums</code> containing <code>n</code> distinct numbers in the range <code>[0, n]</code>, return the <strong>only number in the range that is missing</strong> from the array.",
    "examples": [
        {"title": "Example 1", "input": "nums = [3,0,1]", "output": "2", "explain": "n=3. Range [0,1,2,3]. Missing is 2."},
        {"title": "Example 2", "input": "nums = [0,1]", "output": "2", "explain": "n=2. Range [0,1,2]. Missing is 2."},
        {"title": "Example 3", "input": "nums = [9,6,4,2,3,5,7,0,1]", "output": "8", "explain": "n=9, missing is 8."},
    ],
    "constraints": ["n == nums.length", "1 &le; n &le; 10<sup>4</sup>", "0 &le; nums[i] &le; n", "All numbers are unique"],
    "approaches": [
        {"name": "Sorting", "time": "O(n log n)", "space": "O(1)", "notes": "Sort and scan for gaps.", "cls": ""},
        {"name": "XOR", "time": "O(n)", "space": "O(1)", "notes": "XOR all indices and all values; missing cancels out. Optimal.", "cls": "optimal-row"},
        {"name": "Gauss Sum", "time": "O(n)", "space": "O(1)", "notes": "expected_sum - actual_sum. Equally optimal, easier to explain.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Gauss Sum Formula",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n)", "space": "O(1)",
        "explanation": "The expected sum of [0..n] is <code>n*(n+1)/2</code>. Subtract the actual sum of the array. The difference is the missing number.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public int missingNumber(int[] nums) {
    int n = nums.length, expected = n * (n + 1) / 2, actual = 0;
    for (int x : nums) actual += x;
    return expected - actual;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var missingNumber = function(nums) {
    const n = nums.length;
    return n*(n+1)/2 - nums.reduce((a,b)=>a+b,0);
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func missingNumber(nums []int) int {
    n := len(nums)
    sum := 0
    for _, v := range nums { sum += v }
    return n*(n+1)/2 - sum
}"""},
    },
    "insight_title": "Gauss vs XOR — Both O(n)",
    "insight_text": "The Gauss formula <code>n*(n+1)/2</code> is O(1) for the expected sum (no iteration needed). XOR approach: <code>result = 0; for i in [0..n]: result ^= i ^ nums[i-1]</code>. Both are correct — Gauss is simpler to explain.",
    "tips": [
        "<strong>Know both approaches:</strong> Gauss sum is most readable; XOR shows bit-manipulation knowledge.",
        "<strong>Overflow concern:</strong> In Java/Go, n*(n+1)/2 can overflow 32-bit int for very large n. Mention using long if needed.",
        "<strong>Companies:</strong> Google, Amazon, Microsoft, Adobe.",
    ]
})

add_problem("q12", {
    "name": "3Sum",
    "num": 15,
    "diff": "Medium",
    "topics": ["Array", "Two Pointers", "Sorting"],
    "link": "https://leetcode.com/problems/3sum",
    "statement": "Given an integer array <code>nums</code>, return all the triplets <code>[nums[i], nums[j], nums[k]]</code> such that <code>i != j</code>, <code>i != k</code>, <code>j != k</code>, and <code>nums[i] + nums[j] + nums[k] == 0</code>. The solution set must <strong>not contain duplicate triplets</strong>.",
    "examples": [
        {"title": "Example 1", "input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explain": "Two distinct triplets that sum to zero."},
        {"title": "Example 2", "input": "nums = [0,1,1]", "output": "[]", "explain": "No triplet sums to zero."},
        {"title": "Example 3", "input": "nums = [0,0,0]", "output": "[[0,0,0]]", "explain": "Only one triplet."},
    ],
    "constraints": ["3 &le; nums.length &le; 3000", "-10<sup>5</sup> &le; nums[i] &le; 10<sup>5</sup>"],
    "approaches": [
        {"name": "Brute Force O(n&sup3;)", "time": "O(n&sup3;)", "space": "O(n)", "notes": "Try all triplets, deduplicate with set.", "cls": ""},
        {"name": "Sort + Two Pointers", "time": "O(n&sup2;)", "space": "O(n)", "notes": "Fix one element, two-pointer scan for the other two. Optimal.", "cls": "optimal-row"},
    ],
    "optimal_approach": {
        "title": "Sort + Two Pointers",
        "badge_cls": "badge-optimal", "badge_text": "Optimal",
        "time": "O(n&sup2;)", "space": "O(n)",
        "explanation": "Sort the array. Fix the first element <code>nums[i]</code>. Use two pointers <code>left=i+1</code>, <code>right=n-1</code> to find pairs summing to <code>-nums[i]</code>. Skip duplicates by advancing past repeated values at each pointer position.",
    },
    "codes": {
        "python": {"id_prefix":"opt","lang":"python","code":"""def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # skip duplicate fixed element
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result"""},
        "java": {"id_prefix":"opt","lang":"java","code":"""public List&lt;List&lt;Integer&gt;&gt; threeSum(int[] nums) {
    Arrays.sort(nums);
    List&lt;List&lt;Integer&gt;&gt; result = new ArrayList&lt;&gt;();
    for (int i = 0; i &lt; nums.length - 2; i++) {
        if (i &gt; 0 &amp;&amp; nums[i] == nums[i-1]) continue;
        int left = i+1, right = nums.length-1;
        while (left &lt; right) {
            int sum = nums[i]+nums[left]+nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i],nums[left],nums[right]));
                while(left&lt;right&amp;&amp;nums[left]==nums[left+1]) left++;
                while(left&lt;right&amp;&amp;nums[right]==nums[right-1]) right--;
                left++; right--;
            } else if (sum &lt; 0) left++;
            else right--;
        }
    }
    return result;
}"""},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":"""var threeSum = function(nums) {
    nums.sort((a,b)=>a-b);
    const result = [];
    for (let i = 0; i < nums.length-2; i++) {
        if (i > 0 && nums[i] === nums[i-1]) continue;
        let [l, r] = [i+1, nums.length-1];
        while (l < r) {
            const sum = nums[i]+nums[l]+nums[r];
            if (sum === 0) {
                result.push([nums[i],nums[l],nums[r]]);
                while(l<r&&nums[l]===nums[l+1])l++;
                while(l<r&&nums[r]===nums[r-1])r--;
                l++; r--;
            } else if (sum < 0) l++;
            else r--;
        }
    }
    return result;
};"""},
        "go": {"id_prefix":"opt","lang":"go","code":"""func threeSum(nums []int) [][]int {
    sort.Ints(nums)
    result := [][]int{}
    for i := 0; i &lt; len(nums)-2; i++ {
        if i &gt; 0 &amp;&amp; nums[i] == nums[i-1] { continue }
        l, r := i+1, len(nums)-1
        for l &lt; r {
            sum := nums[i]+nums[l]+nums[r]
            if sum == 0 {
                result = append(result, []int{nums[i],nums[l],nums[r]})
                for l&lt;r&amp;&amp;nums[l]==nums[l+1] { l++ }
                for l&lt;r&amp;&amp;nums[r]==nums[r-1] { r-- }
                l++; r--
            } else if sum &lt; 0 { l++ } else { r-- }
        }
    }
    return result
}"""},
    },
    "insight_title": "Sorting Enables Duplicate Skipping",
    "insight_text": "By sorting first, all duplicates are adjacent and can be skipped with simple equality checks. The two-pointer scan is O(n) for each fixed element, and there are n elements, giving <strong>O(n&sup2;)</strong> total.",
    "tips": [
        "<strong>Sort first</strong> — this is what enables both the two-pointer technique and easy duplicate skipping.",
        "<strong>Three places to skip duplicates:</strong> the outer i loop, after finding a triplet for left, and after finding a triplet for right.",
        "<strong>Early termination:</strong> If nums[i] > 0, break — no triplet can sum to 0 if the smallest element is already positive.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Uber, Bloomberg — extremely common.",
    ]
})
