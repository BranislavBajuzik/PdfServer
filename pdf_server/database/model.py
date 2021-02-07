from pony.orm import *


__all__ = ["db", "db_session", "select", "delete", "commit", "rollback"]


db = Database()


class Document(db.Entity):
    id = PrimaryKey(int, auto=True)
    processing_status = Required(int, size=8)
    n_pages = Required(int, size=16)
