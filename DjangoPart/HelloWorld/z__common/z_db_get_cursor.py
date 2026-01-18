import sqlite3
from contextlib import contextmanager


@contextmanager
def get_cursor():
    """ Context manager to get a database cursor. """
    conn = sqlite3.connect('data.db')
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()
