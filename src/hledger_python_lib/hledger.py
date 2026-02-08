from asyncio import Lock
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from logging import Logger, getLogger
from typing import Self
from datetime import date

from duckdb import DuckDBPyConnection, connect

from hledger_python_lib.models.hledger import (
    Account,
    HledgerCommand,
    HledgerCommandBuilder,
    LedgerFile,
    Transaction,
    HLEDGER_OUTPUTS,
    HLEDGER_BASIC_REPORTS,
    HLEDGER_STD_REPORTS,
)

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
    _binary: str = field(init=False, default="/usr/bin/hledger")
    _file: str | None = field(init=False)
    _std_report: str | None = field(init=False)
    _basic_report: str | None = field(init=False)
    _start_date: str | None = field(init=False)
    _end_date: str | None = field(init=False)
    _account: str | None = field(init=False)
    _output: HLEDGER_OUTPUTS = field(init=False, default="csv")

    def with_binary(self, path_to_binary: str) -> Self:
        path = Path(path_to_binary)
        if not path.exists():
            raise Exception(f"Could not validate existence of hledger @ {path.name}")

        self._binary = str(path)
        return self

    def with_file(self, path: str) -> Self:
        file = Path(path)
        if not file.exists():
            raise Exception(f"Could not find ledger file @ {file.name}")
        self._file = str(file)
        return self

    def with_std_report(self, report: HLEDGER_STD_REPORTS) -> Self:
        self._std_report = report
        return self

    def with_basic_report(self, report: HLEDGER_BASIC_REPORTS) -> Self:
        self._basic_report = report
        return self

    def with_start_date(self, start_date: date) -> Self:
        if self._end_date is not None:
            end_date = date.fromisoformat(self._end_date)
            if end_date < start_date:
                raise Exception("End date cannot be before start date.")

        self._start_date = start_date.isoformat()
        return self

    def with_end_date(self, end_date: date) -> Self:
        if self._start_date is not None:
            start_date = date.fromisoformat(self._start_date)
            if start_date > end_date:
                raise Exception("Start date cannot be after end date.")

        self._end_date = end_date.isoformat()
        return self

    def with_account(self, account: str) -> Self:
        self._account = account
        return self

    def with_output(self, output: HLEDGER_OUTPUTS) -> Self:
        self._output = output
        return self

    def build(self) -> HledgerCommand: ...
