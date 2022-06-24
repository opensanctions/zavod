from typing import Generic

from followthemoney.proxy import E


class Sink(Generic[E]):
    def emit(self, entity: E) -> None:
        raise NotImplemented

    def close(self) -> None:
        pass
