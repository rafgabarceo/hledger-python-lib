import pytest
import csv
import random
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal


@pytest.fixture
def random_hledger_csv():
    """
    NOTE: THIS PYTEST FIXTURE WAS CREATED WITH GEMINI.

    Generates a randomized, balanced hledger-style CSV using tempfile.
    The file is automatically deleted after the test finishes.
    """
    # 1. Setup Constants
    NUM_TRANSACTIONS = 20
    COMMODITIES = ["₱", "$", "EUR"]
    ACCOUNTS = {
        "assets": [
            "assets:checking",
            "assets:cash",
            "assets:account_a",
            "assets:savings",
        ],
        "expenses": [
            "expenses:food",
            "expenses:commute",
            "expenses:fees",
            "expenses:rent",
        ],
        "liabilities": ["liabilities:card", "liabilities:loan"],
        "income": ["income:salary", "income:gifts"],
    }
    PAYEES = ["Uber", "ColdBucks", "JapaneseResto", "RamenHouse", "Amazon", "Netflix"]

    # 2. Create the temporary file
    # delete=False allows us to close the file and let other processes/code
    # re-open it by path, which is common in CSV testing.
    tmp = tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv", encoding="utf-8"
    )
    file_path = tmp.name

    try:
        writer = csv.writer(tmp)
        writer.writerow(
            [
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
        )

        start_date = datetime(2026, 1, 1)

        for i in range(1, NUM_TRANSACTIONS + 1):
            date = (start_date + timedelta(days=random.randint(0, 60))).strftime(
                "%Y-%m-%d"
            )
            description = f"{random.choice(PAYEES)} | {random.randint(100, 999)}"
            commodity = random.choice(COMMODITIES)

            # Determine how many "legs" (postings) this transaction has
            num_postings = random.choices([2, 3], weights=[80, 20])[0]
            running_balance = Decimal("0.00")

            for p_idx in range(num_postings):
                if p_idx == num_postings - 1:
                    # Final leg: must balance to zero
                    amount = -running_balance
                    account = random.choice(
                        ACCOUNTS["assets"] + ACCOUNTS["liabilities"]
                    )
                else:
                    # Normal leg
                    amount = Decimal(str(round(random.uniform(5.0, 500.0), 2)))
                    running_balance += amount
                    account = random.choice(ACCOUNTS["expenses"] + ACCOUNTS["income"])

                writer.writerow(
                    [
                        i,  # txnidx
                        date,  # date
                        "",  # code
                        description,  # description
                        account,  # account
                        f"{amount:.2f}",  # amount
                        commodity,  # commodity
                        random.choice(["*", "!", ""]),  # status
                        "",  # notes
                    ]
                )

        tmp.close()  # Close the file so the test can open it
        yield file_path

    finally:
        # 3. Teardown: Ensure the file is deleted even if the test fails
        if os.path.exists(file_path):
            os.remove(file_path)
