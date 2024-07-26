import pytest
from deepface.DeepFace import represent

from app.api import FaceVerificationResponse
from app.constants import MANY_FACES_MESSAGE, MODEL
from app.service import FaceVerification, ManyFacesError


def test_vector_generation(one_face_link):
    """Тест генерации вектора."""
    result = FaceVerification(one_face_link).represent()
    expected_result = FaceVerificationResponse(
        link=one_face_link,
        embedding=represent(one_face_link, MODEL)[0]['embedding'],
    )
    assert result == expected_result.model_dump()


def test_many_faces_error(many_faces_link):
    """Тест исключения (несколько лиц на изображении)."""
    with pytest.raises((ManyFacesError)) as excinfo:
        FaceVerification(many_faces_link).represent()
    assert str(excinfo.value) == MANY_FACES_MESSAGE
