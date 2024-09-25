import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from deepface import DeepFace
from deepface.basemodels.Facenet import load_facenet128d_model
from fastapi import FastAPI, HTTPException, Request, status

from app.constants import MODEL
from app.service import ManyFacesError, consumer
from config import config

log = logging.getLogger('uvicorn')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Photo directory creation, model downloading, kafka consumer start and stop."""  # noqa: E501
    if not os.path.exists(config.service.photo_directory):  # type: ignore
        os.makedirs(config.service.photo_directory)  # type: ignore
    await consumer.start()
    log.info('Kafka consumer started')
    DeepFace.build_model(MODEL)  # type: ignore
    consumer_task = asyncio.create_task(consumer.consume())
    load_facenet128d_model()
    yield
    consumer_task.cancel()
    await consumer.stop()
    log.info('Kafka consumer stopped')
    global model_obj  # noqa: WPS420
    model_obj = {}  # type: ignore


app = FastAPI(
    title=config.service.title,  # type: ignore
    description=config.service.description,  # type: ignore
    debug=config.service.debug,  # type: ignore
    lifespan=lifespan,
)


@app.exception_handler(ManyFacesError)
async def many_faces_error_handler(
    request: Request,
    exc: ManyFacesError,
):
    """Exception handler (ManyFacesError)."""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,  # type: ignore
        port=config.service.port,  # type: ignore
    )  # noqa:WPS432
