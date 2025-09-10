import logging
import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # В v3 Dispatcher без аргумента bot

async def main():
    # подключаем хендлеры (routers)
    from finance_tracker.telegram_bot import handlers
    dp.include_router(handlers.router)

    # запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())