"""Batch 4: q21-q30"""
from shared_generator import add_problem

add_problem("q21", {
    "name": "Find Minimum in Rotated Sorted Array",
    "num": 153, "diff": "Medium",
    "topics": ["Array", "Binary Search"],
    "link": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array",
    "statement": "Suppose an array of length <code>n</code> sorted in ascending order is rotated between 1 and n times. Given the rotated array <code>nums</code>, find the minimum element. You must write an algorithm that runs in <strong>O(log n)</strong> time.",
    "examples": [
        {"title":"Example 1","input":"nums = [3,4,5,1,2]","output":"1","explain":"Rotated array. Minimum is 1."},
        {"title":"Example 2","input":"nums = [4,5,6,7,0,1,2]","output":"0","explain":"Original [0,1,2,4,5,6,7] rotated 4 times."},
        {"title":"Example 3","input":"nums = [11,13,15,17]","output":"11","explain":"No rotation; minimum is the first element."},
    ],
    "constraints":["n in [1, 5000]","All values unique","-5000 &le; nums[i] &le; 5000"],
    "approaches":[
        {"name":"Linear Scan","time":"O(n)","space":"O(1)","notes":"Too slow; misses the log n requirement.","cls":""},
        {"name":"Binary Search","time":"O(log n)","space":"O(1)","notes":"The minimum is at the inflection point. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Binary Search","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(log n)","space":"O(1)",
        "explanation":"The minimum is at the rotation point. Compare <code>nums[mid]</code> with <code>nums[right]</code>: if nums[mid] &gt; nums[right], the minimum is in the right half; otherwise it's in the left half (including mid)."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int findMin(int[] nums) {
    int left=0,right=nums.length-1;
    while(left&lt;right){int mid=(left+right)/2;
        if(nums[mid]&gt;nums[right]) left=mid+1; else right=mid;}
    return nums[left];
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var findMin = function(nums) {
    let l=0,r=nums.length-1;
    while(l<r){const m=(l+r)>>1;if(nums[m]>nums[r])l=m+1;else r=m;}
    return nums[l];
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func findMin(nums []int) int {
    l,r:=0,len(nums)-1
    for l<r{m:=(l+r)/2;if nums[m]>nums[r]{l=m+1}else{r=m}}
    return nums[l]
}"""},
    },
    "insight_title":"Compare Mid with Right, Not Left",
    "insight_text":"Comparing with right (not left) avoids ambiguity when the array isn't rotated. If nums[mid] &gt; nums[right], the right portion has been rotated and the minimum is to the right of mid.",
    "tips":[
        "<strong>Why right, not left?</strong> If nums[left] &lt; nums[mid], left might still be the minimum (no rotation). Comparing with right cleanly determines which half is sorted.",
        "<strong>Duplicates variant:</strong> LeetCode #154 adds duplicates, requiring right-- when nums[mid]==nums[right].",
        "<strong>Companies:</strong> Amazon, Google, Microsoft, Uber.",
    ]
})

add_problem("q22", {
    "name": "Search in Rotated Sorted Array",
    "num": 33, "diff": "Medium",
    "topics": ["Array", "Binary Search"],
    "link": "https://leetcode.com/problems/search-in-rotated-sorted-array",
    "statement": "Given a rotated sorted array <code>nums</code> with unique values and an integer <code>target</code>, return the index of <code>target</code> if it is in <code>nums</code>, or <code>-1</code> if it is not there. Must run in <strong>O(log n)</strong>.",
    "examples": [
        {"title":"Example 1","input":"nums=[4,5,6,7,0,1,2], target=0","output":"4","explain":"0 is at index 4."},
        {"title":"Example 2","input":"nums=[4,5,6,7,0,1,2], target=3","output":"-1","explain":"3 is not in the array."},
    ],
    "constraints":["1 &le; n &le; 5000","All values unique","-10<sup>4</sup> &le; nums[i], target &le; 10<sup>4</sup>"],
    "approaches":[
        {"name":"Linear Scan","time":"O(n)","space":"O(1)","notes":"Too slow.","cls":""},
        {"name":"Modified Binary Search","time":"O(log n)","space":"O(1)","notes":"At each step determine which half is sorted. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Modified Binary Search","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(log n)","space":"O(1)",
        "explanation":"At each step, one of the two halves [left,mid] or [mid,right] must be sorted. Determine which one, then check if target falls within that sorted half. If yes, search that half; otherwise search the other."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public int search(int[] nums, int target) {
    int l=0,r=nums.length-1;
    while(l&lt;=r){int m=(l+r)/2;
        if(nums[m]==target) return m;
        if(nums[l]&lt;=nums[m]){if(nums[l]&lt;=target&amp;&amp;target&lt;nums[m])r=m-1;else l=m+1;}
        else{if(nums[m]&lt;target&amp;&amp;target&lt;=nums[r])l=m+1;else r=m-1;}
    }
    return -1;
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var search = function(nums, target) {
    let l=0,r=nums.length-1;
    while(l<=r){const m=(l+r)>>1;
        if(nums[m]===target) return m;
        if(nums[l]<=nums[m]){if(nums[l]<=target&&target<nums[m])r=m-1;else l=m+1;}
        else{if(nums[m]<target&&target<=nums[r])l=m+1;else r=m-1;}
    }
    return -1;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func search(nums []int, target int) int {
    l,r:=0,len(nums)-1
    for l<=r{m:=(l+r)/2
        if nums[m]==target{return m}
        if nums[l]<=nums[m]{if nums[l]<=target&&target<nums[m]{r=m-1}else{l=m+1}}else{if nums[m]<target&&target<=nums[r]{l=m+1}else{r=m-1}}
    }
    return -1
}"""},
    },
    "insight_title":"One Half is Always Sorted",
    "insight_text":"Even in a rotated array, at least one of [left,mid] or [mid,right] is always non-decreasing. This invariant is what makes binary search still applicable.",
    "tips":[
        "<strong>Draw two cases</strong>: rotation pivot in the left half vs right half. Walk through both.",
        "<strong>Key check:</strong> <code>nums[left] &le; nums[mid]</code> determines which half is sorted.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft, Uber.",
    ]
})

add_problem("q23", {
    "name": "Pacific Atlantic Water Flow",
    "num": 417, "diff": "Medium",
    "topics": ["Graph", "BFS", "DFS"],
    "link": "https://leetcode.com/problems/pacific-atlantic-water-flow",
    "statement": "Given an <code>m x n</code> matrix of non-negative integers representing heights, water can flow to adjacent cells with height &le; current. Find all cells that can flow to <strong>both</strong> the Pacific (top/left edges) and Atlantic (bottom/right edges) oceans.",
    "examples": [
        {"title":"Example 1","input":"heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]","output":"[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]","explain":"These 7 cells have paths to both oceans."},
        {"title":"Example 2","input":"heights = [[1]]","output":"[[0,0]]","explain":"Single cell touches both oceans."},
    ],
    "constraints":["1 &le; m,n &le; 200","0 &le; heights[i][j] &le; 10<sup>5</sup>"],
    "approaches":[
        {"name":"DFS from each cell","time":"O(m&sup2;n&sup2;)","space":"O(mn)","notes":"Too slow for large grids.","cls":""},
        {"name":"Reverse BFS from ocean borders","time":"O(mn)","space":"O(mn)","notes":"BFS inward from each ocean. Intersection = answer. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Reverse Multi-Source BFS","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(mn)","space":"O(mn)",
        "explanation":"Instead of checking if each cell can reach an ocean, reverse the flow: BFS from each ocean's border inward, marking reachable cells. A cell is in the answer only if it's reachable from <em>both</em> BFS traversals."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""from collections import deque

def pacificAtlantic(heights):
    m, n = len(heights), len(heights[0])
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    def bfs(starts):
        visited = set(starts)
        q = deque(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0<=nr<m and 0<=nc<n and (nr,nc) not in visited and heights[nr][nc]>=heights[r][c]:
                    visited.add((nr,nc))
                    q.append((nr,nc))
        return visited

    pacific = [(0,c) for c in range(n)] + [(r,0) for r in range(1,m)]
    atlantic = [(m-1,c) for c in range(n)] + [(r,n-1) for r in range(m-1)]
    return list(bfs(pacific) & bfs(atlantic))"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public List&lt;List&lt;Integer&gt;&gt; pacificAtlantic(int[][] h) {
    int m=h.length,n=h[0].length;
    boolean[][] pac=new boolean[m][n],atl=new boolean[m][n];
    Queue&lt;int[]&gt; pq=new LinkedList&lt;&gt;(),aq=new LinkedList&lt;&gt;();
    for(int r=0;r&lt;m;r++){pq.add(new int[]{r,0});pac[r][0]=true;aq.add(new int[]{r,n-1});atl[r][n-1]=true;}
    for(int c=0;c&lt;n;c++){pq.add(new int[]{0,c});pac[0][c]=true;aq.add(new int[]{m-1,c});atl[m-1][c]=true;}
    bfs(h,pq,pac,m,n);bfs(h,aq,atl,m,n);
    List&lt;List&lt;Integer&gt;&gt; res=new ArrayList&lt;&gt;();
    for(int r=0;r&lt;m;r++) for(int c=0;c&lt;n;c++) if(pac[r][c]&amp;&amp;atl[r][c]) res.add(Arrays.asList(r,c));
    return res;
}
void bfs(int[][] h,Queue&lt;int[]&gt; q,boolean[][] vis,int m,int n){
    int[][]dirs={{0,1},{0,-1},{1,0},{-1,0}};
    while(!q.isEmpty()){int[]cur=q.poll();for(int[]d:dirs){int r=cur[0]+d[0],c=cur[1]+d[1];
        if(r&gt;=0&amp;&amp;r&lt;m&amp;&amp;c&gt;=0&amp;&amp;c&lt;n&amp;&amp;!vis[r][c]&amp;&amp;h[r][c]&gt;=h[cur[0]][cur[1]]){vis[r][c]=true;q.add(new int[]{r,c});}}}
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var pacificAtlantic = function(heights) {
    const [m,n]=[heights.length,heights[0].length];
    const bfs=starts=>{const vis=new Set(starts.map(([r,c])=>r*n+c)),q=[...starts];
        while(q.length){const[r,c]=q.shift();for(const[dr,dc]of[[0,1],[0,-1],[1,0],[-1,0]]){const[nr,nc]=[r+dr,c+dc];
            if(nr>=0&&nr<m&&nc>=0&&nc<n&&!vis.has(nr*n+nc)&&heights[nr][nc]>=heights[r][c]){vis.add(nr*n+nc);q.push([nr,nc]);}}}
        return vis;};
    const pac=bfs([...Array(n).keys()].map(c=>[0,c]).concat([...Array(m).keys()].slice(1).map(r=>[r,0])));
    const atl=bfs([...Array(n).keys()].map(c=>[m-1,c]).concat([...Array(m).keys()].slice(0,m-1).map(r=>[r,n-1])));
    return [...pac].filter(k=>atl.has(k)).map(k=>[Math.floor(k/n),k%n]);
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func pacificAtlantic(heights [][]int) [][]int {
    m,n:=len(heights),len(heights[0]);dirs:=[][2]int{{0,1},{0,-1},{1,0},{-1,0}}
    bfs:=func(starts [][2]int)[][]bool{vis:=make([][]bool,m);for i:=range vis{vis[i]=make([]bool,n)};q:=starts
        for _,s:=range starts{vis[s[0]][s[1]]=true}
        for len(q)>0{cur:=q[0];q=q[1:];for _,d:=range dirs{r,c:=cur[0]+d[0],cur[1]+d[1]
            if r>=0&&r<m&&c>=0&&c<n&&!vis[r][c]&&heights[r][c]>=heights[cur[0]][cur[1]]{vis[r][c]=true;q=append(q,[2]int{r,c})}}}
        return vis}
    pac,atl:=[][2]int{},[][2]int{}
    for r:=0;r<m;r++{pac=append(pac,[2]int{r,0});atl=append(atl,[2]int{r,n-1})}
    for c:=0;c<n;c++{pac=append(pac,[2]int{0,c});atl=append(atl,[2]int{m-1,c})}
    vp,va:=bfs(pac),bfs(atl);res:=[][]int{}
    for r:=0;r<m;r++{for c:=0;c<n;c++{if vp[r][c]&&va[r][c]{res=append(res,[]int{r,c})}}}
    return res
}"""},
    },
    "insight_title":"Reverse the Direction of Flow",
    "insight_text":"Checking flow forward (from cell to ocean) requires O(mn) per cell. Reversing — BFS backwards from ocean → land — naturally follows the &ge; height rule and covers all cells in O(mn) total.",
    "tips":[
        "<strong>Multi-source BFS:</strong> Initialize the queue with all border cells simultaneously.",
        "<strong>Reverse condition:</strong> When flowing backward from ocean to land, move to neighbor only if neighbor height &ge; current height.",
        "<strong>Companies:</strong> Amazon, Google, Uber.",
    ]
})

add_problem("q24", {
    "name": "Combination Sum",
    "num": 39, "diff": "Medium",
    "topics": ["Array", "Backtracking"],
    "link": "https://leetcode.com/problems/combination-sum",
    "statement": "Given an array of distinct integers <code>candidates</code> and a target integer <code>target</code>, return a list of all unique <strong>combinations</strong> of candidates where the chosen numbers sum to target. The same number may be chosen an unlimited number of times.",
    "examples": [
        {"title":"Example 1","input":"candidates=[2,3,6,7], target=7","output":"[[2,2,3],[7]]","explain":"2+2+3=7 and 7=7."},
        {"title":"Example 2","input":"candidates=[2,3,5], target=8","output":"[[2,2,2,2],[2,3,3],[3,5]]","explain":"Three distinct combinations."},
    ],
    "constraints":["1 &le; candidates.length &le; 30","2 &le; candidates[i] &le; 40","All distinct","1 &le; target &le; 40"],
    "approaches":[
        {"name":"Backtracking","time":"O(N^(T/M))","space":"O(T/M)","notes":"N candidates, T target, M min candidate. Standard approach. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Backtracking","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(N^(T/M))","space":"O(T/M)",
        "explanation":"Use DFS: at each step, try adding each candidate (starting from current index to avoid duplicate permutations). If remaining target reaches 0, record the combination. If it goes negative, prune that branch."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""def combinationSum(candidates, target):
    result = []
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(list(current))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                continue
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()
    backtrack(0, [], target)
    return result"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""public List&lt;List&lt;Integer&gt;&gt; combinationSum(int[] c, int target) {
    List&lt;List&lt;Integer&gt;&gt; res=new ArrayList&lt;&gt;();
    backtrack(c,target,0,new ArrayList&lt;&gt;(),res);
    return res;
}
void backtrack(int[] c,int rem,int start,List&lt;Integer&gt; cur,List&lt;List&lt;Integer&gt;&gt; res){
    if(rem==0){res.add(new ArrayList&lt;&gt;(cur));return;}
    for(int i=start;i&lt;c.length;i++){if(c[i]&gt;rem)continue;cur.add(c[i]);backtrack(c,rem-c[i],i,cur,res);cur.remove(cur.size()-1);}
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""var combinationSum = function(candidates, target) {
    const res=[];
    const bt=(start,cur,rem)=>{if(rem===0){res.push([...cur]);return;}
        for(let i=start;i<candidates.length;i++){if(candidates[i]>rem)continue;cur.push(candidates[i]);bt(i,cur,rem-candidates[i]);cur.pop();}};
    bt(0,[],target);return res;
};"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""func combinationSum(candidates []int, target int) [][]int {
    res:=[][]int{}
    var bt func(start,rem int,cur []int)
    bt=func(start,rem int,cur []int){
        if rem==0{res=append(res,append([]int{},cur...));return}
        for i:=start;i<len(candidates);i++{if candidates[i]>rem{continue}
            bt(i,rem-candidates[i],append(cur,candidates[i]))}
    }
    bt(0,target,[]int{});return res
}"""},
    },
    "insight_title":"Start Index Prevents Duplicate Permutations",
    "insight_text":"By passing <code>start=i</code> (not 0) to the recursive call, we allow reusing the current element while preventing using previous elements again. This ensures each combination is generated in non-decreasing order, eliminating duplicates.",
    "tips":[
        "<strong>Explain the start index:</strong> This is the key to avoiding duplicate combinations like [2,3] and [3,2] both being included.",
        "<strong>Sort first (optional):</strong> Sorting candidates lets you break early when a candidate exceeds remaining target.",
        "<strong>Follow-up:</strong> Combination Sum II (cannot reuse) and III (k numbers from 1-9) use the same pattern with minor tweaks.",
        "<strong>Companies:</strong> Amazon, Google, Meta, Microsoft.",
    ]
})

add_problem("q25", {
    "name": "Find Median from Data Stream",
    "num": 295, "diff": "Hard",
    "topics": ["Heap", "Design", "Two Pointers"],
    "link": "https://leetcode.com/problems/find-median-from-data-stream",
    "statement": "Design a data structure that supports adding integers from a stream and finding the median at any time. Implement <code>MedianFinder()</code>, <code>addNum(int num)</code>, and <code>findMedian()</code>.",
    "examples": [
        {"title":"Example 1","input":"addNum(1), addNum(2), findMedian() → 1.5, addNum(3), findMedian() → 2.0","output":"[null, null, 1.5, null, 2.0]","explain":"Median of [1,2] is 1.5; median of [1,2,3] is 2."},
    ],
    "constraints":["−10<sup>5</sup> &le; num &le; 10<sup>5</sup>","At most 5×10<sup>4</sup> calls to addNum and findMedian","At least one element before calling findMedian"],
    "approaches":[
        {"name":"Sorting on each findMedian","time":"O(n log n)","space":"O(n)","notes":"Too slow for repeated calls.","cls":""},
        {"name":"Two Heaps (max-heap + min-heap)","time":"O(log n) add, O(1) median","space":"O(n)","notes":"Left max-heap stores smaller half, right min-heap larger half. Optimal.","cls":"optimal-row"},
    ],
    "optimal_approach":{"title":"Two Heaps","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(log n) / O(1)","space":"O(n)",
        "explanation":"Maintain a max-heap for the lower half and a min-heap for the upper half, balanced so their sizes differ by at most 1. Median = top of the larger heap (if sizes differ) or average of both tops (if equal)."},
    "codes":{
        "python":{"id_prefix":"opt","lang":"python","code":"""import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        # Balance: largest of lo must be <= smallest of hi
        if self.hi and -self.lo[0] > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Keep sizes balanced (lo can be at most 1 larger)
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2"""},
        "java":{"id_prefix":"opt","lang":"java","code":"""class MedianFinder {
    PriorityQueue&lt;Integer&gt; lo=new PriorityQueue&lt;&gt;(Collections.reverseOrder());
    PriorityQueue&lt;Integer&gt; hi=new PriorityQueue&lt;&gt;();
    public void addNum(int num){lo.offer(num);hi.offer(lo.poll());if(lo.size()&lt;hi.size())lo.offer(hi.poll());}
    public double findMedian(){return lo.size()&gt;hi.size()?lo.peek():(lo.peek()+hi.peek())/2.0;}
}"""},
        "javascript":{"id_prefix":"opt","lang":"javascript","code":"""// Note: JS lacks a built-in heap; conceptual implementation
class MedianFinder {
    constructor(){ this.lo=[]; this.hi=[]; }
    addNum(num){
        // push to lo (conceptual max-heap), rebalance
        this.lo.push(num); this.lo.sort((a,b)=>b-a);
        this.hi.push(this.lo.shift()); this.hi.sort((a,b)=>a-b);
        if(this.lo.length < this.hi.length){ this.lo.unshift(this.hi.shift()); }
    }
    findMedian(){
        return this.lo.length > this.hi.length ? this.lo[0] : (this.lo[0]+this.hi[0])/2;
    }
}"""},
        "go":{"id_prefix":"opt","lang":"go","code":"""// Max-heap for lower half
type MaxH []int
func(h MaxH)Len()int{return len(h)};func(h MaxH)Less(i,j int)bool{return h[i]>h[j]}
func(h MaxH)Swap(i,j int){h[i],h[j]=h[j],h[i]}
func(h *MaxH)Push(x interface{}){*h=append(*h,x.(int))}
func(h *MaxH)Pop()interface{}{o:=*h;v:=o[len(o)-1];*h=o[:len(o)-1];return v}

type MinH []int
func(h MinH)Len()int{return len(h)};func(h MinH)Less(i,j int)bool{return h[i]<h[j]}
func(h MinH)Swap(i,j int){h[i],h[j]=h[j],h[i]}
func(h *MinH)Push(x interface{}){*h=append(*h,x.(int))}
func(h *MinH)Pop()interface{}{o:=*h;v:=o[len(o)-1];*h=o[:len(o)-1];return v}

type MedianFinder struct{lo MaxH;hi MinH}
func(mf *MedianFinder)AddNum(num int){heap.Push(&mf.lo,num);heap.Push(&mf.hi,heap.Pop(&mf.lo));if mf.lo.Len()<mf.hi.Len(){heap.Push(&mf.lo,heap.Pop(&mf.hi))}}
func(mf *MedianFinder)FindMedian()float64{if mf.lo.Len()>mf.hi.Len(){return float64(mf.lo[0])};return float64(mf.lo[0]+mf.hi[0])/2}"""},
    },
    "insight_title":"Two Heaps Split the Data at the Median",
    "insight_text":"The max-heap stores the smaller half (its root = the lower median), the min-heap stores the larger half (its root = the upper median). After each insertion, we maintain the invariant that |lo| - |hi| &le; 1.",
    "tips":[
        "<strong>Draw the invariant:</strong> lo.top &le; hi.top always, and |lo| - |hi| &le; 1.",
        "<strong>Python trick:</strong> Negate values to simulate a max-heap with heapq (which is min-heap by default).",
        "<strong>Time complexity:</strong> addNum is O(log n); findMedian is O(1).",
        "<strong>Companies:</strong> Google, Amazon, Apple, LinkedIn — common for senior roles.",
    ]
})
