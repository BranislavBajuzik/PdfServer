from collections import Callable
from functools import partial, wraps
from hmac import compare_digest
from typing import Any

import flask
from pony.orm import db_session, rollback

from pdf_server.exceptions import DatabaseException, PdfException, RequestException, UnauthorizedRequestException

from . import app

__all__ = ["api"]

auth_token = app.config["auth_token"]


app.register_error_handler(RequestException, RequestException.handler)
app.register_error_handler(DatabaseException, DatabaseException.handler)
app.register_error_handler(PdfException, PdfException.handler)
app.register_error_handler(Exception, lambda ex: (flask.jsonify(error=f"Unknown error: {ex}"), 500))


def assert_authorized() -> None:
    """Check that the request is authorized."""
    if token := flask.request.headers.get("Authorization", default=None):
        token = token.split(" ")[1]

    if not compare_digest(auth_token, token):
        raise UnauthorizedRequestException("Invalid token")


def api(api_function: Callable = None, /, *, rule: str, **options: Any) -> Callable:
    """Wrap the :param api_function: to simplify (error) handling."""
    # Called with brackets: @api()
    if api_function is None:
        return partial(api, rule=rule, **options)

    # Called without brackets: @api

    @wraps(api_function)
    @db_session
    def handler(*args, **kwargs):
        try:
            assert_authorized()

            return api_function(*args, **kwargs)

        except Exception as ex:
            rollback()
            raise ex

    return app.route(rule, **options)(handler)
