from sqlparse import format


def formatter(sql: str) -> str:
    """Форматирование запроса с удалением комментарией."""

    return format(sql=sql.rstrip().rstrip(";"),
                  strip_comments=True,)
