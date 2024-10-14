from typing import Dict, List
from uuid import uuid4

from requests import Session, Response

from .connection import get_conn, UserConn
from .errors import FrameMultiQueryError, ClickHttpError
from .frame import Frame, _FrameType
from .log import to_log
from .read import read_frame
from .sql_formatter import formatter


def clickhouse_multiquery(multiquery: str, connection: str,) -> None:
    """Функция для выполнения мультизапроса в одной сессии.
       Упрощенный вариант работы !!!ТОЛЬКО ДЛЯ Airflow!!!.
       Для запросов, требующих работу с temporary table,
       но не требующих возврат DataFrame с сервера."""

    if not isinstance(multiquery, str):
        raise ClickHttpError("Multi-Query must be a string.")
    elif not isinstance(connection, str):
        raise ClickHttpError("Airflow connection_id must be a string.")

    conn: UserConn = get_conn(connection)

    protocol: str = "https" if conn.port == 443 else "http"
    url: str = f"{protocol}://{conn.host}:{conn.port if conn.port != 9000 else 8123}"
    session_id: str = str(uuid4())
    headers: Dict[str, str,] = {
        "X-ClickHouse-User": conn.user,
        "X-ClickHouse-Key": conn.password,
    }

    to_log(f"Clickhouse Multi-Query session started. Session ID: {session_id}.")

    with Session() as sess:
        sess.headers.update(headers)

        for num, query in enumerate(formatter(multiquery).split(";")):
            resp: Response = sess.post(url=url,
                                       params={
                                           "database": conn.database,
                                           "query": query,
                                           "session_id": session_id,
                                       },)

            code: int = resp.status_code
            text: str = resp.text or "Empty"

            if code != 200:
                raise ClickHttpError(f"Status code: {code}. Error message: {text}")

            to_log(f"Part {num + 1} success. Server answer: {text}.")

    to_log("Clickhouse Multi-Query session finished.")


def send_multiquery(sess: Session,
                    session_id: str,
                    url: str,
                    database: str,
                    frame_type: _FrameType,
                    multiquery: str,
                    timeout: int = 10,) -> Frame:
    """Множественный запрос на сервер Clickhouse.
       Возвращается только последний фрейм."""

    _multiquery: List[str] = formatter(multiquery).split(";")

    for num, query in enumerate(_multiquery):

        to_log(f"Part {num + 1} started.")

        if num + 1 == len(_multiquery):
            frame: Frame = read_frame(sess=sess,
                                      session_id=session_id,
                                      url=url,
                                      database=database,
                                      query=query,
                                      frame_type=frame_type,)
            break

        resp: Response = sess.post(url=url,
                                   params={
                                       "database": database,
                                       "query": query,
                                       "session_id": session_id,
                                   },
                                   timeout=timeout,)

        code: int = resp.status_code
        text: str = resp.text or "Empty"

        if code != 200:
            raise FrameMultiQueryError(f"Status code: {code}. Error message: {text}")

        to_log(f"Part {num + 1} success.")

    to_log(f"Part {len(_multiquery)} success. All done.")

    return frame
