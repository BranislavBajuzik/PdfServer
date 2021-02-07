from collections import Callable
from functools import partial, wraps
from typing import Any

import flask
from pony.orm import db_session, rollback

from pdf_server.app import app
from pdf_server.exceptions import DatabaseException, PdfException, RequestException, UnauthorizedRequestException

__all__ = ["api"]

auth_token = app.config["auth_token"]


def assert_authorized() -> None:
    """Checks that the request is authorized."""

    if token := flask.request.headers.get("Authorization", default=None):
        token = token.split(" ")[1]

    if not auth_token == token:
        raise UnauthorizedRequestException("Invalid token")


def api(api_function: Callable = None, /, *, rule: str, **options: Any) -> Callable:
    """Wraps the :param api_function: to simplify (error) handling"""

    # Called with brackets: @api()
    if api_function is None:
        return partial(api, rule=rule, **options)

    # Called without brackets: @api

    @wraps(api_function)
    @db_session
    def handler(*args, **kwargs):
        try:
            try:
                assert_authorized()

                ret = api_function(*args, **kwargs)

                if issubclass(ret, flask.Response):
                    return ret
                if issubclass(ret, tuple):
                    return flask.jsonify(ret[0]), *ret[1:]

                return flask.jsonify(ret)

            except Exception as ex:
                rollback()
                raise ex

        except RequestException as ex:
            ret = flask.jsonify(error=str(ex)), ex.code
        except DatabaseException as ex:
            ret = flask.jsonify(error=f"Database error: {ex}"), 500
        except PdfException as ex:
            ret = flask.jsonify(error=f"Internal error: {ex}"), 500
        except Exception as ex:
            ret = flask.jsonify(error=f"Unknown error: {ex}"), 500

        return ret

    return app.route(rule, **options)(handler(api_function))
