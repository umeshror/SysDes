import os

filepath = 'pages/12-coding-interview-patterns.html'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Correct the relative path to the image
    # The image is in ../brain/<id>/...
    # But files in pages/ are at level 1, so they go up one level.
    # However, the brain directory is outside the project?
    # No, it's typically relative to the app data, but let's assume it's accessible.
    # Actually, I should probably copy the image to the project directory for better durability.
    
    pass

# Copy image to project for better hosting
img_src = '/Users/umeshsaruk/.gemini/antigravity/brain/687941b6-316e-4c2e-ba3f-e79d156b4f3e/coding_patterns_infographic_1772561190709.png'
img_dest = 'coding_patterns.png'

import shutil
if os.path.exists(img_src):
    shutil.copy(img_src, img_dest)
    print(f"Copied {img_src} to {img_dest}")

# Update HTML to use the local copy
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('../brain/687941b6-316e-4c2e-ba3f-e79d156b4f3e/coding_patterns_infographic_1772561190709.png', '../coding_patterns.png')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML with local image path.")
