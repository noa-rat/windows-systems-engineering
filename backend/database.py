from contextlib import contextmanager
from queue import Empty, Queue
from threading import Lock

import pyodbc

from backend.config import settings


class _PooledConnection:
    def __init__(self, connection, pool):
        self._connection = connection
        self._pool = pool
        self._closed = False

    def __getattr__(self, name):
        return getattr(self._connection, name)

    def close(self):
        if not self._closed:
            self._closed = True
            self._pool.release(self._connection)


class ConnectionPool:
    def __init__(self, connection_string, minimum, maximum):
        self.connection_string = connection_string
        self.minimum = minimum
        self.maximum = maximum
        self._connections = Queue(maxsize=maximum)
        self._lock = Lock()
        self._total = 0

    def _create(self):
        connection = pyodbc.connect(self.connection_string, timeout=10)
        self._total += 1
        return connection

    @staticmethod
    def _healthy(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except pyodbc.Error:
            return False

    def _discard(self, connection):
        try:
            connection.close()
        finally:
            with self._lock:
                self._total = max(0, self._total - 1)

    def acquire(self):
        try:
            connection = self._connections.get_nowait()
        except Empty:
            with self._lock:
                if self._total == 0:
                    target = min(self.minimum, self.maximum)
                    for _ in range(target):
                        created = self._create()
                        if _ == 0:
                            connection = created
                        else:
                            self._connections.put_nowait(created)
                    if not self._healthy(connection):
                        self._discard(connection)
                        connection = self._create()
                    return _PooledConnection(connection, self)
                if self._total < self.maximum:
                    connection = self._create()
                else:
                    connection = None
            if connection is None:
                try:
                    connection = self._connections.get(timeout=10)
                except Empty as error:
                    raise TimeoutError(
                        "Database connection pool is exhausted."
                    ) from error
        return _PooledConnection(connection, self)

    def release(self, connection):
        try:
            self._connections.put_nowait(connection)
        except Exception:
            connection.close()
            with self._lock:
                self._total -= 1

    def close_all(self):
        while True:
            try:
                connection = self._connections.get_nowait()
                connection.close()
                with self._lock:
                    self._total = max(0, self._total - 1)
            except Empty:
                break


connection_pool = ConnectionPool(
    settings.DATABASE_URL,
    settings.DB_POOL_MIN_SIZE,
    settings.DB_POOL_MAX_SIZE,
)


def get_connection():
    return connection_pool.acquire()


@contextmanager
def database_connection():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()
