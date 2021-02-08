"""This file contains nothing but dirty hacks.

However, it is necessary, as those hacks make our lives easier
"""

__all__: list = []


def single_pony_exception() -> None:
    """Encapsulate all Pony exceptions.

    PonyORM doesn't have a single Exception at the top of its Exception hierarchy.
    """
    import builtins

    from pdf_server.exceptions import DatabaseException

    original_exception = builtins.Exception

    builtins.Exception = DatabaseException  # type: ignore
    import pony.orm  # noqa: F401  # Do the magic

    builtins.Exception = original_exception  # type: ignore


# Apply patches
single_pony_exception()
