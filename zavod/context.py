from os import PathLike
from pathlib import Path
from zavod import settings


class Zavod(object):
    def __init__(self, prefix: str, data_path: PathLike = settings.DATA_PATH):
        self.data_path = Path(data_path).resolve()
        self.prefix = prefix

    def close(self) -> None:
        """Flush and tear down the context."""
        # self.http.close()
        # clear_contextvars()
