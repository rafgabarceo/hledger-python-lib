from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from hledger_python_lib.hledger import LedgerFile


def test_initialization(random_hledger_csv):
    uut = LedgerFile(random_hledger_csv)
