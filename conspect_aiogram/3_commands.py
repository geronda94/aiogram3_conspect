from aiogram import Bot,F, Dispatcher
from aiogram.filters import Command, Filter, Text
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault #Узнать про скопы
import asyncio
from core.settings import TOKEN, ADMIN

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начало'),
        BotCommand(command='help', description='Описание Бота'),
        BotCommand(command='inline', description='Карточка товара функция'),
        BotCommand(command='form', description='Вызвать анкету'),
        BotCommand(command='cancel', description='Сбросить'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN, text='Бот запущен!')

async def get_start(message: Message, bot: Bot):
    await message.answer('Давай начнем!')


async def start():


    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot)

    #устанавливаем набор команд которые появляются рядом с чатом
    dp.message.register(get_start, Command(commands=['start']))




    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ =="__main__":
    asyncio.run(start())


