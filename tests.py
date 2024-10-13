from clickhttp.log import to_log
from clickhttp.connection import UserConn
from clickhttp.sql_formatter import formatter

def isinstance_namedtuple(obj) -> bool:
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )

def test_connobj():
    conn = UserConn('user', 'password', 'localhost', 8123, 'default',)

    assert isinstance_namedtuple(conn) is True

def test_log():
    assert to_log("hello world") is None


def test_connection():
    conn = UserConn('user', 'password', 'localhost', 8123, 'default',)

    assert isinstance(conn, UserConn) == isinstance(conn, tuple)


def test_formatter():

    assert formatter(
            "-- test query\n"
            "SELECT * FROM table "
            "WHERE column = 'value'/* some big comment"
            "*/"
        ) == "SELECT * FROM table WHERE column = 'value'"
