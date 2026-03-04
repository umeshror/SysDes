import re

filepath = "case_studies/open-table.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract main content (original lines 976 to approx 1400)
# We look for the <div class="main"> and stop before the script/button
start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if '<div class="main">' in line:
        start_line = i
    if '<button id="back-to-top"' in line or '<script>' in line and i > 1400:
        if end_line == -1: end_line = i

if start_line != -1 and end_line != -1:
    main_content = "".join(lines[start_line:end_line])
else:
    # Fallback if detection fails
    main_content = "<!-- Main content extraction failed -->"

new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="System Design Reference — Case Studies">
  <title>📚 Case Studies — System Design Fundamentals</title>
  <link rel="stylesheet" href="../styles.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <link rel="stylesheet" href="../system-design.css">
  <link rel="stylesheet" href="../system-design-common.css">
  <script defer src="../system-design-common.js"></script>
</head>
<body>
  <div class="layout">
    <nav class="sidebar" style="display:flex;flex-direction:column">
      <div class="sidebar-header">
        <div style="margin-bottom:14px">
          <a href="../index.html" class="back-link">&#8592; Back to Home</a>
        </div>
        <h1>System Design Fundamentals</h1>
        <p>180+ topics &nbsp;|&nbsp; Complete Reference</p>
      </div>
      <div class="sidebar-accordion">
        <!-- Will be filled by fix_navigation.py -->
      </div>
    </nav>
{main_content}
    </div>
  </div>
  <button id="back-to-top" title="Back to top" aria-label="Back to top">&#8593;</button>
  <script>
    if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose'
        }});
    }}
  </script>
</body>
</html>
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("OpenTable sanitized!")
