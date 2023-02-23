import asyncio
import logging
from asyncio import WindowsSelectorEventLoopPolicy
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncpg
from booking_core.middlewares.db_middlewares import DbSession
from booking_core.settings import TOKEN, ADMIN, DB_HOST, DB_PORT,DB_NAME, DB_USER,DB_PASSWORD



asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
############################
#Стартвые функции
async def start_bot( bot: Bot):
    await bot.send_message(ADMIN, 'Бот запущен')

async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, 'Бот остановлен')

async def create_pool(user, host, password, db_name, port):
    return await asyncpg.create_pool(user=user, password=password, host=host,
                                              port=port, database=db_name)

#############################

#Тело бота
async def run_bot():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


    bot = Bot(TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    pool = create_pool(user=DB_USER, host=DB_HOST, password=DB_PASSWORD, db_name=DB_NAME, port=DB_PORT)
    dp.message.middleware(DbSession(pool))












    try:
        #Начало сессии
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()



##########################

#Запуск
if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except Exception as ex:
        print(ex)