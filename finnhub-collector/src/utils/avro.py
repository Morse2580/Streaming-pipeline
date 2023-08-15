from io import BytesIO
from pathlib import Path

from avro import io, schema
from avro.io import BinaryEncoder


def avro_encode(data, data_schema):
    writer = io.DatumWriter(data_schema)
    bytes_writer = BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    return bytes_writer.getvalue()


def avro_decode(avro_message, data_schema):
    reader = io.DatumReader(data_schema)
    bytes_reader = io.BytesIO(avro_message)
    decoder = io.BinaryDecoder(bytes_reader)
    return reader.read(decoder)


def load_avro_schema(schema_path: str):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    conf_file_path = Path(BASE_DIR / "config" / schema_path)
    return schema.parse(open(conf_file_path).read())

