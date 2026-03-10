import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from tools.printer.zebra.zebra import get_zebra_printer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/print", tags=["print"])


class PrintRequest(BaseModel):
    host: str = "localhost"
    port: int = 9100
    zpl: str


@router.post("/zebra")
async def print_zebra(request: PrintRequest):
    try:
        printer = get_zebra_printer(request.host, request.port)
        result = printer.send_label(request.zpl)

        if result["success"]:
            return {
                "status": "success",
                "message": "Label sent successfully",
                "printer": f"{request.host}:{request.port}",
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to send label to printer"
            )

    except Exception as e:
        logger.error(f"Print error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Print error: {str(e)}")
