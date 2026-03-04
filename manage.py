#!/usr/bin/env python3
"""
manage.py - Central CLI utility for the System Design Reference repository.
"""
import os
import sys
import subprocess
import re

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

def print_help():
    print("System Design Reference CLI")
    print("Usage: python3 manage.py [command]")
    print("")
    print("Commands:")
    print("  build-blind75   - Rebuilds the Blind 75 page generation")
    print("  split-pages     - Splits the monolithic system-design-complete.html into individual pages")
    print("  update-sidebars - Ensure all sidebars have the new Chapter 12 (Coding Patterns) linked correctly")
    print("  fix-assets      - Fixes all broken CSS/JS paths globally")
    print("  help            - Show this help message")

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"Error: Could not find script {script_name} in {SCRIPT_DIR}")
        return False
    
    print(f"🚀 Running {script_name}...")
    try:
        subprocess.run([sys.executable, script_path], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def update_sidebars():
    print("🚀 Updating all sidebars in pages/ and case_studies/...")
    
    new_chapter_block = """        <details class="acc-chapter">
          <summary class="acc-summary">
            <span class="chap-icon">🧩</span>
            <span class="chap-text">
              <span class="chap-num">Chapter 12</span>
              <span class="chap-label">Coding Patterns</span>
            </span>
            <span class="acc-arrow">›</span>
          </summary>
          <div class="acc-sub">
              <a class="acc-sub-item" href="REL_PATH12-coding-interview-patterns.html#patterns">20 Essential Patterns</a>
          </div>
        </details>"""

    def fix_file(filepath, is_page=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Fix literal \n first
        content = content.replace('\\n', '\n')
        
        # 2. Fix skewed Chapter numbers
        # If "Case Studies" is Chapter 12, make it 13
        content = re.sub(r'<span class="chap-num">Chapter 12</span>(\s*)<span class="chap-label">Case Studies</span>', 
                         r'<span class="chap-num">Chapter 13</span>\1<span class="chap-label">Case Studies</span>', content)

        # 3. Remove existing "Coding Patterns" blocks if they exist (to re-add cleanly)
        # We use a non-greedy regex and check for "Coding Patterns" specifically
        parts = re.split(r'(<details class="acc-chapter".*?</details>)', content, flags=re.DOTALL)
        new_parts = []
        for p in parts:
            if 'Coding Patterns' in p and 'acc-chapter' in p:
                continue
            new_parts.append(p)
        content = "".join(new_parts)

        # 4. Insert Chapter 12 before Chapter 13 (Case Studies)
        # Look for Chapter 13 block
        case_studies_match = re.search(r'(<details class="acc-chapter".*?Chapter 13.*?Case Studies.*?</details>)', content, flags=re.DOTALL)
        if case_studies_match:
            rel_path = "" if is_page else "../pages/"
            local_html = new_chapter_block.replace('REL_PATH', rel_path)
            content = content.replace(case_studies_match.group(1), local_html + "\n        " + case_studies_match.group(1))
        else:
            # Fallback: if no Case Studies, put it at the very end of sidebar-accordion
            content = content.replace('</div>\n    </nav>', new_chapter_block + '\n      </div>\n    </nav>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')
    if os.path.exists(pages_dir):
        for f in os.listdir(pages_dir):
            if f.endswith('.html'):
                fix_file(os.path.join(pages_dir, f), is_page=True)

    case_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'case_studies')
    if os.path.exists(case_dir):
        for f in os.listdir(case_dir):
            if f.endswith('.html'):
                fix_file(os.path.join(case_dir, f), is_page=False)

    print("✅ All sidebars updated and deduplicated!")

def fix_assets():
    print("🚀 Fixing all asset paths globally...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    replacements = [
        ('../styles.css', '../assets/css/styles.css'),
        ('../system-design.css', '../assets/css/system-design.css'),
        ('../system-design-common.css', '../assets/css/system-design-common.css'),
        ('../landing.css', '../assets/css/landing.css'),
        ('../system-design-common.js', '../assets/js/system-design-common.js'),
        ('href="styles.css"', 'href="assets/css/styles.css"'),
        ('href="landing.css"', 'href="assets/css/landing.css"'),
        ('src="system-design-common.js"', 'src="assets/js/system-design-common.js"'),
    ]
    
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath: continue
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                for old, new in replacements:
                    if old in content:
                        content = content.replace(old, new)
                        changed = True
                
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Fixed: {os.path.relpath(filepath, root_dir)}")

    print("✅ All asset paths fixed!")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "build-blind75":
        run_script("run_all_batches.py")
    elif command == "split-pages":
        run_script("split_pages.py")
    elif command == "update-sidebars":
        update_sidebars()
    elif command == "fix-assets":
        fix_assets()
    elif command == "help":
        print_help()
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
