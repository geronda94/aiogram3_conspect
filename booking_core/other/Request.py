import asyncpg


class Request:
    def __int__(self,conn):
        self.conn = conn

    async def add_user(self):
        pass


# class Request:
#     def __init__(self, connector: asyncpg.pool.Pool):
#         self.connector = connector
#
#     #функци записывает данные в бд
#     async def add_user(self, user_id, user_name):
#         query = f"INSERT INTO booking (user_id, user_name)"\
#                 f"VALUES ({user_id}, '{user_name}') ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
#         await self.connector.execute(query)
