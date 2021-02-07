import logging
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict

from pony.orm import commit

from pdf_server.app import app
from pdf_server.database import Document
from pdf_server.exceptions import BadEntityRequestException

__all__ = ["PdfManager"]


class PdfStatus(IntEnum):
    PROCESSING = 0
    DONE = 1


@dataclass
class PdfInfo:
    status: PdfStatus
    n_pages: int

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status.name.lower(), "n_pages": self.n_pages}


def page_path(document: Document, page_number: int) -> Path:
    return Path(document.id, f"{page_number:04d}")


class PdfManager:
    def __init__(self) -> None:
        self._root = Path(app.config["storage"])
        self._logger = logging.getLogger(self.__class__.__name__)

    def upload(self, document: bytes) -> int:
        doc = Document(status=PdfStatus.PROCESSING, n_pages=0)

        commit()

        return doc.id

    def get_info(self, document_id: int) -> PdfInfo:
        doc = Document.get(id=document_id)

        if doc is None:
            raise BadEntityRequestException(f"Document[{document_id}] not found")

        return PdfInfo(PdfStatus(doc.status), doc.n_pages)

    def get_page(self, document_id: int, page_number: int) -> Path:
        doc = Document.get(id=document_id)

        if not doc:
            raise BadEntityRequestException(f"Document[{document_id}] not found")

        if doc.status == PdfStatus.PROCESSING:
            raise BadEntityRequestException(f"Document[{document_id}] is still being processed")

        if not 0 < page_number <= doc.n_pages:
            raise BadEntityRequestException(f"Document[{document_id}] does not have page no.{page_number}")

        return self._root / page_path(doc, page_number)
