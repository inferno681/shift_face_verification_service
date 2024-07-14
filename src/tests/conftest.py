import pytest


@pytest.fixture()
def one_face_link():
    """Фикстура с корректным изображением."""
    return 'src/tests/images/one_face.jpg'


@pytest.fixture()
def many_faces_link():
    """Фикстура с некорректным изображением."""
    return 'src/tests/images/many_faces.jpg'
