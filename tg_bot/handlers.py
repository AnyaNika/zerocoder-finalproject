from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services import get_today_transactions

# Создаем router
router = Router()

# /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я помогу вести учет финансов 😊")

# /today
@router.message(Command("today"))
async def today_handler(message: Message):
    tg_id = message.from_user.id
    transactions = await get_today_transactions(tg_id)  # 🔑 await обязательно

    if transactions:
        text = "\n".join([
            f"{t['amount']} руб — {t['category']}"
            for t in transactions
        ])
    else:
        text = "Сегодня ещё не было транзакций."

    await message.answer(text)