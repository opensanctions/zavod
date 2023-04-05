from typing import BinaryIO
from nomenklatura.entity import CE
from nomenklatura.statement.serialize import write_json_statement

from zavod.sinks.common import FileSink


class JSONStatementSink(FileSink[CE]):
    def emit_locked(self, fh: BinaryIO, entity: CE) -> None:
        for stmt in entity.statements:
            write_json_statement(fh, stmt)

    def __repr__(self) -> str:
        return f"<JSONStatementSink({self.path!r})>"
