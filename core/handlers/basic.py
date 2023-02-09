from aiogram import Bot
from aiogram.types import Message
from core.settings import ADMIN

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




