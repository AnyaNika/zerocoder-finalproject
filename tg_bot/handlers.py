from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from services import (
    get_today_transactions, get_week_transactions, get_categories,
    get_category_transactions, register_user, add_transaction, calculate_week_expenses
)

router = Router()


# ---------- FSM ----------
class AddExpense(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()


# ---------- START ----------
@router.message(Command("start"))
async def start_handler(message: Message):
    tg_id = message.from_user.id
    tg_username = message.from_user.username
    display_name = message.from_user.first_name or message.from_user.username

    data = await register_user(tg_id, tg_username)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить расход", callback_data="add_expense")]
        ]
    )

    if data.get("created"):
        await message.answer(
            f"Привет, {display_name}! Я создал тебе аккаунт ✅", reply_markup=kb
        )
    else:
        await message.answer(
            f"С возвращением, {display_name}! 👋", reply_markup=kb
        )


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


# ---------- FSM: ДОБАВЛЕНИЕ РАСХОДА ----------
@router.callback_query(F.data == "add_expense")
async def add_expense_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddExpense.waiting_for_amount)
    await callback.message.answer("Введите сумму расхода:")
    await callback.answer()  # закрыть "часики"


@router.message(AddExpense.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("⚠️ Введите число, например: 200")
        return

    await state.update_data(amount=amount)

    # подтягиваем категории из базы для конкретного пользователя
    tg_id = message.from_user.id
    categories = await get_categories(tg_id)

    if not categories:
        await message.answer("❌ У вас пока нет категорий. Добавьте их через меню!")
        await state.clear()
        return

     # строим клавиатуру из списка категорий
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat["name"], callback_data=f"category:{cat['name']}")]
            for cat in categories
        ]
    )

    await state.set_state(AddExpense.waiting_for_category)
    await message.answer("Выберите категорию:", reply_markup=kb)


@router.callback_query(AddExpense.waiting_for_category, F.data.startswith("category:"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]

    category = callback.data.split(":", 1)[1]
    tg_id = callback.from_user.id

    # сохраняем расход
    await add_transaction(tg_id, amount, category)

    await state.clear()
    await callback.message.answer(f"✅ Добавлена трата: {amount} руб, категория: {category}")
    await callback.answer()