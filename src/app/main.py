from deepface.DeepFace import represent

from app.constants import MANY_FACES_MESSAGE, MODEL


class FaceVerification:
    """Сервис верификации."""

    def __init__(self, link: str) -> None:
        """Конструктор класса."""
        self.link = link

    def represent(self) -> dict[str, list[float]]:
        """Функция получения эмбеддинга лица."""
        result = represent(img_path=self.link, model_name=MODEL)
        if len(result) > 1:
            raise ValueError(MANY_FACES_MESSAGE)
        return {self.link: result[0]['embedding']}
