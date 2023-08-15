import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.handlers.error_handler import validation_exception_handler
from src.routes import collector

app = FastAPI()


app.include_router(collector.router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)