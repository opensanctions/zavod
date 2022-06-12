import logging
from os import PathLike
from typing import Generator
from contextlib import contextmanager
from zavod import settings
from zavod.context import Zavod
from zavod.logs import configure_logging, get_logger

__version__ = "0.1.1"
__all__ = ["init", "context", "Zavod", "configure_logging", "get_logger", "settings"]


def init(verbose: bool = False, data_path: PathLike = settings.DATA_PATH) -> Zavod:
    """Initiate the zavod working environment and create a processing context."""
    level = logging.DEBUG if verbose else logging.INFO
    configure_logging(level=level)
    return Zavod(data_path=data_path)


@contextmanager
def init_context(
    verbose: bool = False, data_path: PathLike = settings.DATA_PATH
) -> Generator[Zavod, None, None]:
    ctx = init(verbose=verbose, data_path=data_path)
    try:
        yield ctx
    finally:
        ctx.close()
