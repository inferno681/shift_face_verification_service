

from deepface import DeepFace

MODEL = "Facenet"


class FaceVerification:
    def __init__(self, link: str) -> None:
        self.link = link

    def represent(self) -> list:
        result = DeepFace.represent(img_path=self.link, model_name=MODEL)
        if len(result) > 1:
            return "more than 1 face"
        return result[0]['embedding']


print(FaceVerification('face.jpeg').represent())
