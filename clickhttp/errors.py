class ClickHttpError(Exception):
    """Base error class."""


class ClosedError(ClickHttpError):
    """Error when attempting to perform an action after session has been closed."""

    def __init__(self):
        super().__init__("Session is closed. Please, reopen session first!")


class FrameError(ClickHttpError):
    """Error retrieving DataFrame."""


class FrameMultiQueryError(ClickHttpError):
    """Error executing multiquery."""


class InsertError(ClickHttpError):
    """Error executing insert into table."""
