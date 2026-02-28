import re
import sys

html_file = "blind75-spa.html"

# Define the exact 75 questions distributed into 15 Blind 75 categories
categories = {
    "Arrays & Hashing": [
        "Contains Duplicate",
        "Valid Anagram",
        "Two Sum",
        "Group Anagrams",
        "Top K Frequent Elements",
        "Product of Array Except Self",
        "Encode and Decode Strings",
        "Longest Consecutive Sequence"
    ],
    "Two Pointers": [
        "Valid Palindrome",
        "3Sum",
        "Container With Most Water"
    ],
    "Sliding Window": [
        "Best Time to Buy and Sell Stock",
        "Longest Substring Without Repeating Characters",
        "Longest Repeating Character Replacement",
        "Minimum Window Substring"
    ],
    "Stack": [
        "Valid Parentheses"
    ],
    "Binary Search": [
        "Find Minimum in Rotated Sorted Array",
        "Search in Rotated Sorted Array"
    ],
    "Linked List": [
        "Reverse Linked List",
        "Merge Two Sorted Lists",
        "Reorder List",
        "Remove Nth Node From End of List",
        "Linked List Cycle",
        "Merge k Sorted Lists"
    ],
    "Trees": [
        "Invert Binary Tree",
        "Maximum Depth of Binary Tree",
        "Same Tree",
        "Subtree of Another Tree",
        "Lowest Common Ancestor of a BST",
        "Binary Tree Level Order Traversal",
        "Validate Binary Search Tree",
        "Kth Smallest Element in a BST",
        "Construct Binary Tree from Preorder and Inorder Traversal",
        "Binary Tree Maximum Path Sum",
        "Serialize and Deserialize Binary Tree"
    ],
    "Tries": [
        "Implement Trie (Prefix Tree)",
        "Design Add and Search Words Data Structure",
        "Word Search II"
    ],
    "Heap / Priority Queue": [
        "Find Median from Data Stream"
    ],
    "Backtracking": [
        "Combination Sum",
        "Word Search"
    ],
    "Graphs": [
        "Number of Islands",
        "Clone Graph",
        "Pacific Atlantic Water Flow",
        "Course Schedule",
        "Number of Connected Components in an Undirected Graph",
        "Graph Valid Tree",
        "Alien Dictionary"
    ],
    "1-D Dynamic Programming": [
        "Climbing Stairs",
        "House Robber",
        "House Robber II",
        "Longest Palindromic Substring",
        "Palindromic Substrings",
        "Decode Ways",
        "Coin Change",
        "Maximum Product Subarray",
        "Word Break",
        "Longest Increasing Subsequence"
    ],
    "2-D Dynamic Programming": [
        "Unique Paths",
        "Longest Common Subsequence"
    ],
    "Greedy": [
        "Maximum Subarray",
        "Jump Game"
    ],
    "Intervals": [
        "Insert Interval",
        "Merge Intervals",
        "Non-overlapping Intervals",
        "Meeting Rooms",
        "Meeting Rooms II"
    ],
    "Math & Geometry": [
        "Rotate Image",
        "Spiral Matrix",
        "Set Matrix Zeroes"
    ],
    "Bit Manipulation": [
        "Number of 1 Bits",
        "Counting Bits",
        "Reverse Bits",
        "Missing Number",
        "Sum of Two Integers"
    ]
}

try:
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found.")
    sys.exit(1)

# 1. Isolate the sidebar list
start_marker = '<div class="sidebar-scroll" id="sidebar-list">'
end_marker = '<div class="progress-footer">'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find sidebar boundaries.")
    sys.exit(1)

# Ensure we get the correct closing div before MAIN CONTENT
sidebar_html = content[start_idx:end_idx]

# 2. Extract every single q-item accurately
q_item_pattern = re.compile(r'(<div class="q-item".*?</div>)', re.DOTALL)
q_items = q_item_pattern.findall(sidebar_html)

# Extract name mapping
item_map = {}
name_pattern = re.compile(r'<span class="q-name">(.*?)</span>')

for item in q_items:
    match = name_pattern.search(item)
    if match:
        name = match.group(1).strip()
        item_map[name] = item

# 3. Build new categorized html
new_sidebar = start_marker + '\n'

mapped_count = 0
first_module = True

for category, names in categories.items():
    expanded_class = " expanded" if first_module else ""
    cat_block = f'    <div class="nav-module{expanded_class}">\n'
    cat_block += f'        <div class="nav-module-title">{category}</div>\n'
    
    for name in names:
        if name in item_map:
            # indent appropriately
            indented_item = item_map[name].replace('<div class="q-item"', '        <div class="q-item"')
            cat_block += indented_item + '\n'
            mapped_count += 1
        else:
            print(f"Missing mapping for: {name}")
            
    cat_block += '    </div>\n'
    new_sidebar += cat_block
    first_module = False

# Make sure we close the sidebar-scroll div
new_sidebar += '</div>\n\n'

print(f"Successfully mapped {mapped_count} items out of {len(q_items)}")

if mapped_count > 0:
    # 4. Replace in original content
    new_content = content[:start_idx] + new_sidebar + content[end_idx:]
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Wrote categorized sidebar to blind75-spa.html")
