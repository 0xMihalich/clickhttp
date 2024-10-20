from .connection import get_conn, UserConn
from .errors import ClickHttpError, ClosedError, FrameError, FrameMultiQueryError, InsertError
from .frame import FrameType, Frame
from .multiquery import clickhouse_multiquery
from .session import ClickHttpSession


__all__ = ("clickhouse_multiquery",
           "ClickHttpSession",
           "ClickHttpError",
           "ClosedError",
           "Frame",
           "FrameError",
           "FrameType",
           "FrameMultiQueryError",
           "get_conn",
           "InsertError",
           "UserConn",)

__author__ = "0xMihalich"

__doc__ = """Библиотека для работы с БД Clickhouse по HTTP-протоколу.
Возможности:
- чтение DataFrame на основании SQL-запроса
- выполнение множественного SQL-запроса с возвратом последнего результата как DataFrame
- автоматическое создание временной таблицы с данными на движке MergeTree на основании запроса и возврат ее названия
- insert в таблицу из DataFrame
- поддержка compressed режима работы (сервер принимает и отправляет данные, упакованные в gzip)
- поддержка работы через прокси-сервер
- возможность задать timeout для сессии
- поддержка DataFrame в форматах: dask, numpy, pandas, polars, python, vaex
- инициализация сессии через Airflow connection id либо ручное указание коннектора
"""

__version__ = "0.1.1"
