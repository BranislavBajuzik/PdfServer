from abc import ABC

__all__ = [
    "PdfException",
    "RequestException",
    "BadRequestException",
    "UnauthorizedRequestException",
    "BadEntityRequestException",
    "DatabaseException",
]


class PdfException(Exception):
    """The exception at the top of hierarchy of this module."""

    pass


class RequestException(PdfException, ABC):
    """Base Exception for requests."""

    code: int


class BadRequestException(RequestException):
    """Concrete RequestException."""

    code = 400


class UnauthorizedRequestException(RequestException):
    """Concrete RequestException."""

    code = 403


class BadEntityRequestException(RequestException):
    """Concrete RequestException."""

    code = 422


class DatabaseException(PdfException):
    """The exception at the top of hierarchy of Pony ORM (enforced in patch.py)."""

    pass
