"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_subscription_plans.py
Output          : data/source/subscription_plans.json
Developer       : Ritesh Herkal

Purpose:
    Generate 20 synthetic subscription plan master records.

Notes:
    - Uses only Python's standard library.
    - Prices are synthetic and expressed in USD.
    - Running the script overwrites the output JSON file.
================================================================================
"""

import json
from pathlib import Path

# Configuration
OUTPUT_PATH = Path("00_Dataset/02_Generated/subscription_plans.json")

PLANS = [
    {
        "PlanID": "PLAN001",
        "PlanName": "Starter Monthly",
        "PlanCategory": "Basic",
        "BillingCycle": "Monthly",
        "Price": 19.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN002",
        "PlanName": "Starter Annual",
        "PlanCategory": "Basic",
        "BillingCycle": "Annual",
        "Price": 199.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN003",
        "PlanName": "Basic Monthly",
        "PlanCategory": "Basic",
        "BillingCycle": "Monthly",
        "Price": 29.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-02-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN004",
        "PlanName": "Basic Annual",
        "PlanCategory": "Basic",
        "BillingCycle": "Annual",
        "Price": 299.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-02-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN005",
        "PlanName": "Growth Monthly",
        "PlanCategory": "Professional",
        "BillingCycle": "Monthly",
        "Price": 49.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN006",
        "PlanName": "Growth Annual",
        "PlanCategory": "Professional",
        "BillingCycle": "Annual",
        "Price": 499.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN007",
        "PlanName": "Professional Monthly",
        "PlanCategory": "Professional",
        "BillingCycle": "Monthly",
        "Price": 79.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-03-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN008",
        "PlanName": "Professional Annual",
        "PlanCategory": "Professional",
        "BillingCycle": "Annual",
        "Price": 799.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-03-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN009",
        "PlanName": "Business Monthly",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Monthly",
        "Price": 149.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN010",
        "PlanName": "Business Annual",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Annual",
        "Price": 1499.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN011",
        "PlanName": "Enterprise Monthly",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Monthly",
        "Price": 299.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-04-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN012",
        "PlanName": "Enterprise Annual",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Annual",
        "Price": 2999.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2024-04-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN013",
        "PlanName": "Legacy Basic Monthly",
        "PlanCategory": "Basic",
        "BillingCycle": "Monthly",
        "Price": 14.99,
        "Currency": "USD",
        "IsActive": False,
        "EffectiveStartDate": "2022-01-01",
        "EffectiveEndDate": "2024-01-31"
    },
    {
        "PlanID": "PLAN014",
        "PlanName": "Legacy Basic Annual",
        "PlanCategory": "Basic",
        "BillingCycle": "Annual",
        "Price": 149.99,
        "Currency": "USD",
        "IsActive": False,
        "EffectiveStartDate": "2022-01-01",
        "EffectiveEndDate": "2024-01-31"
    },
    {
        "PlanID": "PLAN015",
        "PlanName": "Legacy Growth Monthly",
        "PlanCategory": "Professional",
        "BillingCycle": "Monthly",
        "Price": 39.99,
        "Currency": "USD",
        "IsActive": False,
        "EffectiveStartDate": "2022-06-01",
        "EffectiveEndDate": "2024-02-29"
    },
    {
        "PlanID": "PLAN016",
        "PlanName": "Legacy Growth Annual",
        "PlanCategory": "Professional",
        "BillingCycle": "Annual",
        "Price": 399.99,
        "Currency": "USD",
        "IsActive": False,
        "EffectiveStartDate": "2022-06-01",
        "EffectiveEndDate": "2024-02-29"
    },
    {
        "PlanID": "PLAN017",
        "PlanName": "Team Monthly",
        "PlanCategory": "Professional",
        "BillingCycle": "Monthly",
        "Price": 99.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2025-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN018",
        "PlanName": "Team Annual",
        "PlanCategory": "Professional",
        "BillingCycle": "Annual",
        "Price": 999.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2025-01-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN019",
        "PlanName": "Scale Monthly",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Monthly",
        "Price": 499.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2025-06-01",
        "EffectiveEndDate": None
    },
    {
        "PlanID": "PLAN020",
        "PlanName": "Scale Annual",
        "PlanCategory": "Enterprise",
        "BillingCycle": "Annual",
        "Price": 4999.99,
        "Currency": "USD",
        "IsActive": True,
        "EffectiveStartDate": "2025-06-01",
        "EffectiveEndDate": None
    }
]


def main() -> None:
    # Create the output directory if it does not exist.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write the subscription plans to JSON.
    with OUTPUT_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(PLANS, json_file, indent=4)
        json_file.write("\n")

    # Validate basic record counts.
    unique_plan_ids = {plan["PlanID"] for plan in PLANS}

    print(f"Generated {len(PLANS):,} subscription plans.")
    print(f"Unique PlanID count: {len(unique_plan_ids):,}")
    print(f"Output file: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
