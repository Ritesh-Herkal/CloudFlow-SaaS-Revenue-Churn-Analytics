"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_regions.py
Output          : data/source/regions.csv
Developer       : Ritesh Herkal
Description     : Generates the region master dataset for the warehouse.
================================================================================
"""

import csv
from pathlib import Path


# ==============================================================================
# CONFIGURATION
# ==============================================================================

OUTPUT_FILE = Path("00_Dataset/02_Generated/regions.csv")

HEADERS = [
    "RegionID",
    "RegionName",
    "Country",
    "IsActive",
]

REGIONS = [
    [1, "South India", "India", True],
    [2, "North India", "India", True],
    [3, "West India", "India", True],
    [4, "East India", "India", True],
    [5, "Central India", "India", True],
    [6, "North America", "United States", True],
    [7, "Europe", "United Kingdom", True],
    [8, "Asia Pacific", "Singapore", True],
]


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("Starting Region Master data generation...")

    region_ids = [region[0] for region in REGIONS]

    if len(region_ids) != len(set(region_ids)):
        raise ValueError("Duplicate RegionID values detected.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        writer.writerows(REGIONS)

    print("\nRegion Master data generation completed.")
    print(f"Output file : {OUTPUT_FILE.resolve()}")
    print(f"Data records: {len(REGIONS)}")
    print(f"Columns     : {len(HEADERS)}")


if __name__ == "__main__":
    main()
