from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services import (get_today_transactions, get_week_transactions,
                      calculate_week_expenses, get_category_transactions)

router = Router()


# ---------- TODAY ----------
@router.message(Command("today"))
async def today_handler(message: Message):
    tg_id = message.from_user.id
    transactions = await get_today_transactions(tg_id)

    if transactions:
        text = "\n".join([f"{t['amount']} руб — {t['category']}" for t in transactions])
    else:
        text = "Сегодня ещё не было транзакций."

    await message.answer(text)


# ---------- WEEK ----------
@router.message(Command("week"))
async def week_handler(message: Message):
    tg_id = message.from_user.id
    transactions = await get_week_transactions(tg_id)

    total_expenses = calculate_week_expenses(transactions)
    print("Расходы за неделю:", total_expenses)

    if transactions:
        total = sum(float(t["amount"]) for t in transactions)
        text = f"За последние 7 дней: {total} руб."
    else:
        text = "За неделю транзакций нет."

    await message.answer(text)


# ---------- CATEGORY ----------
@router.message(Command("category"))
async def category_handler(message: Message):
    tg_id = message.from_user.id
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Укажи категорию: /category food")
        return

    category = parts[1]
    transactions = await get_category_transactions(tg_id, category)

    if transactions:
        total = sum(float(t["amount"]) for t in transactions)
        text = f"Всего по категории '{category}': {total} руб."
    else:
        text = f"Нет транзакций по категории '{category}'."

    await message.answer(text)