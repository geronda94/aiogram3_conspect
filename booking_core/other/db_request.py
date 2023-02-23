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
    async def add_data(self,  user_name):
        query = f"INSERT INTO test (name) VALUES ('ALFRED') "
        await self.connector.execute(query)
