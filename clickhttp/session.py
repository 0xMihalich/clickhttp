from typing import Any, Dict, Optional, Union
from uuid import uuid4

from requests import Session

from .connection import get_conn, UserConn
from .check_conn import is_namedtuple
from .create_temp import temp_query
from .errors import ClosedError, FrameError
from .frame import DTYPE, FrameType, Frame, _FrameType
from .insert import CHUNK_SIZE, insert_table
from .log import to_log
from .multiquery import send_multiquery
from .read import read_frame


GZIP_STR: str = "/?enable_http_compression=1&http_zlib_compression_level=9"


class ClickHttpSession:
    """Executing multiqueries to Clickhouse within a single session.
       This class does not validate the connection for compatibility
       with the Clickhouse database; this action must be performed
       by the user before initializing the class."""

    def __init__(self: "ClickHttpSession",
                 connection: Union[str, UserConn],
                 frame_type: _FrameType = FrameType.set("pandas"),
                 chunk_size: int = CHUNK_SIZE,
                 is_compressed: bool = True,
                 proxy: Optional[str] = None,
                 timeout: Optional[int] = None,) -> None:
        """Class initialization."""

        if isinstance(connection, str):
            connection: UserConn = get_conn(connection)
        elif not is_namedtuple(connection):
            raise FrameError("Unknown connection type")

        if not isinstance(frame_type, FrameType):
            raise FrameError("Unknown frame type")

        self.chunk_size: int = chunk_size
        self.is_compressed: bool = is_compressed
        self.proxy: Optional[str] = proxy
        self.timeout: Optional[int] = timeout

        mode: str = GZIP_STR if self.is_compressed else ""
        protocol: str = "https" if connection.port == 443 else "http"

        self.url: str = (f"""{protocol}://{connection.host}:{connection.port
                                                             if connection.port != 9000
                                                             else 8123}""" + mode)
        self.session_id: str = str(uuid4())
        self.database: str = connection.database
        self.frame_type: _FrameType = frame_type
        self.headers: Dict[str, str] = {
            "X-ClickHouse-User": connection.user,
            "X-ClickHouse-Key": connection.password,
            "X-Content-Type-Options": "nosniff",
            "X-ClickHouse-Format": "JSONCompact",
        }

        if self.is_compressed:
            self.headers["Accept-Encoding"] = "gzip"

        self.sess: Session = Session()
        self.sess.headers.update(self.headers)
        self.set_proxy(self.proxy, False,)

        self.is_closed: bool = False
        to_log(f"Clickhouse Multi-Query session started. Session ID: {self.session_id}.")

    def __str__(self: "ClickHttpSession") -> str:
        """String representation of class."""

        status: str = "Closed" if self.is_closed else "Open"
        session_id: str = "Undefined" if self.is_closed else self.session_id
        mode: str = "Compressed" if self.is_compressed else "Normal"

        return ("ClickHttpSession object."
                f"\nStatus:      {status}"
                f"\nSession ID:  {session_id}"
                f"\nServer Mode: {mode}")

    def __repr__(self: "ClickHttpSession") -> str:
        """String representation of class in interpreter."""

        return self.__str__()

    def __enter__(self: "ClickHttpSession") -> "ClickHttpSession":
        """Starting to work with context manager."""

        if self.is_closed:
            self.reopen()

        return self

    def __exit__(self: "ClickHttpSession", *_: Any) -> None:
        """Ending work with context manager."""

        self.close()

    @property
    def output_format(self: "ClickHttpSession") -> str:
        """Type of returned DataFrame."""

        return self.frame_type.name

    @property
    def change_mode(self: "ClickHttpSession") -> None:
        """Change server operating mode (compression/no compression)."""

        if self.is_compressed:
            self.url: str = self.url[:-57]
            self.is_compressed: bool = False
            del self.headers["Accept-Encoding"]
            to_log("Clickhouse Multi-Query session mode changed to Normal.")
        elif not self.is_compressed:
            self.url: str = self.url + GZIP_STR
            self.is_compressed: bool = True
            self.headers["Accept-Encoding"] = "gzip"
            to_log("Clickhouse Multi-Query session mode changed to Compressed.")

        self.sess.headers.clear()
        self.sess.headers.update(self.headers)

    def close(self: "ClickHttpSession") -> None:
        """Closing session."""

        if not self.is_closed:
            self.sess.close()
            self.is_closed = True
            to_log("Clickhouse Multi-Query session closed.")
        else:
            to_log("Clickhouse Multi-Query already closed.")

    def reopen(self: "ClickHttpSession") -> None:
        """Opening with a new session. Old session will be closed."""

        if not self.is_closed:
            self.sess.close()

        self.session_id: str = str(uuid4())
        self.sess: Session = Session()
        self.sess.headers.update(self.headers)

        self.set_proxy(self.proxy, False,)
        self.is_open: bool = True
        to_log(f"New Clickhouse Multi-Query session started. Session ID: {self.session_id}.")

    def set_proxy(self: "ClickHttpSession",
                  proxy: Optional[str] = None,
                  logging: bool = True,) -> None:
        """Set a proxy server for current session."""

        self.proxy = proxy

        if not self.proxy:
            self.sess.proxies = {}
            if logging:
                to_log("ClickHttpSession proxy settings clear.")
        else:
            proxies: Dict[str, str] = {
                'https': self.proxy,
                'http': self.proxy,
            }
            self.sess.proxies.update(proxies)
            if logging:
                to_log(f"ClickHttpSession change proxy settings with proxy '{proxy}'.")

        self.sess.trust_env = False

    def execute(self: "ClickHttpSession",
                query: str,) -> None:
        """Execute query without returning a result."""

        self.read_frame(query)
        to_log("Command send.")

    def read_frame(self: "ClickHttpSession",
                   query: str,) -> Frame:
        """Retrieve server response as a DataFrame."""

        if self.is_closed:
            raise ClosedError()

        return read_frame(sess=self.sess,
                          session_id=self.session_id,
                          url=self.url,
                          database=self.database,
                          query=query,
                          frame_type=self.frame_type,
                          timeout=self.timeout,)

    def temp_query(self: "ClickHttpSession",
                   query: str,) -> str:
        """Write query result to a temporary table.
           After execution, it returns name of temporary table."""

        if self.is_closed:
            raise ClosedError()

        return temp_query(sess=self.sess,
                          session_id=self.session_id,
                          url=self.url,
                          database=self.database,
                          query=query,
                          timeout=self.timeout,)

    def send_multiquery(self: "ClickHttpSession",
                        multiquery: str,) -> Frame:
        """Send a multiquery to server.
           Only last frame is returned."""

        if self.is_closed:
            raise ClosedError()

        return send_multiquery(sess=self.sess,
                               session_id=self.session_id,
                               url=self.url,
                               database=self.database,
                               frame_type=self.frame_type,
                               multiquery=multiquery,
                               timeout=self.timeout,)

    def insert_table(self: "ClickHttpSession",
                     table: str,
                     data_frame: DTYPE,  # type: ignore
                     use_columns: bool = True,) -> None:
        """Writing data from DataFrame to target table."""

        if self.is_closed:
            raise ClosedError()

        return insert_table(sess=self.sess,
                            session_id=self.session_id,
                            url=self.url,
                            database=self.database,
                            table=table,
                            data_frame=data_frame,
                            is_compressed=self.is_compressed,
                            chunk_size=self.chunk_size,
                            timeout=self.timeout,
                            use_columns=use_columns,)
