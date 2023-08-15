from datetime import datetime

from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the details of the validation error
    error_messages = exc.errors()
    error_details = []
    for error_msg in error_messages:
        error_loc = ".".join(str(loc) for loc in error_msg["loc"])
        error_detail = {
            "location": error_loc,
            "type": error_msg["type"],
            "msg": error_msg["msg"],
            "ctx": error_msg["ctx"],
        }
        error_details.append(error_detail)

    # Build the response content with error details
    response_content = {
        "error": "Invalid payload",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "timestamp": datetime.now().isoformat(),
        "url": request.url._url,
        "details": error_details,
        "fix": "Ensure that the request payload follows the correct format.",
    }

    return JSONResponse(content=response_content, status_code=status.HTTP_400_BAD_REQUEST)
