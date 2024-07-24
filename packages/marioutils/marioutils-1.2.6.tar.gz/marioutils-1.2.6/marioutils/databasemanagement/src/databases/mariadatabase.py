from .baseclass import Database
from marioutils.databasemanagement.src import exceptions
import sqlalchemy
import mariadb

class MariaDatabase(Database):
    def __init__(
            self,
            server: str,
            user: str,
            password: str,
            database: str = None,
            as_dict: bool = True,
            port: int = 3306,
            pool_size: int | sqlalchemy.pool.NullPool = 5,
            max_overflow: int = 10):
        super().__init__(
            server,
            user,
            password,
            database,
            as_dict,
            port,
            pool_size,
            max_overflow)
        self.create_pool()

    def get_connection(self):
        c = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.server,
            port=self.port,
            database=self.database
        )
        return c

    def get_cursor(self):
        if self._connection is None:
            raise exceptions.ConnectionException
        if self._cursor is None:
            self._cursor = self._connection.cursor()
        else:
            return self._cursor

    def fetchall(self):
        try:
            res = self._cursor.fetchall()
            if not self.as_dict:
                return res
            else:
                columns = [a[0] for a in self._cursor.description]
                results = [{c: v for c, v in zip(columns, r)} for r in res]
                return results
        except Exception as e:
            return e

