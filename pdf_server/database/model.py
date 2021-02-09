from enum import IntEnum

from pony.orm import Database, Required

__all__ = ["db", "Document", "PdfStatus"]


db = Database()


class Document(db.Entity):  # type: ignore
    """ORM definition."""

    status = Required(int, size=8)
    n_pages = Required(int, size=16)


class PdfStatus(IntEnum):
    """Enum representing the state of a Document."""

    PROCESSING = 0
    DONE = 1
