from typing import Any


def is_namedtuple(connection: Any) -> bool:
    """Проверка объекта connection на принадлежность к NamedTuple."""

    return (isinstance(connection, tuple) and
            hasattr(connection, '_asdict') and
            hasattr(connection, '_fields'))
