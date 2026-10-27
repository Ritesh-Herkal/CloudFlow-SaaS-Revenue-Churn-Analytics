"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_subscription_events.py
Output          : data/source/subscription_events.csv
Developer       : Ritesh Herkal

Purpose:
    Generate 500,000 synthetic subscription lifecycle events.

Dependencies:
    - data/source/customers.csv
    - data/source/subscription_plans.json
    - Python standard library only

Notes:
    - Uses synthetic customer and plan records.
    - EventID values are unique.
    - Annual plan prices are converted to monthly recurring revenue (MRR).
    - Running the script overwrites the output CSV.
================================================================================
"""

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

# Configuration
RECORD_COUNT = 500_000
RANDOM_SEED = 20261024

CUSTOMERS_PATH = Path("00_Dataset/02_Generated/customers.csv")
PLANS_PATH = Path("00_Dataset/02_Generated/subscription_plans.json")
OUTPUT_PATH = Path("00_Dataset/02_Generated/subscription_events.csv")

EVENT_TYPES = [
    "Created",
    "Renewed",
    "Upgraded",
    "Downgraded",
    "Cancelled",
    "Reactivated",
]

EVENT_WEIGHTS = [25, 30, 12, 8, 15, 10]


def load_customers() -> list[dict[str, str]]:
    """Load customer records from the existing CSV."""
    with CUSTOMERS_PATH.open("r", newline="", encoding="utf-8-sig") as file:
        customers = list(csv.DictReader(file))

    if not customers:
        raise ValueError("Customer dataset is empty.")

    return customers


def load_plans() -> list[dict]:
    """Load subscription plan records from the existing JSON."""
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


def is_plan_valid(plan: dict, event_date: date) -> bool:
    """Check whether a plan was effective on the event date."""
    start_date = plan["EffectiveStartDate"]
    end_date = plan["EffectiveEndDate"]

    return (
        start_date <= event_date
        and (end_date is None or event_date <= end_date)
    )


def calculate_mrr(plan: dict) -> float:
    """Convert annual plan prices to monthly recurring revenue."""
    price = float(plan["Price"])

    if plan["BillingCycle"] == "Annual":
        return round(price / 12, 2)

    return round(price, 2)


def generate_event(
    event_number: int,
    customer: dict[str, str],
    plans: list[dict],
    rng: random.Random,
    today: date,
) -> dict:
    """Generate one synthetic subscription event."""

    signup_date = date.fromisoformat(customer["SignupDate"])

    # Events begin no earlier than the first plan's effective date.
    earliest_date = max(
        signup_date,
        min(plan["EffectiveStartDate"] for plan in plans),
    )

    if earliest_date > today:
        raise ValueError(
            f"Customer {customer['CustomerID']} has a future signup date."
        )

    event_date = earliest_date + timedelta(
        days=rng.randint(0, (today - earliest_date).days)
    )

    eligible_plans = [
        plan for plan in plans
        if is_plan_valid(plan, event_date)
    ]

    if not eligible_plans:
        raise ValueError(
            f"No subscription plan is valid on {event_date}."
        )

    event_type = rng.choices(
        EVENT_TYPES,
        weights=EVENT_WEIGHTS,
        k=1,
    )[0]

    current_plan = rng.choice(eligible_plans)
    previous_plan_id = None
    new_plan_id = current_plan["PlanID"]
    associated_plan_id = current_plan["PlanID"]
    status = "Active"
    mrr = calculate_mrr(current_plan)

    if event_type == "Created":
        previous_plan_id = None
        new_plan_id = current_plan["PlanID"]
        status = "Active"
        mrr = calculate_mrr(current_plan)

    elif event_type == "Renewed":
        previous_plan_id = current_plan["PlanID"]
        new_plan_id = current_plan["PlanID"]
        status = "Active"
        mrr = calculate_mrr(current_plan)

    elif event_type in ("Upgraded", "Downgraded"):
        current_mrr = calculate_mrr(current_plan)

        if event_type == "Upgraded":
            alternatives = [
                plan for plan in eligible_plans
                if calculate_mrr(plan) > current_mrr
            ]
        else:
            alternatives = [
                plan for plan in eligible_plans
                if calculate_mrr(plan) < current_mrr
            ]

        if alternatives:
            previous_plan_id = current_plan["PlanID"]

            # Choose a plan with a higher or lower MRR, as appropriate.
            new_plan = rng.choice(alternatives)
            new_plan_id = new_plan["PlanID"]
            associated_plan_id = new_plan["PlanID"]
            mrr = calculate_mrr(new_plan)
        else:
            # If no suitable transition exists, use a renewal instead.
            event_type = "Renewed"
            previous_plan_id = current_plan["PlanID"]
            new_plan_id = current_plan["PlanID"]
            mrr = current_mrr

        status = "Active"

    elif event_type == "Cancelled":
        previous_plan_id = current_plan["PlanID"]
        new_plan_id = None
        associated_plan_id = current_plan["PlanID"]
        status = "Cancelled"
        mrr = 0.00

    elif event_type == "Reactivated":
        previous_plan_id = None
        new_plan_id = current_plan["PlanID"]
        status = "Active"
        mrr = calculate_mrr(current_plan)

    return {
        "EventID": f"EVT{event_number:06d}",
        "CustomerID": customer["CustomerID"],
        "PlanID": associated_plan_id,
        "EventType": event_type,
        "EventDate": event_date.isoformat(),
        "PreviousPlanID": previous_plan_id,
        "NewPlanID": new_plan_id,
        "SubscriptionStatus": status,
        "MonthlyRecurringRevenue": mrr,
    }


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    today = date.today()

    print("Loading customer and subscription plan data...")

    customers = load_customers()
    plans = load_plans()

    customer_ids = {customer["CustomerID"] for customer in customers}
    plan_ids = {plan["PlanID"] for plan in plans}

    if len(customer_ids) != len(customers):
        raise ValueError("Duplicate CustomerID values found.")

    if len(plan_ids) != len(plans):
        raise ValueError("Duplicate PlanID values found.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "EventID",
        "CustomerID",
        "PlanID",
        "EventType",
        "EventDate",
        "PreviousPlanID",
        "NewPlanID",
        "SubscriptionStatus",
        "MonthlyRecurringRevenue",
    ]

    print(f"Generating {RECORD_COUNT:,} subscription events...")

    # Stream records directly to CSV instead of holding 500,000 rows in memory.
    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for event_number in range(1, RECORD_COUNT + 1):
            customer = rng.choice(customers)

            event = generate_event(
                event_number,
                customer,
                plans,
                rng,
                today,
            )

            writer.writerow(event)

            if event_number % 100_000 == 0:
                print(f"Generated {event_number:,} events...")

    print("\nSubscription event generation completed.")
    print(f"Records generated: {RECORD_COUNT:,}")
    print(f"Unique customers available: {len(customer_ids):,}")
    print(f"Subscription plans available: {len(plan_ids):,}")
    print(f"Output file: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
