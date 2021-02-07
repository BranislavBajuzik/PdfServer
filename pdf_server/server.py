import patch  # isort:skip  # noqa: F401  # Patch libraries, must be called first

import logging
from typing import Any, Dict

import flask

from pdf_server.api import api
from pdf_server.app import app
from pdf_server.database import DatabaseConnection
from pdf_server.exceptions import BadRequestException
from pdf_server.pdf_manager import PdfManager


@api(rule="/documents", methods=["POST"])
def pdf_upload() -> Dict[str, int]:
    if (doc := flask.request.files.get("document")) is None:
        raise BadRequestException("Form-data `document` is required")

    document_id = pdf_manager.upload(document=doc.read())

    return {"id": document_id}


@api(rule="/documents/<int:document_id>", methods=["GET"])
def pdf_info(document_id: int) -> Dict[str, Any]:
    return pdf_manager.get_info(document_id).to_dict()


@api(rule="/documents/<int:document_id>/pages/<int:number>", methods=["GET"])
def pdf_page(document_id: int, number: int) -> flask.Response:
    page_path = pdf_manager.get_page(document_id, number)

    return flask.send_file(page_path, mimetype="image/png")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level="DEBUG")

    pdf_manager = PdfManager()

    with DatabaseConnection():
        app.run(host="0.0.0.0", threaded=True)
