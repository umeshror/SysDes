import os
import re

PAGES_DIR = "pages"
COMMON_CSS = "../system-design-common.css"
COMMON_JS = "../system-design-common.js"

# Files to skip (may have unique requirements)
SKIP_FILES = []

def refactor_page(filepath):
    print(f"Refactoring {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove sidebar-improvements style block
    content = re.sub(r'<style id="sidebar-improvements">.*?</style>', '', content, flags=re.DOTALL)
    
    # 2. Add common assets to <head>
    common_assets = f'\n  <link rel="stylesheet" href="{COMMON_CSS}">\n  <script defer src="{COMMON_JS}"></script>'
    if '</head>' in content and COMMON_CSS not in content:
        content = content.replace('</head>', f'{common_assets}\n</head>')

    # 3. Clean up the bottom scripts (keep mermaid.initialize but simplify)
    # We want to remove the redundant section switching, progress bar, and back-to-top logic
    # which is now in system-design-common.js
    
    script_pattern = re.compile(r'<script>\s*mermaid\.initialize.*?// Scroll progress.*?</script>', re.DOTALL)
    
    # Simplified mermaid init that doesn't duplicate the common logic
    simplified_script = """
  <script>
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose'
        });
    }
  </script>"""

    content = script_pattern.sub(simplified_script, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    for filename in os.listdir(PAGES_DIR):
        if filename.endswith(".html") and filename not in SKIP_FILES:
            refactor_page(os.path.join(PAGES_DIR, filename))
    print("Refactoring complete!")
