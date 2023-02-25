import asyncio
import logging
import asyncpg
import psycopg_pool
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncpg
from booking_core.middlewares.db_middlewares import DbSession
from booking_core.other.db_entry import database_entry
from booking_core.other.state_user import States
from booking_core.settings import TOKEN, ADMIN, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from booking_core.handlers.steps import get_data, get_name, get_time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

############################
# Стартвые функции
async def start_bot(bot: Bot):
    await bot.send_message(ADMIN, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, 'Бот остановлен')


async def create_pool(user, host, password, db_name, port):
    return await asyncpg.create_pool(user=user, password=password, host=host,
                                     port=port, database=db_name)




#############################

# Тело бота
async def run_bot():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(TOKEN, parse_mode='HTML')
    dp = Dispatcher()


    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    pool = await create_pool(user=DB_USER, host=DB_HOST, password=DB_PASSWORD, db_name=DB_NAME, port=DB_PORT)
    dp.message.middleware(DbSession(pool))
    dp.callback_query.middleware(DbSession(pool))

    dp.callback_query.register(get_time, States.state_date)
    dp.message.register(get_data, States.state_name)
    dp.message.register(get_name, Command(commands='start'))



    await database_entry()

    scheduler = AsyncIOScheduler(timezone='Europe/Kiev')
    scheduler.add_job(database_entry, 'cron', hour=1, minute=00, start_date='2023-02-26 20:27:00')
    scheduler.start()


    try:
        # Начало сессии
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию
        await bot.session.close()


##########################

# Запуск
if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except Exception as ex:
        print(ex)
