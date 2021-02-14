import flask

from pdf_server.exceptions import BadRequestException

from .pdf_manager import PdfManager
from .requests import api

__all__: list = []

pdf_manager = PdfManager()


@api(rule="/documents", methods=["POST"])
def pdf_upload() -> flask.Response:
    """Upload PDF for processing."""
    if (doc := flask.request.files.get("document")) is None:
        raise BadRequestException("Form-data `document` is required")

    document_id = pdf_manager.upload(document_bytes=doc.read())

    return flask.jsonify({"id": document_id})


@api(rule="/documents/<int:document_id>", methods=["GET"])
def pdf_info(document_id: int) -> flask.Response:
    """Get info about the requested PDF.

    :param document_id: Id of the requested document.
    """
    return flask.jsonify(pdf_manager.get_info(document_id).to_dict())


@api(rule="/documents/<int:document_id>/pages/<int:number>", methods=["GET"])
def pdf_page(document_id: int, number: int) -> flask.Response:
    """Get PNG of the Requested page.

    :param document_id: Id of the requested document.
    :param number: Number of the requested page.
    """
    page_path = pdf_manager.get_page(document_id, number)

    return flask.send_file(page_path, mimetype="image/png")
