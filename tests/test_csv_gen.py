import csv
from decimal import Decimal


def test_parsing_logic(random_hledger_csv):
    """
    Example test showing how to consume the fixture.
    """
    with open(random_hledger_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Verify we have data
        assert len(rows) > 0

        # Verify that all transactions balance to zero
        # Group by txnidx
        transactions = {}
        for row in rows:
            idx = row["txnidx"]
            if idx not in transactions:
                transactions[idx] = Decimal("0.00")
            transactions[idx] += Decimal(row["amount"])

        for idx, balance in transactions.items():
            assert balance == Decimal("0.00"), f"Transaction {idx} is not balanced!"
