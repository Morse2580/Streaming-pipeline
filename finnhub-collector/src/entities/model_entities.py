from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel

from src.utils.avro import load_avro_schema


# class for the data schema for validation
class AvroEventDataSchema:
    def __init__(self, file_path="trades.asvc"):
        self.file_path = file_path
        load_avro_schema(self.file_path)


# Custom class for receiving the encoded avro data
class TradeEventPayload(BaseModel):
    c: Optional[List[str]] = []
    p: float
    s: str
    t: int
    v: float


class TradeEventMessage(BaseModel):
    data: List[TradeEventPayload]
    type: str


class InvalidEventPayload(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid payload")
