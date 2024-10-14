from enum import Enum
from logging import warning
from typing import List, NamedTuple, NewType, Union

from .json_type import JsonType


_dtypes: list = [JsonType, None,]
_enums: dict = {"python": list}

try:
    from dask.dataframe import DataFrame as da_frame
    _dtypes.append(da_frame)
    _enums.update({"dask": da_frame})
except ImportError:
    warning("dask not installed. Use: pip install dask dask[dataframe]")

try:
    from numpy import ndarray, datetime64
    _dtypes.append(ndarray)
    _enums.update({"numpy": ndarray})
except ImportError:
    warning("numpy not installed. Use: pip install numpy")
    from datetime import datetime
    from typing import Any

    class datetime64(datetime):
        """Заплатка для неверного импорта."""

        def astype(self: datetime, cls: Any) -> datetime:
            return self

try:
    from pandas import DataFrame as pd_frame
    _dtypes.append(pd_frame)
    _enums.update({"pandas": pd_frame})
except ImportError:
    warning("pandas not installed. Use: pip install pandas")

try:
    from polars import DataFrame as pl_frame
    _dtypes.append(pl_frame)
    _enums.update({"polars": pl_frame})
except ImportError:
    warning("polars not installed. Use: pip install polars")

try:
    from vaex.dataframe import DataFrameLocal as vx_frame
    _dtypes.append(vx_frame)
    _enums.update({"vaex": vx_frame})
except ImportError:
    warning("vaex not installed. Use: pip install vaex")


DTYPE = NewType("DTYPE", Union[tuple(_dtypes)])


class _FrameType(Enum):
    """Класс FrameType."""

    @classmethod
    def get_names(cls: "_FrameType") -> List[str]:
        """Вернуть список доступных значений."""

        return list(cls._member_map_)

    @classmethod
    def set(cls: "_FrameType", name: str) -> "_FrameType":
        """_FrameType.name если существует иначе _FrameType.python."""

        if name in cls.get_names():
            return cls[name]

        return cls["python"]


FrameType: _FrameType = _FrameType('FrameType', _enums)


class Frame(NamedTuple):
    """Полученный датафрейм."""

    columns: List[str]
    types: List[str]
    data: DTYPE  # type: ignore
    time_read: float
    bytes_read: int
