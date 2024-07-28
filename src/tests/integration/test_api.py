import pytest

from app.constants import MANY_FACES_MESSAGE


@pytest.mark.anyio
async def test_vector_generation(client, face_embedding_link, one_face_data):
    """Тест генерации вектора."""
    response = await client.post(face_embedding_link, json=one_face_data)
    assert response.status_code == 200
    response_data = response.json()
    assert 'user_id' in response_data
    assert 'link' in response_data
    assert 'embedding' in response_data
    assert len(response_data['embedding']) == 128


@pytest.mark.anyio
async def test_many_faces_error(client, face_embedding_link, many_faces_data):
    """Тест исключения (несколько лиц на изображении)."""
    response = await client.post(face_embedding_link, json=many_faces_data)
    assert response.status_code == 400
    assert response.json()['detail'] == MANY_FACES_MESSAGE
