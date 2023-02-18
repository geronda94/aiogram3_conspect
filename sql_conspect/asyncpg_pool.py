import asyncio
import asyncpg
from aiohttp import web
from config import user, password, host, port, db_name

dsn = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

async def print_db():
    async def con_db():

        pool = await asyncpg.create_pool(dsn)
        async with pool.acquire() as connection:
            result = await connection.fetch("SELECT * FROM users2")

        await pool.close()

        return [x for x in result]

    lst = await con_db()


    for i in lst:
        print(*i)



class Database:
    def __init__(self, user, password, host, port, db_name):
        self.pool = None
        self.dsn = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)

    async def disconnect(self):
        await self.pool.close()

    async def fetch(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)

    async def execute(self, query):
        async with self.pool.acquire() as connection:
            return await connection.execute(query)


async def main():
    db = Database(user, password, host, port, db_name)
    await db.connect()
    #result = await db.fetch("SELECT * FROM users2")
    await db.execute("INSERT INTO users2 (name, dob) VALUES ('Valera', '1991-5-10');")
    await db.disconnect()



if __name__ == "__main__":
    asyncio.run(main())





