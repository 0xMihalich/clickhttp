from datetime import date, datetime
from gzip import compress
from io import StringIO
from math import isnan
from typing import Any, Generator, Optional, Union
from uuid import UUID

from requests import Session, Response

from .errors import InsertError
from .frame import DTYPE, datetime64, FrameType
from .log import to_log


CHUNK_SIZE: int = 52_428_800


def to_str(col: Any) -> str:
    """Форматирование значения колонки в строку."""

    if isinstance(col, Union[str, UUID]):
        col = str(col).replace("'", "''")
        return f"'{col}'"
    elif isinstance(col, datetime):
        return f"'{col.strftime('%Y-%m-%d %H:%M:%S')}'"
    elif isinstance(col, date):
        return f"'{col.isoformat()}'"
    elif isinstance(col, datetime64):
        return to_str(col.astype(datetime))
    elif isinstance(col, float):
        if isnan(col):
            return to_str(None)
        return str(col).rstrip('0').rstrip('.')
    elif isinstance(col, list):
        list_string: str = ",".join(to_str(_col) for _col in col)
        return f"[{list_string}]"
    elif col is None:
        return "DEFAULT"
    return str(col)


def make_chunk(string: str,
               is_compressed: bool = True,) -> bytes:
    """Собрать пакет данных для отправки на сервер."""

    if is_compressed:
        return compress(data=string.encode("utf-8"), compresslevel=9,)

    return string.encode("utf-8")


def generate_chunks(data_frame: DTYPE,  # type: ignore
                    frame_type: str,
                    is_compressed: bool = True,
                    chunk_size: int = CHUNK_SIZE,) -> Generator[bytes, None, None]:
    """Разбить DataFrame на куски не более чем CHUNK_SIZE."""

    if frame_type == "dask":
        data_arr = data_frame.to_dask_array().compute()
    elif frame_type == "pandas":
        data_arr = data_frame.values
    elif frame_type == "polars":
        data_arr = data_frame.rows()
    elif frame_type == "vaex":
        data_arr = data_frame.to_pandas_df().to_numpy()
    elif frame_type in ("numpy", "python",):
        data_arr = data_frame

    io: StringIO = StringIO()

    start_row: int = 1
    total_rows: int = len(data_arr)

    for num, row in enumerate(data_arr):
        row_string: str = f"({','.join(to_str(col) for col in row)})"

        if io.tell() + len(row_string) > chunk_size:
            to_log(f"Sending chunk with {start_row}—{num + 1} rows from {total_rows} rows.")
            yield make_chunk(io.getvalue(), is_compressed,)
            io.truncate(0)
            io.seek(0)
            start_row = num + 1

        io.write(row_string)

    to_log(f"Sending chunk with {start_row}—{total_rows} rows from {total_rows} rows.")
    yield make_chunk(io.getvalue(), is_compressed,)


def insert_table(sess: Session,  # noqa: C901
                 session_id: str,
                 url: str,
                 database: str,
                 table: str,
                 data_frame: DTYPE,  # type: ignore
                 is_compressed: bool = True,
                 chunk_size: int = CHUNK_SIZE,
                 timeout: int = 10,
                 use_columns: bool = True,) -> None:
    """Записать DataFrame в целевую таблицу."""

    errmsg: Optional[str] = None
    columns: str = ""

    if is_compressed:
        sess.headers["Content-Encoding"] = "gzip"
        sep: str = "&"
    else:
        sep: str = "/?"

    try:
        try:
            frame_type: str = FrameType(type(data_frame)).name
        except ValueError:
            raise InsertError(f"DataFrame type {type(data_frame)} not accepted.")

        if use_columns:
            if frame_type in ("dask", "pandas", "polars", "vaex",):
                if frame_type == "vaex":
                    cols = data_frame.column_names
                else:
                    cols = data_frame.columns
                columns: str = f"({','.join(cols)}) "

        for data in generate_chunks(data_frame=data_frame,
                                    frame_type=frame_type,
                                    is_compressed=is_compressed,
                                    chunk_size=chunk_size,):
            resp: Response = sess.post(url=url + sep + "date_time_input_format=best_effort",
                                       data=data,
                                       params={
                                            "database": database,
                                            "query": f"INSERT INTO {table} {columns}VALUES",
                                            "session_id": session_id,
                                       },
                                       timeout=timeout,)

            if resp.status_code != 200:
                raise InsertError(resp.text)

            to_log("Insert chunk success.")
    except Exception as _errmsg:
        errmsg: str = _errmsg

    if is_compressed:
        del sess.headers["Content-Encoding"]

    if errmsg:
        raise InsertError(errmsg)

    to_log("Insert operation success.")
