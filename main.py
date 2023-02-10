from aiogram import Bot, Dispatcher, F #импортируем бота и диспетчер
from aiogram.types import Message, ContentType #импортируем объект Message
from aiogram.filters import Command #Имортируем объект через который устанавливаем команды
import asyncio #Импортируем asyncio чтобы иметь возможность запускать бота асинхронно
import logging #импортируем библиотеку логирования
from core.settings import TOKEN, ADMIN
from core.handlers.basic import get_start, start_bot, stop_bot, get_photo


#созздаем асинхронную функцию с запуском бота
async def start():
    logging.basicConfig(level=logging.INFO,#создаем конфиг логирования и прописываем формат отображения логов
                        format="%(asctime)s - [%(levelname)s] - %(name)s -" \
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    #parse_mode = html позволяет использовать html cтили для оформления текста
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    #Регистирируем события которые срабатывают при запуске и останвоке бота, функции мы прописали в core.handlers.basic
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # регистрируем хэндлеры из core.hanlers.basic
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_photo, F.content_type == ContentType.PHOTO)


    try:
        # Через await запускаем асинхронную функцию
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию с ботом
        await bot.session.close()



if __name__ == "__main__":
    #Заупскаем Бота для асинхронной работы
    asyncio.run(start())







