import csv
from decimal import Decimal


def test_csv_structure(random_hledger_csv):
    with open(random_hledger_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

        assert len(data) > 0
        # Verify the first transaction is balanced
        first_id = data[0]["txnidx"]
        first_txn = [Decimal(r["amount"]) for r in data if r["txnidx"] == first_id]
        assert sum(first_txn) == Decimal("0.00")
