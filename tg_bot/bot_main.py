import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router  # импортируем router вместо функции register_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Подключаем router с хендлерами
    dp.include_router(router)

    # Запускаем бота (polling)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())