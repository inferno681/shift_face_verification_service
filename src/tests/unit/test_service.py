import pytest
from deepface.DeepFace import represent

from app.constants import MANY_FACES_MESSAGE, MODEL


def test_vector_generation(one_face_data):
    """Тест генерации вектора."""
    from app.service import FaceVerification

    result = FaceVerification(**one_face_data).represent()
    expected_result = {
        'user_id': one_face_data['user_id'],
        'link': one_face_data['link'],
        'embedding': represent(one_face_data['link'], MODEL)[0]['embedding'],
    }
    assert result == expected_result


def test_many_faces_error(many_faces_data):
    """Тест исключения (несколько лиц на изображении)."""
    from app.service import FaceVerification, ManyFacesError

    with pytest.raises((ManyFacesError)) as excinfo:
        FaceVerification(**many_faces_data).represent()
    assert str(excinfo.value) == MANY_FACES_MESSAGE
