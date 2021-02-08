import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import dramatiq
from pony.orm import commit

from pdf_server.database import Document, PdfStatus
from pdf_server.exceptions import BadEntityRequestException

from . import app

__all__ = ["PdfManager"]


@dramatiq.actor
def process_pdf(path: str) -> None:
    pass


@dataclass
class PdfInfo:
    status: PdfStatus
    n_pages: int

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status.name.lower(), "n_pages": self.n_pages}


class PdfManager:
    def __init__(self) -> None:
        self._root = Path(app.config["storage"]).absolute()
        self._logger = logging.getLogger(self.__class__.__name__)

    def upload(self, document_bytes: bytes) -> int:
        doc = Document(status=PdfStatus.PROCESSING, n_pages=0)

        commit()

        path = self._pdf_path(doc)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(document_bytes)

        process_pdf.send(str(path))

        return doc.id

    @staticmethod
    def get_info(document_id: int) -> PdfInfo:
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

        return self._page_path(doc, page_number)

    def _directory_path(self, document: Document) -> Path:
        return self._root / str(document.id)

    def _pdf_path(self, document: Document) -> Path:
        return self._directory_path(document) / "document.pdf"

    def _page_path(self, document: Document, page_number: int) -> Path:
        return self._directory_path(document) / f"{page_number}.png"
