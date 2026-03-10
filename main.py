import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tools.ocr import get_ocr_engine

# routes
from tools.ocr.routes import router as ocr_router

import paddle
import paddleocr

print(f"PaddlePaddle 版本: {paddle.__version__}")
print(f"PaddleOCR 版本: {paddleocr.__version__}")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("正在加载OCR模型，请稍候...")
    try:
        get_ocr_engine()
        logger.info("OCR模型加载完成，服务就绪")
    except Exception as e:
        logger.error(f"模型加载失败: {str(e)}")
        raise
    yield


app = FastAPI(
    title="Common Tools",
    description="common tools for web applications",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Offline OCR Service", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}



app.include_router(ocr_router)


if __name__ == "__main__":
    import uvicorn

    logger.info("启动Common Tools服务...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
