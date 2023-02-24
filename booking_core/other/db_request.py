import asyncpg


# class Request:
#     def __int__(self,conn):
#         self.conn = conn
#
#     async def add_user(self):
#         pass


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    #функци записывает данные в бд
    async def get_user(self,  id_user, first_name, last_name, username):
        query = f"INSERT INTO users (id_telegram, first_name, last_name, username) " \
                f"VALUES ('{id_user}', '{first_name}','{last_name}', '{username}') " \
                f"ON CONFLICT (id_telegram) DO UPDATE SET username='{username}', first_name='{first_name}', " \
                f"last_name='{last_name}';"
        await self.connector.fetch(query)

        # async with self.connector.acquire() as connection:
        #     await connection.fetch(query)
