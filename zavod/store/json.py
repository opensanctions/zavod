import orjson
from typing import BinaryIO
from followthemoney.proxy import E


def write_entity(fh: BinaryIO, entity: E) -> None:
    data = entity.to_dict()
    entity_id = data.pop("id")
    assert entity_id is not None, data
    sort_data = dict(id=entity_id)
    sort_data.update(data)
    out = orjson.dumps(sort_data, option=orjson.OPT_APPEND_NEWLINE)
    fh.write(out)
