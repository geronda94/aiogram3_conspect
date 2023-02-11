#BOT API Telegram InlineKeyboardButton узнать по подробнее все функции
import time

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
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
#Формируем карточки с инлайн клавиатурой
catalog = ['cofe', 'tea','watter','jam','bread']

async def get_inline(message: Message, bot: Bot):
    for num,i in enumerate(catalog):
        shop_card = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Заказать оптом {i}', callback_data=f'order_{num}'),
                InlineKeyboardButton(text=f'Купить {i}', callback_data=f'buy_{num}')
            ], [
                InlineKeyboardButton(text='Узнать погоду', url='https://gismeteo.md'),
                InlineKeyboardButton(text='Связаться с продавцом', url='tg://user?id=413281115')
            ]
        ])
        await message.answer_photo('AgACAgIAAxkBAAID6GPl5EGxygzZnX8LeAOHfglqwCvnAAKIwTEbzRMwS1mZK4NKeH1ZAQADAgADeQADLgQ',
                                caption=f'✅    Товар {i}\n\n'
                                        f'Какое то описание в 250 символов '
                                        f'которое кратко описывает основные характеристикаи и свойства'
                                        f'данного товара.',
                                reply_markup=shop_card)
        time.sleep(0.5)

################################################
#Обработка колбэков
async def callback_order(call: CallbackQuery, bot: Bot):
    index= int(call.data.split('_')[-1])

    await call.message.answer(f'Вы добавили в оптовый заказ {catalog[index]}')
    await bot.send_message(ADMIN, f'Пользователь {call.from_user.id} добавили в оптовый заказ {catalog[index]}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк

async def callback_buy(call: CallbackQuery, bot: Bot):
    index= int(call.data.split('_')[-1])

    await call.message.answer(f'Вы заказали в розницу {catalog[index]}')
    await bot.send_message(ADMIN, f'Пользователь {call.from_user.id} хочет купить {catalog[index]}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк

################################################
#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бота запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Bot is stoped</s>')
async def get_start(message: Message, bot: Bot): #Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')
###############################################

#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)



    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(get_inline, Command(commands=['inline']))


    dp.callback_query.register(callback_order, F.data.startswith('order_')) #Регистрируем колбэки
    dp.callback_query.register(callback_buy, F.data.startswith('buy_'))



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


