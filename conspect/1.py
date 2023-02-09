from aiogram import Bot, Dispatcher #импортируем бота и диспетчер
from aiogram.types import Message #импортируем объект Message
from aiogram.filters import Command #Имортируем объект через который устанавливаем команды
import asyncio #Импортируем asyncio чтобы иметь возможность запускать бота асинхронно
import logging #импортируем библиотеку логирования
from core.handlers.basic import get_start, start_bot, stop_bot #Импортируем из хэндлера основыне функции

TOKEN = '5783446935:AAFyAOVxRAic6Wx5bSVfoDX6hjs7EC3yjrE'
ADMIN = 413281115

#Создаем асинхронную функцию для работы внутри бота
async def get_start(message: Message, bot: Bot):
    #обязательно не забываем await, ведь это асинхронная функция, ниже представлены
    #await message.answer(f'Привет {message.from_user.first_name}, давай начнем?')
    await bot.send_message(message.from_user.id, text=f'<tg-spoiler>Привет {message.from_user.first_name}'
                                                      f', давай начнем?</tg-spoiler>')
    #await message.reply( text=f'Привет {message.from_user.first_name}, давай начнем?') #ответ с возвратом сообщения


#создаем функцию которая выполняется при запуске бота
async def start_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<b>Bot is started</b>')
#создаем функцию которая выполняется при остановке бота
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Bot is stoped</s>')





#созздаем асинхронную функцию с запуском бота
async def start():
    logging.basicConfig(level=logging.INFO,#создаем конфиг логирования и прописываем формат отображения логов
                        format="%(asctime)s - [%(levelname)s] - %(name)s -" \
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    #parse_mode = html позволяет использовать html cтили для оформления текста
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    #Регистирируем события которые срабатывают при запуске и останвоке бота, функции мы прописали выше
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=['start']))

    try:
        # Через awqit запускаем асинхронную функцию
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию с ботом
        await bot.session.close()



if __name__ == "__main__":
    #Заупскаем Бота для асинхронной работы
    asyncio.run(start())







