"""
force_inject.py
Force-replaces ALL question panels in blind75-spa.html with
fully-generated content, deduplicating panels as we go.
Run: python3 force_inject.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# Load all problem data into shared_generator._PROBLEMS
import batch2_content
import batch3_content
import batch4_content
import batch5_content
import batch6_content
import batch7_content
import batch8_content
import batch9_content  # q1-q5, q33, q42, q46, q49, q53, q54, q59, q67
from shared_generator import _PROBLEMS, _generate_panel_html, INPUT_FILE
from bs4 import BeautifulSoup

print(f"Problems loaded: {len(_PROBLEMS)}")
print("Problems:", sorted(_PROBLEMS.keys()))

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

if "</body>" in raw:
    raw = raw.split("</body>")[0] + "</body>\n</html>"

soup = BeautifulSoup(raw, "html.parser")
main_panel = soup.find("div", id="main-panel")

# Track which IDs we've already processed to avoid duplicates
processed = set()

# Get all question panels, process each unique ID once
all_panels = soup.find_all("div", class_="question-panel")
print(f"Found {len(all_panels)} total panels before dedup")

# First pass: remove ALL panels except q1
for p in all_panels:
    if p.get("id") == "q1":
        continue
    p.decompose()

print("Removed all panels (except q1). Re-injecting with full content...")

injected = 0
skipped = []

# Inject in order q1..q75
for i in range(1, 76):
    q_id = f"q{i}"
    if q_id == "q1":
        continue # manually preserved
    if q_id in _PROBLEMS:
        html = _generate_panel_html(q_id, _PROBLEMS[q_id])
        new_node = BeautifulSoup(html, "html.parser").find("div", id=q_id)
        if new_node and main_panel:
            main_panel.append(new_node)
            injected += 1
            print(f"  ✓ {q_id}: {_PROBLEMS[q_id]['name']}")
        else:
            print(f"  ✗ {q_id}: Failed to generate node")
    else:
        # No content for this ID — add a minimal placeholder
        placeholder_html = f'<div class="question-panel" id="{q_id}"><p class="placeholder-text">Content coming soon for {q_id}.</p></div>'
        node = BeautifulSoup(placeholder_html, "html.parser").find("div", id=q_id)
        if node and main_panel:
            main_panel.append(node)
        skipped.append(q_id)

print(f"\nInjected: {injected} | Placeholders: {len(skipped)}")
if skipped:
    print("Placeholders:", skipped)

with open(INPUT_FILE, "w", encoding="utf-8") as f:
    f.write(str(soup))
print(f"\nWritten to {INPUT_FILE}")

print("\nRebuilding individual pages...")
os.system("python3 build_blind75_pages.py")
print("Done!")
