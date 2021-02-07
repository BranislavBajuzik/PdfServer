from pony.orm import Database, Required

__all__ = ["db", "Document"]


db = Database()


class Document(db.Entity):  # type: ignore
    status = Required(int, size=8)
    n_pages = Required(int, size=16)
