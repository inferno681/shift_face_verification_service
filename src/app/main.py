from deepface.DeepFace import represent

from app.constants import MANY_FACES, MODEL


class FaceVerification:
    def __init__(self, link: str) -> None:
        self.link = link

    def represent(self) -> dict[str, list[float]]:
        result = represent(img_path=self.link, model_name=MODEL)
        if len(result) > 1:
            raise ValueError(MANY_FACES)
        return {self.link: result[0]["embedding"]}
