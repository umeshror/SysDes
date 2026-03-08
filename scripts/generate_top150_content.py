#!/usr/bin/env python3
"""
generate_top150_content.py
Uses the Gemini API to generate level problem content for all 150
Top Interview 150 problems, then rebuilds the HTML pages.

Requirements:
    pip install google-generativeai

Usage:
    export GOOGLE_API_KEY="your-api-key"
    python3 scripts/generate_top150_content.py [--start 1] [--end 150] [--delay 2]

Options:
    --start N   First problem number to generate (default: 1)
    --end   N   Last problem number to generate (default: 150)
    --delay N   Seconds to wait between API calls (default: 1.5)
    --dry-run   Print prompts without calling the API
"""

import json, os, sys, time, argparse, re
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
ITEMS_FILE = Path(__file__).parent / "top150_items.json"
OUTPUT_DIR = ROOT / "top150"

# ── Gemini setup ──────────────────────────────────────────────────────────────
def get_gemini_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set.")
        print("   export GOOGLE_API_KEY='your-key'")
        sys.exit(1)
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.0-flash")
    except ImportError:
        print("❌ google-generativeai not installed. Run: pip install google-generativeai")
        sys.exit(1)


# ── Prompt builder ────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """
You are a FAANG interview coach. Generate a comprehensive editorial for the following LeetCode problem.
Return ONLY valid HTML (no markdown, no code fences). Use the exact HTML structure shown below.

Problem: {name}
LeetCode Number: #{num}
Difficulty: {difficulty}
Category: {category}

Required HTML output structure (fill in the content between tags):

<div class="problem-statement">
  <h3>Problem Statement</h3>
  <p>[2-3 concise sentences describing the problem clearly]</p>
</div>

<div class="examples">
  <div class="example-block">
    <div class="example-header">Example 1</div>
    <div class="example-body">
      <div><span class="label">Input: </span><span class="val">[input here]</span></div>
      <div><span class="label">Output: </span><span class="val">[output here]</span></div>
      <div class="explanation">Explanation: [brief explanation]</div>
    </div>
  </div>
  <div class="example-block">
    <div class="example-header">Example 2</div>
    <div class="example-body">
      <div><span class="label">Input: </span><span class="val">[input here]</span></div>
      <div><span class="label">Output: </span><span class="val">[output here]</span></div>
    </div>
  </div>
</div>

<div class="constraints">
  <h4>Constraints</h4>
  <ul>
    <li>[constraint 1 in mathematical notation]</li>
    <li>[constraint 2]</li>
    <li>[constraint 3 if applicable]</li>
  </ul>
</div>

<table class="compare-table">
  <thead><tr><th>Approach</th><th>Time</th><th>Space</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Brute Force</td><td>[O(?) ]</td><td>[O(?)]</td><td>[one-line note]</td></tr>
    <tr class="optimal-row"><td>Optimal</td><td>[O(?)]</td><td>[O(?)]</td><td>[one-line note]</td></tr>
  </tbody>
</table>

<h2 class="approach-title">Optimal Solution <span class="approach-badge badge-optimal">Optimal</span></h2>
<div class="complexity-row">
  <div class="complexity-pill"><span class="cp-label">Time</span><span class="cp-value">[O(?)]</span></div>
  <div class="complexity-pill"><span class="cp-label">Space</span><span class="cp-value">[O(?)]</span></div>
</div>
<p class="approach-explanation">[2-3 sentences explaining the key insight of the optimal approach]</p>

<div class="code-tabs">
  <div class="tab-buttons">
    <button class="tab-btn active" onclick="switchLangTab(this, 'py-{slug}')">Python</button>
    <button class="tab-btn" onclick="switchLangTab(this, 'java-{slug}')">Java</button>
  </div>
  <div id="py-{slug}" class="tab-content active">
    <div class="code-wrap"><pre><code class="language-python">[clean, commented Python solution]</code></pre></div>
  </div>
  <div id="java-{slug}" class="tab-content">
    <div class="code-wrap"><pre><code class="language-java">[clean, commented Java solution]</code></pre></div>
  </div>
</div>

<div class="insight">
  <div class="insight-title">💡 Key Insight</div>
  <p>[One sentence describing the core trick or pattern — what makes this problem "click"]</p>
</div>

<div class="warn-box">
  <div class="warn-box-title">⚠️ Common Mistakes</div>
  <p>[The #1 mistake candidates make on this problem in interviews]</p>
</div>
"""

def build_prompt(item):
    return PROMPT_TEMPLATE.format(
        name=item["name"],
        num=item["num"],
        difficulty=item["difficulty"],
        category=item["category"],
        slug=item["data_q"],
    )


# ── HTML page builder ─────────────────────────────────────────────────────────
def read_page(slug):
    filepath = OUTPUT_DIR / f"{slug}.html"
    if not filepath.exists():
        return None, None
    return filepath, filepath.read_text(encoding="utf-8")


def inject_content(html, generated_html):
    """Replace the Content Pending placeholder with generated content."""
    pending_pattern = re.compile(
        r'<div[^>]*class="[^"]*content-pending[^"]*"[^>]*>.*?</div>',
        re.DOTALL
    )
    if pending_pattern.search(html):
        return pending_pattern.sub(generated_html, html, count=1)

    # Fallback: look for the yellow placeholder box
    fallback = re.compile(
        r'<div[^>]*style="[^"]*background:\s*#fffff[^"]*"[^>]*>.*?Content Pending.*?</div>',
        re.DOTALL | re.IGNORECASE
    )
    if fallback.search(html):
        return fallback.sub(generated_html, html, count=1)

    # Last resort: inject before the Mark as Solved button
    return html.replace(
        '<button class="mark-solved-btn"',
        generated_html + '\n<button class="mark-solved-btn"',
        1
    )


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate Top 150 content via Gemini")
    parser.add_argument("--start", type=int, default=1, help="First problem number")
    parser.add_argument("--end",   type=int, default=150, help="Last problem number")
    parser.add_argument("--delay", type=float, default=1.5, help="Seconds between API calls")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without API calls")
    args = parser.parse_args()

    # Load manifest
    with open(ITEMS_FILE, "r") as f:
        items = json.load(f)

    # Filter by range
    items = [it for it in items if args.start <= int(it["num"]) <= args.end]
    print(f"🔢 Processing {len(items)} problems (#{args.start}–#{args.end})\n")

    client = None if args.dry_run else get_gemini_client()

    success, skipped, failed = 0, 0, []

    for item in items:
        num, name, slug = item["num"], item["name"], item["data_q"]
        print(f"  [{num:>3}] {name}", end=" ", flush=True)

        filepath, html = read_page(slug)
        if filepath is None:
            print("⚠️  page not found, skipping")
            skipped += 1
            continue

        # Skip if already has real content (not "Content Pending")
        if "Content Pending" not in html and "content-pending" not in html:
            print("✅ already has content")
            skipped += 1
            continue

        prompt = build_prompt(item)

        if args.dry_run:
            print("📋 [dry-run] prompt built")
            continue

        try:
            response = client.generate_content(prompt)
            generated = response.text.strip()

            # Strip any accidental markdown fences
            generated = re.sub(r'^```html\s*', '', generated, flags=re.IGNORECASE)
            generated = re.sub(r'\s*```$', '', generated)

            new_html = inject_content(html, generated)
            filepath.write_text(new_html, encoding="utf-8")
            print("✅ generated")
            success += 1

        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed.append(f"#{num} {name}")

        time.sleep(args.delay)

    print(f"\n{'─'*50}")
    print(f"✅ Generated: {success}  |  ⏭ Skipped: {skipped}  |  ❌ Failed: {len(failed)}")
    if failed:
        print("Failed problems:")
        for f_ in failed:
            print(f"  • {f_}")

    if success > 0:
        print("\n📦 Rebuilding pages with hljs highlighting…")
        os.system("python3 scripts/build_top150_pages.py")
        print("Done! Open top150/001-merge-sorted-array.html to verify.")


if __name__ == "__main__":
    main()
