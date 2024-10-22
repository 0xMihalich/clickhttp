from os import urandom
from typing import List

from requests import Session

from .frame import FrameType
from .log import to_log
from .read import read_frame
from .sql_formatter import formatter


DDL_TEMPLATE: str = """CREATE TEMPORARY TABLE {table_name}
(
    {table_struct}
)
ENGINE = MergeTree
ORDER BY {column}
AS
{query}"""


def temp_query(sess: Session,
               session_id: str,
               url: str,
               database: str,
               query: str,
               timeout: int = 10,) -> str:
    """Writing the query to a temporary table. Returns the name of the temporary table."""

    _query: str = formatter(query)

    to_log("Get names and data types from query")
    describe: List[List[str]] = read_frame(sess=sess,
                                           session_id=session_id,
                                           url=url,
                                           database=database,
                                           query=f"describe table ({_query})",
                                           frame_type=FrameType.python,
                                           timeout=timeout,).data
    table_name: str = "temp_" + urandom(8).hex()

    to_log(f"Generate DDL for temporary table {table_name}")
    column: str = describe[0][0]
    table_struct: str = ",\n    ".join(" ".join(column) for column in
                                       (row[:2] for row in describe))
    read_frame(sess=sess,
               session_id=session_id,
               url=url,
               database=database,
               query=DDL_TEMPLATE.format(table_name=table_name,
                                         table_struct=table_struct,
                                         column=column,
                                         query=_query,),
               frame_type=FrameType.python,
               timeout=timeout,)

    to_log(f"Temporary table {table_name} created.")
    return table_name
