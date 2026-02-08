import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from logging import DEBUG

import pytest

from hledger_python_lib.hledger import BaseFile


def test_initialization(random_hledger_csv):
    uut = BaseFile(random_hledger_csv)


@pytest.mark.asycnio
async def test_get_account_names(random_hledger_csv):
    expected_headers = []
    with open(random_hledger_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            expected_headers.append(row[4])
    uut = BaseFile(random_hledger_csv)
    headers = await uut.get_accounts()

    available_headers = [header.get_name() for header in headers]

    assert expected_headers.sort() == available_headers.sort()
