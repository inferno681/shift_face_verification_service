import pytest


@pytest.fixture()
def one_face_data():
    """Correct image test data."""
    return {'user_id': 1, 'link': 'src/tests/images/one_face.jpg'}


@pytest.fixture()
def many_faces_data():
    """Incorrect image test data."""
    return {'user_id': 1, 'link': 'src/tests/images/many_faces.jpg'}


@pytest.fixture()
def consumer_test_data():
    """Kafka consumer test data."""
    return {1: 'src/tests/images/one_face.jpg'}
