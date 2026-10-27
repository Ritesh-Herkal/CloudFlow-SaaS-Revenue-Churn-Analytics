"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_customers.py
Output          : data/source/customers.csv
Developer       : Ritesh Herkal

Purpose:
    Generate 100,000 reproducible synthetic customer master records.

Notes:
    - Uses only Python's standard library.
    - Does not use real personal data; email addresses use example.com.
    - CustomerID is unique and stable for a given generation run.
    - RegionID values are placeholders for the region definitions to be
      documented and validated in the source-model tasks.
    - Running the script overwrites the output CSV.
================================================================================
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Configuration
RECORD_COUNT = 100_000
RANDOM_SEED = 20261022
START_DATE = date(2020, 1, 1)
END_DATE = date.today()
OUTPUT_PATH = Path("00_Dataset/02_Generated/customers.csv")

FIRST_NAMES = [
    "Aarav", "Aditi", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Meera",
    "Neha", "Rohan", "Saanvi", "Vihaan", "Aanya", "Dev", "Ira", "Kabir",
    "Maya", "Nikhil", "Priya", "Rahul", "Sara", "Tanvi", "Varun", "Zoya",
    "Alex", "Amelia", "Daniel", "Ella", "Ethan", "Grace", "Jacob", "Lily",
    "Lucas", "Mia", "Noah", "Olivia", "Ryan", "Sofia", "Thomas", "William",
]
LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Rao", "Iyer", "Nair", "Mehta", "Kapoor",
    "Joshi", "Desai", "Kulkarni", "Gupta", "Singh", "Verma", "Khan", "Das",
    "Brown", "Davis", "Garcia", "Johnson", "Miller", "Wilson", "Taylor",
    "Anderson", "Thomas", "Moore", "Martin", "Clark", "Lewis", "Walker",
]
CUSTOMER_SEGMENTS = ["SMB", "Mid-Market", "Enterprise", "Startup"]
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Retail", "Manufacturing",
    "Education", "Professional Services", "Media", "Logistics", "Hospitality",
]
COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
REGION_IDS = list(range(1, 9))


def random_date(rng: random.Random, start: date, end: date) -> date:
    """Return a random date between start and end, inclusive."""
    days = (end - start).days
    return start + timedelta(days=rng.randint(0, days))


def generate_customers(record_count: int = RECORD_COUNT) -> list[dict[str, object]]:
    """Generate deterministic synthetic customer records."""
    rng = random.Random(RANDOM_SEED)
    rows = []

    for customer_number in range(1, record_count + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        # Reserved example.com domain prevents use of real email addresses.
        email = f"customer{customer_number:06d}@cloudflow.com"

        rows.append({
            "CustomerID": f"CUST{customer_number:06d}",
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "SignupDate": random_date(rng, START_DATE, END_DATE).isoformat(),
            "RegionID": rng.choice(REGION_IDS),
            "CustomerSegment": rng.choice(CUSTOMER_SEGMENTS),
            "Industry": rng.choice(INDUSTRIES),
            "CompanySize": rng.choice(COMPANY_SIZES),
            "IsActive": rng.choices([True, False], weights=[85, 15], k=1)[0],
        })

    return rows


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_customers()

    fieldnames = [
        "CustomerID", "FirstName", "LastName", "Email", "SignupDate",
        "RegionID", "CustomerSegment", "Industry", "CompanySize", "IsActive",
    ]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows):,} customer records: {OUTPUT_PATH.resolve()}")
    print(f"Unique CustomerID count: {len({row['CustomerID'] for row in rows}):,}")
    print(f"Unique Email count: {len({row['Email'] for row in rows}):,}")


if __name__ == "__main__":
    main()
