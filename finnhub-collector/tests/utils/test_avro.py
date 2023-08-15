import pytest

from src.utils import avro
from src.utils.avro import load_avro_schema


@pytest.fixture
def avro_encode(request):
    def encode(data, schema):
        return avro_encode(data, schema)

    return encode


@pytest.fixture
def avro_decode(request):
    def decode(avro_message, schema):
        return avro_decode(avro_message, schema)

    return decode


@pytest.mark.parametrize("data,schema", [
    ({"name": "John", "age": 30},
     {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}),
    ({"name": "Jane", "age": 31},
     {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}),
    (123, {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}),
    (None, {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]})
])
def test_avro_encode(avro_encode, data, schema):
    encoded_data = avro_encode(data, schema)
    assert encoded_data == b'\x1a\n\x04name\x08\x02John\x04age\x08\x0330'


@pytest.mark.parametrize("avro_message,schema", [
    (b'\x1a\n\x04name\x08\x02John\x04age\x08\x0330',
     {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}),
    (b'Invalid Avro data',
     {"type": "object", "properties": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]})
])
def test_avro_decode(avro_decode, avro_message, schema):
    try:
        result = avro_decode(avro_message, schema)
        assert result == {'name': 'John', 'age': 30}
    except AvroRuntimeException as e:
        assert str(e) == 'Invalid Avro data'


@pytest.mark.parametrize("schema_path", ['tests/avro_schemas/valid_schema.avsc'])
def test_load_avro_schema(schema_path):
    schema = load_avro_schema(schema_path)
    assert schema == {'type': 'object',
                      'properties': [{'name': 'name', 'type': 'string'}, {'name': 'age', 'type': 'int'}]}
