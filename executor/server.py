from typing import Annotated

from fastapi import FastAPI, Form, Request, Response
import uvicorn

from logger import get_logger
from pipeline.pipeline import handle_batch_operation_webhook

logger = get_logger(__name__)

app = FastAPI()


@app.middleware("http")
async def debug(request: Request, call_next):
    body = await request.body()
    message = {
        "method": request.method,
        "path": str(request.url),
        "body": str(body),
    }
    logger.info(message)
    response = await call_next(request)
    message["status_code"] = response.status_code
    logger.info(message)
    return response


@app.get("/")
async def health_check():
    return Response()


@app.post("/")
async def webhook_callback(url: Annotated[str, Form(alias="data[response_body_url]")]):
    try:
        handle_batch_operation_webhook(url)
    except Exception as e:
        logger.warning(e)
    return Response()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
