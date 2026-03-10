import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io

from tools.ocr import get_ocr_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("")
async def ocr_image(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
        ):
            raise HTTPException(
                status_code=400, detail="不支持的文件类型，请上传图片文件"
            )

        logger.info(f"收到OCR请求: {file.filename}")

        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        ocr_engine = get_ocr_engine()
        texts = ocr_engine.recognize_from_image(image)

        logger.info(f"OCR识别完成: {file.filename}, 识别到 {len(texts)} 条文本")

        return JSONResponse(
            content={
                "filename": file.filename,
                "text": texts,
                "count": len(texts),
                "status": "success",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR识别失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR识别失败: {str(e)}")
