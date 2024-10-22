from logging import info
from typing import Any


def _msg(msg: Any) -> str:

    msg = str(msg)

    return f"\n{'-' * (len(msg) + 4)}\n| {msg} |\n{'-' * (len(msg) + 4)}"


def to_log(msg: Any) -> None:
    """Formatted log."""

    info(_msg(msg))
