# SCHEMA UTILS
from pydantic import ValidationError

from src.entities.model_entities import TradeEventMessage


def validate_entity_schema(schema):
    try:
        trade_message = TradeEventMessage.model_validate(schema)
        return True, None  # Validation succeeded
    except ValidationError as e:
        return False, str(e)

