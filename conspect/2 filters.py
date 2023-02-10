"""Разобраться с самописными фильтрами"""


from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command, Text
import asyncio
from core.settings import TOKEN, ADMIN
from core.handlers.basic import get_start
import logging
from aiogram.filters import BaseFilter

async def get_photo(message: Message, bot: Bot):
    await message.answer('Получил картинку')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, rf'../photo_upload/{message.photo[-1].file_id}.jpg')

    # await message.answer(f'Сохраняю фото!')
    # file = await bot.get_file(message.photo[-1].file_id)
    # await bot.download_file(file.file_path, f'files/{message.photo[-1].file_id}.jpg')

async def hello(message: Message, bot: Bot):
    #await message.answer('Привет')
    await bot.send_message(message.chat.id, text='Привет')


#Создаем функцию которая принимает телефон пользователя и проверяет его на подлинность
async def get_contact(message: Message, bot: Bot):
    flag = 'Свой' if message.contact.user_id == message.from_user.id else 'Чужой'

    await message.answer(f'Ты отправил <b>{flag}</b> контакт!')





async def start():
    logging.basicConfig(level=logging.INFO,  # создаем конфиг логирования и прописываем формат отображения логов
                        format="%(asctime)s - [%(levelname)s] - %(name)s -" \
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    dp.message.register(get_start, Command(commands=['start']))
    #Регистрируем хэндлер на скачивание фото
    dp.message.register(get_photo, F.content_type == ContentType.PHOTO)
    #Регистрируем хэндлер на текстовое апдейт со словом привет
    dp.message.register(hello, Text(text=['привет','здарова'], ignore_case=True))
    #dp.message.register(hello, F.text=='Привет')

    #Регистрируем хэндлер на прием контактов пользователя
    dp.message.register(get_contact, F.content_type == ContentType.CONTACT)


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
