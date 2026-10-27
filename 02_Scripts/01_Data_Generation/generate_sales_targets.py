"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_sales_targets.py
Output          : data/source/sales_targets.csv
Developer       : Ritesh Herkal
Description     : Generates monthly sales targets for 8 regions.
================================================================================
"""

import csv
import random
from datetime import date
from pathlib import Path


# ==============================================================================
# CONFIGURATION
# ==============================================================================

RECORD_COUNT = 96
RANDOM_SEED = 20261027
TARGET_YEAR = 2025

OUTPUT_FILE = Path("00_Dataset/02_Generated/sales_targets.csv")

REGION_IDS = range(1, 9)
MONTHS = range(1, 13)

random.seed(RANDOM_SEED)

HEADERS = [
    "TargetID",
    "RegionID",
    "TargetMonth",
    "TargetRevenue",
    "TargetNewCustomers",
]


# ==============================================================================
# GENERATE SALES TARGETS
# ==============================================================================

def generate_sales_targets():
    records = []
    target_number = 1

    # Each region receives one target for every month.
    for region_id in REGION_IDS:
        # Regions have different baseline revenue targets.
        regional_baseline = random.randint(30_000, 100_000)

        for month in MONTHS:
            target_month = date(TARGET_YEAR, month, 1)

            # Apply a small variation to the regional revenue target.
            target_revenue = round(
                regional_baseline * random.uniform(0.90, 1.15), 2
            )

            target_new_customers = random.randint(10, 80)

            records.append([
                f"TGT{target_number:06d}",
                region_id,
                target_month.isoformat(),
                target_revenue,
                target_new_customers,
            ])

            target_number += 1

    return records


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("Starting Sales Targets data generation...")

    records = generate_sales_targets()

    if len(records) != RECORD_COUNT:
        raise ValueError(
            f"Expected {RECORD_COUNT} records, generated {len(records)}."
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        writer.writerows(records)

    # Validate record count and target ID uniqueness.
    target_ids = [record[0] for record in records]

    if len(target_ids) != len(set(target_ids)):
        raise ValueError("Duplicate TargetID values detected.")

    print("\nSales Targets generation completed successfully.")
    print(f"Output file : {OUTPUT_FILE.resolve()}")
    print(f"Data records: {len(records):,}")
    print(f"Regions     : {len(REGION_IDS)}")
    print(f"Months      : {len(MONTHS)}")
    print(f"Target year : {TARGET_YEAR}")


if __name__ == "__main__":
    main()