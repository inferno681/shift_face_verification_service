import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, drop_database

from config import config


@pytest.fixture(scope='session', autouse=True)
async def clear_database():
    """Фикстура подготовки базы данных для тестов."""
    config.service.db_name = 'test_db'
    create_database(config.sync_database_url)
    engine = create_async_engine(url=config.database_url)
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS "user" (
          "id" serial PRIMARY KEY,
          "login" varchar UNIQUE,
          "hashed_password" varchar,
          "balance" integer,
          "is_verified" bool DEFAULT false
);
            """,
            ),
        )
        await conn.execute(
            text(
                """
            INSERT INTO "user" (login, hashed_password, balance)
            VALUES ('login', 'hashed_password', 1000);
            """,
            ),
        )
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector;'))
        await conn.commit()
        from app.db import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text('DROP EXTENSION IF EXISTS vector;'))
        await conn.commit()
    drop_database(config.sync_database_url)
    await engine.dispose()


@pytest.fixture(scope='session')
def anyio_backend():
    """Бэкэнд для тестирования."""
    return 'asyncio'


@pytest.fixture
async def client(monkeypatch):
    """Фикстура клиента."""
    from app.main import app

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://127.0.0.1:8000/api/',
        ) as client:
            yield client


@pytest.fixture
def face_embedding_link():
    """Ссылка на формирование эмбеддинга."""
    return '/face_embedding'


@pytest.fixture()
def one_face_data():
    """Фикстура с корректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Фикстура с некорректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/many_faces.jpg'}
