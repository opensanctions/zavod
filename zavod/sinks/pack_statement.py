import _csv
from io import TextIOWrapper
from typing import Optional
from nomenklatura.entity import CE
from nomenklatura.statement.serialize import pack_row, pack_writer
from followthemoney.util import PathLike

from zavod.sinks.common import FileSink


class PackStatementSink(FileSink[CE]):
    def __init__(self, path: PathLike) -> None:
        super().__init__(path)
        self.fh = open(self.path, "wb")
        self.wrapper = TextIOWrapper(self.fh, encoding="utf-8")
        self.writer = pack_writer(self.wrapper)

    def emit(self, entity: CE) -> None:
        with self.lock:
            for stmt in entity.statements:
                self.writer.writerow(pack_row(stmt))

    def close(self) -> None:
        with self.lock:
            self.wrapper.close()
            super().close()

    def __repr__(self) -> str:
        return f"<PackStatementSink({self.path!r})>"
