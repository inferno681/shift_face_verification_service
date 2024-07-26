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


app = FastAPI(debug=config.service.debug)  # type: ignore

app.include_router(router)


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
