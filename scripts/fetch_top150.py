import json
import requests
import re

def fetch_top_150():
    url = "https://leetcode.com/graphql"
    
    # We query the study plan top-interview-150
    # Actually LeetCode's study plan GraphQL is a bit complex. 
    # An easier reliable way is to query the specific question list or just search GitHub for a static top 150 json to avoid over-engineering.
    # Wait, the study plan API:
    query = """
    query studyPlanDetail($slug: String!) {
      studyPlanV2Detail(planSlug: $slug) {
        planSubGroups {
          slug
          name
          questions {
            titleSlug
            title
            questionFrontendId
            difficulty
          }
        }
      }
    }
    """
    
    variables = {
        "slug": "top-interview-150"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    print("Fetching Top Interview 150 from LeetCode...")
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return
        
    data = response.json()
    try:
        subgroups = data["data"]["studyPlanV2Detail"]["planSubGroups"]
    except Exception as e:
        print(f"Error parsing response: {e}, {data}")
        return
        
    items = []
    
    for subgroup in subgroups:
        category = subgroup["name"]
        for q in subgroup["questions"]:
            slug = q["titleSlug"]
            title = q["title"]
            diff = q["difficulty"]
            q_id = q["questionFrontendId"]
            
            # Create a file name format similar to Blind 75 (e.g., 01-merge-sorted-array.html)
            # We'll assign a sequential number later to preserve order
            
            items.append({
                "id": f"q{q_id}",
                "num": q_id, # We'll reassign sequential nums for the file names
                "real_id": q_id,
                "name": title,
                "slug": slug,
                "diff": diff,
                "category": category
            })
            
    # Assign sequential numbers 1 to 150
    final_items = []
    for i, item in enumerate(items, 1):
        num_str = str(i).zfill(3)
        filename = f"{num_str}-{item['slug']}.html"
        
        diff_class = "diff-easy"
        if item["diff"] == "Medium":
            diff_class = "diff-medium"
        elif item["diff"] == "Hard":
            diff_class = "diff-hard"
            
        final_items.append({
            "href": filename,
            "classes": "q-item",
            "data_q": item["id"],
            "inner": f'<span class="q-num">{i}</span>      <span class="q-check"></span>      <span class="q-name">{item["name"]}</span>      <span class="q-diff {diff_class}">TODO</span>',
            "name": item["name"],
            "num": i,
            "real_id": item["real_id"],
            "slug": item["slug"],
            "diff": item["diff"],
            "category": item["category"]
        })
        
    print(f"Found {len(final_items)} problems.")
    
    out_file = "scripts/top150_items.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"items": final_items}, f, indent=2)
        
    print(f"Saved to {out_file}")

if __name__ == "__main__":
    fetch_top_150()
