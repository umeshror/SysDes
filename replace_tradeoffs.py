#!/usr/bin/env python3
"""Splice new tradeoffs section into system-design-complete.html"""

with open('tradeoffs_new.html', encoding='utf-8') as f:
    new_section = f.read().strip()

with open('system-design-complete.html', encoding='utf-8') as f:
    content = f.read()

START = '      <div class="section" id="tradeoffs">'
# The section closes just before the networking section
END_MARKER = '      <div class="section" id="networking">'

start_idx = content.find(START)
end_idx = content.find(END_MARKER, start_idx)

# find the </div> right before networking
close_tag = '      </div>'
section_end = content.rfind(close_tag, start_idx, end_idx) + len(close_tag)

if start_idx == -1 or end_idx == -1:
    print("ERROR: markers not found")
    import sys; sys.exit(1)

new_content = content[:start_idx] + new_section + '\n\n\n\n' + content[section_end:].lstrip('\n')

with open('system-design-complete.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('system-design-complete.html', encoding='utf-8') as f:
    verify = f.read()

checks = [
    'FAANG level' in verify or 'FAANG' in verify,
    'id="tradeoffs"' in verify,
    'id="networking"' in verify,
    'Little\'s Law' in verify,
    'Knight Capital' in verify,
    'Token Bucket' in verify,
]
print(f"File size: {len(verify):,} bytes")
print(f"All checks passed: {all(checks)}")
for i, c in enumerate(checks):
    print(f"  Check {i+1}: {'✅' if c else '❌'}")
