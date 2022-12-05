from typing import Generic

from nomenklatura.entity import CE


class Sink(Generic[CE]):
    def emit(self, entity: CE) -> None:
        raise NotImplemented

    def close(self) -> None:
        pass
