from pathlib import Path
from typing import Any, Generic, Optional, Type, Union
from followthemoney import model
from followthemoney.schema import Schema
from followthemoney.proxy import EntityProxy, E
from followthemoney.util import make_entity_id

from zavod import settings
from zavod.http import fetch_file, make_session
from zavod.util import join_slug, PathLike
from zavod.logs import get_logger


class Zavod(Generic[E]):
    def __init__(
        self,
        name: str,
        entity_type: Type[E],
        prefix: Optional[str] = None,
        data_path: PathLike = settings.DATA_PATH,
    ):
        self.name = name
        self.prefix = prefix
        self.entity_type = entity_type
        self.path = Path(data_path).resolve()
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

    def close(self) -> None:
        """Flush and tear down the context."""
        self.http.close()
