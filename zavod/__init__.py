import logging
from typing import Generator, Optional
from contextlib import contextmanager
from followthemoney.proxy import EntityProxy

from zavod import settings
from zavod.context import Zavod
from zavod.logs import configure_logging, get_logger
from zavod.util import PathLike

__version__ = "0.2.0"
__all__ = [
    "init",
    "context",
    "Zavod",
    "PathLike",
    "configure_logging",
    "get_logger",
    "settings",
]


def init(
    name: str,
    prefix: Optional[str] = None,
    verbose: bool = False,
    data_path: PathLike = settings.DATA_PATH,
) -> Zavod[EntityProxy]:
    """Initiate the zavod working environment and create a processing context."""
    level = logging.DEBUG if verbose else logging.INFO
    configure_logging(level=level)
    return Zavod(name, EntityProxy, prefix=prefix, data_path=data_path)


@contextmanager
def init_context(
    name: str,
    prefix: Optional[str] = None,
    verbose: bool = False,
    data_path: PathLike = settings.DATA_PATH,
) -> Generator[Zavod[EntityProxy], None, None]:
    ctx = init(name, prefix=prefix, verbose=verbose, data_path=data_path)
    try:
        yield ctx
    finally:
        ctx.close()
