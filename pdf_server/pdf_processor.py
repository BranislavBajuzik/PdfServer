from pathlib import Path
from typing import List

import dramatiq
from pdf2image import convert_from_path
from PIL import Image
from pony.orm import db_session

from .database import Document, PdfStatus

__all__ = ["process_pdf"]


TARGET_RECTANGLE = 1200, 1600
TARGET_RATIO = TARGET_RECTANGLE[1] / TARGET_RECTANGLE[0]


def normalize_image(img: Image.Image) -> Image.Image:
    """Resize the picture so it fits into :ref:`TARGET_RECTANGLE` while preserving ratio."""
    ratio = img.height / img.width

    if TARGET_RATIO > ratio:
        scale = TARGET_RECTANGLE[0] / img.width
    else:
        scale = TARGET_RECTANGLE[1] / img.height

    width, height = int(img.width * scale), int(img.height * scale)

    img = img.resize((width, height), resample=Image.LANCZOS).convert("RGBA")

    ret = Image.new(img.mode, (width, height))

    ret.paste(img)

    return ret


@dramatiq.actor
def process_pdf(path: str) -> None:
    try:
        pages: List[Image.Image] = convert_from_path(path, dpi=500, fmt="png")
    except Exception:
        pages = []

    page_index = 0
    directory = Path(path).parent

    for page_index, page in enumerate(pages, 1):
        normalize_image(page).save(directory / f"{page_index}.png")

    with db_session:
        if doc := Document.get(int(directory.name)):
            doc.status = PdfStatus.DONE
            doc.n_pages = page_index
        # Else ????
