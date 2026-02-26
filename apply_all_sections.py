#!/usr/bin/env python3
"""
Master splice script: reads new section HTML files and replaces corresponding
sections in system-design-complete.html.

For each (section_id, new_file) pair:
  - Find the section boundary in the source HTML
  - Replace it with the new content
  - Write the updated file

Then regenerate all pages via split_pages.py.
"""

import os
import re
import glob
import subprocess

# Map: section_id → new content file
REPLACEMENTS = {
    'hashing':       'sections/hashing_new.html',
    'proxy':         'sections/proxy_new.html',
    'cdn':           'sections/cdn_new.html',
    'storage':       'sections/storage_new.html',
    'db-internals':  'sections/db-internals_new.html',
    'search':        'sections/search_new.html',
    'security':      'sections/security_new.html',
    'time-ordering': 'sections/time-ordering_new.html',
    'api-infra':     'sections/api-infra_new.html',
}

def find_section_bounds(content, sec_id):
    """Return (start, end) indices of the section div with the given id."""
    start_pattern = re.compile(
        r'\s{2,6}<div class="section[^"]*"\s+id="' + re.escape(sec_id) + r'"'
    )
    m = start_pattern.search(content)
    if not m:
        return None, None
    start = m.start()

    # Find the next section boundary or a top-level comment after it
    # Look for the next <div class="section or a <!--  comment
    next_sec = re.compile(r'\n\s{2,6}<div class="section[^"]*"\s+id="')
    next_m = next_sec.search(content, m.end())

    if next_m:
        # End is just before the next section's \n
        # We need to include the closing </div> that belongs to OUR section
        # Find the last </div> before the next section
        end_of_ours = content.rfind('      </div>', start, next_m.start())
        if end_of_ours == -1:
            end_of_ours = content.rfind('</div>', start, next_m.start())
        section_end = end_of_ours + len('      </div>')
    else:
        # Last section — find closing div
        end_of_ours = content.rfind('      </div>', start)
        section_end = end_of_ours + len('      </div>')

    return start, section_end


def main():
    src_file = 'system-design-complete.html'

    with open(src_file, encoding='utf-8') as f:
        content = f.read()

    print(f"Source file: {len(content):,} bytes")

    replaced = []
    skipped = []

    for sec_id, new_file in REPLACEMENTS.items():
        if not os.path.exists(new_file):
            print(f"  ⚠️  {sec_id}: new file not found ({new_file})")
            skipped.append(sec_id)
            continue

        start, end = find_section_bounds(content, sec_id)
        if start is None:
            print(f"  ⚠️  {sec_id}: section not found in source")
            skipped.append(sec_id)
            continue

        with open(new_file, encoding='utf-8') as f:
            new_section = f.read().strip()

        old_size = end - start
        content = content[:start] + new_section + content[end:]
        new_size = len(new_section)
        print(f"  ✅  {sec_id}: replaced {old_size:,} bytes → {new_size:,} bytes")
        replaced.append(sec_id)

    with open(src_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nFinal file size: {len(content):,} bytes")
    print(f"Replaced: {replaced}")
    if skipped:
        print(f"Skipped: {skipped}")

    # Quick sanity check
    for sec_id in replaced:
        if f'id="{sec_id}"' not in content:
            print(f"  ❌ SANITY FAIL: {sec_id} not found in output!")
        else:
            print(f"  ✅ Verified: {sec_id} present in output")


if __name__ == '__main__':
    main()
