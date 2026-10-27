"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_payment_transactions.py
Output          : data/source/payment_transactions.json
Developer       : Ritesh Herkal

Purpose:
    Generate 500,000 synthetic payment transaction records.

Dependencies:
    - data/source/customers.csv
    - data/source/subscription_plans.json
    - Python standard library only

Notes:
    - Uses synthetic customer and plan records.
    - PaymentID is unique.
    - Failed and pending payments are not collected revenue.
    - RefundAmount never exceeds Amount.
    - Running the script overwrites the output JSON file.
================================================================================
"""

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

# Configuration
RECORD_COUNT = 500_000
RANDOM_SEED = 20261025

CUSTOMERS_PATH = Path("00_Dataset/02_Generated/customers.csv")
PLANS_PATH = Path("00_Dataset/02_Generated/subscription_plans.json")
OUTPUT_PATH = Path("00_Dataset/02_Generated/payment_transactions.json")

PAYMENT_METHODS = [
    "CreditCard",
    "DebitCard",
    "UPI",
    "BankTransfer",
]

PAYMENT_METHOD_WEIGHTS = [35, 25, 25, 15]

PAYMENT_STATUSES = [
    "Successful",
    "Failed",
    "Pending",
    "Refunded",
]

PAYMENT_STATUS_WEIGHTS = [80, 10, 5, 5]

TRANSACTION_TYPES = [
    "Initial",
    "Recurring",
    "OneTime",
]

TRANSACTION_TYPE_WEIGHTS = [15, 70, 15]


def load_customers() -> list[dict[str, str]]:
    """Load customer records from the existing CSV."""
    with CUSTOMERS_PATH.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        customers = list(csv.DictReader(file))

    if not customers:
        raise ValueError("Customer dataset is empty.")

    return customers


def load_plans() -> list[dict]:
    """Load subscription plans from the existing JSON."""
    with PLANS_PATH.open("r", encoding="utf-8") as file:
        plans = json.load(file)

    if not plans:
        raise ValueError("Subscription plan dataset is empty.")

    for plan in plans:
        plan["EffectiveStartDate"] = date.fromisoformat(
            plan["EffectiveStartDate"]
        )

        if plan["EffectiveEndDate"]:
            plan["EffectiveEndDate"] = date.fromisoformat(
                plan["EffectiveEndDate"]
            )

    return plans


def random_date_between(
    start_date: date,
    end_date: date,
    rng: random.Random,
) -> date:
    """Return a random date between the supplied dates, inclusive."""
    days = (end_date - start_date).days
    return start_date + timedelta(days=rng.randint(0, days))


def get_valid_plans(
    customer_signup_date: date,
    plans: list[dict],
    today: date,
) -> list[dict]:
    """Return plans whose effective periods overlap the customer's timeline."""
    valid_plans = []

    for plan in plans:
        plan_start = plan["EffectiveStartDate"]
        plan_end = plan["EffectiveEndDate"] or today

        if max(customer_signup_date, plan_start) <= min(today, plan_end):
            valid_plans.append(plan)

    return valid_plans


def generate_payment(
    payment_number: int,
    customer: dict[str, str],
    plans: list[dict],
    rng: random.Random,
    today: date,
) -> dict:
    """Generate one synthetic payment transaction."""

    signup_date = date.fromisoformat(customer["SignupDate"])

    eligible_plans = get_valid_plans(
        signup_date,
        plans,
        today,
    )

    if not eligible_plans:
        raise ValueError(
            f"No valid subscription plan for {customer['CustomerID']}."
        )

    plan = rng.choice(eligible_plans)

    # Keep the payment date within the customer and plan timelines.
    start_date = max(
        signup_date,
        plan["EffectiveStartDate"],
    )

    end_date = min(
        today,
        plan["EffectiveEndDate"] or today,
    )

    payment_date = random_date_between(
        start_date,
        end_date,
        rng,
    )

    amount = round(float(plan["Price"]), 2)

    payment_status = rng.choices(
        PAYMENT_STATUSES,
        weights=PAYMENT_STATUS_WEIGHTS,
        k=1,
    )[0]

    refund_amount = 0.00

    if payment_status == "Refunded":
        # Full or partial refund.
        refund_percentage = rng.choice([25, 50, 75, 100])
        refund_amount = round(
            amount * refund_percentage / 100,
            2,
        )

    return {
        "PaymentID": f"PAY{payment_number:06d}",
        "CustomerID": customer["CustomerID"],
        "PlanID": plan["PlanID"],
        "PaymentDate": payment_date.isoformat(),
        "Amount": amount,
        "Currency": "USD",
        "PaymentMethod": rng.choices(
            PAYMENT_METHODS,
            weights=PAYMENT_METHOD_WEIGHTS,
            k=1,
        )[0],
        "PaymentStatus": payment_status,
        "TransactionType": rng.choices(
            TRANSACTION_TYPES,
            weights=TRANSACTION_TYPE_WEIGHTS,
            k=1,
        )[0],
        "RefundAmount": refund_amount,
    }


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    today = date.today()

    print("Loading customer and subscription plan data...")

    customers = load_customers()
    plans = load_plans()

    customer_ids = {
        customer["CustomerID"]
        for customer in customers
    }

    plan_ids = {
        plan["PlanID"]
        for plan in plans
    }

    if len(customer_ids) != len(customers):
        raise ValueError("Duplicate CustomerID values found.")

    if len(plan_ids) != len(plans):
        raise ValueError("Duplicate PlanID values found.")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Generating {RECORD_COUNT:,} payment transactions...")

    # Write a valid JSON array incrementally to avoid holding
    # all 500,000 payment records in memory.
    with OUTPUT_PATH.open("w", encoding="utf-8") as json_file:
        json_file.write("[\n")

        for payment_number in range(1, RECORD_COUNT + 1):
            customer = rng.choice(customers)

            payment = generate_payment(
                payment_number,
                customer,
                plans,
                rng,
                today,
            )

            if payment_number > 1:
                json_file.write(",\n")

            json.dump(payment, json_file)

            if payment_number % 100_000 == 0:
                print(
                    f"Generated {payment_number:,} payment transactions..."
                )

        json_file.write("\n]\n")

    print("\nPayment transaction generation completed.")
    print(f"Records generated: {RECORD_COUNT:,}")
    print(f"Unique PaymentID count: {RECORD_COUNT:,}")
    print(f"Unique customers available: {len(customer_ids):,}")
    print(f"Subscription plans available: {len(plan_ids):,}")
    print(f"Output file: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()