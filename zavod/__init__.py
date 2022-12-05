import logging
from pathlib import Path
from typing import Generator, Optional
from contextlib import contextmanager
from nomenklatura.entity import CompositeEntity
from followthemoney.util import PathLike

from zavod import settings
from zavod.context import GenericZavod
from zavod.logs import configure_logging, get_logger
from zavod.sinks.common import Sink
from zavod.sinks.file import JSONFileSink

__version__ = "0.4.2"
__all__ = [
    "init",
    "context",
    "Zavod",
    "PathLike",
    "configure_logging",
    "get_logger",
    "settings",
]

logging.getLogger("prefixdate").setLevel(logging.ERROR)


class Zavod(GenericZavod[CompositeEntity]):
    pass


def init(
    name: str,
    prefix: Optional[str] = None,
    verbose: bool = False,
    data_path: Path = settings.DATA_PATH,
    out_file: Optional[PathLike] = "fragments.json",
) -> Zavod:
    """Initiate the zavod working environment and create a processing context."""
    level = logging.DEBUG if verbose else logging.INFO
    configure_logging(level=level)
    sink: Optional[Sink[CompositeEntity]] = None
    if out_file is not None:
        out_path = data_path.joinpath(out_file)
        out_path.parent.mkdir(exist_ok=True, parents=True)
        sink = JSONFileSink[CompositeEntity](out_path)
    return Zavod(name, CompositeEntity, prefix=prefix, data_path=data_path, sink=sink)


@contextmanager
def init_context(
    name: str,
    prefix: Optional[str] = None,
    verbose: bool = False,
    data_path: Path = settings.DATA_PATH,
    out_file: Optional[PathLike] = "fragments.json",
) -> Generator[Zavod, None, None]:
    ctx = init(
        name,
        prefix=prefix,
        verbose=verbose,
        data_path=data_path,
        out_file=out_file,
    )
    try:
        yield ctx
    finally:
        ctx.close()
