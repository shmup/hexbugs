import sqlite3


def initialize_db(db_name):
    db_handler = DBHandler(db_name)
    with db_handler as cursor:
        with open('sql/schema.sql', 'r') as f:
            cursor.executescript(f.read())


class DBHandler:

    def __init__(self, db_name):
        self.db_name = db_name
        self._conn = None
        self._cursor = None

    def get_cursor(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name)
        if self._cursor is None:
            self._cursor = self._conn.cursor()
        return self._cursor

    def commit(self):
        if self._conn is not None:
            self._conn.commit()

    def rollback(self):
        if self._conn is not None:
            self._conn.rollback()

    def close(self):
        if self._conn is not None:
            self._conn.close()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = exc_type, exc_val, exc_tb  # are you happy pyright
        self.conn.commit()
        self.conn.close()
