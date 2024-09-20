import pytest


@pytest.fixture()
def one_face_data():
    """Фикстура с корректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Фикстура с некорректным изображением."""
    return {'user_id': 1, 'link': 'src/tests/images/many_faces.jpg'}


@pytest.fixture()
def consumer_test_data():
    """Фикстура с данными для теста консьюмера."""
    return {1: 'src/tests/images/one_face.jpg'}
