class ClickHttpError(Exception):
    """Базовый класс ошибки."""


class ClosedError(ClickHttpError):
    """Ошибка при попытке выполнить действие после закрытия сессии."""

    def __init__(self):
        super().__init__("Session is closed. Please, reopen session first!")


class FrameError(ClickHttpError):
    """Ошибка получения дата фрейм."""


class FrameMultiQueryError(ClickHttpError):
    """Ошибка при выполнении множественного запроса."""


class InsertError(ClickHttpError):
    """Ошибка при выполнении Isert в таблицу."""
