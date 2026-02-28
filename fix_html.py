with open("system-design-complete.html", "r") as f:
    lines = f.readlines()

# Line 1919 in 1-indexed is lines[1918].
# Let's just find "    </div>\n" right after "      </div>\n" at 1918.
# Actually let's just match the exact text.
import re
content = "".join(lines)

# Remove the premature </div> closing .main
# It is located exactly at:
# 1918:       </div>
# 1919:     </div>
# 1920:     <div class="def">
# 1921:       <dt>Instagram's 2012 peak: vertical first</dt>
target = """      </div>
    </div>
    <div class="def">
      <dt>Instagram's 2012 peak: vertical first</dt>"""
replacement = """      </div>
    <div class="section" id="extra-advanced">
    <div class="def">
      <dt>Instagram's 2012 peak: vertical first</dt>"""

content = content.replace(target, replacement)

# Now close this new section right before networking
target2 = """    </div>
  </div>



  <!-- ==================== DATA STRUCTURES ==================== -->
  <div class="section" id="networking">"""
replacement2 = """    </div>
  </div>
  </div>



  <!-- ==================== DATA STRUCTURES ==================== -->
  <div class="section" id="networking">"""
content = content.replace(target2, replacement2)

with open("system-design-complete.html", "w") as f:
    f.write(content)
print("done")
