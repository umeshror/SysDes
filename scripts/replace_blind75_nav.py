import json
import os
import re

# Load parsed items from items.json
with open('items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)["items"]

# Standard NeetCode / Blind 75 categories with corresponding leetcode IDs/titles or keywords
categories = [
    {
        "name": "Arrays & Hashing",
        "keywords": ["Contains Duplicate", "Valid Anagram", "Two Sum", "Group Anagrams", "Top K Frequent Elements", "Product of Array Except Self", "Encode and Decode Strings", "Longest Consecutive Sequence"]
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
        "keywords": ["Find Minimum in Rotated Sorted Array", "Search in Rotated Sorted Array"]
    },
    {
        "name": "Linked List",
        "keywords": ["Reverse Linked List", "Merge Two Sorted Lists", "Reorder List", "Remove Nth Node From End", "Linked List Cycle", "Merge k Sorted Lists"]
    },
    {
        "name": "Trees",
        "keywords": ["Invert Binary Tree", "Maximum Depth of Binary Tree", "Same Tree", "Subtree of Another Tree", "Lowest Common Ancestor of a BST", "Binary Tree Level Order Traversal", "Validate Binary Search Tree", "Kth Smallest Element in a BST", "Construct Binary Tree from Preorder", "Binary Tree Maximum Path Sum", "Serialize and Deserialize Binary Tree"]
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
        "keywords": ["Climbing Stairs", "House Robber", "House Robber II", "Longest Palindromic Substring", "Palindromic Substrings", "Decode Ways", "Coin Change", "Maximum Product Subarray", "Word Break", "Longest Increasing Subsequence"]
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

# Assign each item to a category
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
        if found:
            break
    if not found:
        categorized_items["Other"].append(item)

# Validate Other is empty
if len(categorized_items["Other"]) > 0:
    print("Warning: Some missing items from mapping!", [x["name"] for x in categorized_items["Other"]])

# Generate the new sidebar-scroll HTML
new_sidebar_html = '<div class="sidebar-scroll" id="sidebar-list">\n'
for cat_name in categorized_items:
    cat_items = categorized_items[cat_name]
    if len(cat_items) == 0:
        continue
        
    new_sidebar_html += f'            <div class="nav-module">\n'
    new_sidebar_html += f'                <div class="nav-module-title">{cat_name}</div>\n'
    for item in cat_items:
        # Reconstruct the anchor tag
        # We drop the "active" class here because we will inject the active class dynamically or keep it clean
        classes = item["classes"] # already stripped 'active'
        new_sidebar_html += f'                <a href="{item["href"]}" class="{classes}" data-q="{item["data_q"]}" style="text-decoration:none;">\n'
        new_sidebar_html += f'                    {item["inner"]}\n'
        new_sidebar_html += f'                </a>\n'
    new_sidebar_html += f'            </div>\n'
new_sidebar_html += '        </div>'

# Now we need to update ALL HTML files in blind75 directory.
blind75_dir = 'blind75'
updated_count = 0
for filename in os.listdir(blind75_dir):
    if filename.endswith('.html') and filename != 'index.html':
        filepath = os.path.join(blind75_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the boundaries to replace
        start_marker = '<div class="sidebar-scroll" id="sidebar-list">'
        end_marker = '<div class="progress-footer">'
        start = content.find(start_marker)
        end = content.find(end_marker, start)
        
        if start != -1 and end != -1:
            # We inject "active" dynamically for this specific file
            # Wait, the easiest way is to add "active" class dynamically to the currently open item based on filename
            # The structure is <a href="filename" class="q-item" ...>
            # Let's string replace
            local_sidebar = new_sidebar_html.replace(f'href="{filename}" class="q-item"', f'href="{filename}" class="q-item active"')
            
            # The sidebar should start completely expanded for the section containing the active element
            # To do this, we can find the nav-module that contains active and add "expanded"
            module_pattern = r'(<div class="nav-module">)(.*?active.*?</div\s*>)' # naive match inside module
            # We can use regex to add expanded
            # Actually since we want the javascript `index.html` logic to expand it on load or let the CSS handle it
            # We will just write a small replace script inside the module string:
            # Let's split by nav-module and if it has 'active', add 'expanded'
            modules = local_sidebar.split('<div class="nav-module">')
            for i in range(1, len(modules)):
                if 'active' in modules[i]:
                    modules[i] = ' expanded' + modules[i] # This will make <div class="nav-module expanded"> NO WAIT
                    # The split consumed '<div class="nav-module">', so I need to rebuild it
            
            final_sidebar = modules[0]
            for i in range(1, len(modules)):
                if 'active' in modules[i]:
                    final_sidebar += '<div class="nav-module expanded">' + modules[i]
                else:
                    final_sidebar += '<div class="nav-module">' + modules[i]

            new_content = content[:start] + final_sidebar + "\n        " + content[end:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1

print(f"Successfully updated {updated_count} files with collapsible sidebar!")
