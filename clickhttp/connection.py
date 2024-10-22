from typing import NamedTuple


class UserConn(NamedTuple):
    """NamedTuple class for retrieving data from the BaseHook object."""

    user: str
    password: str
    host: str
    port: int
    database: str


def get_conn(connection_id: str,) -> UserConn:
    """Retrieving UserConn from the name of the BaseHook connection."""

    try:
        from airflow.hooks.base import BaseHook  # type: ignore

        conn = BaseHook.get_connection(connection_id)

        return UserConn(conn.login,
                        conn.password,
                        conn.host,
                        conn.port,
                        conn.schema,)
    except ImportError:
        raise ModuleNotFoundError("apache airflow not installed. Please, use pip install apache-airflow.")
