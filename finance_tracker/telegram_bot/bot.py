import logging
import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import sys
import os
import django

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Указываем Django, где искать настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_tracker.finance_tracker.settings")
django.setup()

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