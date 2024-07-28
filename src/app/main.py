from contextlib import asynccontextmanager

import uvicorn
from deepface import DeepFace
from fastapi import FastAPI, HTTPException, Request, status

from app.api import router
from app.constants import MODEL
from app.service import ManyFacesError
from config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загрузка модели перед запуском API."""
    DeepFace.build_model(MODEL)  # type: ignore
    yield
    global model_obj  # noqa: WPS420
    model_obj = {}  # type: ignore


tags_metadata = [config.service.tags_metadata]  # type: ignore

app = FastAPI(
    title=config.service.title,  # type: ignore
    description=config.service.description,  # type: ignore
    tags_metadata=tags_metadata,
    debug=config.service.debug,  # type: ignore
)

app.include_router(
    router,
    prefix='/api',
    tags=[config.service.tags_metadata['name']],  # type: ignore
)


@app.exception_handler(ManyFacesError)
async def many_faces_error_handler(
    request: Request,
    exc: ManyFacesError,
):
    """Глобальный обработчик исключений для ManyFacesError."""
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
