from pathlib import Path
from tempfile import NamedTemporaryFile
from logging import DEBUG

import pytest

from hledger_python_lib.hledger import BaseFile


def test_initialization(random_hledger_csv, caplog):
    caplog.set_level(DEBUG)
    uut = LedgerFile(random_hledger_csv)
