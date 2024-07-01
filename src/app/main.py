from deepface import DeepFace

from app.constants import MANY_FACES, MODEL


class FaceVerification:
    def __init__(self, link: str) -> None:
        self.link = link

    def represent(self) -> list[float]:
        result = DeepFace.represent(img_path=self.link, model_name=MODEL)
        if len(result) > 1:
            raise ValueError(MANY_FACES)
        return {self.link: result[0]["embedding"]}
