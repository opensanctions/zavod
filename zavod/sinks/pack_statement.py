import sys
import csv
import _csv
from io import TextIOWrapper
from typing import Optional
from nomenklatura.entity import CE
from nomenklatura.statement.serialize import pack_statement, PACK_COLUMNS
from followthemoney.util import PathLike

from zavod.sinks.common import FileSink


class PackStatementSink(FileSink[CE]):
    def __init__(self, path: PathLike) -> None:
        super().__init__(path)
        self.wrapper: Optional[TextIOWrapper] = None
        self.writer: Optional[_csv._writer] = None

    def emit(self, entity: CE) -> None:
        with self.lock:
            if self.fh is None:
                self.fh = open(self.path, "wb")
            if self.wrapper is None and self.fh is not None:
                self.wrapper = TextIOWrapper(self.fh, encoding="utf-8")
            if self.writer is None and self.wrapper is not None:
                self.writer = csv.writer(
                    self.wrapper,
                    dialect=csv.unix_dialect,
                    quoting=csv.QUOTE_MINIMAL,
                )
            if self.writer is not None:
                for stmt in entity.statements:
                    row = pack_statement(stmt)
                    self.writer.writerow([row.get(c) for c in PACK_COLUMNS])

    def close(self) -> None:
        with self.lock:
            if self.wrapper is not None:
                self.wrapper.close()
                self.wrapper = None
            super().close()

    def __repr__(self) -> str:
        return f"<PackStatementSink({self.path!r})>"
