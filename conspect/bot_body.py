from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env


env = Env()
env.read_env('.env')
TOKEN = env.str('TOKEN')
ADMIN = env.int('ADMIN_ID')



async def start():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()








    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ =="__main__":
    asyncio.run(start())


