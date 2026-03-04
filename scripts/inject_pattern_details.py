import re
import os

HTML_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pages", "12-coding-interview-patterns.html")

DATA = {
    "1": {
        "title": "Sliding Window",
        "mental_model": "Maintain a moving window of valid elements. The right pointer expands the window to explore new elements, while the left pointer shrinks it when the window becomes invalid.",
        "mistakes": "<ul><li>Forgetting to shrink the window completely when invalid.</li><li>Updating the global maximum/minimum state at the wrong time (before vs after shrinking).</li></ul>",
        "walkthrough": "<h4>Walkthrough: Longest Substring Without Repeating</h4><pre>Input: 'abcabcbb'\nStep 1: window='a', max=1\nStep 2: window='ab', max=2\nStep 3: window='abc', max=3\nStep 4: hit 'a', window becomes 'bca', max=3</pre>"
    },
    "2": {
        "title": "Two Pointers",
        "mental_model": "Exploit sorted order or symmetric properties to eliminate large portions of the search space instantly. Bring two pointers towards each other based on comparison.",
        "mistakes": "<ul><li>Not ensuring the array is strictly sorted first.</li><li>Crossing boundaries (`left > right`) incorrectly causing out-of-bounds index errors.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Two Sum II (Sorted)</h4><pre>Input: [2, 7, 11, 15], Target = 9\nL=2, R=15 -> Sum 17 (Too big, shrink R)\nL=2, R=11 -> Sum 13 (Too big, shrink R)\nL=2, R=7 -> Sum 9 (Match found!)</pre>"
    },
    "3": {
        "title": "Fast & Slow Pointers",
        "mental_model": "Use two pointers moving at different speeds to detect cycles or find fractional properties (like the exact middle) of a linked list or sequence without extra memory.",
        "mistakes": "<ul><li>Null pointer exceptions (checking `fast.next.next` when `fast.next` is null).</li><li>Failing to reset one pointer to the head to find the cycle start exactly.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Linked List Middle</h4><pre>List: 1 -> 2 -> 3 -> 4 -> 5\nStep 1: S=1, F=1\nStep 2: S=2, F=3\nStep 3: S=3, F=5 (F has nowhere to double-jump, S is the middle)</pre>"
    },
    "4": {
        "title": "Merge Intervals",
        "mental_model": "Sort elements by their start time. Then, sequentially combine overlapping ranges by updating the end time of the current range to the maximum of the overlapping ends.",
        "mistakes": "<ul><li>Forgetting to sort the array first (Critical!).</li><li>Only updating the end time instead of taking `max(current_end, next_end)`.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Merge Intervals</h4><pre>Input: [[1,3], [2,6], [8,10]]\nSort: [[1,3], [2,6], [8,10]]\nMerge [1,3] & [2,6] -> overlap! New: [1, max(3,6)] -> [1,6]\nNext [8,10] -> no overlap. Final: [[1,6], [8,10]]</pre>"
    },
    "5": {
        "title": "Cyclic Sort",
        "mental_model": "When an array contains numbers in a given range (e.g., 1 to N), each number belongs at exactly `index = value - 1`. Swap elements until they land accurately in their place.",
        "mistakes": "<ul><li>Infinite loops caused by returning the number to the same wrong index.</li><li>Out of bounds errors when the number is <= 0 or > N.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Missing Number</h4><pre>Input: [3, 0, 1] (Range 0 to 3, N=3)\nIndex 0 starts with 3. 3 is out of bounds (N). Ignore or place at end.\nSwap 0 -> 0 belongs at index 0. [0, 3, 1]\nMissing index 2 has value 1 -> swap! Final: [0, 1, 3]. Missing is 2.</pre>"
    },
    "6": {
        "title": "In-place Reversal",
        "mental_model": "To reverse a linked list node-by-node without O(N) space memory, carefully juggle three pointers: `prev`, `current`, and `next`.",
        "mistakes": "<ul><li>Losing the rest of the list because you overwrote `current.next` before saving it.</li><li>Returning `head` instead of `prev` as the new starting point.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Reverse List</h4><pre>List: 1 -> 2 -> 3\nStart: prev=null, curr=1\nCurr.next points to prev (null). prev moves to 1, curr moves to 2.\nNext: curr(2).next points to prev(1). prev moves to 2.\nFinished: prev=3 -> 2 -> 1</pre>"
    },
    "7": {
        "title": "Tree BFS",
        "mental_model": "Use a Queue to process a tree horizontally. Everything currently in the queue represents exactly one level horizontally in the tree.",
        "mistakes": "<ul><li>Forgetting to capture the current queue length before the inner for-loop, causing level-mixing.</li><li>Enqueuing null children.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Tree Level Order</h4><pre>Tree: Root 1, Children 2 & 3\nQ = [1]\nPop 1. Add 2, 3. Level=[1]. Q=[2, 3]\nPop 2, Pop 3. Add their children. Level=[2, 3].</pre>"
    },
    "8": {
        "title": "Tree DFS",
        "mental_model": "Dive as deep as possible down one branch using Recursion or a Stack. Bubble up boolean results or accumulated paths from the leaf nodes back to the root.",
        "mistakes": "<ul><li>Passing mutable reference types (lists/arrays) into the recursive function without making independent copies.</li><li>Missing the base-case (`if not node: return`).</li></ul>",
        "walkthrough": "<h4>Walkthrough: Root to Leaf Path Sum</h4><pre>Tree: 1 -> 2, sum=3\nStart at 1: sum=3-1=2. Go left to 2.\nAt 2: sum=2-2=0. It's a leaf and sum=0! Return True.</pre>"
    },
    "9": {
        "title": "Two Heaps",
        "mental_model": "Split a stream of numbers into two halves: a Max-Heap for the smaller half and a Min-Heap for the larger half. The medians/extremes are always at the top.",
        "mistakes": "<ul><li>Failing to rebalance the heaps when their size difference exceeds 1.</li><li>Inserting into the wrong heap simply based on size instead of comparing against the tops of the heaps.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Find Median</h4><pre>Insert 5: MaxHeap=[5], MinHeap=[] -> Median: 5\nInsert 10: MaxHeap=[5], MinHeap=[10] -> Median: (5+10)/2 = 7.5\nInsert 1: MaxHeap=[5, 1], MinHeap=[10] -> Median: 5</pre>"
    },
    "10": {
        "title": "Subsets",
        "mental_model": "Build solutions incrementally element by element. Use recursion to thoroughly branch out taking both options: 'Include This Element' and 'Skip This Element'.",
        "mistakes": "<ul><li>Appending the actual list reference to results, mutating it later (instead of appending a deep copy `path[:]`).</li><li>Not sorting the array first when dealing with duplicates.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Subsets</h4><pre>Input: [1, 2]\nStart: []\nAdd 1: [1]\nFrom [1] Add 2: [1, 2]\nBacktrack to []: Add 2: [2]\nResult: [], [1], [1, 2], [2]</pre>"
    },
    "11": {
        "title": "Modified Binary Search",
        "mental_model": "For any monotonically ordered space (even if slightly rotated), cut the search space in half logarithmically by asking a True/False question about the midpoint.",
        "mistakes": "<ul><li>Over-calculating mid (`(L+R)//2`) leading to integer overflow vs `L + (R-L)//2`.</li><li>Off-by-one errors when setting `left = mid` vs `left = mid + 1`.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Rotated Array Search</h4><pre>Array: [4, 5, 6, 7, 0, 1, 2] Target: 0\nMid is 7. Left side [4..7] is sorted uniformly. 0 is not in it.\nTherefore search Right space! L=mid+1.</pre>"
    },
    "12": {
        "title": "Top 'K' Elements",
        "mental_model": "Maintain exactly K elements in a Min-Heap. Whenever you see a number larger than the heap's minimum, pop the minimum and push the new number.",
        "mistakes": "<ul><li>Using a Max-Heap instead of a Min-Heap for Top K Largest elements (a common counter-intuitive blunder).</li><li>Pushing elements before checking the heap's size.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Top 2 Largest</h4><pre>Input: [3, 1, 5, 12, 2, 11], K=2\nHeap up to K: [1, 3]\nSee 5 (5>1): Pop 1, Push 5. Heap: [3, 5]\nSee 12 (12>3): Pop 3, Push 12. Heap: [5, 12]\nFinal top 2: 5 and 12.</pre>"
    },
    "13": {
        "title": "K-way Merge",
        "mental_model": "Push the very first element of each of the K sorted lists into a Min-Heap. Pop the global minimum, and push the next element from exactly the list that the minimum came from.",
        "mistakes": "<ul><li>Not storing a reference to the array/list index inside the heap node so you don't know where to pull the next item from.</li><li>Extracting from exhausted lists.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Merge 3 Sorted Arrays</h4><pre>A1=[1, 4], A2=[2, 5], A3=[3, 6]\nHeap inserts firsts: [1, 2, 3]\nPop 1 (from A1). Insert next from A1 (which is 4). Heap: [2, 3, 4]\nPop 2 (from A2). Insert next from A2 (5)...</pre>"
    },
    "14": {
        "title": "Topological Sort",
        "mental_model": "Count the number of incoming edges (indegrees) to all nodes. Start a BFS strictly from nodes that have 0 incoming dependencies. As they execute, free up their neighbors.",
        "mistakes": "<ul><li>Failing to check if the final sorted array length matches the total number of vertices (to detect cycles!).</li><li>Mixing up directed edge direction `A->B` vs `B->A`.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Course Schedule</h4><pre>Need A to take B. B to take C.\nIndegrees: A:0, B:1, C:1\nQueue gets [A]. Pop A.\nA allows B. B indegree goes to 0! Add B to Queue.\nPop B. C indegree goes to 0... Sort: A, B, C.</pre>"
    },
    "15": {
        "title": "Prefix Sum",
        "mental_model": "Pre-calculate a running total of the array. The sum of any sub-array from index i to j is instantly `PrefixSum[j] - PrefixSum[i-1]` in O(1) time.",
        "mistakes": "<ul><li>Forgetting to initialize the Prefix array with a default initial value of 0 to handle sums starting from the 0th index.</li><li>Using a nested loop when a Hash Map tracking previous prefix sums is required.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Range Sum</h4><pre>Input: [2, 4, 6, 8]\nPrefix arrays: [0, 2, 6, 12, 20]\nSum from index 1 to 2 (4+6 = 10)\nPrefix calculation: Prefix[3] - Prefix[1] = 12 - 2 = 10.</pre>"
    },
    "16": {
        "title": "Monotonic Stack",
        "mental_model": "Keep a stack strictly sorted (e.g. decreasing). If a new element breaks the monotonic order, iteratively pop the stack until the rule is satisfied.",
        "mistakes": "<ul><li>Storing values instead of indices in the stack, making it impossible to calculate the positional distance (like in Daily Temperatures).</li><li>Popping the wrong direction (>< vs <).</li></ul>",
        "walkthrough": "<h4>Walkthrough: Next Greater Element</h4><pre>Input: [2, 1, 5]\nStack=[], Push 2.\nSee 1. 1 < 2, monotonic order kept. Push 1. Stack=[2, 1]\nSee 5. 5 > 1! Break! Pop 1 (Next greater for 1 is 5). 5 > 2! Break! Pop 2 (Next greater for 2 is 5).\nPush 5. Stack=[5].</pre>"
    },
    "17": {
        "title": "Union Find",
        "mental_model": "Group interconnected items into distinct network sets. To check if two items are naturally connected, check if their absolute 'root' parents are identical.",
        "mistakes": "<ul><li>Not implementing Path Compression or Union By Rank, causing the tree to degenerate to O(N) linear time lookups.</li><li>Initializing the parents array to incorrect generic zeros instead of `parent[i] = i`.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Connected Components</h4><pre>Edges: A-B, C-D.\nSets: [A,B], [C,D]\nNew Edge B-C introduced.\nFind root of B (is A). Find root of C (is C).\nUnion them: Make C point to A. Now [A, B, C, D] is one giant set.</pre>"
    },
    "18": {
        "title": "Dynamic Programming",
        "mental_model": "Recursively solve smaller sub-problems. Realize that many sub-problems are identical. Cache the result of identical subproblems in an array/matrix so you never compute them twice.",
        "mistakes": "<ul><li>Attempting a bottom-up 2D Matrix DP before properly writing out the Top-Down recursive transition equation.</li><li>Off-by-one errors when sizing the `dp` array.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Fibonacci</h4><pre>Fib(4) = Fib(3) + Fib(2)\nFib(3) = Fib(2) + Fib(1)\nNotice Fib(2) is calculated twice? Cache it the first time!\nDP[2] = 1. The second time, just return DP[2] instantly.</pre>"
    },
    "19": {
        "title": "Greedy",
        "mental_model": "In some problems, making the absolute best short-term choice at every single step miraculously leads to the mathematically optimal long-term result, bypassing complex DP.",
        "mistakes": "<ul><li>Applying Greedy to problems that actually require DP (like the standard Coin Change problem with non-standard denominations).</li><li>Forgetting to sort the input array before executing the greedy pass.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Jump Game</h4><pre>Array: [2, 3, 1, 1, 4]\nGreedy strategy: Track furthest absolute index we can reach.\nAt idx 0 (val 2), furthest is max(0, 0+2) = 2.\nAt idx 1 (val 3), furthest is max(2, 1+3) = 4.\nSince furthest >= last index, return True.</pre>"
    },
    "20": {
        "title": "Bit Manipulation",
        "mental_model": "Use boolean algebraic operations at the hardware bit level to toggle numbers, mask flags, or isolate specific properties (like XORing a number by itself zeroes it out).",
        "mistakes": "<ul><li>Confusion with operator precedence (e.g. `n & 1 == 0` evaluates as `n & (1 == 0)` in some languages, always use brackets `(n & 1) == 0`).</li><li>Negative number two's complement behavior shifting infinitely.</li></ul>",
        "walkthrough": "<h4>Walkthrough: Find Single Number</h4><pre>Input: [2, 1, 2]\nA XOR A = 0. A XOR 0 = A.\n2 XOR 1 = 3.\n3 XOR 2 = 1. (The two 2's cancelled each other perfectly to 0!)\nResult is 1.</pre>"
    }
}

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# We will look for <div class="pattern-section" id="p1">
# and find the end of its <div class="pattern-header">...</div><p>...</p> block.
for pid, info in DATA.items():
    section_start = f'id="p{pid}"'
    if section_start not in html:
        print(f"Skipping p{pid}")
        continue
    
    # regex to find where to put the mental model.
    # We want to put it right after the first <p> that follows the .pattern-header
    # Wait, let's just insert it right after <div class="signal-box"> ... </div>
    # Actually, let's insert Mental Model right before <div class="signal-box">
    
    # 1. Inject Mental Model
    mental_model_html = f'''
                            <div class="callout concept" style="background:#eef2ff; border-left:4px solid #6366f1; padding: 16px; margin-top: 24px; margin-bottom: 24px; border-radius: 4px;">
                                <h4 style="margin-top:0; color:#4338ca; font-size:1.05rem;">🧠 Mental Model</h4>
                                <p style="margin-bottom:0; color:#312e81;">{info["mental_model"]}</p>
                            </div>'''
    
    # Find the signal-box for this pattern to insert the mental model right before it.
    regex_signal = re.compile(rf'(<div class="pattern-section" id="p{pid}">.*?)(<div class="signal-box">)', re.DOTALL)
    
    if "🧠 Mental Model" not in html: # Prevent duplicate additions
        html = regex_signal.sub(rf'\1{mental_model_html}\n                            \2', html, count=1)
    
    # 2. Inject Walkthrough and Mistakes at the VERY END of this pattern block
    # A pattern block ends with </div> just before the next 
    # <!-- Pattern X --> or <!-- Blind 75 Mapping -->
    
    append_html = f'''
                            <div style="background:#f8fafc; padding: 16px; border-radius:8px; margin-top: 30px; margin-bottom: 20px; border:1px solid #e2e8f0;">
                                {info["walkthrough"]}
                            </div>
                            <div class="callout warning" style="background:#fef2f2; border-left:4px solid #ef4444; padding: 16px; margin-bottom: 30px; border-radius: 4px;">
                                <h4 style="margin-top:0; color:#b91c1c; font-size:1.05rem;">⚠️ Common Interview Mistakes</h4>
                                <div style="color:#7f1d1d; margin-bottom:0;">{info["mistakes"]}</div>
                            </div>
                        </div><!-- end of individual pattern {pid} -->'''
    
    # We capture from <div class="pattern-section" id="p{pid}"> up until the very final </div> of that block.
    # To do this safely, we can replace the last </div> before the NEXT pattern section starts.
    # Since we can't easily parse nested divs with regex, we can match the start of the NEXT block!
    next_pid = str(int(pid) + 1)
    if int(pid) < 20:
        next_tag = f'                        <!-- Pattern {next_pid}'
    else:
        next_tag = f'                <!-- Blind 75 Mapping -->'
        
    # Replace the `</div>\n\n  next_tag` with `append_html \n\n next_tag`
    # We find the specific occurrence of `</div>\n                <!-- Pattern X`
    # We'll use a regex that matches from the id="pX" to the next tag.
    
    regex_block = re.compile(rf'(<div class="pattern-section" id="p{pid}">.*?)(</div>\s+){next_tag}', re.DOTALL)
    
    if "⚠️ Common Interview Mistakes" not in html[html.find(f'id="p{pid}"'):html.find(next_tag)]:
        # Note: the group(1) includes the entire content from p1 to the last element. The last element is a </div>
        html = regex_block.sub(rf'\1{append_html}\n\n{next_tag}', html, count=1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully injected all 20 patterns with the new parsing logic.")
