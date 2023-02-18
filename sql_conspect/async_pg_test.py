import asyncio
import asyncpg
import datetime


async def main():
    conn = await asyncpg.connect('postgresql://geronda:19941994@localhost:5432/test_bd')

    #await conn.execute("INSERT INTO users1 (name, nick_name) VALUES ('igor2', 'harry94');")
    #rows = await conn.fetch('SELECT * FROM users2')

    rows = await conn.fetch("SELECT * FROM users2 WHERE id=$1;",5)

    print(rows)


    await conn.close()
asyncio.run(main())


