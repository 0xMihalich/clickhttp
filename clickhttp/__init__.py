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

__doc__ = """Library for working with Clickhouse Database via HTTP protocol.
Features:
- Reading DataFrame based on SQL queries
- Executing multiple SQL queries with the return of the last result as a DataFrame
- Automatic creation of a temporary table with data on the MergeTree engine based on the query and returning its name
- Inserting into a table from a DataFrame
- Support for compressed mode (the server accepts and sends data packed in gzip)
- Support for working through a proxy server
- Ability to set a timeout for the session
- Support for DataFrame in formats: dask, numpy, pandas, polars, python, vaex
- Session initialization via Airflow connection ID or manual specification of the connector.
______________________________________________________________________________________________________________________

Библиотека для работы с БД Clickhouse по HTTP-протоколу.
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

__version__ = "0.1.2"
