import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Literal, Optional

from followthemoney.util import PathLike
from nomenklatura.entity import CompositeEntity

from zavod import settings
from zavod.context import GenericZavod
from zavod.dataset import ZD, ZavodDataset
from zavod.logs import configure_logging, get_logger
from zavod.sinks.common import Sink
from zavod.sinks.file import JSONFileSink
from zavod.sinks.ftmstore import FtmStoreSink

SinkType = Literal["file", "ftmstore"]

__version__ = "0.5.4"
__all__ = [
    "init",
    "context",
    "Zavod",
    "ZavodDataset",
    "ZD",
    "PathLike",
    "configure_logging",
    "get_logger",
    "settings",
]

logging.getLogger("prefixdate").setLevel(logging.ERROR)


class Zavod(GenericZavod[CompositeEntity, ZavodDataset]):
    pass


def init(
    metadata_path: PathLike,
    verbose: bool = False,
    data_path: Path = settings.DATA_PATH,
    sink_type: Optional[SinkType] = "file",
    out_file: Optional[PathLike] = "fragments.json",
) -> Zavod:
    """Initiate the zavod working environment and create a processing context."""
    level = logging.DEBUG if verbose else logging.INFO
    configure_logging(level=level)
    sink: Optional[Sink[CompositeEntity]] = None
    dataset = ZavodDataset.from_path(metadata_path)
    if sink_type == "file":
        out_path = data_path.joinpath(out_file)
        out_path.parent.mkdir(exist_ok=True, parents=True)
        sink = JSONFileSink[CompositeEntity](out_path)
    elif sink_type == "ftmstore":
        sink = FtmStoreSink[CompositeEntity](dataset.name)
    return Zavod(dataset, CompositeEntity, data_path=data_path, sink=sink)


@contextmanager
def init_context(
    metadata_path: PathLike,
    verbose: bool = False,
    data_path: Path = settings.DATA_PATH,
    sink_type: Optional[SinkType] = "file",
    out_file: Optional[PathLike] = "fragments.json",
) -> Generator[Zavod, None, None]:
    ctx = init(
        metadata_path,
        verbose=verbose,
        data_path=data_path,
        sink_type=sink_type,
        out_file=out_file,
    )
    try:
        yield ctx
    finally:
        ctx.close()
