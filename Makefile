# SysDes Makefile
# Run from project root.  Usage: make <target>

.PHONY: site blind75 top150 patterns serve validate clean help

# ── Default ──────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  SysDes Build Targets"
	@echo "  ─────────────────────────────────────────────────────"
	@echo "  make site       Rebuild all system design pages from monolith"
	@echo "  make blind75    Rebuild all Blind 75 problem pages"
	@echo "  make top150     Rebuild all Top 150 problem pages"
	@echo "  make validate   Validate monolith has all 38 sections"
	@echo "  make serve      Start local HTTP server on http://localhost:8080"
	@echo "  make clean      Remove Python __pycache__ dirs"
	@echo "  make all        Run site + blind75 + top150"
	@echo ""

# ── Generators ────────────────────────────────────────────────────────────────
site:
	@echo "🔧 Rebuilding system design pages…"
	python3 scripts/split_pages.py
	@echo "✅ Done — pages/ and case_studies/ updated."

blind75:
	@echo "🔧 Rebuilding Blind 75 pages…"
	python3 scripts/run_all_batches.py
	python3 scripts/build_blind75_pages.py
	@echo "✅ Done — blind75/ updated."

top150:
	@echo "🔧 Rebuilding Top 150 pages…"
	python3 scripts/build_top150_pages.py
	@echo "✅ Done — top150/ updated."

all: site blind75 top150
	@echo "✅ Full rebuild complete."

# ── Validate ──────────────────────────────────────────────────────────────────
validate:
	@echo "🔍 Validating monolith…"
	python3 scripts/validate_monolith.py

# ── Dev server ────────────────────────────────────────────────────────────────
serve:
	@echo "🌐 Serving at http://localhost:8080  (Ctrl-C to stop)"
	python3 -m http.server 8080

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	@echo "🧹 Cleaning Python cache…"
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean."
