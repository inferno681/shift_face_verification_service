from fastapi import APIRouter

from app.api.schemes import FaceVerificationRequest, FaceVerificationResponse
from app.service import FaceVerification

router = APIRouter()


@router.post('/face_embedding', response_model=FaceVerificationResponse)
async def registration(link: FaceVerificationRequest):
    """Эндпоинт регистрации пользователя."""
    return FaceVerification(link.link).represent()
