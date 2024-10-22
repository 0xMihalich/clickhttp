from typing import Any


def is_namedtuple(connection: Any) -> bool:
    """Checking the connection object for its affiliation with NamedTuple."""

    return (isinstance(connection, tuple) and
            hasattr(connection, '_asdict') and
            hasattr(connection, '_fields'))
