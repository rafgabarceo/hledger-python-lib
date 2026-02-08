from asyncio import Lock
from dataclasses import dataclass, field
from pathlib import Path
from logging import Logger, getLogger

from duckdb import DuckDBPyConnection, connect

from hledger_python_lib.models.hledger import Account, LedgerFile


@dataclass
class BaseFile(LedgerFile):
    path_to_ledger: Path
    logger: Logger = field(default_factory=lambda: getLogger(__name__), init=False)
    _duck_conn: DuckDBPyConnection = field(init=False)

    def __post_init__(self):
        self._duck_conn = connect()
        self.logger.info(f"Loading ledger file @ {self.path_to_ledger} into memory.")
        _ = self._duck_conn.sql(
            f"CREATE TABLE hledger_table AS SELECT * FROM read_csv('{self.path_to_ledger}')"
        )
        self.logger.info(f"Ledger file loaded into DuckDB")

    def get_accounts_names(self) -> list[str]: ...
    def get_accounts(self) -> list[Account]: ...
    def get_account(self, acct_name: str) -> Account: ...
