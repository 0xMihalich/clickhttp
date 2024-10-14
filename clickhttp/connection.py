from typing import NamedTuple


class UserConn(NamedTuple):
    """Класс NamedTuple для получения данных из объекта BaseHook."""

    user: str
    password: str
    host: str
    port: int
    database: str


def get_conn(connection_id: str,) -> UserConn:
    """Получение UserConn из названия коннекта BaseHook."""

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
