"""
This file contains nothing but dirty hacks.
However, it is necessary, as those hacks make our lives easier
"""


def single_pony_exception():
    """Encapsulate all Pony exceptions because PonyORM doesn't have
    a single Exception at the top of its Exception hierarchy.
    """
    import builtins
    from exceptions import DatabaseException

    original_exception = builtins.Exception

    builtins.Exception = DatabaseException
    import pony.orm  # Do the magic

    builtins.Exception = original_exception


# Apply patches
single_pony_exception()
