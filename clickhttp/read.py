from collections import OrderedDict
from json import loads
from typing import Dict, List, Union

from requests import Session, Response

from .dtypes import dt_detect, date, datetime, ZoneInfo
from .errors import FrameError
from .frame import FrameType, Frame, _FrameType
from .json_type import JsonType
from .sql_formatter import formatter


def read_frame(sess: Session,
               session_id: str,
               url: str,
               database: str,
               query: str,
               frame_type: _FrameType = FrameType.set("pandas"),
               timeout: int = 10,) -> Frame:
    """Результат выполнения запроса как датафрейм."""

    resp: Response = sess.post(url=url,
                               params={
                                   "database"  : database,
                                   "query"     : formatter(query),
                                   "session_id": session_id,
                               },
                               timeout=timeout,)
    
    code: int = resp.status_code
    text: str = resp.text

    if code != 200:
        raise FrameError(f"Status code: {code}. Error message: {text}")
    elif not text:
        return Frame([], [], None, 0.0, 0,)
    
    json: JsonType = loads(resp.content)
    stats: Dict[str, Union[int, float,]] = json["statistics"]

    columns: List[str] = [col["name"] for col in json["meta"]]
    types: List[str] = [col["type"] for col in json["meta"]]
    data: JsonType = json["data"]
    time_read: float = stats["elapsed"]
    bytes_read: int = stats["bytes_read"]

    dt_cols: Dict[int, Union[date, datetime, ZoneInfo,]] = {
        num: dt_detect(dtype)
        for num, dtype in enumerate(types)
        if dt_detect(dtype)
    }

    if dt_cols:
        for row in range(len(data)):
            for col, dtype in dt_cols.items():
                if data[row][col]:
                    data[row][col] = (dtype.fromisoformat(data[row][col]) if not isinstance(dtype, ZoneInfo)
                                      else datetime.fromisoformat(data[row][col]).replace(tzinfo=dtype))
                else:
                    data[row][col] = None

    if frame_type.name == "dask":
        frame = frame_type.value.from_dict(OrderedDict({col: [row[num] for row in data]
                                                        for num, col in enumerate(columns)}))
    elif frame_type.name == "numpy":
        try:
            from numpy import asarray
            frame = asarray(data)
        except ImportError:
            raise ModuleNotFoundError("numpy not installed. Use: pip install numpy")
    elif frame_type.name == "pandas":
        frame = frame_type.value(data=data, columns=columns)
    elif frame_type.name == "polars":
        frame = frame_type.value(data=data, schema=columns, orient="row")
    elif frame_type.name == "python":
        frame: JsonType = data
    elif frame_type.name == "vaex":
        try:
            from vaex import from_records
            frame = from_records([OrderedDict({columns[num]: col
                                  for num, col in enumerate(row)})
                                  for row in data])
        except ImportError:
            raise ModuleNotFoundError("vaex not installed. Use: pip install vaex")
    else:
        raise FrameError(f"Unknown type {frame_type.value}.")
    
    return Frame(columns, types, frame, time_read, bytes_read,)
