import json, os, re

try:
    with open('items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)["items"]
except Exception as e:
    print("Failed reading items.json", e)
    import sys
    sys.exit(1)

categories = [
    {
        "name": "Arrays & Hashing",
        "keywords": ["Contains Duplicate", "Valid Anagram", "Two Sum", "Group Anagrams", "Top K Frequent Elements", "Product of Array", "Encode and Decode Strings", "Longest Consecutive Sequence"]
    },
    {
        "name": "Two Pointers",
        "keywords": ["Valid Palindrome", "3Sum", "Container With Most Water"]
    },
    {
        "name": "Sliding Window",
        "keywords": ["Best Time to Buy and Sell Stock", "Longest Substring Without Repeating", "Longest Repeating Character Replacement", "Minimum Window Substring"]
    },
    {
        "name": "Stack",
        "keywords": ["Valid Parentheses"]
    },
    {
        "name": "Binary Search",
        "keywords": ["Find Minimum in Rotated Sorted Array", "Search in Rotated Sorted"]
    },
    {
        "name": "Linked List",
        "keywords": ["Reverse Linked List", "Merge Two Sorted Lists", "Reorder List", "Remove Nth Node", "Linked List Cycle", "Merge k Sorted Lists"]
    },
    {
        "name": "Trees",
        "keywords": ["Invert Binary Tree", "Maximum Depth of Binary Tree", "Same Tree", "Subtree of Another Tree", "Lowest Common Ancestor of a BST", "Binary Tree Level Order Traversal", "Validate Binary Search Tree", "Kth Smallest Element in a BST", "Construct Binary Tree", "Binary Tree Maximum Path Sum", "Serialize and Deserialize Binary Tree"]
    },
    {
        "name": "Tries",
        "keywords": ["Implement Trie", "Search Words Data Structure", "Word Search II"]
    },
    {
        "name": "Heap / Priority Queue",
        "keywords": ["Find Median from Data Stream"]
    },
    {
        "name": "Backtracking",
        "keywords": ["Combination Sum", "Word Search"]
    },
    {
        "name": "Graphs",
        "keywords": ["Number of Islands", "Clone Graph", "Pacific Atlantic Water", "Course Schedule", "Number of Connected Components", "Graph Valid Tree", "Alien Dictionary"]
    },
    {
        "name": "1-D Dynamic Programming",
        "keywords": ["Climbing Stairs", "House Robber", "House Robber II", "Longest Palindromic", "Palindromic Substrings", "Decode Ways", "Coin Change", "Maximum Product Subarray", "Word Break", "Longest Increasing Subsequence"]
    },
    {
        "name": "2-D Dynamic Programming",
        "keywords": ["Unique Paths", "Longest Common Subsequence"]
    },
    {
        "name": "Math & Geometry",
        "keywords": ["Rotate Image", "Spiral Matrix", "Set Matrix Zeroes"]
    },
    {
        "name": "Bit Manipulation",
        "keywords": ["Number of 1 Bits", "Counting Bits", "Reverse Bits", "Missing Number", "Sum of Two Integers"]
    },
    {
        "name": "Intervals",
        "keywords": ["Insert Interval", "Merge Intervals", "Non-overlapping Intervals", "Meeting Rooms", "Meeting Rooms II"]
    }
]

categorized_items = {cat["name"]: [] for cat in categories}
categorized_items["Other"] = []

for item in items:
    found = False
    for cat in categories:
        for keyword in cat["keywords"]:
            if keyword.lower() in item["name"].lower():
                categorized_items[cat["name"]].append(item)
                found = True
                break
        if found: break
    if not found:
        categorized_items["Other"].append(item)

def build_sidebar(filename):
    html = ['<div class="sidebar-scroll" id="sidebar-list">']
    for cat in categories:
        cat_name = cat["name"]
        cat_items = categorized_items[cat_name]
        if not cat_items: continue
        
        has_active = any(item["href"] == filename for item in cat_items)
        module_class = 'nav-module expanded' if has_active else 'nav-module'
        
        html.append(f'            <div class="{module_class}">')
        html.append(f'                <div class="nav-module-title">{cat_name}</div>')
        for item in cat_items:
            is_active = (item["href"] == filename)
            classes = item["classes"].replace("active", "").strip()
            if is_active: classes += " active"
            
            html.append(f'                <a href="{item["href"]}" class="{classes}" data-q="{item["data_q"]}" style="text-decoration:none;">')
            html.append(f'                    {item["inner"]}')
            html.append(f'                </a>')
        html.append(f'            </div>')
    html.append('        </div>')
    return '\n'.join(html)

blind75_dir = 'blind75'
updated = 0
for filename in os.listdir(blind75_dir):
    if filename.endswith('.html') and filename != 'index.html':
        filepath = os.path.join(blind75_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        start = content.find('<div class="sidebar-scroll" id="sidebar-list">')
        end = content.find('<div class="progress-footer">')
        
        if start != -1 and end != -1:
            new_sidebar = build_sidebar(filename)
            new_content = content[:start] + new_sidebar + "\n\n        " + content[end:]
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1

print(f"Updated {updated} files out of {len(os.listdir(blind75_dir))}")
