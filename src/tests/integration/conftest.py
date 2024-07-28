import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    """Бэкэнд для тестирования."""
    return 'asyncio'


@pytest.fixture
async def client():
    """Фикстура клиента."""
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
    return {'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Фикстура с некорректным изображением."""
    return {'link': 'src/tests/images/many_faces.jpg'}
