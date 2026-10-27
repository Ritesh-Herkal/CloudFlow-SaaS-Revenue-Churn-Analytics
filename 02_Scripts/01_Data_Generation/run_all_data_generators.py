"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : run_all_data_generators.py
Developer       : Ritesh Herkal
Description     : Executes all synthetic source-data generation scripts sequentially.
================================================================================
"""

import subprocess
import sys
import time
from pathlib import Path


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# PROJECT_ROOT is two levels up from 02_Scripts/01_Data_Generation
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT_DIRECTORY = Path(__file__).resolve().parent

# Explicit list of generators in their correct dependency execution order
GENERATORS = [
    "generate_regions.py",
    "generate_subscription_plans.py",
    "generate_customers.py",
    "generate_subscription_events.py",
    "generate_payment_transactions.py",
    "generate_support_tickets.py",
    "generate_sales_targets.py",
    "generate_sales_transactions.py",
]


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 75)
    print("CLOUDFLOW — MASTER DATA GENERATION")
    print("=" * 75)
    print(f"Project Root    : {PROJECT_ROOT}")
    print(f"Script Directory: {SCRIPT_DIRECTORY}")
    print("=" * 75)

    start_time = time.time()

    for index, script_name in enumerate(GENERATORS, start=1):
        script_path = SCRIPT_DIRECTORY / script_name

        print(f"\n[{index}/{len(GENERATORS)}] Running: {script_name}")
        print("-" * 75)

        if not script_path.exists():
            print(f"ERROR: Script not found: {script_path}")
            sys.exit(1)

        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=PROJECT_ROOT,
                check=True,
            )
        except subprocess.CalledProcessError as error:
            print(f"\nFAILED: {script_name}")
            print(f"Exit code: {error.returncode}")
            print("Remaining generators will not run.")
            sys.exit(error.returncode or 1)

        print(f"SUCCESS: {script_name}")

    elapsed_time = time.time() - start_time

    print("\n" + "=" * 75)
    print("ALL DATA GENERATORS COMPLETED SUCCESSFULLY")
    print(f"Generators executed   : {len(GENERATORS)}")
    print(f"Total execution time  : {elapsed_time:.2f} seconds")
    print(f"Output directory      : {PROJECT_ROOT / '00_Dataset' / '02_Generated'}")
    print("=" * 75)


if __name__ == "__main__":
    main()