from enum import Enum
from dataclasses import dataclass

__all__ = ["PdfManager"]

from pathlib import Path


class PdfStatus(Enum):
    PROCESSING = 0
    DONE = 1


@dataclass
class PdfInfo:
    status: PdfStatus
    n_pages: int


class PdfManager:
    def upload(self, document: bytes) -> int:
        return 1

    def get_info(self, document_id: int) -> PdfInfo:
        return PdfInfo(PdfStatus.DONE, 9)

    def get_page(self, document_id: int, page_number: int) -> Path:
        return Path('file.jpg')

