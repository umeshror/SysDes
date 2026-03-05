#!/usr/bin/env python3
"""
add_section_markers.py
One-time script: adds <!-- SECTION: id --> comment before each <div class="section"
in system-design-complete.html so that validate_monolith.py reports clean.
Run once from project root:  python3 scripts/add_section_markers.py
"""
import re, os

SOURCE = "system-design-complete.html"

with open(SOURCE, "r", encoding="utf-8") as f:
    content = f.read()

# Match any <div class="section..." id="some-id"> or <div class="section active" id="...">
pattern = re.compile(r'(<div class="section[^"]*"\s+id="([^"]+)">)')

count = 0
def replacer(m):
    global count
    full_tag = m.group(1)
    section_id = m.group(2)
    marker = f'<!-- SECTION: {section_id} -->\n  '
    # Don't double-add
    count += 1
    return marker + full_tag

new_content = pattern.sub(replacer, content)

# Some sections have id before class
pattern2 = re.compile(r'(<div\s+id="([^"]+)"\s+class="section[^"]*">)')
def replacer2(m):
    global count
    full_tag = m.group(1)
    section_id = m.group(2)
    marker = f'<!-- SECTION: {section_id} -->\n  '
    count += 1
    return marker + full_tag

new_content = pattern2.sub(replacer2, new_content)

with open(SOURCE, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"✅ Added {count} SECTION comment markers to {SOURCE}")
