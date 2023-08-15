import logging
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from config.config import KafkaConf
from src.entities.model_entities import TradeEventMessage
from src.utils.avro import avro_encode, load_avro_schema
from src.utils.kafka import get_kafka_producer, send_to_kafka

router = APIRouter()


# construct the response for the POST method
def post_response(f):
    """Construct a JSON response for an endpoint."""

    @wraps(f)
    def wrap(request: Request, *args, **kwargs) -> Dict:
        results = f(request, *args, **kwargs)
        return {
            "message": "Data posted successfully",
            "method": request.method,
            "status-code": results["status-code"],
            "timestamp": datetime.now().isoformat(),
            "url": request.url._url,
        }

    return wrap


@router.post("/v1/collector", tags=["Collector"])
@post_response
def post_event_data(
        request: Request,
        data: TradeEventMessage,
):
    # Use automate data discovery and data catalogs to generate and maintain metadata => Data catalog
    data_dict = data.model_dump()

    # load in avro_schema
    avro_schema = load_avro_schema("trades.asvc")

    avro_message = avro_encode(
        {
            'data': data_dict['data'],
            'type': data_dict['type']
        },
        avro_schema
    )

    # Send the data to the Raw Events Topic if valid, or a Dead Letter Queue if there are errors
    try:
        producer = get_kafka_producer()
        send_to_kafka(producer, KafkaConf().config_values.kafka_topic_name, avro_message)

        response = {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
        }
        return response

    except Exception as e:
        # Return an error response if data couldn't be sent to Kafka
        return JSONResponse(content={"error": "Failed to send data to Kafka"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
