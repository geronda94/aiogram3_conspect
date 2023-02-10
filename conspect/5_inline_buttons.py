#BOT API Telegram InlineKeyboardButton узнать по подробнее все функции
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования

#Блок инициализации#############################
env = Env()                                    #
env.read_env('.env')                           #
TOKEN = env.str('TOKEN')                       #
ADMIN = env.int('ADMIN_ID')                    #
################################################

################################################
#Формируем инлайн клавиатуру
async def get_inline(message: Message, bot: Bot):
    shop_card = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Заказать', callback_data='заказать товар'),
            InlineKeyboardButton(text='Купить оптом', callback_data='заказать оптом')
        ], [
            InlineKeyboardButton(text='Узнать погоду', url='https://gismeteo.md'),
            InlineKeyboardButton(text='Связаться с продавцом', url='tg://user?id=413281115')
        ]
    ])

    await message.answer('Карточка товара',reply_markup=shop_card)


################################################

#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бота запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Bot is stoped</s>')
async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')


#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)



    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(get_inline, Command(commands=['inline']))




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


