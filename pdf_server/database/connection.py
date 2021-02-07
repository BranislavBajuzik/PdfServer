from pony.orm import set_sql_debug

from pdf_server.app import app
from pdf_server.exceptions import DatabaseException

from . import db

__all__ = ["DatabaseConnection"]


class DatabaseConnection:
    def __init__(self, debug: bool = False):
        self._connected = False

        set_sql_debug(debug)

    def connect(self) -> None:
        try:
            db.bind(provider="postgres", host="localhost", **app.config["database"])
        except DatabaseException:
            raise DatabaseException("Unable to connect to the database") from None

        db.generate_mapping(create_tables=True)

        self._connected = True

    def disconnect(self) -> None:
        if self._connected:
            db.disconnect()

    def __del__(self):
        self.disconnect()

    def __enter__(self) -> "DatabaseConnection":
        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
