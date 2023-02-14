from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, LabeledPrice, PreCheckoutQuery
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

async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка черезе телеграм бота',
        description='Учимся принимать платежи через телеграм',
        payload='Payment',
        provider_token='381764678:TEST:49867',
        currency='RUB',
        prices=[
            LabeledPrice(label='Доступ', amount=100000),
            LabeledPrice(label='НДС', amount=20000),
            LabeledPrice(label='Скидка', amount=-20000),
            LabeledPrice(label='Бонус', amount=-40000)
        ],
        max_tip_amount=500000,
        suggested_tip_amounts=[5000, 100000, 200000, 500000],
        start_parameter='Geronda',
        provider_data=None,
        photo_url='https://cdn-icons-png.flaticon.com/512/5816/5816466.png',
        photo_size=150,
        photo_width=150,
        photo_height=200,
        need_name=True, #Если нужно имя пользователя
        need_phone_number=True, #Если нужен телефон пользователя
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False, #Если конечная цена зависит от способа доставки
        disable_notification=True, #СОобщение доставляется без звука
        protect_content=False, #Если нужно защитить пост от пересылки и копирования ТРуе
        reply_to_message_id= False, #указываем ид сообщения если хотим прикрепть его к счету
        allow_sending_without_reply= True, #Разрешается отправить счет на оплату даже если цитируемое сообщение не найдено
        reply_markup=None, #МОжно добавить клавиатуру
        #request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True )

async def succesful_payment(message: Message):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}' \
          f'\r\nнаш менеджер получил заявку и уже звонит вам'
    await message.answer(msg)












#Блок стартовых функций#########################
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await bot.send_message(ADMIN, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Бот остановлен</s>')
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

    dp.message.register(order, Command(commands='pay'))

    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start





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


