import asyncio
import logging
from typing import Union, Optional

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool


logger = logging.getLogger(__name__)


class Database:

    def __init__(self, username: str, password: str, host: str, database: str, port: str,
                 loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None):
        self._main_loop = loop
        self.pool: Union[Pool, None] = None
        self._pool: Union[Pool, None] = None
        self._username = username
        self._password = password
        self._host = host
        self._database = database
        self._port = port

    async def create_pool(self):
        self._pool = await asyncpg.create_pool(user=self._username,
                                               password=self._password,
                                               host=self._host,
                                               database=self._database,
                                               port=self._port,
                                               min_size=10,
                                               max_size=15
                                               )
        logger.info("Created asyncpg connection pool")
        return self._pool

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._main_loop

    async def get_pool(self):
        if self._pool is None: self._pool = await self.create_pool()
        if not self._pool._loop.is_running():
            logger.info("Pool is not running in loop")
            await self._pool.close()
            self._pool = await self.create_pool()
        return self._pool

    async def close(self):
        if self._pool: await self._pool.close()

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        if self._pool is None: await self.get_pool()
        async with self._pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_servers_table(self):
        sql = "CREATE TABLE IF NOT EXISTS vpn_servers (" \
              "id bigserial PRIMARY KEY, " \
              "server_name VARCHAR(60) NOT NULL," \
              "api_link VARCHAR(255) NOT NULL UNIQUE, " \
              "UNIQUE (api_link, server_name))"
        return await self.execute(sql, execute=True)

    async def create_users_table(self):
        sql = "CREATE TABLE IF NOT EXISTS users (" \
              "id bigserial PRIMARY KEY, " \
              "user_id BIGINT NOT NULL UNIQUE, " \
              "username VARCHAR(255) NOT NULL UNIQUE, " \
              "is_banned BOOLEAN DEFAULT FALSE, " \
              "subscription_end_date TIMESTAMP, " \
              "UNIQUE (user_id, username))"
        return await self.execute(sql, execute=True)

    async def create_users_keys_table(self):
        sql = "CREATE TABLE IF NOT EXISTS users_keys (" \
              "id bigserial PRIMARY KEY, " \
              "user_id BIGINT NOT NULL, " \
              "vpn_key VARCHAR(255) UNIQUE, " \
              "CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id), " \
              "UNIQUE (vpn_key))"
        return await self.execute(sql, execute=True)

    async def get_servers(self):
        sql = "SELECT (id, server_name) FROM vpn_servers"
        return await self.execute(sql, fetch=True)

    async def get_server_key(self, server_id):
        sql = "SELECT api_link FROM vpn_servers WHERE id=$1"
        return await self.execute(sql, server_id, fetchval=True)

    async def get_users(self):
        sql = "SELECT user_id FROM users"
        return await self.execute(sql, fetch=True)

    async def get_user_keys(self, user_id):
        sql = "SELECT vpn_key FROM users_keys WHERE user_id=$1"
        return await self.execute(sql, user_id, fetch=True)

    async def add_server(self, server_name, api_link):
        sql = "INSERT INTO vpn_servers (server_name, api_link) VALUES ($1, $2)"
        return await self.execute(sql, server_name, api_link, execute=True)

    async def add_user(self, user_id, username):
        sql = "INSERT INTO users(user_id, username) VALUES ($1, $2) ON CONFLICT DO NOTHING"
        return await self.execute(sql, user_id, username, execute=True)

    async def add_user_key(self, user_id, vpn_key):
        sql = "INSERT INTO users_keys (user_id, vpn_key) VALUES ($1, $2)"
        return await self.execute(sql, user_id, vpn_key, execute=True)

    async def delete_server(self, server_id):
        sql = "DELETE FROM vpn_servers WHERE id=$1"
        return await self.execute(sql, server_id, execute=True)
