import sqlite3
import typing
from typing import Iterable
import aiosqlite
from loguru import logger

if typing.TYPE_CHECKING:
    from app.config import Config


__all__ = [
    "Database"
]


class Database:

    __debug: bool
    __autocommit: bool
    __connection: aiosqlite.Connection = None

    def __new__(cls):
        """ Singleton pattern """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    async def query(
            self,
            query_string: str,
            parameters: list | tuple | None = None
    ) -> list[sqlite3.Row]:

        if not self.__connection:
            raise Exception("Не соединения с базой данных. В начале нужно сделать - `Database().connect()`")

        cursor = await self.__connection.execute(query_string, parameters)
        result: list[sqlite3.Row] = list(await cursor.fetchall())
        await cursor.close()

        if self.__autocommit:
            await self.__connection.commit()

        if self.__debug:
            logger.debug(f"[Database]: Новая транзакция - {query_string}")
            logger.debug(f"[Database]: Ответ БД - {result}")

        return result

    def get_connection(self) -> aiosqlite.Connection:
        return self.__connection

    async def get_all(self, query_string: str, parameters: list | tuple | None = None) -> list[sqlite3.Row]:
        return await self.query(query_string, parameters)

    async def get_one_or_null(self, query_string: str, parameters: list | tuple | None = None) -> sqlite3.Row:
        result = await self.query(query_string, parameters)
        return result[0] if result else None

    async def connect(self, db_path: str = 'app/DataBase/Bot.db', autocommit: bool = True, debug: bool = False):
        logger.info("[Database]: Открываю соедиенение с БД.")

        self.__debug = debug
        self.__autocommit = autocommit
        self.__connection = await aiosqlite.connect(db_path)

    async def disconnect(self):
        logger.info("[Database]: Закрываю соедиенение с БД.")

        if not self.__connection:
            return
        await self.__connection.close()
