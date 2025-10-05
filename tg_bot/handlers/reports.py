from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.services import (get_today_transactions, get_week_transactions,
                             calculate_week_expenses, get_category_transactions, get_category_id_by_name
                             )

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

    category_name = parts[1]
    category_id = await get_category_id_by_name(tg_id, category_name)
    if not category_id:
        await message.answer(f"Категория '{category_name}' не найдена.")
        return

    transactions = await get_category_transactions(tg_id, category_id)
    print(transactions)

    if transactions:
        expenses = [float(t["amount"]) for t in transactions if t.get("type") == "expense"]
        incomes = [float(t["amount"]) for t in transactions if t.get("type") == "income"]

        total_expense = sum(expenses)
        total_income = sum(incomes)
        total = total_income - total_expense

        text = (
            f"Всего расходов по категории '{category_name}': {total_expense} руб.\n"
            f"Всего доходов по категории '{category_name}': {total_income} руб.\n"
            f"Общий итог по категории '{category_name}': {total} руб."
        )
    else:
        text = f"Нет транзакций по категории '{category_name}'."

    await message.answer(text)