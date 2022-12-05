import sys
from threading import Lock
from typing import BinaryIO, Optional
from nomenklatura.entity import CE
from followthemoney.util import PathLike
from followthemoney.cli.util import write_entity

from zavod.sinks.common import Sink


class JSONFileSink(Sink[CE]):
    def __init__(self, path: PathLike) -> None:
        self.path = path
        self.lock = Lock()
        self.fh: Optional[BinaryIO] = None

    def emit(self, entity: CE) -> None:
        with self.lock:
            if self.fh is None:
                if str(self.path) == "-":
                    self.fh = sys.stdout.buffer
                else:
                    self.fh = open(self.path, "wb")
            write_entity(self.fh, entity)

    def close(self) -> None:
        with self.lock:
            if self.fh is not None:
                if str(self.path) != "-":
                    self.fh.close()
                self.fh = None

    def __str__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return f"<JSONFileSink({self.path!r})>"
