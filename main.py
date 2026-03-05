import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from paddleocr import PaddleOCR

import paddle
import paddleocr

print(f"PaddlePaddle 版本: {paddle.__version__}")
print(f"PaddleOCR 版本: {paddleocr.__version__}")

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 模型目录
MODEL_DIR = os.path.join(BASE_DIR, "models", "official_models")
# 临时文件目录
TEMP_DIR = os.path.join(BASE_DIR, "temp")
# 确保目录存在
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# 环境变量配置
os.environ["PADDLE_PDX_MODEL_DIR"] = MODEL_DIR
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"  # 禁用GPU
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_enable_pir_in_executor"] = "0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("正在加载OCR模型，请稍候...")
    try:
        get_ocr()
        logger.info("OCR模型加载完成，服务就绪")
    except Exception as e:
        logger.error(f"模型加载失败: {str(e)}")
        raise
    yield


app = FastAPI(
    title="Offline OCR Service",
    description="PaddleOCR based offline OCR service",
    lifespan=lifespan,
)

ocr = None


def get_ocr():
    """获取OCR实例"""
    global ocr
    if ocr is None:
        try:
            ocr = PaddleOCR(
                use_textline_orientation=True,
                lang="ch",
                text_detection_model_dir=os.path.join(MODEL_DIR, "PP-OCRv5_server_det"),
                text_recognition_model_dir=os.path.join(
                    MODEL_DIR, "PP-OCRv5_server_rec"
                ),
            )
            logger.info("OCR模型初始化成功")
        except Exception as e:
            logger.error(f"OCR模型初始化失败: {str(e)}")
            raise
    return ocr


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Offline OCR Service", "status": "running"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """OCR识别接口"""
    try:
        # 验证文件类型
        if not file.filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
        ):
            raise HTTPException(
                status_code=400, detail="不支持的文件类型，请上传图片文件"
            )

        logger.info(f"收到OCR请求: {file.filename}")

        # 读取和处理图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        if image.mode != "RGB":
            image = image.convert("RGB")

        # 保存临时文件
        temp_path = os.path.join(TEMP_DIR, "temp_ocr_input.jpg")
        image.save(temp_path)

        ocr_engine = get_ocr()
        result = ocr_engine.predict(temp_path)

        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # 处理识别结果
        if result is None or len(result) == 0 or result[0] is None:
            logger.info(f"未识别到文本: {file.filename}")
            return JSONResponse(content={"text": [], "message": "No text found"})

        texts = result[0].get("rec_texts", [])

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


if __name__ == "__main__":
    import uvicorn

    logger.info("启动OCR服务...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
