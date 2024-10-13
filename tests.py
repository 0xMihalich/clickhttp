from datetime import date

from clickhttp import UserConn, ClickHttpSession, FrameType
from clickhttp.check_conn import is_namedtuple
from clickhttp.log import to_log
from clickhttp.sql_formatter import formatter


def test_connobj():
    """Проверка что объект connection является NamedTuple."""

    conn = UserConn('user', 'password', 'localhost', 8123, 'default',)

    assert is_namedtuple(conn) is True


def test_formatter():
    """Проверка работы форматтера."""

    assert formatter(
            "-- test query\n"
            "SELECT * FROM table "
            "WHERE column = 'value'/* some big comment"
            "*/"
        ) == "SELECT * FROM table WHERE column = 'value'"


def test_log():
    """Проверка что лог ничего не возвращает."""

    assert to_log("hello world") is None


def test_session():
    """Проверка работы объекта сессии."""

    conn = UserConn('play', None, 'play.clickhouse.com', 443, None)
    sess = ClickHttpSession(connection=conn, is_compressed=False, frame_type=FrameType.python,)
    query = """select
                   today()  as test_date
                 , 1        as test_int
                 , 1.0      as test_float
                 , true     as test_bool
                 , array(1
                       , 2
                       , 3) as test_arrayint
                """
    df = sess.read_frame(query)
    
    assert df.data[0] == [date.today(), 1, 1.0, True, [1, 2, 3,]]
