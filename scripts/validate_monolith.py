#!/usr/bin/env python3
"""
validate_monolith.py
Checks that system-design-complete.html contains all expected sections.
Run: python3 scripts/validate_monolith.py
"""

import os, re, sys

SOURCE = "system-design-complete.html"
EXPECTED_SECTIONS = [
    # Chapter 1 — Introduction
    ("intro",              "Intro → Introduction to System Design"),
    # Chapter 2 — Core Concepts
    ("core",               "Core → Core Concepts"),
    ("cap",                "Core → CAP Theorem"),
    ("pacelc",             "Core → PACELC Theorem"),
    ("hashing",            "Core → Consistent Hashing"),
    # Chapter 3 — Tradeoffs
    ("tradeoffs",          "Tradeoffs → System Design Trade-offs"),
    # Chapter 4 — Networking
    ("networking",         "Networking → Fundamentals"),
    ("proxy",              "Networking → Proxy & Reverse Proxy"),
    ("lb",                 "Networking → Load Balancing"),
    ("caching",            "Networking → Caching Architecture"),
    ("cdn",                "Networking → CDN"),
    # Chapter 5 — Infrastructure / Storage
    ("storage",            "Storage → Storage Architecture"),
    ("db-types",           "Storage → Database Types"),
    ("db-internals",       "Storage → DB Internals"),
    ("db-scaling",         "Storage → DB Scaling"),
    # Chapter 6 — API
    ("api-design",         "API → API Design"),
    ("api-infra",          "API → API Infrastructure"),
    ("api-auth",           "API → API Authentication"),
    ("realtime",           "API → Real-time Communication"),
    ("async",              "API → Async Messaging"),
    # Chapter 7 — Architecture
    ("arch-patterns",      "Arch → Architecture Patterns"),
    ("microservices",      "Arch → Microservices"),
    ("containers",         "Arch → Containers"),
    # Chapter 9 — Distributed Systems
    ("dist-fundamentals",  "Dist → Distributed Fundamentals"),
    ("time-ordering",      "Dist → Time & Ordering"),
    ("consensus",          "Dist → Consensus"),
    ("dist-tx",            "Dist → Distributed Transactions"),
    # Chapter 10 — Search & Ops
    ("data-structures",    "Search → Data Structures"),
    ("big-data",           "Search → Big Data"),
    ("search",             "Search → Search Systems"),
    ("disaster-recovery",  "Search → Disaster Recovery"),
    ("observability",      "Search → Observability"),
    ("security",           "Search → Security"),
    # Chapter 11 — Interview Framework
    ("framework",          "Interview → Framework"),
    # Chapter 12 — Coding Patterns
    ("patterns",           "Coding → Interview Patterns"),
    # Case Study
    ("case-opentable",     "Case Study → OpenTable"),
]

def validate():
    if not os.path.exists(SOURCE):
        print(f"❌ ERROR: {SOURCE} not found. Run from project root.")
        sys.exit(1)

    with open(SOURCE, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"✔  Loaded {SOURCE} ({len(content):,} bytes)\n")

    errors = []
    warnings = []

    for section_id, label in EXPECTED_SECTIONS:
        # Check for the section id as an HTML id attribute or SECTION comment
        id_pattern = f'id="{section_id}"'
        comment_pattern = f'<!-- SECTION: {section_id} -->'

        found_id = id_pattern in content
        found_comment = comment_pattern in content

        if found_comment:
            print(f"  ✅ {label:48s}  [marker + id]")
        elif found_id:
            warnings.append(f"  ⚠️  {label}: found via id='{section_id}' but missing <!-- SECTION: {section_id} --> comment marker.")
            print(f"  🟡 {label:48s}  [id only — add SECTION comment]")
        else:
            errors.append(label)
            print(f"  ❌ {label:48s}  [MISSING]")

    print()
    # Summary
    if errors:
        print(f"❌ VALIDATION FAILED — {len(errors)} missing section(s):")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)
    elif warnings:
        print(f"⚠️  Passed with {len(warnings)} warning(s) — add <!-- SECTION: id --> markers for full hygiene.")
        for w in warnings:
            print(f"   {w}")
    else:
        print(f"✅ All {len(EXPECTED_SECTIONS)} sections validated successfully.")

    # Byte-size warning
    size_kb = len(content) // 1024
    if size_kb > 500:
        print(f"\n⚠️  File is {size_kb} KB — consider modular authoring for new content.")
    else:
        print(f"\n📦 File size: {size_kb} KB")

if __name__ == "__main__":
    validate()
