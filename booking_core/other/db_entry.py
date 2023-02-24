import asyncio
import asyncpg
from booking_core.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from datetime import datetime as DT, timedelta, date
import datetime


async def pool_connect():
    return await asyncpg.create_pool(user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                              port=DB_PORT, database=DB_NAME)


async def get_count_row(pool: asyncpg.pool.Pool):
    async with pool.acquire() as connection:
        result = await connection.fetch(f"SELECT COUNT(*) FROM booking;")
        return result[0]['count']


async def database_entry():
    conn = await pool_connect()

    if await get_count_row(conn) <1:
        query = await get_query(3,str(DT.today().date()))
    else:
        query = await get_query(1, str(DT.today().date()))

    async with conn.acquire() as connection:
        await connection.fetch(query)


    #await conn.close()


async def get_query(count_days, target_day):
    query = f"INSERT INTO booking(b_date, b_time, b_statuse, b_datetime)"

    target = DT.strptime(str(target_day), "%Y-%m-%d").date() + timedelta(days=1)

    for x in range(count_days):
        date_target = target + datetime.timedelta(days=x)

        for i in range(0, 10*60, 60):
            time_delta = (datetime.datetime.combine(date.today(), datetime.time(8, 0)) + timedelta(minutes=i)).strftime(
                "%H:%M")


            full_datetime = f"{date_target} {time_delta}"
            line = f"\r\n('{date_target}', '{time_delta}', 'free',  {full_datetime}),"

            query += line

    query = f'{query.rstrip(query[-1])};'
    return query


async def runi():
    await database_entry()



asyncio.run(runi())