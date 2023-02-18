import asyncio
import random
from asyncio import sleep
import asyncpg




async def db_run():
    DSN = 'postgresql://geronda:19941994@localhost:5432/test_bd'
    conn = await asyncpg.connect(DSN)

    async with conn.transaction():
        #rows = await conn.fetch("SELECT * FROM users2 WHERE id=$1;",1)
        rows = await conn.fetch("SELECT * FROM users2;")

    lst_name = [x['name'] for x in rows]
    print(lst_name)


if __name__ == "__main__":
    asyncio.run(db_run())




