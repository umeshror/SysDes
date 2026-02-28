        """Batch 6: q31-q50 — Intervals, Dynamic Programming, Trees, Backtracking, Binary Search"""
from shared_generator import add_problem

problems_data = [
    ("q31", 435, "Non-overlapping Intervals", "Medium", ["Array","Greedy"],
     "https://leetcode.com/problems/non-overlapping-intervals",
     "Given an array of intervals, return the minimum number of intervals you need to remove to make the rest non-overlapping.",
     [{"title":"Example 1","input":"intervals = [[1,2],[2,3],[3,4],[1,3]]","output":"1","explain":"Remove [1,3] to make the rest non-overlapping."},
      {"title":"Example 2","input":"intervals = [[1,2],[1,2],[1,2]]","output":"2","explain":"Remove two [1,2] intervals."}],
     ["1 &le; intervals.length &le; 10<sup>5</sup>","intervals[i].length == 2","-5*10<sup>4</sup> &le; start &lt; end &le; 5*10<sup>4</sup>"],
     [{"name":"Greedy — sort by end","time":"O(n log n)","space":"O(1)","notes":"Sort by end time, greedily keep non-overlapping. Optimal.","cls":"optimal-row"}],
     {"title":"Greedy — Sort by End Time","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n log n)","space":"O(1)",
      "explanation":"Sort intervals by end time. Greedily keep each interval if it doesn't overlap with the last kept one. Count how many need to be removed."},
     """def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])
    count = 0
    end = float('-inf')
    for s, e in intervals:
        if s >= end:
            end = e    # keep this interval
        else:
            count += 1 # remove it (overlap)
    return count""",
     "Sort by End Time to Maximize Kept Intervals",
     "Sorting by end time gives the earliest possible end for each kept interval, maximizing room for future intervals — classic interval scheduling.",
     ["<strong>Classic greedy pattern:</strong> Sort by end time for interval scheduling problems.",
      "<strong>Follow-up:</strong> 'Minimum number of arrows to burst balloons' (LeetCode 452) uses the same pattern.",
      "<strong>Companies:</strong> Google, Amazon, Bloomberg."]),

    ("q32", 53, "Maximum Subarray", "Medium", ["Array","DP","Divide and Conquer"],
     "https://leetcode.com/problems/maximum-subarray",
     "Given an integer array <code>nums</code>, find the contiguous subarray with the largest sum, and return its sum.",
     [{"title":"Example 1","input":"nums = [-2,1,-3,4,-1,2,1,-5,4]","output":"6","explain":"Subarray [4,-1,2,1] has the largest sum = 6."},
      {"title":"Example 2","input":"nums = [1]","output":"1","explain":"Single element."},
      {"title":"Example 3","input":"nums = [5,4,-1,7,8]","output":"23","explain":"Entire array."}],
     ["1 &le; nums.length &le; 10<sup>5</sup>","-10<sup>4</sup> &le; nums[i] &le; 10<sup>4</sup>"],
     [{"name":"Kadane's Algorithm","time":"O(n)","space":"O(1)","notes":"Track current and global max. Optimal.","cls":"optimal-row"}],
     {"title":"Kadane's Algorithm","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
      "explanation":"At each index, either extend the current subarray or start a new one. <code>cur_max = max(num, cur_max + num)</code>. Update global max each step."},
     """def maxSubArray(nums):
    cur_max = global_max = nums[0]
    for n in nums[1:]:
        cur_max = max(n, cur_max + n)
        global_max = max(global_max, cur_max)
    return global_max""",
     "Reset When cur_max Goes Negative",
     "If cur_max drops below 0, starting fresh at the next element is always better — a negative prefix only hurts the total.",
     ["<strong>Know Kadane's by heart</strong> — this is a foundational DP problem every engineer should know.",
      "<strong>If all negative:</strong> The answer is the maximum single element (Kadane's handles this correctly).",
      "<strong>Companies:</strong> Amazon, Google, Apple, Meta — very commonly asked."]),

    ("q34", 55, "Jump Game", "Medium", ["Array","Greedy"],
     "https://leetcode.com/problems/jump-game",
     "Given an integer array <code>nums</code> where <code>nums[i]</code> is the maximum jump length at position <code>i</code>, return <code>true</code> if you can reach the last index.",
     [{"title":"Example 1","input":"nums = [2,3,1,1,4]","output":"true","explain":"Jump 1 to index 1, then 3 to last."},
      {"title":"Example 2","input":"nums = [3,2,1,0,4]","output":"false","explain":"Always land on index 3 with max jump 0."}],
     ["1 &le; nums.length &le; 10<sup>4</sup>","0 &le; nums[i] &le; 10<sup>5</sup>"],
     [{"name":"Greedy — track max reach","time":"O(n)","space":"O(1)","notes":"Track furthest reachable index. Optimal.","cls":"optimal-row"}],
     {"title":"Greedy — Max Reach","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(1)",
      "explanation":"Track the maximum index reachable so far (<code>max_reach</code>). For each index, if <code>i &gt; max_reach</code>, we're stuck. Otherwise update <code>max_reach = max(max_reach, i + nums[i])</code>."},
     """def canJump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True""",
     "Greedy Max Reach is Always Correct",
     "If we can reach position i, we can always use nums[i] to potentially extend our reach. The greedy choice — always maximizing reachable index — never causes us to miss a valid path.",
     ["<strong>Greedy over DP here:</strong> No need for O(n²) DP since the greedy proof is straightforward.",
      "<strong>Follow-up:</strong> Jump Game II (minimum jumps) uses a similar greedy approach.",
      "<strong>Companies:</strong> Amazon, Google, Microsoft."]),

    ("q35", 56, "Merge Intervals", "Medium", ["Array","Sorting"],
     "https://leetcode.com/problems/merge-intervals",
     "Given an array of intervals, merge all overlapping intervals and return an array of the non-overlapping intervals.",
     [{"title":"Example 1","input":"intervals = [[1,3],[2,6],[8,10],[15,18]]","output":"[[1,6],[8,10],[15,18]]","explain":"[1,3] and [2,6] overlap; merge to [1,6]."},
      {"title":"Example 2","input":"intervals = [[1,4],[4,5]]","output":"[[1,5]]","explain":"Touching intervals are merged."}],
     ["1 &le; intervals.length &le; 10<sup>4</sup>","intervals[i].length == 2","0 &le; start &le; end &le; 10<sup>4</sup>"],
     [{"name":"Sort + Linear Scan","time":"O(n log n)","space":"O(n)","notes":"Sort by start, merge overlapping. Optimal.","cls":"optimal-row"}],
     {"title":"Sort by Start + Linear Merge","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n log n)","space":"O(n)",
      "explanation":"Sort by start time. For each interval, if it overlaps the last result interval (start &le; prev_end), extend. Otherwise append."},
     """def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged""",
     "After Sorting, One Pass Suffices",
     "Sorting guarantees that any overlapping interval follows the one it overlaps. A single linear scan then handles all merges correctly.",
     ["<strong>Overlap condition:</strong> interval.start &le; prev.end (the new one starts before the old one ends).",
      "<strong>Companies:</strong> Google, Facebook, LinkedIn, Amazon."]),

    ("q36", 57, "Insert Interval", "Medium", ["Array"],
     "https://leetcode.com/problems/insert-interval",
     "Given an array of non-overlapping intervals sorted by start time, insert a new interval and merge if necessary. Return the new array of intervals.",
     [{"title":"Example 1","input":"intervals=[[1,3],[6,9]], newInterval=[2,5]","output":"[[1,5],[6,9]]","explain":"[2,5] overlaps [1,3]; merge to [1,5]."},
      {"title":"Example 2","input":"intervals=[[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval=[4,8]","output":"[[1,2],[3,10],[12,16]]","explain":"[4,8] overlaps [3,5],[6,7],[8,10]."}],
     ["0 &le; intervals.length &le; 10<sup>4</sup>","Intervals are non-overlapping and sorted"],
     [{"name":"Three-pass Linear","time":"O(n)","space":"O(n)","notes":"Add before, merge overlap, add after. Optimal.","cls":"optimal-row"}],
     {"title":"Three-Phase Pass","badge_cls":"badge-optimal","badge_text":"Optimal","time":"O(n)","space":"O(n)",
      "explanation":"Phase 1: Add all intervals that end before newInterval starts. Phase 2: Merge all overlapping intervals with newInterval. Phase 3: Add all remaining intervals."},
     """def insert(intervals, newInterval):
    result = []
    i, n = 0, len(intervals)
    # Phase 1: before
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i]); i += 1
    # Phase 2: merge
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    # Phase 3: after
    result.extend(intervals[i:])
    return result""",
     "Three Clear Phases Map to Three Conditions",
     "Any existing interval is in exactly one of three states relative to newInterval: entirely before, overlapping, or entirely after. Processing each phase separately keeps the logic clean and O(n).",
     ["<strong>No sorting needed:</strong> Input is already sorted and non-overlapping — we can do a single O(n) pass.",
      "<strong>Companies:</strong> Google, Facebook, Amazon."]),
]

def _make_simple_codes(py_code, problem_name):
    """Generate simple Java/JS/Go stubs pointing to Python for complex problems."""
    return {
        "python": {"id_prefix":"opt","lang":"python","code":py_code},
        "java": {"id_prefix":"opt","lang":"java","code":f"// See Python solution for full logic\n// {problem_name} — Java: implement same algorithm"},
        "javascript": {"id_prefix":"opt","lang":"javascript","code":f"// See Python solution for full logic\n// {problem_name} — JavaScript: implement same algorithm"},
        "go": {"id_prefix":"opt","lang":"go","code":f"// See Python solution for full logic\n// {problem_name} — Go: implement same algorithm"},
    }

for (q_id, num, name, diff, topics, link, stmt, examples, constraints, approaches, opt, py_code, insight_title, insight_text, tips) in problems_data:
    add_problem(q_id, {
        "name": name, "num": num, "diff": diff, "topics": topics, "link": link,
        "statement": stmt, "examples": examples, "constraints": constraints,
        "approaches": approaches, "optimal_approach": opt,
        "codes": _make_simple_codes(py_code, name),
        "insight_title": insight_title, "insight_text": insight_text, "tips": tips,
    })
