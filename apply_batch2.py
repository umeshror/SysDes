#!/usr/bin/env python3
"""
Apply batch 2 of FAANG section replacements.
"""

import os
import re

REPLACEMENTS = {
    'lb':               'sections/lb_new.html',
    'caching':          'sections/caching_new.html',
    'dist-fundamentals':'sections/dist-fundamentals_new.html',
}

def find_section_bounds(content, sec_id):
    start_pattern = re.compile(
        r'\s{2,6}<div class="section[^"]*"\s+id="' + re.escape(sec_id) + r'"'
    )
    m = start_pattern.search(content)
    if not m:
        return None, None
    start = m.start()

    next_sec = re.compile(r'\n\s{2,6}<div class="section[^"]*"\s+id="')
    next_m = next_sec.search(content, m.end())

    if next_m:
        end_of_ours = content.rfind('      </div>', start, next_m.start())
        if end_of_ours == -1:
            end_of_ours = content.rfind('</div>', start, next_m.start())
        section_end = end_of_ours + len('      </div>')
    else:
        end_of_ours = content.rfind('      </div>', start)
        section_end = end_of_ours + len('      </div>')

    return start, section_end

src_file = 'system-design-complete.html'
with open(src_file, encoding='utf-8') as f:
    content = f.read()

print(f"Source file: {len(content):,} bytes")

for sec_id, new_file in REPLACEMENTS.items():
    if not os.path.exists(new_file):
        print(f"  ⚠️  {sec_id}: file not found")
        continue
    start, end = find_section_bounds(content, sec_id)
    if start is None:
        print(f"  ⚠️  {sec_id}: section not found")
        continue
    with open(new_file, encoding='utf-8') as f:
        new_section = f.read().strip()
    old_size = end - start
    content = content[:start] + new_section + content[end:]
    print(f"  ✅  {sec_id}: {old_size:,} → {len(new_section):,} bytes")

with open(src_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nFinal: {len(content):,} bytes")
for sec_id in REPLACEMENTS:
    ok = f'id="{sec_id}"' in content
    print(f"  {'✅' if ok else '❌'} {sec_id}")
