from typing import List, Optional

from pydantic import BaseModel


class TradeEventPayload(BaseModel):
    c: Optional[List[str]] = []
    p: float
    s: str
    t: int
    v: float


class TradeEventMessage(BaseModel):
    data: List[TradeEventPayload]
    type: str
