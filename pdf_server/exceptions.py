from abc import ABC
from typing import Tuple

import flask

__all__ = [
    "PdfException",
    "DatabaseException",
    "RequestException",
    "BadRequestException",
    "UnauthorizedRequestException",
    "BadEntityRequestException",
]


class PdfException(Exception):
    """The exception at the top of hierarchy of this module."""

    code = 500
    error_description = "Internal error"

    @staticmethod
    def handler(exception: "PdfException") -> Tuple[flask.Response, int]:
        """Flask exception handler."""
        return flask.jsonify(error=f"{exception.error_description}: {exception}"), exception.code


class DatabaseException(PdfException):
    """The exception at the top of hierarchy of Pony ORM (enforced in patch.py)."""

    error_description = "Database error"


class RequestException(PdfException, ABC):
    """Base Exception for requests."""

    @property
    def error_description(self):
        """Error description."""
        return self.__class__.__name__


class BadRequestException(RequestException):
    """Concrete RequestException."""

    code = 400


class UnauthorizedRequestException(RequestException):
    """Concrete RequestException."""

    code = 403


class BadEntityRequestException(RequestException):
    """Concrete RequestException."""

    code = 422
