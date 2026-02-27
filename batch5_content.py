"""Batch 5: q26-q36 — covering topics: Trees, DP, Arrays, Greedy"""
from shared_generator import add_problem

add_problem("q26", {
    "name": "Serialize and Deserialize Binary Tree",
    "num": 297, "diff": "Hard",
    "topics": ["Tree", "BFS", "DFS", "Design"],
    "link": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree",
    "statement": "Design an algorithm to serialize a binary tree to a string and deserialize that string back to the original tree. The encoding/decoding algorithm is your choice — there is no constraint on format.",
    "examples": [
        {"title":"Example 1","input":"root = [1,2,3,null,null,4,5]","output":"[1,2,3,null,null,4,5]","explain":"Tree can be serialized to any string and reconstructed correctly."},
    ],
    "constraints":["0 &le; nodes &le; 10<sup>4</sup>","-1000 &le; Node.val &le; 1000"],
    "approaches":[
        {"name":"BFS Level Order","time":"O(n)","space":"O(n)","notes":"Encode level by level using null markers. Simple to implement.","cls":""},
        {"name":"DFS Preorder","time":"O(n)","space":"O(n)","notes":"Preorder with null markers. Recursive and clean. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"DFS Preorder with Null Markers","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
        "explanation":"Serialize via preorder DFS, writing node values and 'N' for null, comma-separated. Deserialize by reading values in order, building nodes recursively using an index pointer."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""class Codec:
    def serialize(self, root):
        vals = []
        def dfs(node):
            if not node:
                vals.append('N')
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(vals)

    def deserialize(self, data):
        vals = iter(data.split(','))
        def dfs():
            v = next(vals)
            if v == 'N':
                return None
            node = TreeNode(int(v))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public String serialize(TreeNode root) {
    StringBuilder sb=new StringBuilder();
    dfs(root,sb); return sb.toString();
}
void dfs(TreeNode n,StringBuilder sb){
    if(n==null){sb.append("N,");return;}
    sb.append(n.val).append(',');dfs(n.left,sb);dfs(n.right,sb);
}
public TreeNode deserialize(String data) {
    Queue&lt;String&gt; q=new LinkedList&lt;&gt;(Arrays.asList(data.split(",")));
    return build(q);
}
TreeNode build(Queue&lt;String&gt; q){
    String v=q.poll();if(v.equals("N")) return null;
    TreeNode n=new TreeNode(Integer.parseInt(v));n.left=build(q);n.right=build(q);return n;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var serialize = function(root) {
    const vals=[];const dfs=n=>{if(!n){vals.push('N');return;}vals.push(n.val);dfs(n.left);dfs(n.right);};
    dfs(root);return vals.join(',');
};
var deserialize = function(data) {
    const q=data.split(',');let i=0;
    const dfs=()=>{const v=q[i++];if(v==='N')return null;const n=new TreeNode(+v);n.left=dfs();n.right=dfs();return n;};
    return dfs();
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func serialize(root *TreeNode) string {
    var sb strings.Builder;var dfs func(*TreeNode)
    dfs=func(n *TreeNode){if n==nil{sb.WriteString("N,");return};fmt.Fprintf(&sb,"%d,",n.Val);dfs(n.Left);dfs(n.Right)}
    dfs(root);return sb.String()
}
func deserialize(data string) *TreeNode {
    parts:=strings.Split(data,",");i:=0
    var dfs func()*TreeNode;dfs=func()*TreeNode{v:=parts[i];i++;if v=="N"{return nil}
        val,_:=strconv.Atoi(v);n:=&TreeNode{Val:val};n.Left=dfs();n.Right=dfs();return n}
    return dfs()
}"""},
    },
    "insight_title":"Preorder + Null Markers is Self-Describing",
    "insight_text":"Preorder traversal (root, left, right) with explicit null markers gives enough information to uniquely reconstruct the tree. The key: reading the serialized stream in preorder naturally rebuilds the tree in preorder.",
    "tips":[
        "<strong>Most flexible encoding:</strong> Preorder DFS is simplest to implement. BFS (level-order) is more intuitive but requires tracking nulls carefully.",
        "<strong>Iterator trick:</strong> In Python, wrapping the split array in iter() and using next() gives a clean recursive implementation without an index variable.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Uber — a classic design+tree combination.",
    ]
})

add_problem("q27", {
    "name": "Longest Repeating Character Replacement",
    "num": 424, "diff": "Medium",
    "topics": ["String", "Sliding Window"],
    "link": "https://leetcode.com/problems/longest-repeating-character-replacement",
    "statement": "You are given a string <code>s</code> and an integer <code>k</code>. You can choose any character in the string and change it to any other uppercase English character at most <code>k</code> times. Return the length of the longest substring containing the same letter you can get after performing these operations.",
    "examples": [
        {"title":"Example 1","input":'s = "ABAB", k = 2',"output":"4","explain":"Replace two 'A's with 'B's or vice-versa: 'BBBB' or 'AAAA'."},
        {"title":"Example 2","input":'s = "AABABBA", k = 1',"output":"4","explain":"Replace the 'A' at index 3 to get 'AABBBBA', window = 'BBBB' length 4."},
    ],
    "constraints":["1 &le; s.length &le; 10<sup>5</sup>","s consists of uppercase English letters","0 &le; k &le; s.length"],
    "approaches":[
        {"name":"Brute Force","time":"O(n&sup2;)","space":"O(1)","notes":"Check all substrings.","cls":""},
        {"name":"Sliding Window","time":"O(n)","space":"O(1)","notes":"Window invalid if (length - maxFreq) > k. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Sliding Window","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)","explanation":"Maintain a window [left, right]. Track the frequency of the most common character (maxFreq). A window is valid if <code>window_len - maxFreq &le; k</code> (we can replace all non-maxFreq chars). When invalid, slide left by 1."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def characterReplacement(s, k):
    count = {}
    left = 0
    max_len = 0
    max_freq = 0
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int characterReplacement(String s, int k) {
    int[] count=new int[26];int left=0,maxFreq=0,maxLen=0;
    for(int right=0;right&lt;s.length();right++){
        count[s.charAt(right)-'A']++;maxFreq=Math.max(maxFreq,count[s.charAt(right)-'A']);
        while((right-left+1)-maxFreq&gt;k) count[s.charAt(left++)-'A']--;
        maxLen=Math.max(maxLen,right-left+1);
    }
    return maxLen;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var characterReplacement = function(s, k) {
    const count=new Array(26).fill(0);let left=0,maxFreq=0,maxLen=0;
    for(let right=0;right<s.length;right++){
        count[s.charCodeAt(right)-65]++;
        maxFreq=Math.max(maxFreq,count[s.charCodeAt(right)-65]);
        while(right-left+1-maxFreq>k) count[s.charCodeAt(left++)-65]--;
        maxLen=Math.max(maxLen,right-left+1);
    }
    return maxLen;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func characterReplacement(s string, k int) int {
    count:=[26]int{};left,maxFreq,maxLen:=0,0,0
    for right:=0;right<len(s);right++{
        count[s[right]-'A']++;if count[s[right]-'A']>maxFreq{maxFreq=count[s[right]-'A']}
        for right-left+1-maxFreq>k{count[s[left]-'A']--;left++}
        if right-left+1>maxLen{maxLen=right-left+1}
    }
    return maxLen
}"""},
    },
    "insight_title":"Key Invariant: window_len − maxFreq ≤ k",
    "insight_text":"The minimum number of replacements needed to make a window all one character = window_length - count_of_most_frequent_char. This is O(1) to check at every step, enabling the O(n) sliding window.",
    "tips":[
        "<strong>maxFreq can only increase:</strong> We never need to recalculate it downward when shrinking the window. The window size won't grow if maxFreq doesn't increase, so we never miss the optimal answer.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Bloomberg.",
    ]
})

add_problem("q28", {
    "name": "Longest Increasing Subsequence",
    "num": 300, "diff": "Medium",
    "topics": ["Array", "Dynamic Programming", "Binary Search"],
    "link": "https://leetcode.com/problems/longest-increasing-subsequence",
    "statement": "Given an integer array <code>nums</code>, return the length of the <strong>longest strictly increasing subsequence</strong>.",
    "examples": [
        {"title":"Example 1","input":"nums = [10,9,2,5,3,7,101,18]","output":"4","explain":"LIS is [2,3,7,101]."},
        {"title":"Example 2","input":"nums = [0,1,0,3,2,3]","output":"4","explain":"[0,1,2,3] has length 4."},
        {"title":"Example 3","input":"nums = [7,7,7,7,7,7,7]","output":"1","explain":"No increasing pair; LIS has length 1."},
    ],
    "constraints":["1 &le; nums.length &le; 2500","-10<sup>4</sup> &le; nums[i] &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"DP O(n²)","time":"O(n&sup2;)","space":"O(n)","notes":"dp[i] = LIS ending at index i. Standard.","cls":""},
        {"name":"Patience Sort + Binary Search","time":"O(n log n)","space":"O(n)","notes":"Maintain sorted piles. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Patience Sort + Binary Search","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n log n)","space":"O(n)",
        "explanation":"Maintain a <code>tails</code> array where <code>tails[i]</code> is the smallest tail element of all increasing subsequences of length i+1. For each number, binary search for its position in tails and replace; or append if it's larger than all. The length of tails = LIS length."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""import bisect

def lengthOfLIS(nums):
    tails = []
    for n in nums:
        idx = bisect.bisect_left(tails, n)
        if idx == len(tails):
            tails.append(n)
        else:
            tails[idx] = n
    return len(tails)"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int lengthOfLIS(int[] nums) {
    List&lt;Integer&gt; tails=new ArrayList&lt;&gt;();
    for(int n:nums){int lo=0,hi=tails.size();
        while(lo&lt;hi){int m=(lo+hi)/2;if(tails.get(m)&lt;n)lo=m+1;else hi=m;}
        if(lo==tails.size())tails.add(n);else tails.set(lo,n);
    }
    return tails.size();
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var lengthOfLIS = function(nums) {
    const tails=[];
    for(const n of nums){
        let lo=0,hi=tails.length;
        while(lo<hi){const m=(lo+hi)>>1;if(tails[m]<n)lo=m+1;else hi=m;}
        if(lo===tails.length)tails.push(n);else tails[lo]=n;
    }
    return tails.length;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func lengthOfLIS(nums []int) int {
    tails:=[]int{}
    for _,n:=range nums{
        lo,hi:=0,len(tails)
        for lo<hi{m:=(lo+hi)/2;if tails[m]<n{lo=m+1}else{hi=m}}
        if lo==len(tails){tails=append(tails,n)}else{tails[lo]=n}
    }
    return len(tails)
}"""},
    },
    "insight_title":"tails[] Doesn't Store the Actual LIS",
    "insight_text":"The tails array may NOT be the actual LIS — it's a construction artifact. However, its length always equals the LIS length. If you need the actual sequence, use the O(n²) DP approach with backtracking.",
    "tips":[
        "<strong>Know both approaches:</strong> O(n²) DP is easier to explain and code under pressure; O(n log n) shows sophistication.",
        "<strong>bisect_left:</strong> Finds the leftmost position where n can be inserted to keep tails sorted. If equal exists, it replaces it (maintaining strictly increasing invariant).",
        "<strong>Companies:</strong> Google, Amazon, Meta, Microsoft.",
    ]
})

add_problem("q29", {
    "name": "Rotate Image",
    "num": 48, "diff": "Medium",
    "topics": ["Array", "Math", "Matrix"],
    "link": "https://leetcode.com/problems/rotate-image",
    "statement": "Given an <code>n x n</code> 2D matrix representing an image, rotate it 90 degrees clockwise <strong>in-place</strong>.",
    "examples": [
        {"title":"Example 1","input":"matrix = [[1,2,3],[4,5,6],[7,8,9]]","output":"[[7,4,1],[8,5,2],[9,6,3]]","explain":"90-degree clockwise rotation."},
        {"title":"Example 2","input":"matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]","output":"[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]","explain":"4x4 rotation."},
    ],
    "constraints":["n == matrix.length == matrix[0].length","1 &le; n &le; 20","-1000 &le; matrix[i][j] &le; 1000"],
    "approaches":[
        {"name":"Extra Matrix","time":"O(n²)","space":"O(n²)","notes":"Copy to new matrix. Not in-place.","cls":""},
        {"name":"Transpose + Reverse Rows","time":"O(n²)","space":"O(1)","notes":"Transpose then reverse each row. Optimal in-place.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Transpose + Reverse Rows","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n²)","space":"O(1)",
        "explanation":"Step 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i]). Step 2: Reverse each row. These two steps together produce a 90° clockwise rotation."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def rotate(matrix):
    n = len(matrix)
    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public void rotate(int[][] m) {
    int n=m.length;
    for(int i=0;i&lt;n;i++) for(int j=i+1;j&lt;n;j++){int t=m[i][j];m[i][j]=m[j][i];m[j][i]=t;}
    for(int[] row:m){int l=0,r=n-1;while(l&lt;r){int t=row[l];row[l++]=row[r];row[r--]=t;}}
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var rotate = function(matrix) {
    const n=matrix.length;
    for(let i=0;i<n;i++) for(let j=i+1;j<n;j++) [matrix[i][j],matrix[j][i]]=[matrix[j][i],matrix[i][j]];
    for(const row of matrix) row.reverse();
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func rotate(matrix [][]int) {
    n:=len(matrix)
    for i:=0;i<n;i++{for j:=i+1;j<n;j++{matrix[i][j],matrix[j][i]=matrix[j][i],matrix[i][j]}}
    for _,row:=range matrix{for l,r:=0,n-1;l<r;l,r=l+1,r-1{row[l],row[r]=row[r],row[l]}}
}"""},
    },
    "insight_title":"Matrix Rotation = Transpose + Mirror",
    "insight_text":"90° clockwise: transpose then reverse each row. 90° counter-clockwise: transpose then reverse each column. 180°: reverse each row then each column. Memorize these patterns.",
    "tips":[
        "<strong>Derive on the fly:</strong> For a 90° clockwise rotation, element at (i,j) goes to (j, n-1-i). Verify this with a 3×3 example on paper.",
        "<strong>Don't try to do it in one pass</strong> — the two-step method is O(n²) but clear and bug-free.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft.",
    ]
})

add_problem("q30", {
    "name": "Group Anagrams",
    "num": 49, "diff": "Medium",
    "topics": ["Array", "Hash Map", "String"],
    "link": "https://leetcode.com/problems/group-anagrams",
    "statement": "Given an array of strings <code>strs</code>, group the <strong>anagrams</strong> together. You can return the answer in any order. Two strings are anagrams if one is a rearrangement of the other.",
    "examples": [
        {"title":"Example 1","input":'strs = ["eat","tea","tan","ate","nat","bat"]',"output":'[["bat"],["nat","tan"],["ate","eat","tea"]]',"explain":"Anagram groups."},
        {"title":"Example 2","input":'strs = [""]',"output":'[[""]]',"explain":"Empty string is its own group."},
        {"title":"Example 3","input":'strs = ["a"]',"output":'[["a"]]',"explain":"Single character, one group."},
    ],
    "constraints":["1 &le; strs.length &le; 10<sup>4</sup>","0 &le; strs[i].length &le; 100","strs[i] consists of lowercase letters"],
    "approaches":[
        {"name":"Sort each word as key","time":"O(n·k log k)","space":"O(n·k)","notes":"Sort each string and use as map key. Simple.","cls":""},
        {"name":"Character count as key","time":"O(n·k)","space":"O(n·k)","notes":"26-char frequency tuple as key. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Character Count as Key","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n·k)","space":"O(n·k)",
        "explanation":"For each string, compute a 26-element character frequency array and use it as a hash map key. All anagrams will produce the same frequency array, so they'll be grouped together."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or use char count tuple
        groups[key].append(s)
    return list(groups.values())"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public List&lt;List&lt;String&gt;&gt; groupAnagrams(String[] strs) {
    Map&lt;String,List&lt;String&gt;&gt; map=new HashMap&lt;&gt;();
    for(String s:strs){char[] c=s.toCharArray();Arrays.sort(c);String k=new String(c);
        map.computeIfAbsent(k,x->new ArrayList&lt;&gt;()).add(s);}
    return new ArrayList&lt;&gt;(map.values());
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var groupAnagrams = function(strs) {
    const map=new Map();
    for(const s of strs){const k=s.split('').sort().join('');if(!map.has(k))map.set(k,[]);map.get(k).push(s);}
    return [...map.values()];
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func groupAnagrams(strs []string) [][]string {
    groups:=map[[26]int][]string{}
    for _,s:=range strs{var key [26]int;for _,c:=range s{key[c-'a']++};groups[key]=append(groups[key],s)}
    res:=[][]string{};for _,v:=range groups{res=append(res,v)};return res
}"""},
    },
    "insight_title":"Any Canonical Form Works as a Key",
    "insight_text":"Anagrams are equivalent under character permutation. Any transformation that maps all permutations of a string to the same value works as a key. Sorting (O(k log k)) and counting (O(k)) both achieve this.",
    "tips":[
        "<strong>Two valid keys:</strong> sorted string, or tuple of 26 character counts. The count approach is asymptotically better.",
        "<strong>Follow-up:</strong> If strings are very long, comparison via character count is significantly faster than sorting.",
        "<strong>Companies:</strong> Amazon, Google, Facebook, Microsoft — extremely common.",
    ]
})
