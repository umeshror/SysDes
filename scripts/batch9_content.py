"""Batch 9: Missing problems q1-q5, q33, q42, q46, q49, q53, q54, q59, q67"""
from shared_generator import add_problem

def _codes(py, name):
    stub = f"// See Python solution above — translate to this language\n// {name}"
    return {
        "python": {"id_prefix":"opt","lang":"python","code": py},
        "java":   {"id_prefix":"opt","lang":"java","code": stub},
        "javascript": {"id_prefix":"opt","lang":"javascript","code": stub},
        "go":     {"id_prefix":"opt","lang":"go","code": stub},
    }

add_problem("q1", {
    "name": "Longest Consecutive Sequence", "num": 128, "diff": "Medium",
    "topics": ["Array", "Hash Set", "Union Find"],
    "link": "https://leetcode.com/problems/longest-consecutive-sequence",
    "statement": "Given an unsorted array of integers <code>nums</code>, return the length of the <strong>longest consecutive elements sequence</strong>. You must write an algorithm that runs in <strong>O(n)</strong> time.",
    "examples": [
        {"title":"Example 1","input":"nums = [100,4,200,1,3,2]","output":"4","explain":"The longest consecutive sequence is [1,2,3,4]. Length = 4."},
        {"title":"Example 2","input":"nums = [0,3,7,2,5,8,4,6,0,1]","output":"9","explain":"Sequence [0,1,2,...,8] has length 9."},
        {"title":"Example 3 (Edge Case)","input":"nums = []","output":"0","explain":"Empty array → return 0."},
    ],
    "constraints":["0 &le; nums.length &le; 10<sup>5</sup>","-10<sup>9</sup> &le; nums[i] &le; 10<sup>9</sup>","Must run in O(n) time"],
    "approaches":[
        {"name":"Sorting","time":"O(n log n)","space":"O(1)","notes":"Sort and scan. Too slow — violates O(n) requirement.","cls":""},
        {"name":"Hash Set — Start Detection","time":"O(n)","space":"O(n)","notes":"Only start counting from sequence beginnings. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Hash Set — Sequence Start Detection","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Add all numbers to a set. For each number, only start counting if <code>num-1</code> is NOT in the set (this is a sequence start). Count up while consecutive numbers exist. O(n) because each number is visited at most twice."},
    "codes": _codes("""def longestConsecutive(nums):
    num_set = set(nums)
    best = 0
    for n in num_set:
        if n - 1 not in num_set:  # sequence start
            length = 1
            while n + length in num_set:
                length += 1
            best = max(best, length)
    return best""", "Longest Consecutive Sequence"),
    "insight_title":"Only Count from Sequence Starts",
    "insight_text":"The key insight: only begin counting when n-1 is NOT in the set. This ensures each sequence is counted exactly once from its start, giving total O(n) across all iterations.",
    "tips":[
        "<strong>Common mistake:</strong> Starting a count from every element gives O(n²) worst case.",
        "<strong>The guard:</strong> <code>if n-1 not in num_set</code> is the critical check.",
        "<strong>Companies:</strong> Google, Amazon, Meta, Airbnb. Blind 75 #1.",
    ]
})

add_problem("q2", {
    "name": "Two Sum", "num": 1, "diff": "Easy",
    "topics": ["Array", "Hash Map"],
    "link": "https://leetcode.com/problems/two-sum",
    "statement": "Given an array of integers <code>nums</code> and an integer <code>target</code>, return <em>indices</em> of the two numbers such that they add up to <code>target</code>. You may assume each input has exactly one solution, and you may not use the same element twice.",
    "examples": [
        {"title":"Example 1","input":"nums = [2,7,11,15], target = 9","output":"[0,1]","explain":"nums[0] + nums[1] = 2 + 7 = 9."},
        {"title":"Example 2","input":"nums = [3,2,4], target = 6","output":"[1,2]","explain":"nums[1] + nums[2] = 2 + 4 = 6."},
        {"title":"Example 3 (Edge)","input":"nums = [3,3], target = 6","output":"[0,1]","explain":"Both 3s at different indices."},
    ],
    "constraints":["2 &le; nums.length &le; 10<sup>4</sup>","-10<sup>9</sup> &le; nums[i] &le; 10<sup>9</sup>","Exactly one valid answer","You may not use the same element twice"],
    "approaches":[
        {"name":"Brute Force","time":"O(n²)","space":"O(1)","notes":"Check every pair. Too slow.","cls":""},
        {"name":"Hash Map (One-Pass)","time":"O(n)","space":"O(n)","notes":"Store complement in map while iterating. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Hash Map — One Pass","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Iterate through the array. For each element, compute its complement (target - num). If the complement is already in the hash map, return the two indices. Otherwise store num:index in the map."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int[] twoSum(int[] nums, int target) {
    Map&lt;Integer,Integer&gt; seen = new HashMap&lt;&gt;();
    for (int i = 0; i &lt; nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement))
            return new int[]{seen.get(complement), i};
        seen.put(nums[i], i);
    }
    return new int[]{};
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var twoSum = function(nums, target) {
    const seen = {};
    for (let i = 0; i &lt; nums.length; i++) {
        const comp = target - nums[i];
        if (comp in seen) return [seen[comp], i];
        seen[nums[i]] = i;
    }
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func twoSum(nums []int, target int) []int {
    seen := map[int]int{}
    for i, n := range nums {
        if j, ok := seen[target-n]; ok { return []int{j, i} }
        seen[n] = i
    }
    return nil
}"""},
    },
    "flow_matrix": {
        "headers": ["Step", "i", "num", "Complement", "In Map?", "Hash Map State", "Action"],
        "rows": [
            ["1", "0", "2", "<code>9 - 2 = 7</code>", "No", "<code>{2: 0}</code>", "Store <code>num: i</code>"],
            ["2", "1", "7", "<code>9 - 7 = 2</code>", "Yes", "<code>{2: 0}</code>", "Return <code>[map[2], 1] &rarr; [0, 1]</code>"]
        ]
    },
    "insight_title":"Why One-Pass Works",
    "insight_text":"At each index i, we ask: 'Have I already seen the number that would complete a pair with nums[i]?' If yes, return immediately. If no, record nums[i] for future lookups. Hash map operations are O(1) average → O(n) total.",
    "tips":[
        "<strong>Don't jump to two pointers:</strong> Two pointers only work on sorted arrays. For unsorted, use hash map.",
        "<strong>State the trade-off:</strong> O(n²) time vs O(n) space is the classic time-space trade-off.",
        "<strong>Companies:</strong> LeetCode #1 — asked at virtually every company.",
    ]
})

add_problem("q3", {
    "name": "Longest Substring Without Repeating Characters", "num": 3, "diff": "Medium",
    "topics": ["String", "Sliding Window", "Hash Map"],
    "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters",
    "statement": "Given a string <code>s</code>, find the length of the <strong>longest substring without repeating characters</strong>.",
    "examples": [
        {"title":"Example 1","input":'s = "abcabcbb"',"output":"3","explain":'"abc" is the longest substring, length 3.'},
        {"title":"Example 2","input":'s = "bbbbb"',"output":"1","explain":"Longest is 'b' with length 1."},
        {"title":"Example 3","input":'s = "pwwkew"',"output":"3","explain":'"wke" has length 3. Note: answer is a substring not subsequence.'},
    ],
    "constraints":["0 &le; s.length &le; 5*10<sup>4</sup>","s consists of English letters, digits, symbols, spaces"],
    "approaches":[
        {"name":"Brute Force","time":"O(n&sup2;)","space":"O(min(m,n))","notes":"Check every substring.","cls":""},
        {"name":"Sliding Window + Set","time":"O(n)","space":"O(min(m,n))","notes":"Expand right, shrink left on duplicate. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Sliding Window","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(min(m,n))",
        "explanation":"Maintain a window [left, right] with a set of characters. Expand right, adding each character. When a duplicate is found, shrink from the left until the duplicate is removed. Track max window size."},
    "codes": _codes("""def lengthOfLongestSubstring(s):
    char_set = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len""", "Longest Substring Without Repeating"),
    "flow_matrix": {
        "headers": ["Iteration (right)", "Current Char", "Set State", "Left Pointer", "Action & Max Len"],
        "rows": [
            ["0", "'a'", "<code>{'a'}</code>", "0", "max(0, 1) = 1"],
            ["1", "'b'", "<code>{'a', 'b'}</code>", "0", "max(1, 2) = 2"],
            ["2", "'c'", "<code>{'a', 'b', 'c'}</code>", "0", "max(2, 3) = 3"],
            ["3", "'a'", "Duplicate! Remove <code>'a'</code>", "1", "max(3, 3) = 3"]
        ]
    },
    "insight_title":"Shrink Only When Necessary",
    "insight_text":"The window shrinks from the left only when a duplicate is found. Each character is added and removed at most once → O(n) total.",
    "tips":["<strong>Optimization:</strong> Use a map of char→last_index to jump left pointer directly instead of shrinking one by one.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Bloomberg."]
})

add_problem("q4", {
    "name": "Longest Palindromic Substring", "num": 5, "diff": "Medium",
    "topics": ["String", "Dynamic Programming"],
    "link": "https://leetcode.com/problems/longest-palindromic-substring",
    "statement": "Given a string <code>s</code>, return the <strong>longest palindromic substring</strong> in <code>s</code>.",
    "examples": [
        {"title":"Example 1","input":'s = "babad"',"output":'"bab" or "aba"',"explain":"Both 'bab' and 'aba' are valid answers."},
        {"title":"Example 2","input":'s = "cbbd"',"output":'"bb"',"explain":'"bb" is the longest palindromic substring.'},
    ],
    "constraints":["1 &le; s.length &le; 1000","s consists of only lowercase English letters"],
    "approaches":[
        {"name":"Brute Force","time":"O(n&sup3;)","space":"O(1)","notes":"Check every substring.","cls":""},
        {"name":"Expand Around Center","time":"O(n&sup2;)","space":"O(1)","notes":"Expand from each of 2n-1 centers. Optimal.","cls":"optimal-row"},
        {"name":"Manacher's Algorithm","time":"O(n)","space":"O(n)","notes":"Advanced; rarely needed in interviews.","cls":""},
    ],
    "optimal_approach":{"title":"Expand Around Center","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n&sup2;)","space":"O(1)",
        "explanation":"For each of the 2n-1 centers (each character and each gap between characters), expand outward while characters match, tracking the longest palindrome found."},
    "codes": _codes("""def longestPalindrome(s):
    res = ""
    for i in range(len(s)):
        # Odd length
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > len(res):
                res = s[l:r+1]
            l -= 1; r += 1
        # Even length
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if r - l + 1 > len(res):
                res = s[l:r+1]
            l -= 1; r += 1
    return res""", "Longest Palindromic Substring"),
    "insight_title":"2n-1 Centers Cover All Palindromes",
    "insight_text":"Every palindrome has a center: a single character (odd-length) or a gap between two characters (even-length). Checking all 2n-1 centers guarantees we find the longest.",
    "tips":["<strong>Don't forget even-length palindromes!</strong> Expand from (i, i+1) gaps.",
            "<strong>Companies:</strong> Amazon, Microsoft, Google."]
})

add_problem("q5", {
    "name": "Clone Graph", "num": 133, "diff": "Medium",
    "topics": ["Graph", "DFS", "BFS", "Hash Map"],
    "link": "https://leetcode.com/problems/clone-graph",
    "statement": """Given a reference to a node in a <strong>connected undirected graph</strong>, return a deep copy (clone) of the graph. Each node in the graph contains a value and a list of its neighbors.<br><br><strong>Graph Visualization:</strong><br><div class="mermaid">
graph LR
    1 --- 2
    2 --- 3
    3 --- 4
    4 --- 1
</div>""",
    "examples": [
        {"title":"Example 1","input":"adjList = [[2,4],[1,3],[2,4],[1,3]]","output":"[[2,4],[1,3],[2,4],[1,3]]","explain":"4-node graph correctly deep-cloned."},
        {"title":"Example 2","input":"adjList = [[]]","output":"[[]]","explain":"Single node with no neighbors."},
    ],
    "constraints":["0 &le; nodes &le; 100","1 &le; Node.val &le; 100","No repeated edges or self-loops","Connected graph"],
    "approaches":[
        {"name":"DFS + HashMap","time":"O(V+E)","space":"O(V+E)","notes":"Recursive DFS. HashMap tracks original→clone.","cls":""},
        {"name":"BFS + Queue (User Solution)","time":"O(V+E)","space":"O(V+E)","notes":"Iterative BFS. HashMap tracks original→clone. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"BFS with Queue and Visited Map","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(V+E)","space":"O(V+E)",
        "explanation":"Use a queue for Breadth-First Search and a hash map (clones) to handle cycles. For each node popped from the queue, iterate its neighbors. If a neighbor isn't cloned yet, clone it, add to map, and push to queue. Finally, link the current clone to the neighbor clone."},
    "codes": _codes("""from collections import deque
from typing import Optional

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        
        # Edge case: if input graph is empty
        if not node:
            return None
        
        # Dictionary to map original node -> cloned node
        # This acts as:
        # 1. Visited set (prevents cycles)
        # 2. Storage of cloned nodes
        cloned_nodes = {node: Node(node.val)}
        
        # BFS queue initialized with the starting node (original graph node)
        queue = deque([node])
        
        # Standard BFS traversal
        while queue:
             
            # Pop the next node from queue (original graph node)
            current_node = queue.popleft()
            
            # Iterate through its neighbors in the original graph
            for neighbor in current_node.neighbors:
                
                # If this neighbor has not been cloned yet
                if neighbor not in cloned_nodes:
                    
                    # Create clone of neighbor
                    cloned_nodes[neighbor] = Node(neighbor.val)
                    
                    # Add original neighbor to queue for further traversal
                    queue.append(neighbor)
                
                # Connect cloned current node to cloned neighbor
                # cloned_nodes[current_node]  -> cloned version of current node
                # cloned_nodes[neighbor]      -> cloned version of neighbor
                cloned_nodes[current_node].neighbors.append(cloned_nodes[neighbor])
        
        # Return cloned version of the starting node
        return cloned_nodes[node]""", "Clone Graph"),
    "insight_title":"HashMap Breaks Cycles",
    "insight_text":"Without the clones dictionary, BFS would loop infinitely on cycles (which are common in undirected graphs). Storing the clone before pushing to the queue is the key: it makes the clone available to break any cycle.",
    "tips":["<strong>Store the clone BEFORE queuing:</strong> clones[neighbor] = Node(...) must happen before queue.append(neighbor).",
            "<strong>DFS alternative:</strong> Use recursion and return early if node in clones.",
            "<strong>Companies:</strong> Amazon, Google, Meta."]
})

add_problem("q33", {
    "name": "Sort Colors (Dutch National Flag)", "num": 75, "diff": "Medium",
    "topics": ["Array","Two Pointers","Sorting"],
    "link": "https://leetcode.com/problems/sort-colors",
    "statement": "Given an array with values 0, 1, 2 (representing red, white, blue), sort them in-place so that all 0s come first, then 1s, then 2s. Use only one pass with constant extra space.",
    "examples": [
        {"title":"Example 1","input":"nums = [2,0,2,1,1,0]","output":"[0,0,1,1,2,2]","explain":"Sorted in one pass."},
        {"title":"Example 2","input":"nums = [2,0,1]","output":"[0,1,2]","explain":"Three elements sorted."},
    ],
    "constraints":["n == nums.length","1 &le; n &le; 300","nums[i] is 0, 1, or 2"],
    "approaches":[
        {"name":"Count sort","time":"O(n)","space":"O(1)","notes":"Count 0s,1s,2s then fill. Two passes.","cls":""},
        {"name":"Dutch National Flag (3-way partition)","time":"O(n)","space":"O(1)","notes":"One pass with lo/mid/hi pointers. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Dutch National Flag Algorithm","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Maintain three pointers: lo (boundary of 0s), mid (current element), hi (boundary of 2s). Swap nums[mid] based on value: 0→swap with lo+advance both; 1→advance mid; 2→swap with hi, retreat hi only."},
    "codes": _codes("""def sortColors(nums):
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1""", "Sort Colors"),
    "insight_title":"Three Regions Maintained Invariantly",
    "insight_text":"At all times: [0,lo) = all 0s, [lo,mid) = all 1s, (hi,n-1] = all 2s, [mid,hi] = unknown. The loop shrinks the unknown region to empty.",
    "tips":["<strong>When swapping with hi:</strong> Don't advance mid — the swapped value hasn't been seen yet.",
            "<strong>Companies:</strong> Google, Amazon — great example of partitioning thinking."]
})

add_problem("q42", {
    "name": "Design Add and Search Words Data Structure", "num": 211, "diff": "Medium",
    "topics": ["String","Trie","DFS","Design"],
    "link": "https://leetcode.com/problems/design-add-and-search-words-data-structure",
    "statement": "Design a data structure that supports <code>addWord(word)</code> and <code>search(word)</code> where <code>search</code> can use <code>.</code> as a wildcard matching any single letter.",
    "examples": [
        {"title":"Example 1","input":'addWord("bad"),addWord("dad"),addWord("mad"),search("pad")→false,search("bad")→true,search(".ad")→true,search("b..")→true',"output":"[null,null,null,false,true,true,true]","explain":"Wildcard '.' matches any single character."},
    ],
    "constraints":["1 &le; word.length &le; 25","word consists of lowercase letters or '.'","At most 10000 calls total"],
    "approaches":[{"name":"Trie + DFS for wildcards","time":"O(m) add, O(26^m) worst-case search","space":"O(m*n)","notes":"Trie stores words; wildcard triggers DFS on all children. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Trie + Recursive Wildcard DFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(m) add, O(26^m) wildcard","space":"O(m·n)",
        "explanation":"Build a standard Trie for addWord. For search, traverse normally for regular characters. For '.', recursively try all children. Worst case (all wildcards) is exponential but bounded by word length."},
    "codes": _codes("""class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        def dfs(j, node):
            for i in range(j, len(word)):
                ch = word[i]
                if ch == '.':
                    return any(dfs(i+1, child) for child in node.children.values())
                if ch not in node.children:
                    return False
                node = node.children[ch]
            return node.is_end
        return dfs(0, self.root)""", "Word Dictionary"),
    "insight_title":"Wildcard Forces DFS on All Children",
    "insight_text":"A '.' at position i means we must explore all children simultaneously — this is why we use recursive DFS. Regular characters narrow it to one child path.",
    "tips":["<strong>Trie is the foundation:</strong> Build on the Implement Trie knowledge.",
            "<strong>Companies:</strong> Amazon, Google, Meta."]
})

add_problem("q46", {
    "name": "Trapping Rain Water", "num": 42, "diff": "Hard",
    "topics": ["Array","Two Pointers","Stack","DP"],
    "link": "https://leetcode.com/problems/trapping-rain-water",
    "statement": "Given <code>n</code> non-negative integers representing an elevation map where each bar has width 1, compute how much water can be trapped after raining.",
    "examples": [
        {"title":"Example 1","input":"height = [0,1,0,2,1,0,1,3,2,1,2,1]","output":"6","explain":"6 units of rain water trapped."},
        {"title":"Example 2","input":"height = [4,2,0,3,2,5]","output":"9","explain":"9 units trapped."},
    ],
    "constraints":["n == height.length","1 &le; n &le; 2*10<sup>4</sup>","0 &le; height[i] &le; 10<sup>5</sup>"],
    "approaches":[
        {"name":"Prefix/Suffix Max arrays","time":"O(n)","space":"O(n)","notes":"Water at i = min(prefMax, sufMax) - height[i]. Clear.","cls":""},
        {"name":"Two Pointers","time":"O(n)","space":"O(1)","notes":"Same idea; compute on the fly. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Two Pointers","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
        "explanation":"Water at position i = min(max_left, max_right) - height[i]. Use two pointers: process the side with the smaller max first (since that determines the bottleneck)."},
    "codes": _codes("""def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water""", "Trapping Rain Water"),
    "insight_title":"Process the Side with the Smaller Max",
    "insight_text":"When height[left] < height[right], the left side is the bottleneck (less max). Its water contribution is completely determined by left_max regardless of what's on the right.",
    "tips":["<strong>Don't confuse with Container With Most Water:</strong> That problem maximizes area between two walls; this fills water in depressions.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft — very common Hard."]
})

add_problem("q49", {
    "name": "Design Word Search II (Word Search in Grid)", "num": 212, "diff": "Hard",
    "topics": ["Trie","Backtracking","Matrix"],
    "link": "https://leetcode.com/problems/word-search-ii",
    "statement": "Given an <code>m x n</code> board of characters and a list of strings <code>words</code>, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells (horizontally or vertically adjacent), without reusing a cell.",
    "examples": [
        {"title":"Example 1","input":'board=[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words=["oath","pea","eat","rain"]',"output":'["eat","oath"]',"explain":"Both words found on the board."},
    ],
    "constraints":["1 &le; m,n &le; 12","1 &le; words.length &le; 3*10<sup>4</sup>","1 &le; word.length &le; 10"],
    "approaches":[
        {"name":"DFS per word","time":"O(W·4·3<sup>L-1</sup>·mn)","space":"O(mn)","notes":"Too slow for many words.","cls":""},
        {"name":"Trie + Backtracking","time":"O(mn·4·3<sup>L-1</sup>)","space":"O(W·L)","notes":"Build Trie once; one DFS for all words simultaneously. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Trie + DFS Backtracking","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn·4·3^L)","space":"O(W·L)",
        "explanation":"Build a Trie from all words. DFS from every cell, following the Trie to prune paths that don't lead to any word. When a word end is found, add to results."},
    "codes": _codes("""def findWords(board, words):
    # Build Trie
    trie = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node['#'] = w  # mark end

    m, n = len(board), len(board[0])
    result = set()

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node: return
        nxt = node[ch]
        if '#' in nxt: result.add(nxt['#'])
        board[r][c] = '#'  # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != '#':
                dfs(nr, nc, nxt)
        board[r][c] = ch  # restore

    for r in range(m):
        for c in range(n):
            dfs(r, c, trie)
    return list(result)""", "Word Search II"),
    "insight_title":"One Trie, One DFS - All Words Simultaneously",
    "insight_text":"Without a Trie, you'd run DFS for each word separately. The Trie lets all words share a search - one DFS pass from each cell can find all matching words at once, with pruning when no words share the current prefix.",
    "tips":["<strong>Trie pruning is key:</strong> When a prefix doesn't exist in the Trie, stop immediately.",
            "<strong>Companies:</strong> Google, Meta, Amazon — common Hard."]
})

add_problem("q53", {
    "name": "Spiral Matrix", "num": 54, "diff": "Medium",
    "topics": ["Array","Matrix","Simulation"],
    "link": "https://leetcode.com/problems/spiral-matrix",
    "statement": "Given an <code>m x n</code> matrix, return all elements of the matrix in <strong>spiral order</strong>.",
    "examples": [
        {"title":"Example 1","input":"matrix = [[1,2,3],[4,5,6],[7,8,9]]","output":"[1,2,3,6,9,8,7,4,5]","explain":"Traverse in clockwise spiral."},
        {"title":"Example 2","input":"matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]","output":"[1,2,3,4,8,12,11,10,9,5,6,7]","explain":"4x3 matrix spiral."},
    ],
    "constraints":["m == matrix.length","n == matrix[i].length","1 &le; m, n &le; 10","Matrix values in [-100, 100]"],
    "approaches":[{"name":"Layer-by-layer boundary shrink","time":"O(mn)","space":"O(mn)","notes":"Track top/bottom/left/right boundaries. Optimal.","cls":"optimal-row"}],
    "optimal_approach":{"title":"Shrinking Boundary Simulation","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(mn)",
        "explanation":"Maintain four boundaries: top, bottom, left, right. Traverse right along top, down along right, left along bottom, up along left — then shrink each boundary after traversal."},
    "codes": _codes("""def spiralOrder(matrix):
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1): result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1): result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1): result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1): result.append(matrix[r][left])
            left += 1
    return result""", "Spiral Matrix"),
    "insight_title":"Four Sides, Four Shrinks Per Layer",
    "insight_text":"Each full traversal of a layer traverses top row, right column, bottom row, left column — then shrinks all four boundaries by 1. Guard conditions prevent double-counting a single row/column.",
    "tips":["<strong>Guard the bottom and left traversals:</strong> Check top &le; bottom and left &le; right before traversing to avoid duplicates in a single row/column.",
            "<strong>Companies:</strong> Amazon, Google."]
})

add_problem("q54", {
    "name": "Set Matrix Zeroes", "num": 73, "diff": "Medium",
    "topics": ["Array","Matrix","Hash Set"],
    "link": "https://leetcode.com/problems/set-matrix-zeroes",
    "statement": "Given an <code>m x n</code> integer matrix, if an element is 0, set its entire row and column to 0's. Do it <strong>in-place</strong>.",
    "examples": [
        {"title":"Example 1","input":"matrix = [[1,1,1],[1,0,1],[1,1,1]]","output":"[[1,0,1],[0,0,0],[1,0,1]]","explain":"Row 1 and column 1 zeroed."},
        {"title":"Example 2","input":"matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]","output":"[[0,0,0,0],[0,4,5,0],[0,3,1,0]]","explain":"Two zero positions affect two rows and two columns."},
    ],
    "constraints":["m==matrix.length","n==matrix[0].length","1&le;m,n&le;200","-2<sup>31</sup>&le;matrix[i][j]&le;2<sup>31</sup>-1"],
    "approaches":[
        {"name":"Extra arrays","time":"O(mn)","space":"O(m+n)","notes":"Store which rows/cols to zero.","cls":""},
        {"name":"First row/col as markers","time":"O(mn)","space":"O(1)","notes":"Use first row and column as flags. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"First Row/Column as Flags","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(1)",
        "explanation":"Use the first row and first column as markers for which rows/columns need to be zeroed. Handle first row and column specially with boolean flags."},
    "codes": _codes("""def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(n))
    first_col_zero = any(matrix[r][0] == 0 for r in range(m))
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, m):
        for c in range(1, n):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:
        for c in range(n): matrix[0][c] = 0
    if first_col_zero:
        for r in range(m): matrix[r][0] = 0""", "Set Matrix Zeroes"),
    "insight_title":"Repurpose the First Row/Column",
    "insight_text":"Instead of O(m+n) extra space for row/column markers, we repurpose the first row and column of the matrix itself as markers — giving O(1) space.",
    "tips":["<strong>Process inner matrix first,</strong> then handle first row/column at the end.",
            "<strong>Companies:</strong> Amazon, Google."]
})

add_problem("q59", {
    "name": "Kth Largest Element in an Array", "num": 215, "diff": "Medium",
    "topics": ["Array","Heap","Quickselect","Sorting"],
    "link": "https://leetcode.com/problems/kth-largest-element-in-an-array",
    "statement": "Given an integer array <code>nums</code> and an integer k, return the <code>k</code>th largest element. Note: it is the kth largest in sorted order, not the kth distinct element.",
    "examples": [
        {"title":"Example 1","input":"nums=[3,2,1,5,6,4], k=2","output":"5","explain":"Second largest is 5."},
        {"title":"Example 2","input":"nums=[3,2,3,1,2,4,5,5,6], k=4","output":"4","explain":"Fourth largest is 4."},
    ],
    "constraints":["1&le;k&le;nums.length&le;10<sup>5</sup>","-10<sup>4</sup>&le;nums[i]&le;10<sup>4</sup>"],
    "approaches":[
        {"name":"Sort","time":"O(n log n)","space":"O(1)","notes":"Sort descending, return index k-1.","cls":""},
        {"name":"Min Heap size k","time":"O(n log k)","space":"O(k)","notes":"Keep k-element min heap. Optimal.","cls":"optimal-row"},
        {"name":"Quickselect","time":"O(n) avg","space":"O(1)","notes":"Partition-based; O(n²) worst case.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Min Heap of Size k","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n log k)","space":"O(k)",
        "explanation":"Maintain a min-heap of size k. For each element, push it. If heap size exceeds k, pop the minimum. At the end, the heap's minimum is the k-th largest."},
    "codes": _codes("""import heapq
def findKthLargest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]""", "Kth Largest Element"),
    "insight_title":"Min Heap of Size k = k-th Largest at Root",
    "insight_text":"By keeping only k elements in the heap and discarding smaller ones, the smallest element remaining is the k-th largest overall — at heap[0].",
    "tips":["<strong>Quickselect alternative:</strong> Average O(n) but O(n²) worst case. Use for time-sensitive scenarios with good pivot selection.",
            "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft."]
})

add_problem("q67", {
    "name": "Balanced Binary Tree", "num": 110, "diff": "Easy",
    "topics": ["Tree","DFS"],
    "link": "https://leetcode.com/problems/balanced-binary-tree",
    "statement": "Given a binary tree, determine if it is height-balanced. A binary tree is balanced if the depth of the two subtrees of every node never differs by more than 1.",
    "examples": [
        {"title":"Example 1","input":"root=[3,9,20,null,null,15,7]","output":"true","explain":"Heights differ by at most 1 at every node."},
        {"title":"Example 2","input":"root=[1,2,2,3,3,null,null,4,4]","output":"false","explain":"Left subtree height 4, right 2 — difference of 2."},
    ],
    "constraints":["0 &le; nodes &le; 5000","-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"Top-down (naive)","time":"O(n log n)","space":"O(n)","notes":"Computes height at each node repeatedly.","cls":""},
        {"name":"Bottom-up DFS","time":"O(n)","space":"O(n)","notes":"Return -1 as imbalance signal. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Bottom-Up DFS with -1 Signal","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"DFS returns the height of the subtree, or -1 to signal imbalance. At each node: if left or right returns -1, propagate -1 up. Also check if |left - right| > 1 to detect new imbalance."},
    "codes": _codes("""def isBalanced(root):
    def dfs(node):
        if not node: return 0
        left = dfs(node.left)
        right = dfs(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return dfs(root) != -1""", "Balanced Binary Tree"),
    "insight_title":"-1 as an Early Exit Signal",
    "insight_text":"Using -1 as a sentinel value propagates imbalance up the call stack without needing a global variable. Once -1 is returned at any level, all parent calls immediately propagate it — O(n) total.",
    "tips":["<strong>Better than naive:</strong> The top-down O(n log n) approach recalculates heights repeatedly. Bottom-up calculates each height once.",
            "<strong>Companies:</strong> Amazon, Google, Bloomberg."]
})
