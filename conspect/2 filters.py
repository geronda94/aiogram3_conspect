from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command
import asyncio
from core.settings import TOKEN, ADMIN
from core.handlers.basic import get_start
import logging


async def get_photo(message: Message, bot: Bot):
    await message.answer('Получил картинку')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, rf'../photo_upload/{message.photo[-1].file_id}.jpg')

    # await message.answer(f'Сохраняю фото!')
    # file = await bot.get_file(message.photo[-1].file_id)
    # await bot.download_file(file.file_path, f'files/{message.photo[-1].file_id}.jpg')


async def start():
    logging.basicConfig(level=logging.INFO,  # создаем конфиг логирования и прописываем формат отображения логов
                        format="%(asctime)s - [%(levelname)s] - %(name)s -" \
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_photo, F.content_type == ContentType.PHOTO)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
