import logging

from ftmstore import get_dataset
from nomenklatura.entity import CE

from zavod.sinks.common import Sink

log = logging.getLogger(__name__)


class FtmStoreSink(Sink[CE]):
    def __init__(self, dataset: str) -> None:
        self.dataset = get_dataset(dataset)
        self.bulk = self.dataset.bulk()
        self.i = 0

    def emit(self, entity: CE) -> None:
        self.i += 1
        self.bulk.put(entity, self.i)

    def close(self) -> None:
        self.bulk.flush()

    def __str__(self) -> str:
        return str(self.dataset)

    def __repr__(self) -> str:
        return f"<FtmStoreSink({self.dataset!r})>"
