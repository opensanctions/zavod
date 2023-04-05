import sys
from threading import Lock
from typing import Generic, BinaryIO, Optional
from followthemoney.util import PathLike

from nomenklatura.entity import CE


class Sink(Generic[CE]):
    def emit(self, entity: CE) -> None:
        raise NotImplemented

    def close(self) -> None:
        pass


class FileSink(Sink[CE]):
    def __init__(self, path: PathLike) -> None:
        self.path = path
        self.lock = Lock()
        self.fh: Optional[BinaryIO] = None

    def emit_locked(self, fh: BinaryIO, entity: CE) -> None:
        raise NotImplemented

    def emit(self, entity: CE) -> None:
        with self.lock:
            if self.fh is None:
                if str(self.path) == "-":
                    self.fh = sys.stdout.buffer
                else:
                    self.fh = open(self.path, "wb")
            self.emit_locked(self.fh, entity)

    def close(self) -> None:
        with self.lock:
            if self.fh is not None:
                if str(self.path) != "-":
                    self.fh.close()
                self.fh = None

    def __str__(self) -> str:
        return str(self.path)
