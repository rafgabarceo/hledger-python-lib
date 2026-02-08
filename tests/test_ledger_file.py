from pathlib import Path
from tempfile import NamedTemporaryFile

from hledger_python_lib.hledger import LedgerFile


def test_initialization():
    with NamedTemporaryFile() as tf:
        path_to_ledger = Path(str(tf.name))
        ledger = LedgerFile(path_to_ledger)
