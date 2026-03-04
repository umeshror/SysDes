import os
import re
import json
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "blind75-spa.html"
MODEL_ID = "gemini-2.5-pro"
API_KEY = os.environ.get("GEMINI_API_KEY")

# We read the template from Longest Consecutive Sequence to give to Gemini
def get_template():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    if "</body>" in raw:
        raw = raw.split("</body>")[0] + "</body>\n</html>"
    soup = BeautifulSoup(raw, "html.parser")
    # Get q1 (Longest Consecutive Sequence)
    q1_panel = soup.find("div", id="q1", class_="question-panel")
    return str(q1_panel) if q1_panel else ""

def generate_problem_html(q_id, q_name, q_diff, template_html):
    prompt = f"""
I am building a high-quality FAANG interview prep guide (Blind 75).
I need you to generate the HTML content for the problem: "{q_name}".
Difficulty: {q_diff}.

Here is the exact HTML structure and CSS classes you MUST use. This is the template for "Longest Consecutive Sequence".

TEMPLATE:
{template_html}

INSTRUCTIONS:
1. Replace the "Longest Consecutive Sequence" content with the content for "{q_name}".
2. You MUST keep the exact same HTML structure:
   - `<div class="question-panel" id="{q_id}">`
   - `<div class="q-header">` with badges.
   - `<div class="problem-statement">` with clear text.
   - Multiple `<div class="example-block">`
   - `<div class="constraints">`
   - `<h2 class="approach-title">Approaches Comparison</h2>`
   - `<table class="compare-table">` comparing brute force vs optimal.
   - Code tabs `<div class="code-tabs">` with Python, Java, JS, and Go implementations. (Please provide actual working optimal code for {q_name} in these 4 languages).
   - A `<div class="insight">` explaining exactly WHY the time/space complexity is what it is.
   - An `<div class="interview-tips">` section giving 4-5 bullet points on how to approach this problem in a real interview.
   - The `<button class="mark-solved-btn" ...>` at the bottom must have the id="solve-{q_id}" and onclick="markSolved('{q_id}', this)".
3. IMPORTANT: DO NOT wrap the output in ```html blocks. Return ONLY the raw valid HTML string starting exactly from `<div class="question-panel" id="{q_id}">`. Do NOT return `<html>` or `<body>` tags. DO NOT return emojis like ✅ or 💡 in the text.
"""
    print(f"Generating content for {q_name}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return ""
    
    resp_json = response.json()
    try:
        return resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Failed to parse response: {resp_json}")
        return ""


def main():
    template_html = get_template()
    if not template_html:
        print("Could not find template q1.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    if "</body>" in raw:
        raw = raw.split("</body>")[0] + "</body>\n</html>"
        
    soup = BeautifulSoup(raw, "html.parser")
    
    sidebar = soup.find("div", id="sidebar-list")
    q_items = sidebar.find_all("div", class_="q-item")

    # Let's just do Two Sum (q2) first as a test.
    test_q_id = "q2"
    test_q_name = "Two Sum"
    test_q_diff = "Easy" # you can extract this from the sidebar item if you want

    panel_to_replace = soup.find("div", id=test_q_id, class_="question-panel")
    
    # If the panel is completely missing, we'll create a placeholder for it and append it to main-panel
    if not panel_to_replace:
        print(f"Panel {test_q_id} missing, creating placeholder...")
        main_panel = soup.find("div", id="main-panel")
        if main_panel:
            placeholder_soup = BeautifulSoup(f'<div class="question-panel" id="{test_q_id}"><h2>Content Pending</h2></div>', "html.parser")
            main_panel.append(placeholder_soup)
            panel_to_replace = soup.find("div", id=test_q_id, class_="question-panel")
    
    if panel_to_replace and ("Content Pending" in str(panel_to_replace) or "Content Pending" in panel_to_replace.text):
        new_html_string = generate_problem_html(test_q_id, test_q_name, test_q_diff, template_html)
        
        # Strip markdown formatting if Gemini accidentally included it
        if new_html_string.startswith("```html"):
            new_html_string = new_html_string[7:]
        if new_html_string.endswith("```"):
            new_html_string = new_html_string[:-3]
        new_html_string = new_html_string.strip()
        
        # We need to replace the node in the soup
        new_soup = BeautifulSoup(new_html_string, "html.parser")
        new_panel_node = new_soup.find("div", id=test_q_id)
        if new_panel_node:
             panel_to_replace.replace_with(new_panel_node)
             
             # Save back to blind75-spa.html
             with open(INPUT_FILE, "w", encoding="utf-8") as f:
                 f.write(str(soup))
             print(f"Successfully injected content for {test_q_name} into {INPUT_FILE}.")
        else:
             print("Gemini did not return a valid top level div.")
    else:
        print(f"Panel {test_q_id} already has content or could not be created.")


if __name__ == "__main__":
    main()
