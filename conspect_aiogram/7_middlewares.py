from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.types import Message, ContentType, TelegramObject
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from typing import Dict, Any, Callable, Awaitable
from datetime import datetime
import asyncpg


#Блок инициализации#############################
env = Env()                                    #
env.read_env('.env')                           #
TOKEN = env.str('TOKEN')                       #
ADMIN = env.int('ADMIN_ID')                    #
################################################
#Пишем мидлварь счетчик
class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       )-> Any:
        self.counter+=1
        data['counter'] = self.counter
        return await handler(event, data)


def office_hours() -> bool:
    return datetime.now().weekday() not in (0,1,2,3,4) and datetime.now().hour in ([i for i in (range(8,19))])

# class OfficeHoursMiddlerware(BaseMiddleware):
#     async def __call__(self,
#                        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#                        event: Message,
#                        data: Dict[str, Any],
#                        ) -> Any:
#         if office_hours():
#             return await handler(event, data)
#
#         await event.answer('Рабочие часы бота пн-пт с 8:00 до 18:00')


class OfficeHoursMiddlerware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
                       ) -> Any:
        if office_hours():
            return await handler(event, data)

        #await event.answer('Рабочие часы бота пн-пт с 8:00 до 18:00')


#Работа с БД
#Создаем класс для манипуляций с данными в бд
class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    #функци записывает данные в бд
    async def add_data(self, user_id, user_name):
        query = f"INSERT INTO data_users (user_id, user_name)"\
                f"VALUES ({user_id}, '{user_name}') ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

class DbSession(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool):
        super().__init__()
        self.connector = connector

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]],Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)



#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Бот остановлен</s>')

async def get_start(message: Message, bot: Bot, counter: str, request: Request): #Функция срабатывает когда юзер дает команду /start
    await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Сообщение №{counter}')
    await message.answer('Давай начнем!')
###############################################
#Создаем функцию на соединение с базой#########
async def create_pool():
    return await asyncpg.create_pool(user='geronda', password='19941994', database='users',
                                             host='127.0.0.1', port=5432, command_timeout=60)
###############################################
#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    pool_connect = await create_pool() #Соединение с базой
    dp = Dispatcher()

    dp.message.middleware.register(CounterMiddleware()) #Middleware нужно регистрировать раньше чем хэндлеры
    dp.update.middleware.register(OfficeHoursMiddlerware()) #Middleware нужно регистрировать раньше чем хэндлеры
    dp.update.middleware.register(DbSession(pool_connect)) #Хэндлер соединения с базой


    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)


    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start





    try:
        #Начало сессии
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем функцию Бота########################
if __name__ =="__main__":
    asyncio.run(start())


