from asyncio import Lock
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from logging import Logger, getLogger

from duckdb import DuckDBPyConnection, connect

from hledger_python_lib.models.hledger import Account, HledgerCommand, HledgerCommandBuilder, LedgerFile, Transaction

HLEDGER_TABLE = "hledger_table"


@dataclass
class BaseFile(LedgerFile):
    path_to_ledger: Path
    logger: Logger = field(default_factory=lambda: getLogger(__name__), init=False)

    async def get_accounts(self) -> list[Account]: ...
    async def get_account(self, acct_name: str) -> Account: ...


@dataclass
class BaseAccount(Account):
    async def get_name(self) -> str: ...
    async def get_transactions(self) -> list[Transaction]: ...


@dataclass
class BaseTransaction(Transaction):
    async def get_credit(self) -> tuple[str, float]: ...
    async def get_debit(self) -> tuple[str, float]: ...
    async def get_date(self) -> datetime: ...

@dataclass
class BaseHledgerCommandBuilder(HledgerCommandBuilder):
