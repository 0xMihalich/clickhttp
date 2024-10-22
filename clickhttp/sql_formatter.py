from re import sub

from sqlparse import format


def formatter(sql: str) -> str:
    """Formatting query by removing comments and extra whitespace characters."""

    return sub('\\s+', ' ', format(sql=sql.rstrip().rstrip(";"), strip_comments=True,)).strip().rstrip()
