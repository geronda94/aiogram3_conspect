from aiogram import Bot,F, Dispatcher
from aiogram.filters import Command, Filter, Text
from aiogram.types import BotCommand, BotCommandScopeDefault #Узнать про скопы
import asyncio
from core.settings import TOKEN

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начало'),
        BotCommand(command='help', description='Описание Бота'),
        BotCommand(command='cancel', description='Сбросить'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем




async def start():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()








    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ =="__main__":
    asyncio.run(start())


