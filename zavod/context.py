from pathlib import Path
from typing import Any, Generic, Optional, Type, Union
from followthemoney import model
from followthemoney.schema import Schema
from followthemoney.proxy import E
from followthemoney.util import make_entity_id, PathLike

from zavod import settings
from zavod.http import fetch_file, make_session
from zavod.sinks.common import Sink
from zavod.util import join_slug
from zavod.logs import get_logger


class GenericZavod(Generic[E]):
    def __init__(
        self,
        name: str,
        entity_type: Type[E],
        sink: Optional[Sink[E]] = None,
        prefix: Optional[str] = None,
        data_path: Path = settings.DATA_PATH,
    ):
        self.name = name
        self.prefix = prefix
        self.entity_type = entity_type
        self.path = data_path
        self.sink = sink
        self.log = get_logger(name)
        self.http = make_session()

    def get_resource_path(self, name: PathLike) -> Path:
        path = self.path.joinpath(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def fetch_resource(
        self,
        name: str,
        url: str,
        auth: Optional[Any] = None,
        headers: Optional[Any] = None,
    ) -> Path:
        """Fetch a URL into a file located in the current run folder,
        if it does not exist."""
        return fetch_file(
            self.http,
            url,
            name,
            data_path=self.path,
            auth=auth,
            headers=headers,
        )

    def make(self, schema: Union[str, Schema]) -> E:
        """Make a new entity with some dataset context set."""
        return self.entity_type(model, {"schema": schema})

    def make_slug(
        self, *parts: str, strict: bool = True, prefix: Optional[str] = None
    ) -> Optional[str]:
        prefix = self.prefix if prefix is None else prefix
        slug = join_slug(*parts, prefix=prefix, strict=strict)
        if slug is not None:
            return slug[:255]
        return None

    def make_id(self, *parts: str, prefix: Optional[str] = None) -> Optional[str]:
        hashed = make_entity_id(*parts, key_prefix=self.name)
        if hashed is None:
            return None
        return self.make_slug(hashed, prefix=prefix, strict=True)

    def emit(self, entity: E) -> None:
        if self.sink is None:
            return None
        return self.sink.emit(entity)

    def close(self) -> None:
        """Flush and tear down the context."""
        self.http.close()
        if self.sink is not None:
            self.sink.close()
