"""
NOTE: This pytest fixture was created by Gemini using AI Studio.
"""

import pytest
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal


@pytest.fixture
def random_hledger_csv(tmp_path: Path):
    """
    Generates a valid, randomized hledger CSV file.
    Each transaction is balanced (sum of amounts == 0).
    """
    csv_file: Path = tmp_path / "random_journal.csv"

    # Configuration for randomness
    NUM_TRANSACTIONS = 20
    COMMODITIES = ["₱", "$", "EUR"]
    ACCOUNTS = {
        "assets": [
            "assets:checking",
            "assets:cash",
            "assets:account_a",
            "assets:account_b",
            "assets:savings",
        ],
        "expenses": [
            "expenses:food",
            "expenses:commute",
            "expenses:fees",
            "expenses:rent",
            "expenses:cloud",
            "expenses:entertainment",
        ],
        "liabilities": ["liabilities:card", "liabilities:loan"],
        "income": ["income:salary", "income:gifts"],
    }
    PAYEES = [
        "Uber",
        "ColdBucks",
        "JapaneseResto",
        "RamenHouse",
        "Me",
        "Amazon",
        "Netflix",
        "Landlord",
        "Employer",
    ]
    NOTES = [
        "Lunch",
        "Dinner",
        "Weekly Grocery",
        "Commute to Office",
        "Subscription",
        "Bonus",
        "Cash Withdrawal",
    ]

    headers = [
        "txnidx",
        "date",
        "code",
        "description",
        "account",
        "amount",
        "commodity",
        "status",
        "notes",
    ]
    rows = []

    start_date = datetime(2026, 1, 1)

    for i in range(1, NUM_TRANSACTIONS + 1):
        # 1. Setup Transaction Metadata
        txn_idx = i
        date = (start_date + timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d")
        payee = random.choice(PAYEES)
        note = random.choice(NOTES)
        description = f"{payee} | {note}"
        commodity = random.choice(COMMODITIES)

        # 2. Generate Postings (Legs)
        # Most transactions have 2 postings, some have 3 or 4
        num_postings = random.choices([2, 3, 4], weights=[70, 20, 10])[0]

        txn_postings = []
        running_balance = Decimal("0.00")

        for p_idx in range(num_postings):
            # If it's the last posting, it MUST balance the transaction to zero
            if p_idx == num_postings - 1:
                amount = -running_balance
                # Pick a logical offset account (Asset or Liability)
                account_cat = random.choice(["assets", "liabilities"])
            else:
                # Generate a random amount
                amount = Decimal(str(round(random.uniform(10.0, 500.0), 2)))
                running_balance += amount
                # Pick a logical source account (usually Expense or Asset transfer)
                account_cat = random.choice(["expenses", "assets", "income"])

            account = random.choice(ACCOUNTS[account_cat])

            txn_postings.append(
                [
                    txn_idx,
                    date,
                    "",
                    description,
                    account,
                    f"{amount:.2f}",
                    commodity,
                    random.choice(["*", "!", ""]),
                    "",
                ]
            )

        rows.extend(txn_postings)

    # Write to CSV
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return csv_file


def test_csv_structure(random_hledger_csv):
    with open(random_hledger_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

        assert len(data) > 0
        # Verify the first transaction is balanced
        first_id = data[0]["txnidx"]
        first_txn = [Decimal(r["amount"]) for r in data if r["txnidx"] == first_id]
        assert sum(first_txn) == Decimal("0.00")
