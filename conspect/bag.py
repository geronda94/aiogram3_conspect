# BOT API Telegram InlineKeyboardButton узнать по подробнее все функции
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery
from aiogram.filters import Filter, Command, Text
import asyncio
from environs import Env
import logging  # импортируем библиотеку логирования
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.types import BotCommand, BotCommandScopeDefault
import os

# Блок инициализации#############################
env = Env()  #
env.read_env('.env')  #
TOKEN = env.str('TOKEN')  #
ADMIN = env.int('ADMIN_ID')  #
################################################

# каталог товаров. В списках под 1 индексом идут ид которое загружены в бот, можно загрузить через функци. ниже
#Фото сохраняются под именем id.jpg, если убрать .jpg то получится тот формат который можно пересылать по телеграму
#В пределах бота, в которого фото загружены
catalog_dict = {
    'cofe': ['Кофе', 'AgACAgIAAxkBAAIHD2Pn9a260-cbFoGysWKrAAGwdaX-MwACDMYxGy2hQEvnXrYqnwABehABAAMCAAN5AAMuBA'],
    'tea': ['Чай', 'AgACAgIAAxkBAAIHC2Pn9ZgQpZQlkR6fKKC8MmyPFl0xAAILxjEbLaFAS0p0JkBZhMHOAQADAgADeQADLgQ'],
    'watter': ['Вода', 'AgACAgIAAxkBAAIHDWPn9aV1zXEGFYwc3_ArwUlNK5UuAAIJxjEbLaFAS14Em7lro5AhAQADAgADeQADLgQ'],
    'jam': ['Варенье', 'AgACAgIAAxkBAAIHEmPn9cklVDw3wxsJ1unyDE3solSpAAIGxjEbLaFAS_mANsJE14hXAQADAgADeQADLgQ'],
    'bread': ['Хлеб', 'AgACAgIAAxkBAAIHFGPn9dCzH0A6frSfmRYob_Fcc-hLAAINxjEbLaFAS5_0YLSb-I_XAQADAgADeQADLgQ']}


#Словарь корзины
orders = dict()

#функция на загрузку фото в бота
async def get_photo(message: Message, bot: Bot):
    await message.answer('Получил картинку')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'../photo_upload/{message.photo[-1].file_id}.jpg')


################################################

# Формируем Карточки товара
# from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

#Регисрируем классы колбэков
class InBag(CallbackData, prefix='inbag'):
    in_bag: int
    index: int
    title: str
    order: int

class SendOrder(CallbackData, prefix='update'):
    index: int
    title: str
    order: int
    in_bag: int

class AddToOrder(CallbackData, prefix='add'):
    index: int
    title: str
    order: int
    in_bag: int

class MinusToOrder(CallbackData, prefix='minus'):
    index: int
    title: str
    order: int
    in_bag: int

#Устанавливаем параметры клавиатуры для карточек
def get_inline_keyboard(name, title, index_mes=0, order=1, bag=0):
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Связаться с продавцом', url=f'tg://user?id={ADMIN}')
    keyboard_builder.button(text=f'В корзине {bag}', callback_data=InBag(index=index_mes, title=title, order=order - 1, in_bag=bag))

    keyboard_builder.button(text=f'➖ 1', callback_data=MinusToOrder(index=index_mes, title=title, order=order - 1, in_bag=bag))
    keyboard_builder.button(text=f'В заказ {order}', callback_data=SendOrder(index=index_mes, title=title, order=order, in_bag=bag))
    keyboard_builder.button(text=f'➕ 1', callback_data=AddToOrder(index=index_mes, title=title, order=order + 1, in_bag=bag))

    keyboard_builder.button(text=f'➖ 10', callback_data=MinusToOrder(index=index_mes, title=title, order=order - 10, in_bag=bag))
    keyboard_builder.button(text=f'➖ 5', callback_data=MinusToOrder(index=index_mes, title=title, order=order - 5, in_bag=bag))
    keyboard_builder.button(text=f'➕ 5', callback_data=AddToOrder(index=index_mes, title=title, order=order + 5, in_bag=bag))
    keyboard_builder.button(text=f'➕ 10', callback_data=AddToOrder(index=index_mes, title=title, order=order + 10, in_bag=bag))


    keyboard_builder.adjust(2, 3, 4)
    return keyboard_builder.as_markup()

#Прописываем генерацию карточек
async def get_simple_inline(message: Message, bot: Bot):
    for key, value in catalog_dict.items():
        await message.answer_photo(value[1])
        await message.answer(text=f'✅    Товар {value[0]}\n\n'
                                  f'Какое то описание в 250 символов '
                                  f'которое кратко описывает основные характеристикаи и свойства'
                                  f' товара {value[0]}.',
                             reply_markup=get_inline_keyboard(value[0], key, index_mes=0, order=1, bag=0))


# Обработка колбэков карточек через классы
# Колбэк отправки заказа в корзину
async def send_order(call: CallbackQuery, bot: Bot, callback_data: SendOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    k = str(callback_data.title)
    v = catalog_dict.get(k)
    piece = callback_data.order

    user = call.from_user.id
    if orders.get(user) is None:
        orders[user] = dict()
    if orders[user].get(k) is None:
        orders[user][k] = dict()
        orders[user][k]['Значение'] = v[0]
        orders[user][k]['В корзине'] = int(piece)
    else:
        if piece <0:
            if orders[user][k]['В корзине'] + piece <= 0:
                orders[user][k]['В корзине'] = 0

            elif (orders[user][k]['В корзине'] - abs(piece)) >= 0:
                orders[user][k]['В корзине'] -= abs(piece)
                print(orders[user][k]['В корзине'])
        else:
            orders[user][k]['В корзине'] = int(orders[user][k]['В корзине']) + piece

    piece = orders[user][k]['В корзине']


    await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                text=f'✅    Товар {v[0]}\n\n' \
                                     f'Какое то описание в 250 символов ' \
                                     f'которое кратко описывает основные характеристикаи и свойства' \
                                     f' товара {v[0]}.',
                                reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=1, bag=piece))


    # await bot.send_message(ADMIN, f'Пользователь {call.from_user.id} добавил {v[0]} \n '
    #                               f'{piece} штук в заказ')

    await call.answer()

# Колбэк на добавление в заказ
async def add_to_order(call: CallbackQuery, bot: Bot, callback_data: AddToOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    in_bag = callback_data.in_bag

    k = str(callback_data.title)
    v = catalog_dict.get(k)

    plus_peace = callback_data.order

    await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                text=f'✅    Товар {v[0]}\n\n' \
                                     f'Какое то описание в 250 символов ' \
                                     f'которое кратко описывает основные характеристикаи и свойства' \
                                     f' товара {v[0]}.',
                                reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=plus_peace, bag=in_bag))

    await call.answer()


# Колбэк на минусование из заказа
async def minus_to_order(call: CallbackQuery, bot: Bot, callback_data: MinusToOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    k = str(callback_data.title)
    v = catalog_dict.get(k)

    in_bag = callback_data.in_bag


    minus_peace = callback_data.order

    await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                text=f'✅    Товар {v[0]}\n\n' \
                                     f'Какое то описание в 250 символов ' \
                                     f'которое кратко описывает основные характеристикаи и свойства' \
                                     f' товара {v[0]}.',
                                reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=minus_peace, bag=in_bag))

    await call.answer()


#Классы колбэков на работу с коризной
class MinBag(CallbackData, prefix='minbag'):
    val: str
    item: int
    id: int
    title: str

class AddBag(CallbackData, prefix='addbag'):
    val: str
    item: int
    id: int
    title: str

# Колбэк на корзину
async def in_bag_piece(call: CallbackQuery, bot: Bot, callback_data: InBag):
    k = str(callback_data.title)
    v = catalog_dict.get(k)
    piece = callback_data.in_bag


    user = call.from_user.id

    if orders.get(user) is None:
        await call.message.answer('Ваша корзина пуста, добавте товар!')
    else:
        def bag_inline_keyboard():
            keyboard_builder = InlineKeyboardBuilder()

            for value, item in orders[user].items():
                if item.get("В корзине") > 0:
                    keyboard_builder.button(text='-', callback_data='-')
                    keyboard_builder.button(text=f'{item["Значение"]}: {item["В корзине"]} ',
                                            callback_data=' ')
                    keyboard_builder.button(text='+', callback_data='+')

            keyboard_builder.adjust(3)
            return keyboard_builder.as_markup()

        await call.message.answer(text='🛒                               КОРЗИНА: ',
                                  reply_markup=bag_inline_keyboard())

    await call.answer()



################################################

# Блок стартовых функций#########################
#Установка команд в меню, при старте
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начало'),
        BotCommand(command='help', description='Описание Бота'),
        BotCommand(command='inline', description='Карточка товара функция'),
        BotCommand(command='pay', description='Оплата'),
        BotCommand(command='cancel', description='Сбросить'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())  # Скоп по умолчанию|ПОказывает команды всем

#Хэндлер отрабатывает при старте бота
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN, text='Бот запущен!')

#Хэнлер отрабатывает при остановке бота
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Bot is stoped</s>')

#Хэндлер если пользователь шлет команду старт
async def get_start(message: Message, bot: Bot):  # Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')


###############################################

# Тело бота#####################################
async def start():
    #Логи
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot)  # Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=['start']))  # Регистрируем хэндлер на команду /start
    # dp.message.register(get_inline, Command(commands=['inline']))
    dp.message.register(get_simple_inline, Command(commands=['inline']))  # вызов карточек с инлайнами через функцию


    dp.callback_query.register(send_order, SendOrder.filter()) #Регистрируем колбэки на работу с карточками
    dp.callback_query.register(add_to_order, AddToOrder.filter())
    dp.callback_query.register(minus_to_order, MinusToOrder.filter())
    dp.callback_query.register(in_bag_piece, InBag.filter())

    dp.message.register(get_photo, F.photo) #Колбэк на скачивание фото загружаемого в  бота

    try:
        # Начало сессии
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию
        await bot.session.close()


###############################################


# Запускаем функцию Бота########################
if __name__ == "__main__":
    asyncio.run(start())
