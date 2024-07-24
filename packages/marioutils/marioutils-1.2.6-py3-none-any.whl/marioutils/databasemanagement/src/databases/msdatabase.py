from .baseclass import Database
import pymssql
from marioutils.databasemanagement.src import exceptions
import sqlalchemy


class MsSQLDatabase(Database):

    def __init__(
            self,
            server: str,
            user: str,
            password: str,
            database: str = None,
            as_dict: bool = True,
            port: int = 1433,
            pool_size: int | sqlalchemy.pool.NullPool = 5,
            max_overflow: int = 10) -> pymssql.Connection:
        super().__init__(
            server,
            user,
            password,
            database,
            as_dict,
            pool_size,
            max_overflow)
        self.create_pool()

    def get_connection(self):
        c = pymssql.connect(
            server=self.server,
            user=self.user,
            password=self.password,
            database=self.database,
            as_dict=self.as_dict,
            login_timeout=20,
            timeout=20
        )
        return c

    def get_cursor(self):
        if self._connection is None:
            raise exceptions.ConnectionException
        if self._cursor is None:
            self._cursor = self.connection.cursor()
