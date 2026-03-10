import os
import logging
from typing import List, Optional

from paddleocr import PaddleOCR

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(BASE_DIR, "models", "official_models")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.environ["PADDLE_PDX_MODEL_DIR"] = MODEL_DIR
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_enable_pir_in_executor"] = "0"


class OCREngine:
    def __init__(self):
        self._ocr = None

    def _initialize(self):
        if self._ocr is None:
            self._ocr = PaddleOCR(
                use_textline_orientation=True,
                lang="ch",
                text_detection_model_dir=os.path.join(MODEL_DIR, "PP-OCRv5_server_det"),
                text_recognition_model_dir=os.path.join(
                    MODEL_DIR, "PP-OCRv5_server_rec"
                ),
            )
            logger.info("OCR模型初始化成功")
        return self._ocr

    def recognize(self, image_path: str) -> List[str]:
        ocr_engine = self._initialize()
        result = ocr_engine.predict(image_path)

        if result is None or len(result) == 0 or result[0] is None:
            return []

        texts = result[0].get("rec_texts", [])
        return texts

    def recognize_from_image(self, image) -> List[str]:
        if image.mode != "RGB":
            image = image.convert("RGB")

        temp_path = os.path.join(TEMP_DIR, "temp_ocr_input.jpg")
        image.save(temp_path)

        try:
            texts = self.recognize(temp_path)
            return texts
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


_engine = None


def get_ocr_engine() -> OCREngine:
    global _engine
    if _engine is None:
        _engine = OCREngine()
    return _engine
