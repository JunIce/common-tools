import logging
import socket
from typing import Optional

logger = logging.getLogger(__name__)


class ZebraPrinter:
    def __init__(self, host: str, port: int = 9100):
        self.host = host
        self.port = port

    def send(self, zpl: str) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((self.host, self.port))
                sock.sendall(zpl.encode("utf-8"))
            logger.info(f"ZPL sent to {self.host}:{self.port} successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send ZPL to {self.host}:{self.port}: {str(e)}")
            return False

    def send_label(self, zpl: str) -> dict:
        success = self.send(zpl)
        return {
            "success": success,
            "host": self.host,
            "port": self.port,
        }


_printer: Optional[ZebraPrinter] = None


def get_zebra_printer(host: str = "localhost", port: int = 9100) -> ZebraPrinter:
    global _printer
    if _printer is None:
        _printer = ZebraPrinter(host, port)
    return _printer
