from typing import Any

from deepface.DeepFace import represent

from app.constants import MANY_FACES_MESSAGE, MODEL
from app.service import ManyFacesError


class FaceVerification:
    """Face verification service."""

    def __init__(self, link: str, user_id: int) -> None:
        """Class constructor."""
        self.link = link
        self.user_id = user_id

    def represent(self) -> dict[str, Any]:
        """Face embedding from image."""
        result = represent(img_path=self.link, model_name=MODEL)
        if len(result) > 1:
            raise ManyFacesError(MANY_FACES_MESSAGE)
        return {
            'user_id': self.user_id,
            'link': self.link,
            'embedding': result[0]['embedding'],
        }
