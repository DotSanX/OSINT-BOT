from aiogram import Bot, Dispatcher
from concurrent.futures import ProcessPoolExecutor
from handlers import setup_handlers

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
executor = ProcessPoolExecutor(max_workers=4)

def main():
    setup_handlers(dp, executor, bot)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()