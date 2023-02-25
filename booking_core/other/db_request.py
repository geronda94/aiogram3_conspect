import datetime

import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

        # Функция извлекает даты из БД

    async def db_get_time(self, date_needed):
        data_now = datetime.datetime.today().strftime("%d.%m.%Y %H:%M")
        query = f"SELECT DISTINCT b_time FROM booking " \
                f"WHERE b_statuse='free' AND b_date='{date_needed}' AND b_datetime > '{data_now}' " \
                f"ORDER BY b_time ASC;"


        async with self.connector.acquire() as connection:
            results = await connection.fetch(query)

        lst_time= [str(result[0].strftime("%H:%M")) for result in results]
        return lst_time


    #Функция извлекает даты из БД
    async def db_get_date(self):
        date_now = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        query = f"SELECT DISTINCT b_date FROM booking WHERE b_statuse='free'" \
                f"AND b_datetime > '{date_now}' ORDER BY b_date ASC LIMIT 3;"

        async with self.connector.acquire() as connection:
            results = await connection.fetch(query)

        lst_date = [str(result[0].strftime("%d.%m.%Y")) for result in results]
        return lst_date



    #функци записывает данные в бд
    async def get_user(self,  id_user, first_name, last_name, username):
        query = f"INSERT INTO users (id_telegram, first_name, last_name, username) " \
                f"VALUES ('{id_user}', '{first_name}','{last_name}', '{username}') " \
                f"ON CONFLICT (id_telegram) DO UPDATE SET username='{username}', first_name='{first_name}', " \
                f"last_name='{last_name}';"

        async with self.connector.acquire() as connection:
            await connection.execute(query)
        # await self.connector.fetch(query)


    async def db_change_statuse(self, statuse, date, time):
        query = f"UPDATE booking SET b_statuse='{statuse}' WHERE b_date='{date}' AND b_time='{time}';"

        async with self.connector.acquire() as connection:
            await connection.execute(query)