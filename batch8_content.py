"""Batch 8: q52-q75 — Final batch"""
from shared_generator import add_problem

def _codes(py, name):
    stub = f"// See Python solution above\n// {name} — translate to this language"
    return {
        "python": {"id_prefix":"opt","lang":"python","code": py},
        "java":   {"id_prefix":"opt","lang":"java","code": stub},
        "javascript": {"id_prefix":"opt","lang":"javascript","code": stub},
        "go":     {"id_prefix":"opt","lang":"go","code": stub},
    }

add_problem("q52", {
    "name": "Counting Bits", "num": 338, "diff": "Easy",
    "topics": ["Bit Manipulation","DP"],
    "link": "https://leetcode.com/problems/counting-bits",
    "statement": "Given an integer <code>n</code>, return an array <code>ans</code> of length <code>n+1</code> where <code>ans[i]</code> is the number of 1's in the binary representation of <code>i</code>.",
    "examples": [{"title":"Example 1","input":"n=2","output":"[0,1,1]","explain":"0=0b0, 1=0b1, 2=0b10."},
                 {"title":"Example 2","input":"n=5","output":"[0,1,1,2,1,2]","explain":"Count of 1 bits for 0..5."}],
    "constraints":["0 &le; n &le; 10<sup>5</sup>"],
    "approaches":[{"name":"DP with bit trick","time":"O(n)","space":"O(n)","notes":"dp[i] = dp[i>>1] + (i&1). Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"DP with Bit Shift","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"<code>dp[i] = dp[i >> 1] + (i & 1)</code>. Right-shifting i drops the LSB; the bit count of i equals the count of i//2 plus 1 if i is odd."},
    "codes": _codes("""def countBits(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp""", "Counting Bits"),
    "insight_title":"Shift and Carry Pattern",
    "insight_text":"Every number i has the same bit count as i//2, plus 1 if the LSB is set. Building dp bottom-up, we can compute all answers in O(n) without any bit-counting operations.",
    "tips":["<strong>Know this pattern:</strong> It's the foundation of many DP-on-bits problems.", "<strong>Companies:</strong> Amazon, Google, Apple."]
})

add_problem("q55", {
    "name": "House Robber II", "num": 213, "diff": "Medium",
    "topics": ["Array","DP"],
    "link": "https://leetcode.com/problems/house-robber-ii",
    "statement": "All houses are arranged in a circle. You cannot rob adjacent houses. Return the maximum amount you can rob. (Same as House Robber but the first and last houses are adjacent.)",
    "examples": [{"title":"Example 1","input":"nums = [2,3,2]","output":"3","explain":"Cannot rob house 1 (2) and house 3 (2), because they are adjacent (circular)."},
                 {"title":"Example 2","input":"nums = [1,2,3,1]","output":"4","explain":"Rob house 1 (1) and house 3 (3). 1+3=4."}],
    "constraints":["1 &le; nums.length &le; 100","0 &le; nums[i] &le; 1000"],
    "approaches":[{"name":"Two runs of House Robber I","time":"O(n)","space":"O(1)","notes":"Run on [0..n-2] and [1..n-1], take max. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Two House Robber I Passes","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"The circular constraint means we can't rob both first and last. Run House Robber I on nums[0..n-2] (exclude last) and on nums[1..n-1] (exclude first). Answer is the maximum of both."},
    "codes": _codes("""def rob(nums):
    def rob_linear(houses):
        prev2 = prev1 = 0
        for n in houses:
            cur = max(prev1, prev2 + n)
            prev2, prev1 = prev1, cur
        return prev1

    n = len(nums)
    if n == 1: return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))""", "House Robber II"),
    "insight_title":"Circular = Two Linear Subproblems",
    "insight_text":"By excluding either the first or last house (two mutually exclusive cases), we reduce the circular problem to two independent linear House Robber I problems.",
    "tips":["<strong>Classic decomposition:</strong> Circular constraint → two linear subproblems.", "<strong>Companies:</strong> Amazon, Google."]
})

add_problem("q56", {
    "name": "Contains Duplicate", "num": 217, "diff": "Easy",
    "topics": ["Array","Hash Map","Sorting"],
    "link": "https://leetcode.com/problems/contains-duplicate",
    "statement": "Given an integer array <code>nums</code>, return <code>true</code> if any value appears at least twice in the array, and <code>false</code> if every element is distinct.",
    "examples": [{"title":"Example 1","input":"nums = [1,2,3,1]","output":"true","explain":"1 appears twice."},
                 {"title":"Example 2","input":"nums = [1,2,3,4]","output":"false","explain":"All distinct."}],
    "constraints":["1 &le; nums.length &le; 10<sup>5</sup>","-10<sup>9</sup> &le; nums[i] &le; 10<sup>9</sup>"],
    "approaches":[
        {"name":"Sorting","time":"O(n log n)","space":"O(1)","notes":"Sort and check adjacent elements.","cls":""},
        {"name":"Hash Set","time":"O(n)","space":"O(n)","notes":"Add to set; if already present, duplicate found. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Hash Set","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Iterate through nums. For each element, check if it's in the set; if yes, return True. Otherwise add it to the set. O(1) average set operations give O(n) total."},
    "codes": _codes("""def containsDuplicate(nums):
    return len(nums) != len(set(nums))""", "Contains Duplicate"),
    "insight_title":"Set Size Tells the Whole Story",
    "insight_text":"If all elements are unique, the set size equals the array length. One-liner: <code>len(nums) != len(set(nums))</code>. In interviews, also show the explicit loop approach to demonstrate understanding.",
    "tips":["<strong>One-liner is fine in Python</strong>, but be ready to write the explicit loop if asked.", "<strong>Companies:</strong> Amazon, Google, Apple — common warm-up."]
})

add_problem("q57", {
    "name": "Decode Ways", "num": 91, "diff": "Medium",
    "topics": ["String","DP"],
    "link": "https://leetcode.com/problems/decode-ways",
    "statement": "A message encoded as a number string can be decoded where 'A'→1, 'B'→2, ..., 'Z'→26. Given a string of digits <code>s</code>, return the number of ways to decode it.",
    "examples": [{"title":"Example 1","input":'s = "12"',"output":"2","explain":'"AB" (1 2) or "L" (12).'},
                 {"title":"Example 2","input":'s = "226"',"output":"3","explain":'"BZ" (2 26), "VF" (22 6), "BBF" (2 2 6).'},
                 {"title":"Example 3","input":'s = "06"',"output":"0","explain":'"06" cannot be decoded (06 is not valid).'}],
    "constraints":["1 &le; s.length &le; 100","s[i] is a digit","s may contain leading zeros"],
    "approaches":[{"name":"DP","time":"O(n)","space":"O(n) or O(1)","notes":"dp[i] = ways to decode s[0..i]. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"1D Dynamic Programming","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"dp[i] = ways to decode first i characters. If s[i-1] != '0', dp[i] += dp[i-1]. If s[i-2:i] forms a valid code (10-26), dp[i] += dp[i-2]. Base case: dp[0]=1, dp[1]=(s[0]!='0')."},
    "codes": _codes("""def numDecodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        one = int(s[i-1])
        two = int(s[i-2:i])
        if one != 0:
            dp[i] += dp[i-1]
        if 10 <= two <= 26:
            dp[i] += dp[i-2]
    return dp[n]""", "Decode Ways"),
    "insight_title":"Leading Zero = 0 Ways",
    "insight_text":"A '0' can only be decoded as part of 10 or 20. If s[i] = '0' and s[i-1] is not '1' or '2', it's an impossible decoding and dp[i] = 0.",
    "tips":["<strong>Edge cases with '0':</strong> s='0' → 0, s='10' → 1, s='30' → 0.", "<strong>Companies:</strong> Amazon, Meta, Google."]
})

add_problem("q58", {
    "name": "Top K Frequent Elements", "num": 347, "diff": "Medium",
    "topics": ["Array","Hash Map","Heap","Bucket Sort"],
    "link": "https://leetcode.com/problems/top-k-frequent-elements",
    "statement": "Given an integer array <code>nums</code> and an integer <code>k</code>, return the <code>k</code> most frequent elements.",
    "examples": [{"title":"Example 1","input":"nums=[1,1,1,2,2,3], k=2","output":"[1,2]","explain":"1 appears 3×, 2 appears 2×."},
                 {"title":"Example 2","input":"nums=[1], k=1","output":"[1]","explain":"Only one element."}],
    "constraints":["1 &le; nums.length &le; 10<sup>5</sup>","k in [1, number of unique elements]"],
    "approaches":[
        {"name":"Sort by frequency","time":"O(n log n)","space":"O(n)","notes":"Count, then sort by count.","cls":""},
        {"name":"Min Heap size k","time":"O(n log k)","space":"O(n)","notes":"Keep a heap of size k.","cls":""},
        {"name":"Bucket Sort","time":"O(n)","space":"O(n)","notes":"Frequency buckets. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Bucket Sort","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Count frequencies. Create buckets where index = frequency (max = n). Place each element in its bucket. Scan buckets from high to low, collecting elements until we have k."},
    "codes": _codes("""from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[freq])
        if len(result) >= k:
            return result[:k]
    return result""", "Top K Frequent Elements"),
    "insight_title":"Frequency as Index Enables O(n)",
    "insight_text":"Since max frequency ≤ n, we can use n+1 buckets. This avoids sorting entirely and gives a true O(n) solution.",
    "tips":["<strong>Mention all three approaches:</strong> Sort O(n log n), Heap O(n log k), Bucket O(n). Justify the choice.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Bloomberg."]
})

add_problem("q60", {
    "name": "Validate Binary Search Tree", "num": 98, "diff": "Medium",
    "topics": ["Tree","DFS","BFS"],
    "link": "https://leetcode.com/problems/validate-binary-search-tree",
    "statement": "Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values < node value, all right subtree values > node value, and both subtrees are also valid BSTs.",
    "examples": [{"title":"Example 1","input":"root=[2,1,3]","output":"true","explain":"1 < 2 < 3, valid BST."},
                 {"title":"Example 2","input":"root=[5,1,4,null,null,3,6]","output":"false","explain":"Root is 5, right child is 4 < 5 — invalid."}],
    "constraints":["1 &le; nodes &le; 10<sup>4</sup>","-2<sup>31</sup> &le; Node.val &le; 2<sup>31</sup>-1"],
    "approaches":[
        {"name":"Inorder traversal check","time":"O(n)","space":"O(n)","notes":"Inorder of BST is sorted. Check sorted.","cls":""},
        {"name":"DFS with bounds","time":"O(n)","space":"O(n)","notes":"Pass min/max bounds down the tree. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"DFS with Min/Max Bounds","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Recursively validate each node with valid range [min, max]. Left subtree: [min, node.val]. Right subtree: [node.val, max]. Start with (root, -∞, +∞)."},
    "codes": _codes("""def isValidBST(root):
    def validate(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return validate(node.left, lo, node.val) and validate(node.right, node.val, hi)
    return validate(root, float('-inf'), float('inf'))""", "Validate BST"),
    "insight_title":"Subtree Bounds Propagate Globally",
    "insight_text":"The naive check (left.val < root.val < right.val) fails for deeply nested violations. Passing bounds down ensures every node respects the global BST property from all its ancestors.",
    "tips":["<strong>Common mistake:</strong> Only checking immediate children. Must propagate global bounds.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft."]
})

add_problem("q61", {
    "name": "Invert Binary Tree", "num": 226, "diff": "Easy",
    "topics": ["Tree","DFS","BFS"],
    "link": "https://leetcode.com/problems/invert-binary-tree",
    "statement": "Given the root of a binary tree, invert the tree (mirror it), and return its root.",
    "examples": [{"title":"Example 1","input":"root=[4,2,7,1,3,6,9]","output":"[4,7,2,9,6,3,1]","explain":"Tree mirrored about the root."}],
    "constraints":["0 &le; nodes &le; 100","-100 &le; Node.val &le; 100"],
    "approaches":[{"name":"DFS Recursive","time":"O(n)","space":"O(n)","notes":"Swap children, recurse. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Recursive DFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"For each node, swap its left and right children, then recursively invert both subtrees."},
    "codes": _codes("""def invertTree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left
    invertTree(root.left)
    invertTree(root.right)
    return root""", "Invert Binary Tree"),
    "insight_title":"Post-Order vs Pre-Order Both Work",
    "insight_text":"The swap can happen before OR after recursing into children — both yield the same result since we're operating on the entire subtree.",
    "tips":["<strong>Legendary problem:</strong> Famously tweeted about by Max Howell (Homebrew creator). Shows recursion fundamentals.",
            "<strong>Companies:</strong> Google, Amazon, Apple."]
})

add_problem("q62", {
    "name": "Same Tree", "num": 100, "diff": "Easy",
    "topics": ["Tree","DFS","BFS"],
    "link": "https://leetcode.com/problems/same-tree",
    "statement": "Given the roots of two binary trees <code>p</code> and <code>q</code>, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
    "examples": [{"title":"Example 1","input":"p=[1,2,3], q=[1,2,3]","output":"true","explain":"Identical structure and values."},
                 {"title":"Example 2","input":"p=[1,2], q=[1,null,2]","output":"false","explain":"Different structures."}],
    "constraints":["0 &le; nodes &le; 100","-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup>"],
    "approaches":[{"name":"DFS Recursive","time":"O(n)","space":"O(n)","notes":"Compare node by node, recurse both trees in sync. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Recursive DFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Base case: both null→true, one null→false. Recursive: values must match AND left subtrees same AND right subtrees same."},
    "codes": _codes("""def isSameTree(p, q):
    if not p and not q: return True
    if not p or not q: return False
    return p.val == q.val and isSameTree(p.left, q.left) and isSameTree(p.right, q.right)""", "Same Tree"),
    "insight_title":"Four Cases, One Function",
    "insight_text":"Null-null, null-nonNull, nonNull-null, nonNull-nonNull — the recursive structure handles all four cases cleanly with just three lines.",
    "tips":["<strong>Build block:</strong> This is the inner function in 'Subtree of Another Tree'.", "<strong>Companies:</strong> Amazon, Google."]
})

add_problem("q63", {
    "name": "Longest Common Subsequence", "num": 1143, "diff": "Medium",
    "topics": ["String","DP"],
    "link": "https://leetcode.com/problems/longest-common-subsequence",
    "statement": "Given two strings <code>text1</code> and <code>text2</code>, return the length of their longest common subsequence. A subsequence doesn't need to be contiguous.",
    "examples": [{"title":"Example 1","input":'text1="abcde", text2="ace"',"output":"3","explain":"LCS is 'ace'."},
                 {"title":"Example 2","input":'text1="abc", text2="abc"',"output":"3","explain":"Entire string."},
                 {"title":"Example 3","input":'text1="abc", text2="def"',"output":"0","explain":"No common subsequence."}],
    "constraints":["1 &le; text1.length, text2.length &le; 1000","Only lowercase letters"],
    "approaches":[{"name":"2D DP","time":"O(mn)","space":"O(mn) or O(n)","notes":"dp[i][j]=LCS of text1[:i] and text2[:j]. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"2D Dynamic Programming","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(mn)",
        "explanation":"dp[i][j] = LCS length for text1[:i] and text2[:j]. If text1[i-1]==text2[j-1]: dp[i][j] = dp[i-1][j-1]+1. Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])."},
    "codes": _codes("""def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]""", "Longest Common Subsequence"),
    "insight_title":"Match = Diagonal; No Match = Best of Left or Above",
    "insight_text":"dp[i][j] transitions make intuitive sense on the 2D table: a character match extends the diagonal (previous of both); no match means we skip one character and take the best of the two options.",
    "tips":["<strong>Space optimization:</strong> O(n) with rolling row since dp[i] only depends on dp[i-1].",
            "<strong>Foundation problem:</strong> Diff tools, DNA alignment, and edit distance all build on LCS.",
            "<strong>Companies:</strong> Google, Amazon, Meta."]
})

add_problem("q64", {
    "name": "Binary Tree Level Order Traversal", "num": 102, "diff": "Medium",
    "topics": ["Tree","BFS"],
    "link": "https://leetcode.com/problems/binary-tree-level-order-traversal",
    "statement": "Given the root of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
    "examples": [{"title":"Example 1","input":"root=[3,9,20,null,null,15,7]","output":"[[3],[9,20],[15,7]]","explain":"Level-by-level output."}],
    "constraints":["0 &le; nodes &le; 2000","-1000 &le; Node.val &le; 1000"],
    "approaches":[{"name":"BFS with queue","time":"O(n)","space":"O(n)","notes":"Process level by level using a deque. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"BFS Level-by-Level","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Use a queue. At each iteration, process all nodes at the current level (size = queue length at start of iteration), collect their values, and enqueue their children."},
    "codes": _codes("""from collections import deque

def levelOrder(root):
    if not root: return []
    result = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result""", "Binary Tree Level Order Traversal"),
    "insight_title":"Snapshot Queue Length Before Inner Loop",
    "insight_text":"Taking <code>len(q)</code> BEFORE the inner loop captures exactly how many nodes are at the current level, since new children are added to the back of the queue during the loop.",
    "tips":["<strong>Captures:</strong> Queue size at the START of each level = number of nodes at that level.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Bloomberg."]
})

add_problem("q65", {
    "name": "Kth Smallest Element in a BST", "num": 230, "diff": "Medium",
    "topics": ["Tree","DFS","Binary Search"],
    "link": "https://leetcode.com/problems/kth-smallest-element-in-a-bst",
    "statement": "Given the root of a BST and an integer k, return the k-th smallest value (1-indexed) of all node values in the tree.",
    "examples": [{"title":"Example 1","input":"root=[3,1,4,null,2], k=1","output":"1","explain":"In-order: [1,2,3,4]. 1st smallest = 1."},
                 {"title":"Example 2","input":"root=[5,3,6,2,4,null,null,1], k=3","output":"3","explain":"In-order: [1,2,3,4,5,6]. 3rd = 3."}],
    "constraints":["1 &le; nodes &le; 10<sup>4</sup>","0 &le; Node.val &le; 10<sup>4</sup>","k in [1, nodes]"],
    "approaches":[{"name":"Iterative In-Order Traversal","time":"O(H+k)","space":"O(H)","notes":"H=height. Early stop at k-th element. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Iterative In-Order","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(H+k)","space":"O(H)",
        "explanation":"In-order traversal of a BST gives elements in sorted order. Use iterative DFS (stack) and stop after visiting k nodes."},
    "codes": _codes("""def kthSmallest(root, k):
    stack = []
    curr = root
    count = 0
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right""", "Kth Smallest in BST"),
    "insight_title":"BST In-Order = Sorted Ascending",
    "insight_text":"The defining property of a BST: in-order traversal visits nodes in non-decreasing order. The k-th visited node is the answer.",
    "tips":["<strong>Early termination:</strong> Stop as soon as we've visited k nodes — O(H+k) instead of O(n).",
            "<strong>Companies:</strong> Amazon, Meta, Microsoft."]
})

add_problem("q66", {
    "name": "Maximum Depth of Binary Tree", "num": 104, "diff": "Easy",
    "topics": ["Tree","DFS","BFS"],
    "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree",
    "statement": "Given the root of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).",
    "examples": [{"title":"Example 1","input":"root=[3,9,20,null,null,15,7]","output":"3","explain":"Depth is 3."},
                 {"title":"Example 2","input":"root=[1,null,2]","output":"2","explain":"Depth is 2."}],
    "constraints":["0 &le; nodes &le; 10<sup>4</sup>","-100 &le; Node.val &le; 100"],
    "approaches":[{"name":"DFS Recursive","time":"O(n)","space":"O(n)","notes":"max(left, right) + 1. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Recursive DFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Base case: null → 0. Recursive: 1 + max(depth(left), depth(right))."},
    "codes": _codes("""def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))""", "Maximum Depth of Binary Tree"),
    "insight_title":"The Classic DFS Template for Trees",
    "insight_text":"This is the foundational template: base_case + 1 + recursive calls on children. Many tree problems are variations of this structure.",
    "tips":["<strong>Know by heart:</strong> Every FAANG candidate should be able to write this instantly.",
            "<strong>Companies:</strong> Amazon, Google, Apple — ubiquitous warm-up."]
})

add_problem("q68", {
    "name": "Lowest Common Ancestor of a BST", "num": 235, "diff": "Medium",
    "topics": ["Tree","DFS","BST"],
    "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-bst",
    "statement": "Given a BST, find the lowest common ancestor (LCA) of two given nodes p and q. The LCA is the deepest node that has both p and q as descendants.",
    "examples": [{"title":"Example 1","input":"root=[6,2,8,0,4,7,9,null,null,3,5], p=2, q=8","output":"6","explain":"LCA of 2 and 8 is root 6."},
                 {"title":"Example 2","input":"root=[6,2,8,0,4,7,9,null,null,3,5], p=2, q=4","output":"2","explain":"LCA of 2 and 4 is 2 since 2 is ancestor of 4."}],
    "constraints":["2 &le; nodes &le; 10<sup>5</sup>","-10<sup>9</sup> &le; Node.val &le; 10<sup>9</sup>","All values unique","p and q exist in the BST"],
    "approaches":[{"name":"BST Property Navigation","time":"O(H)","space":"O(1)","notes":"Use BST ordering to navigate to LCA. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"BST Property","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(H)","space":"O(1)",
        "explanation":"If both p and q are less than the current node, LCA is in the left subtree. If both are greater, go right. Otherwise the current node is the LCA (the paths to p and q diverge here)."},
    "codes": _codes("""def lowestCommonAncestor(root, p, q):
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr""", "LCA of BST"),
    "insight_title":"BST Ordering Eliminates One Side Every Step",
    "insight_text":"Unlike general binary tree LCA (which requires O(n)), BST's ordering property lets us navigate to the LCA in O(H) — O(log n) for balanced, O(n) worst case skewed.",
    "tips":["<strong>Contrast with general BT LCA:</strong> This problem is O(H) thanks to BST property; general BT is O(n).",
            "<strong>Companies:</strong> Amazon, Google, Microsoft, Meta."]
})

add_problem("q69", {
    "name": "Product of Array Except Self", "num": 238, "diff": "Medium",
    "topics": ["Array","Prefix Product"],
    "link": "https://leetcode.com/problems/product-of-array-except-self",
    "statement": "Given an integer array <code>nums</code>, return an array <code>answer</code> where <code>answer[i]</code> is the product of all elements of <code>nums</code> except <code>nums[i]</code>. Must run in O(n) time <strong>without division</strong>.",
    "examples": [{"title":"Example 1","input":"nums=[1,2,3,4]","output":"[24,12,8,6]","explain":"Each element is product of all others."},
                 {"title":"Example 2","input":"nums=[-1,1,0,-3,3]","output":"[0,0,9,0,0]","explain":"Zero element makes most products 0."}],
    "constraints":["2 &le; nums.length &le; 10<sup>5</sup>","-30 &le; nums[i] &le; 30","Product guaranteed to fit in 32-bit integer"],
    "approaches":[
        {"name":"Division","time":"O(n)","space":"O(1)","notes":"Total product / nums[i]. Not allowed (and fails on zeros).","cls":""},
        {"name":"Prefix + Suffix pass","time":"O(n)","space":"O(1)","notes":"Left product pass then right product pass. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Prefix × Suffix","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"answer[i] = product of all elements to the left × product of all elements to the right. Do two passes: first compute left prefix products into answer array, then multiply in right suffix products using a running value."},
    "codes": _codes("""def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n
    # Left prefix
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    # Right suffix
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer""", "Product of Array Except Self"),
    "insight_title":"Two O(n) Passes Instead of O(n²)",
    "insight_text":"answer[i] = left_product[i] × right_product[i]. By computing left prefix in a forward pass and right suffix in a backward pass — using the answer array itself — we achieve O(1) extra space.",
    "tips":["<strong>Classic interview problem:</strong> The 'no division' constraint forces the elegant two-pass solution.",
            "<strong>Zero handling:</strong> This approach handles zeros correctly; division-based doesn't.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Apple."]
})

add_problem("q70", {
    "name": "Valid Anagram", "num": 242, "diff": "Easy",
    "topics": ["String","Hash Map","Sorting"],
    "link": "https://leetcode.com/problems/valid-anagram",
    "statement": "Given two strings <code>s</code> and <code>t</code>, return <code>true</code> if <code>t</code> is an anagram of <code>s</code>, and <code>false</code> otherwise.",
    "examples": [{"title":"Example 1","input":'s="anagram", t="nagaram"',"output":"true","explain":"Same characters, different order."},
                 {"title":"Example 2","input":'s="rat", t="car"',"output":"false","explain":"Different characters."}],
    "constraints":["1 &le; s.length, t.length &le; 5*10<sup>4</sup>","s,t consist of lowercase letters"],
    "approaches":[
        {"name":"Sort both strings","time":"O(n log n)","space":"O(n)","notes":"Sort and compare.","cls":""},
        {"name":"Character count array","time":"O(n)","space":"O(1)","notes":"Count frequency difference in 26-char array. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Character Frequency Count","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Increment counts for s, decrement for t. If all counts are 0 at the end, t is an anagram."},
    "codes": _codes("""def isAnagram(s, t):
    if len(s) != len(t): return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - ord('a')] += 1
        count[ord(b) - ord('a')] -= 1
    return all(c == 0 for c in count)""", "Valid Anagram"),
    "insight_title":"One 26-Element Array = O(1) Space",
    "insight_text":"Since we're only dealing with 26 lowercase letters, the 'hash map' is just an array of size 26 — constant space regardless of string length.",
    "tips":["<strong>Counter shortcut in Python:</strong> <code>Counter(s) == Counter(t)</code>.",
            "<strong>Companies:</strong> Amazon, Google, Apple — common warm-up."]
})

add_problem("q71", {
    "name": "Sum of Two Integers", "num": 371, "diff": "Medium",
    "topics": ["Bit Manipulation","Math"],
    "link": "https://leetcode.com/problems/sum-of-two-integers",
    "statement": "Given two integers <code>a</code> and <code>b</code>, return the sum of the two integers without using <code>+</code> or <code>-</code> operators.",
    "examples": [{"title":"Example 1","input":"a=1, b=2","output":"3","explain":"1+2=3 using only bit ops."},
                 {"title":"Example 2","input":"a=2, b=3","output":"5","explain":"2+3=5 using only bit ops."}],
    "constraints":["-1000 &le; a, b &le; 1000"],
    "approaches":[{"name":"XOR + AND carry","time":"O(1)","space":"O(1)","notes":"XOR gives sum without carry; AND gives carry bits. Repeat. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"XOR + AND Carry Simulation","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(1)","space":"O(1)",
        "explanation":"<code>a XOR b</code> gives the sum without carry. <code>(a AND b) &lt;&lt; 1</code> gives the carry. Repeat until carry is 0."},
    "codes": _codes("""def getSum(a, b):
    MASK = 0xFFFFFFFF
    MAX = 0x7FFFFFFF
    while b & MASK:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a if a <= MAX else ~(a ^ MASK)""", "Sum of Two Integers"),
    "insight_title":"XOR = Add Without Carry; AND<<1 = Carry",
    "insight_text":"This mirrors hardware adder logic: XOR computes the partial sum; AND + shift computes carry. Iterating until carry is 0 produces the full sum.",
    "tips":["<strong>Mask for Python:</strong> Python integers are arbitrary precision; mask to 32 bits to simulate integer overflow.",
            "<strong>Companies:</strong> Amazon, Apple, LeetCode standard."]
})

add_problem("q72", {
    "name": "Meeting Rooms", "num": 252, "diff": "Easy",
    "topics": ["Array","Sorting"],
    "link": "https://leetcode.com/problems/meeting-rooms",
    "statement": "Given an array of meeting time intervals <code>[[start1,end1],[start2,end2],...]</code>, determine if a person can attend all meetings (i.e., no two meetings overlap).",
    "examples": [{"title":"Example 1","input":"intervals = [[0,30],[5,10],[15,20]]","output":"false","explain":"[0,30] overlaps both [5,10] and [15,20]."},
                 {"title":"Example 2","input":"intervals = [[7,10],[2,4]]","output":"true","explain":"No overlap."}],
    "constraints":["0 &le; intervals.length &le; 5*10<sup>4</sup>"],
    "approaches":[{"name":"Sort by start, check overlap","time":"O(n log n)","space":"O(1)","notes":"Sort, then verify no adjacent meetings overlap. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Sort + Adjacent Check","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n log n)","space":"O(1)",
        "explanation":"Sort intervals by start time. Two meetings overlap if the end of one is greater than the start of the next."},
    "codes": _codes("""def canAttendMeetings(intervals):
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True""", "Meeting Rooms"),
    "insight_title":"Sort Puts Conflicts Adjacent",
    "insight_text":"After sorting by start time, any overlap must occur between consecutive meetings. A single linear scan suffices after sorting.",
    "tips":["<strong>Overlap condition:</strong> next.start &lt; prev.end (strictly less than, since [0,30] and [30,45] don't overlap).",
            "<strong>Companies:</strong> Google, Facebook, Amazon."]
})

add_problem("q73", {
    "name": "Best Time to Buy and Sell Stock", "num": 121, "diff": "Easy",
    "topics": ["Array","DP","Sliding Window"],
    "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock",
    "statement": "Given an array <code>prices</code> where <code>prices[i]</code> is the price on day i, maximize profit by choosing a single day to buy and a later single day to sell. Return the maximum profit, or 0 if no profit is possible.",
    "examples": [{"title":"Example 1","input":"prices=[7,1,5,3,6,4]","output":"5","explain":"Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6-1=5."},
                 {"title":"Example 2","input":"prices=[7,6,4,3,1]","output":"0","explain":"No profitable transaction."}],
    "constraints":["1 &le; prices.length &le; 10<sup>5</sup>","0 &le; prices[i] &le; 10<sup>4</sup>"],
    "approaches":[{"name":"Single Pass — Track Min","time":"O(n)","space":"O(1)","notes":"Track min price seen so far; update max profit. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Single Pass — Min Price","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Scan left to right. Maintain the minimum price seen so far. At each day, the potential profit is <code>price[i] - min_price</code>. Update max profit."},
    "codes": _codes("""def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit""", "Best Time to Buy Sell Stock"),
    "insight_title":"Track Minimum to Maximize Profit at Each Step",
    "insight_text":"At any day, the best profit is current_price - min_price_so_far. We only need to track one running minimum, giving O(1) space.",
    "tips":["<strong>Most common Easy problem in interviews:</strong> Know both the greedy approach and how to extend to unlimited transactions (Kadane's variant).",
            "<strong>Companies:</strong> Amazon, Google, Apple, Meta, Microsoft — top 3 most frequently asked Easy."]
})

add_problem("q74", {
    "name": "Binary Tree Maximum Path Sum", "num": 124, "diff": "Hard",
    "topics": ["Tree","DFS","DP"],
    "link": "https://leetcode.com/problems/binary-tree-maximum-path-sum",
    "statement": "Given the root of a binary tree, return the maximum path sum. A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge. The path must contain at least one node and does not need to pass through the root.",
    "examples": [{"title":"Example 1","input":"root=[1,2,3]","output":"6","explain":"Optimal path: 2+1+3=6."},
                 {"title":"Example 2","input":"root=[-10,9,20,null,null,15,7]","output":"42","explain":"Optimal path: 15+20+7=42."}],
    "constraints":["-1000 &le; Node.val &le; 1000","1 &le; nodes &le; 3*10<sup>4</sup>"],
    "approaches":[{"name":"DFS with post-order","time":"O(n)","space":"O(n)","notes":"At each node, compute the max gain going down, update global max. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"DFS Post-Order with Global Max","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"For each node, compute the max one-sided gain from left and right children (use 0 if negative). The path through this node = node.val + left_gain + right_gain. Update global max. Return to parent: node.val + max(left_gain, right_gain) — only one side can extend to the parent."},
    "codes": _codes("""def maxPathSum(root):
    global_max = float('-inf')

    def dfs(node):
        nonlocal global_max
        if not node:
            return 0
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        # Path through current node
        global_max = max(global_max, node.val + left + right)
        # Return max one-sided gain to parent
        return node.val + max(left, right)

    dfs(root)
    return global_max""", "Binary Tree Max Path Sum"),
    "insight_title":"Return vs Update Are Different",
    "insight_text":"The key distinction: the global max can use BOTH children (path through the node), but what we RETURN to the parent can only use ONE child (a path must be linear, not forking).",
    "tips":["<strong>Negative subtrees:</strong> Clamping child gain to 0 means we ignore subtrees that would decrease the path sum.",
            "<strong>Critical distinction:</strong> Return only one branch (to parent); update global with both branches.",
            "<strong>Companies:</strong> Google, Facebook, Amazon — common Hard tree problem."]
})

add_problem("q75", {
    "name": "Valid Palindrome", "num": 125, "diff": "Easy",
    "topics": ["String","Two Pointers"],
    "link": "https://leetcode.com/problems/valid-palindrome",
    "statement": "A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string <code>s</code>, return <code>true</code> if it is a palindrome, or <code>false</code> otherwise.",
    "examples": [{"title":"Example 1","input":'s = "A man, a plan, a canal: Panama"',"output":"true","explain":'"amanaplanacanalpanama" is a palindrome.'},
                 {"title":"Example 2","input":'s = "race a car"',"output":"false","explain":'"raceacar" is not a palindrome.'},
                 {"title":"Example 3","input":'s = " "',"output":"true","explain":"Empty after filtering; empty string is a palindrome."}],
    "constraints":["1 &le; s.length &le; 2*10<sup>5</sup>","s consists only of printable ASCII characters"],
    "approaches":[
        {"name":"Clean + Reverse","time":"O(n)","space":"O(n)","notes":"Filter and compare to reverse.","cls":""},
        {"name":"Two Pointers","time":"O(n)","space":"O(1)","notes":"Skip non-alphanumeric, compare from both ends. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Two Pointers","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Use left and right pointers. Skip non-alphanumeric characters. Compare lowercase versions of remaining chars. If any mismatch, return false."},
    "codes": _codes("""def isPalindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True""", "Valid Palindrome"),
    "insight_title":"Two Pointers + Skip Non-Alphanumeric = O(1) Space",
    "insight_text":"Instead of creating a cleaned string (O(n) space), we skip non-alphanumeric chars in-place with the two pointers. Each character is checked at most once.",
    "tips":["<strong>isalnum() method</strong> handles both letters and digits in one check.",
            "<strong>Companies:</strong> Amazon, Facebook, Google, Apple — extremely common Easy."]
})
