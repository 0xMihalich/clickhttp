from re import sub

from sqlparse import format


def formatter(sql: str) -> str:
    """Форматирование запроса с удалением комментариев и лишних пробельных символов."""

    return sub('\\s+', ' ', format(sql=sql.rstrip().rstrip(";"), strip_comments=True,)).strip().rstrip()
