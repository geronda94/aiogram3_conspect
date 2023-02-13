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
if not os.path.exists('photo_upload'):
    os.mkdir('photo_upload')

# каталог
catalog_dict = {
    'cofe': ['Кофе', 'AgACAgIAAxkBAAIHD2Pn9a260-cbFoGysWKrAAGwdaX-MwACDMYxGy2hQEvnXrYqnwABehABAAMCAAN5AAMuBA'],
    'tea': ['Чай', 'AgACAgIAAxkBAAIHC2Pn9ZgQpZQlkR6fKKC8MmyPFl0xAAILxjEbLaFAS0p0JkBZhMHOAQADAgADeQADLgQ'],
    'watter': ['Вода', 'AgACAgIAAxkBAAIHDWPn9aV1zXEGFYwc3_ArwUlNK5UuAAIJxjEbLaFAS14Em7lro5AhAQADAgADeQADLgQ'],
    'jam': ['Варенье', 'AgACAgIAAxkBAAIHEmPn9cklVDw3wxsJ1unyDE3solSpAAIGxjEbLaFAS_mANsJE14hXAQADAgADeQADLgQ'],
    'bread': ['Хлеб', 'AgACAgIAAxkBAAIHFGPn9dCzH0A6frSfmRYob_Fcc-hLAAINxjEbLaFAS5_0YLSb-I_XAQADAgADeQADLgQ']}

orders = dict()


async def get_photo(message: Message, bot: Bot):
    await message.answer('Получил картинку')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'photo_upload/{message.photo[-1].file_id}.jpg')


################################################
# Формируем карточки с инлайн клавиатурой
# from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, CallbackQuery


async def get_inline(message: Message, bot: Bot):
    for key, value in catalog_dict.items():
        shop_card = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Заказать оптом {value[0]}', callback_data=f'lorder_{key}'),
                InlineKeyboardButton(text=f'Купить {value[0]}', callback_data=f'lbuy_{key}')
            ], [
                InlineKeyboardButton(text='Узнать погоду', url='https://gismeteo.md'),
                InlineKeyboardButton(text='Связаться с продавцом', url='tg://user?id=413281115')
            ]
        ])
        await message.answer_photo(
            value[1],
            caption=f'✅    Товар {value[0]}\n\n'
                    f'Какое то описание в 250 символов '
                    f'которое кратко описывает основные характеристикаи и свойства'
                    f'данного товара.',
            reply_markup=shop_card)
        time.sleep(0.1)


# Обработка колбэков через парсинг
async def lcallback_order(call: CallbackQuery, bot: Bot):
    index = str(call.data.split('_')[-1])

    await call.message.answer(f'Вы добавили в оптовый заказ {catalog_dict.get(index)[0]}')
    await bot.send_message(ADMIN,
                           f'Пользователь {call.from_user.id} добавили в оптовый заказ {catalog_dict.get(index)[0]}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк


async def lcallback_buy(call: CallbackQuery, bot: Bot):
    index = str(call.data.split('_')[-1])

    await call.message.answer(f'Вы заказали в розницу {catalog_dict.get(index)[0]}')
    await bot.send_message(ADMIN, f'Пользователь {call.from_user.id} хочет купить {catalog_dict.get(index)[0]}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк


################################################

# Формируем инлайн кнопки вторым способом
# from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
class CardDataOrder(CallbackData, prefix='order'):
    title: str


class CardDataBuy(CallbackData, prefix='buy'):
    title: str

class SendOrder(CallbackData, prefix='update'):
    index: int
    title: str
    order: int

class AddToOrder(CallbackData, prefix='add'):
    index: int
    title: str
    order: int

class MinusToOrder(CallbackData, prefix='minus'):
    index: int
    title: str
    order: int

def get_inline_keyboard(name, title, index_mes=0, order=1):
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Связаться с продавцом', url=f'tg://user?id={ADMIN}')


    keyboard_builder.button(text=f'➖ 1', callback_data=MinusToOrder(index=index_mes, title=title, order=order-1))
    keyboard_builder.button(text=f'В заказ {order}', callback_data=SendOrder(index=index_mes, title=title, order=order))
    keyboard_builder.button(text=f'➕ 1', callback_data=AddToOrder(index=index_mes, title=title, order=order+1))

    keyboard_builder.button(text=f'➖ 10', callback_data=MinusToOrder(index=index_mes, title=title, order=order - 10))
    keyboard_builder.button(text=f'➖ 5', callback_data=MinusToOrder(index=index_mes, title=title, order=order - 5))
    keyboard_builder.button(text=f'➕ 10', callback_data=AddToOrder(index=index_mes, title=title, order=order + 10))
    keyboard_builder.button(text=f'➕ 5', callback_data=AddToOrder(index=index_mes, title=title, order=order + 5))


    # keyboard_builder.button(text=f'Купить {name}', callback_data=CardDataBuy(title=title))
    # keyboard_builder.button(text=f'Заказать оптом {name}', callback_data=CardDataOrder(title=title))
    #keyboard_builder.button(text='Узнать погоду', url='https://gismeteo.md')
    #

    keyboard_builder.adjust(1, 3, 4)
    return keyboard_builder.as_markup()



async def get_simple_inline(message: Message, bot: Bot):
    for key, value in catalog_dict.items():
        await message.answer_photo(value[1])
        await message.answer(text=f'✅    Товар {value[0]}\n\n'
                    f'Какое то описание в 250 символов '
                    f'которое кратко описывает основные характеристикаи и свойства'
                    f' товара {value[0]}.',
                    reply_markup=get_inline_keyboard(value[0], key, index_mes=0, order=1))


# Обработка колбэков через классы
async def callback_order(call: CallbackQuery, bot: Bot, callback_data: CardDataOrder):
    index = callback_data.title

    await call.message.answer(f'Вы добавили в оптовый заказ {catalog_dict.get(index)[0]}')


    message_num = call.message.message_id
    await bot.send_message(ADMIN,
                           f'Пользователь {call.from_user.id} добавили в оптовый заказ {catalog_dict.get(index)[0]}'
                           f'\nСообщение номер {message_num}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк


async def callback_buy(call: CallbackQuery, bot: Bot, callback_data: CardDataBuy):
    index = callback_data.title
    message_num = call.message.message_id

    await call.message.answer(f'Вы заказали в розницу {catalog_dict.get(index)[0]}')
    await bot.send_message(ADMIN, f'Пользователь {call.from_user.id} хочет купить {catalog_dict.get(index)[0]}'
                           f'\nСообщение номер {message_num}')
    await call.answer()  # Отвечаем телеграму что мы обработали колбэк

async def send_order(call: CallbackQuery, bot:Bot, callback_data: SendOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    k = str(callback_data.title)
    v = catalog_dict.get(k)
    piece = callback_data.order

    user = call.from_user.id

    orders[user] = dict()
    orders[user][k] = {'Значение':v[0], 'В корзине':piece}

    print(orders[user][k])

    await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                text=f'✅    Товар {v[0]}\n\n' \
                                     f'Какое то описание в 250 символов ' \
                                     f'которое кратко описывает основные характеристикаи и свойства' \
                                     f' товара {v[0]}.',
                                reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=1))

    await call.message.answer( f'Вы добавили {v[0]}, {piece} штук в заказ')
    await bot.send_message(ADMIN, f'Пользователь {call.message.from_user.id} добавил {v[0]} \n '
                                  f'{piece} штук в заказ')

    await call.answer()


async def add_to_order(call: CallbackQuery, bot:Bot, callback_data: AddToOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    k = str(callback_data.title)
    v = catalog_dict.get(k)

    plus_peace = callback_data.order

    await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                text=f'✅    Товар {v[0]}\n\n'\
                                    f'Какое то описание в 250 символов '\
                                    f'которое кратко описывает основные характеристикаи и свойства'\
                                    f' товара {v[0]}.',
                                reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=plus_peace))

    await call.answer()


async def minus_to_order(call: CallbackQuery, bot:Bot, callback_data: MinusToOrder):
    message_num = call.message.message_id
    chat = call.message.chat.id
    k = str(callback_data.title)
    v = catalog_dict.get(k)

    if callback_data.order > 0:
        minus_peace = callback_data.order

        await bot.edit_message_text(chat_id=chat, message_id=message_num,
                                    text=f'✅    Товар {v[0]}\n\n'\
                                        f'Какое то описание в 250 символов '\
                                        f'которое кратко описывает основные характеристикаи и свойства'\
                                        f' товара {v[0]}.',
                                    reply_markup=get_inline_keyboard(v[0], k, index_mes=message_num, order=minus_peace))

    await call.answer()

################################################

# Блок стартовых функций#########################
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начало'),
        BotCommand(command='help', description='Описание Бота'),
        BotCommand(command='inline', description='Карточка товара функция'),
        BotCommand(command='cancel', description='Сбросить'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN, text='Бот запущен!')

async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Bot is stoped</s>')


async def get_start(message: Message, bot: Bot):  # Функция срабатывает когда юзер дает команду /start
    await message.answer('Давай начнем!')


###############################################

# Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot)  # Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=['start']))  # Регистрируем хэндлер на команду /start
    # dp.message.register(get_inline, Command(commands=['inline']))
    dp.message.register(get_simple_inline, Command(commands=['inline']))  # вызов карточек с инлайнами через функцию

    dp.callback_query.register(callback_order, CardDataOrder.filter())  # Регистрируем колбэки через классы
    dp.callback_query.register(callback_buy, CardDataBuy.filter())
    dp.callback_query.register(send_order, SendOrder.filter())
    dp.callback_query.register(add_to_order, AddToOrder.filter())
    dp.callback_query.register(minus_to_order, MinusToOrder.filter())

    dp.message.register(get_photo, F.photo)

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
