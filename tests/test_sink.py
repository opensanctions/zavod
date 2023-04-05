import tempfile
from pathlib import Path
from followthemoney import model
from nomenklatura.entity import CompositeEntity
from zavod.sinks import JSONStatementSink, JSONEntitySink

tmp_dir = Path(tempfile.mkdtemp())

ENTITY = {
    "id": "bla",
    "schema": "Person",
    "datasets": ["test"],
    "properties": {
        "name": ["John Doe"],
        "birthDate": ["1976"],
        "country": ["us"],
    },
}


def test_entity_sink():
    entity = CompositeEntity.from_dict(model, ENTITY)
    assert len(list(entity.statements)) == 4
    path = tmp_dir / "test.json"
    sink = JSONEntitySink(path)
    sink.emit(entity)
    sink.close()
    assert repr(path) in repr(sink)

    with open(path, "r") as fh:
        assert len(fh.readlines()) == 1


def test_statement_sink():
    entity = CompositeEntity.from_dict(model, ENTITY)
    assert len(list(entity.statements)) == 4
    path = tmp_dir / "stmts.json"
    sink = JSONStatementSink(path)
    sink.emit(entity)
    sink.close()
    assert repr(path) in repr(sink)

    with open(path, "r") as fh:
        assert len(fh.readlines()) == 4
