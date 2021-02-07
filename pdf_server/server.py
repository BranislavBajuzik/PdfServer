import patch  # Patch libraries
import logging
from flask import send_file
from typing import Any, Dict

from pdf_server.app import app
from pdf_server.api import api
from pdf_server.database import DatabaseConnection
from pdf_server.pdf_manager import PdfManager


@api(rule="/documents", methods=["POST"])
def pdf_upload():
    document_id = pdf_manager.upload(document=b"")

    return {"id": document_id}


@api(rule="/documents/<int:document_id>", methods=["GET"])
def pdf_info(document_id: int) -> Dict[str, Any]:
    info = pdf_manager.get_info(document_id)

    return {"status": info.status, "n_pages": info.n_pages}


@api(rule="/documents/<int:document_id>/pages/<int:number>", methods=["GET"])
def pdf_page(document_id: int, number: int):
    page_path = pdf_manager.get_page(document_id, number)

    return send_file(page_path, mimetype='image/jpeg')


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level="DEBUG")

    pdf_manager = PdfManager()

    with DatabaseConnection():
        app.run(host="0.0.0.0", threaded=True)
