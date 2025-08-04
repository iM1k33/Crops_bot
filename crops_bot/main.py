import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from .config import TELEGRAM_TOKEN
from .handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def run_bot():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Регистрируем роутер
    dp.include_router(router)
    
    logging.info("Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logging.info("Bot stopped")