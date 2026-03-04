"""
run_all_batches.py
Runs all batch content files in order and rebuilds pages.
"""
import os

# Import all batches (each calls add_problem() on shared_generator._PROBLEMS)
import batch2_content   # q6-q12
import batch3_content   # q13-q20
import batch4_content   # q21-q25
import batch5_content   # q26-q30
import batch6_content   # q31-q36
import batch7_content   # q37-q51
import batch8_content   # q52-q75

from shared_generator import run_injection

print("=== Blind 75 Bulk Content Injector ===\n")
injected = run_injection()

if injected > 0:
    print("\nRebuilding individual pages...")
    os.system("python3 scripts/build_blind75_pages.py")
    print("\nAll done!")
else:
    print("Nothing new to inject.")
