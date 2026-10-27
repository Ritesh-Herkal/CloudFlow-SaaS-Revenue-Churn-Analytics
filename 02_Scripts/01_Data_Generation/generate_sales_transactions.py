"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_sales_transactions.py
Output          : data/source/sales_transactions.csv
Developer       : Ritesh Herkal
Description     : Generates 300,000 synthetic sales transactions.
================================================================================
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path
import json


# ==============================================================================
# CONFIGURATION
# ==============================================================================

RECORD_COUNT = 300_000
RANDOM_SEED = 20261027

CUSTOMERS_FILE = Path("00_Dataset/02_Generated/customers.csv")
PLANS_FILE = Path("00_Dataset/02_Generated/subscription_plans.json")
OUTPUT_FILE = Path("00_Dataset/02_Generated/sales_transactions.csv")

random.seed(RANDOM_SEED)

REGION_IDS = list(range(1, 9))

TRANSACTION_TYPES = ["New Sale", "Renewal", "Upgrade", "One-Time"]
TRANSACTION_TYPE_WEIGHTS = [30, 40, 20, 10]

SALES_CHANNELS = ["Direct", "Partner", "Online"]
SALES_CHANNEL_WEIGHTS = [45, 30, 25]

CURRENCIES = ["USD"]

HEADERS = [
    "TransactionID",
    "CustomerID",
    "PlanID",
    "TransactionDate",
    "TransactionType",
    "Quantity",
    "UnitPrice",
    "DiscountAmount",
    "TotalAmount",
    "Currency",
    "SalesChannel",
    "RegionID",
]


# ==============================================================================
# LOAD SOURCE DATA
# ==============================================================================

def load_customers():
    """Load customer identifiers and signup dates."""

    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customer file not found: {CUSTOMERS_FILE}"
        )

    customers = []

    with CUSTOMERS_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required = {"CustomerID", "SignupDate"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                f"customers.csv must contain: {sorted(required)}"
            )

        for row in reader:
            customers.append({
                "CustomerID": row["CustomerID"],
                "SignupDate": date.fromisoformat(row["SignupDate"]),
            })

    if not customers:
        raise ValueError("No customers found.")

    return customers


def load_plans():
    """Load subscription plan identifiers and prices."""

    if not PLANS_FILE.exists():
        raise FileNotFoundError(
            f"Subscription plans file not found: {PLANS_FILE}"
        )

    with PLANS_FILE.open("r", encoding="utf-8") as file:
        plans = json.load(file)

    if not isinstance(plans, list) or not plans:
        raise ValueError("subscription_plans.json must contain a non-empty list.")

    required = {"PlanID", "Price", "Currency", "BillingCycle"}

    for plan in plans:
        if not required.issubset(plan):
            raise ValueError(
                f"Plan is missing required fields: {sorted(required)}"
            )

        if float(plan["Price"]) < 0:
            raise ValueError(f"Negative price found for {plan['PlanID']}.")

    return plans


# ==============================================================================
# GENERATE TRANSACTIONS
# ==============================================================================

def generate_transactions(customers, plans):
    """Generate transactions and stream them to a CSV file."""

    today = date.today()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)

        for number in range(1, RECORD_COUNT + 1):
            customer = random.choice(customers)
            plan = random.choice(plans)

            signup_date = min(customer["SignupDate"], today)
            available_days = (today - signup_date).days

            transaction_date = signup_date + timedelta(
                days=random.randint(0, available_days)
            )

            quantity = 1

            # Use the source plan's price and currency.
            unit_price = round(float(plan["Price"]), 2)
            currency = plan["Currency"]

            # Discounts are 0%, 5%, 10%, or 15%.
            discount_rate = random.choice([0, 0.05, 0.10, 0.15])
            discount_amount = round(
                quantity * unit_price * discount_rate, 2
            )

            total_amount = round(
                quantity * unit_price - discount_amount, 2
            )

            transaction_type = random.choices(
                TRANSACTION_TYPES,
                weights=TRANSACTION_TYPE_WEIGHTS,
                k=1,
            )[0]

            sales_channel = random.choices(
                SALES_CHANNELS,
                weights=SALES_CHANNEL_WEIGHTS,
                k=1,
            )[0]

            region_id = random.choice(REGION_IDS)

            writer.writerow([
                f"TXN{number:06d}",
                customer["CustomerID"],
                plan["PlanID"],
                transaction_date.isoformat(),
                transaction_type,
                quantity,
                f"{unit_price:.2f}",
                f"{discount_amount:.2f}",
                f"{total_amount:.2f}",
                currency,
                sales_channel,
                region_id,
            ])

            if number % 50_000 == 0:
                print(f"Generated {number:,} / {RECORD_COUNT:,} transactions")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("Starting Sales Transactions data generation...")

    customers = load_customers()
    plans = load_plans()

    generate_transactions(customers, plans)

    print("\nSales Transactions generation completed.")
    print(f"Output file : {OUTPUT_FILE.resolve()}")
    print(f"Data records: {RECORD_COUNT:,}")
    print(f"Columns     : {len(HEADERS)}")


if __name__ == "__main__":
    main()
