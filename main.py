from fastapi import FastAPI, Request, Response

import models
from databse import engine
from routers import auth, todos, admin, users, healthcheck
import logging

app = FastAPI()

logging.basicConfig(
    filename="api_log.txt",
    filemode="a",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def api_logger(request: Request, call_next):
    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    log_message = {
        "host": request.url.hostname,
        "endpoint": request.url.path,
        "response": response_body.decode()
    }
    logger.debug(log_message)
    return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)


models.Base.metadata.create_all(bind=engine)

app.include_router(router=healthcheck.router)
app.include_router(router=auth.router)
app.include_router(router=todos.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)
