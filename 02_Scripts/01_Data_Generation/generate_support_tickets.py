"""
================================================================================
Project         : CloudFlow SaaS Revenue & Churn Analytics
Script          : generate_support_tickets.py
Output          : data/source/support_tickets.xlsx
Developer       : Ritesh Herkal
Description     : Generates 100,000 synthetic support ticket records.
================================================================================
"""

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

from openpyxl import Workbook, load_workbook


# ==============================================================================
# CONFIGURATION
# ==============================================================================

RECORD_COUNT = 100_000
RANDOM_SEED = 20261026

CUSTOMERS_FILE = Path("00_Dataset/02_Generated/customers.csv")
OUTPUT_FILE = Path("00_Dataset/02_Generated/support_tickets.xlsx")

random.seed(RANDOM_SEED)

PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [35, 35, 22, 8]

CATEGORIES = [
    "Billing",
    "Technical",
    "Account Access",
    "Subscription",
    "Feature Request",
]
CATEGORY_WEIGHTS = [25, 30, 15, 20, 10]

STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
STATUS_WEIGHTS = [10, 15, 45, 30]

ASSIGNED_TEAMS = [
    "Customer Support",
    "Technical Support",
    "Billing Team",
    "Account Management",
]
TEAM_WEIGHTS = [30, 35, 20, 15]

HEADERS = [
    "TicketID",
    "CustomerID",
    "CreatedDate",
    "ResolvedDate",
    "Priority",
    "Category",
    "Status",
    "ResolutionTimeHours",
    "SatisfactionScore",
    "AssignedTeam",
]


# ==============================================================================
# LOAD CUSTOMER DATA
# ==============================================================================

def load_customers():
    """Load customer IDs and signup dates from customers.csv."""

    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customer source file not found: {CUSTOMERS_FILE}\n"
            "Run the customer generator from the project root first."
        )

    customers = []

    with CUSTOMERS_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {"CustomerID", "SignupDate"}
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"customers.csv must contain these columns: {required_columns}"
            )

        for row in reader:
            signup_date = date.fromisoformat(row["SignupDate"])

            customers.append({
                "CustomerID": row["CustomerID"],
                "SignupDate": signup_date,
            })

    if not customers:
        raise ValueError("No customers found in customers.csv.")

    return customers


# ==============================================================================
# GENERATE SUPPORT TICKETS
# ==============================================================================

def generate_ticket(ticket_number, customers, today):
    """Generate one synthetic support ticket."""

    customer = random.choice(customers)
    customer_id = customer["CustomerID"]
    signup_date = customer["SignupDate"]

    # Ensure the ticket is created after the customer's signup.
    earliest_date = min(signup_date, today)
    days_available = (today - earliest_date).days

    created_date = earliest_date + timedelta(
        days=random.randint(0, days_available)
    )

    status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

    resolved_date = None
    resolution_time_hours = None
    satisfaction_score = None

    if status in ("Resolved", "Closed"):
        max_resolution_days = (today - created_date).days

        # Tickets resolved on the creation date are permitted.
        resolution_days = random.randint(
            0, min(14, max_resolution_days)
        )

        resolved_date = created_date + timedelta(days=resolution_days)

        # Use a realistic positive duration, including same-day resolution.
        resolution_time_hours = round(
            resolution_days * 24 + random.uniform(0.5, 12),
            2,
        )

        # Satisfaction scores are not always provided.
        if random.random() < 0.75:
            satisfaction_score = random.choices(
                [1, 2, 3, 4, 5],
                weights=[5, 10, 20, 35, 30],
                k=1,
            )[0]

    return [
        f"TKT{ticket_number:06d}",
        customer_id,
        created_date,
        resolved_date,
        random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS, k=1)[0],
        random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS, k=1)[0],
        status,
        resolution_time_hours,
        satisfaction_score,
        random.choices(ASSIGNED_TEAMS, weights=TEAM_WEIGHTS, k=1)[0],
    ]


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("Starting Support Tickets data generation...")

    customers = load_customers()
    today = date.today()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write-only mode keeps memory usage lower for large Excel files.
    workbook = Workbook(write_only=True)
    worksheet = workbook.create_sheet(title="SupportTickets")
    worksheet.append(HEADERS)

    for ticket_number in range(1, RECORD_COUNT + 1):
        row = generate_ticket(ticket_number, customers, today)
        worksheet.append(row)

        if ticket_number % 10_000 == 0:
            print(f"Generated {ticket_number:,} / {RECORD_COUNT:,} records")

    workbook.save(OUTPUT_FILE)

    # Verify the generated workbook.
    check_workbook = load_workbook(
        OUTPUT_FILE,
        read_only=True,
        data_only=True,
    )
    check_sheet = check_workbook["SupportTickets"]

    total_rows = check_sheet.max_row - 1
    check_workbook.close()

    print("\nSupport Tickets generation completed.")
    print(f"Output file : {OUTPUT_FILE.resolve()}")
    print(f"Records     : {total_rows:,}")
    print(f"Columns     : {len(HEADERS)}")


if __name__ == "__main__":
    main()
