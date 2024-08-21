import pytest


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
