import asyncio
from sql_conspect.asyncpg_pool import Database
import asyncpg
from booking_core.settings import DB_HOST,DB_PORT, DB_NAME, DB_USER,DB_PASSWORD


#####################################################
#тестирование функций на запись
# async def db_write():
#     db = Database(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
#     await db.connect()
#     await db.execute(f"INSERT INTO test (name) VALUES ('igor');" )
#     await db.disconnect()

async def db_write(insert_data: str):
    db = Database(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    await db.connect()
    await db.execute(insert_data)
    await db.disconnect()

async def runi():
    for i in range(3):
        await db_write(f"INSERT INTO test (name) VALUES ('tolik{i}');" )

############################################################################

###########################################################################
#Тестирование функций на чтение
async def db_read(select_str: str):
    db = Database(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    await db.connect()
    result = await db.fetch(select_str)
    await db.disconnect()

    return result


async def readi():
    lst = list(await db_read("SELECT * FROM test"))
    for i in lst:
        print(i)

############################################################################


asyncio.run(readi())