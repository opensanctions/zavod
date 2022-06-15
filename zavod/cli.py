import json
import click
import logging
import asyncio
from pathlib import Path
from typing import Optional, Generator, Tuple
from followthemoney import model
from followthemoney.proxy import EntityProxy

from zavod.logs import configure_logging, get_logger
from zavod.store import write_entity

log = get_logger(__name__)


@click.group(help="Zavod data factory")
def cli() -> None:
    configure_logging(level=logging.INFO)


@cli.command("sorted-merge", help="Merge sorted entities")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-o", "--out-path", type=click.Path(dir_okay=False, path_type=Path), default="-"
)
def apply(path: Path, out_path: Path) -> None:
    entity: Optional[EntityProxy] = None
    with open(out_path, "wb") as outfh:
        with open(path, "r") as fh:
            while True:
                line = fh.readline()
                if not line:
                    break
                data = json.loads(line)
                next_entity = EntityProxy.from_dict(model, data)
                if entity is None:
                    entity = next_entity
                    continue
                if next_entity.id == entity.id:
                    entity = entity.merge(next_entity)
                    continue
                write_entity(outfh, entity)
                entity = next_entity

        if entity is not None:
            write_entity(outfh, entity)
