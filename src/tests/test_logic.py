import pytest
from deepface.DeepFace import represent

from app.constants import *
from app.main import FaceVerification


def test_vector_generation(one_face_link):
    result = FaceVerification(one_face_link).represent()
    expected_result = {
        one_face_link: represent(one_face_link, MODEL)[0]["embedding"]
    }
    assert result == expected_result


def test_many_faces_error(many_faces_link):
    with pytest.raises((ValueError)) as excinfo:
        FaceVerification(many_faces_link).represent()
    assert str(excinfo.value) == MANY_FACES
