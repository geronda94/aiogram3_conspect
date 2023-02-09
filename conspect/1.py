from aiogram import Bot, Dispatcher
#импортируем бота и диспетчер

#созздаем асинхронную функцию с запуском бота
async def start():
    bot = Bot(token='5783446935:AAFyAOVxRAic6Wx5bSVfoDX6hjs7EC3yjrE')
    dp = Dispatcher()


    try:
        # Через awqit запускаем асинхронную функцию
        await dp.start_polling()
    finally:
        #Закрываем сессию с ботом
        await bot.session.close()











