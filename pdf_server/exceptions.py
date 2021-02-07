__all__ = [
    "PdfException",
    "RequestException",
    "UnauthorizedRequestException",
    "DatabaseException",
]


class PdfException(Exception):
    pass


class RequestException(PdfException):
    code: int


class UnauthorizedRequestException(RequestException):
    code = 403


class DatabaseException(PdfException):
    pass
