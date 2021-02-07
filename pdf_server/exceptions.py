__all__ = [
    "PdfException",
    "RequestException",
    "UnauthorizedRequestException",
    "BadEntityRequestException",
    "DatabaseException",
]


class PdfException(Exception):
    pass


class RequestException(PdfException):
    code: int


class UnauthorizedRequestException(RequestException):
    code = 403


class BadEntityRequestException(RequestException):
    code = 422


class DatabaseException(PdfException):
    pass
