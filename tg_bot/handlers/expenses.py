from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services import get_categories, add_transaction

router = Router()


# ---------- FSM ----------
class AddExpense(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()


# ---------- начало добавления расхода ----------
@router.callback_query(F.data == "add_expense")
async def add_expense_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddExpense.waiting_for_amount)
    await callback.message.answer("Введите сумму расхода:")
    await callback.answer()  # закрываем "часики"


# ---------- ввод суммы ----------
@router.message(AddExpense.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("⚠️ Введите число, например: 200")
        return

    await state.update_data(amount=amount)

    tg_id = message.from_user.id
    categories = await get_categories(tg_id)

    if not categories:
        await message.answer("❌ У вас пока нет категорий. Добавьте их через меню!")
        await state.clear()
        return

    # строим клавиатуру категорий
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat["name"], callback_data=f"category:{cat['id']}")]
for cat in categories
        ]
    )

    await state.set_state(AddExpense.waiting_for_category)
    await message.answer("Выберите категорию:", reply_markup=kb)


# ---------- выбор категории ----------
@router.callback_query(AddExpense.waiting_for_category, F.data.startswith("category:"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    category_id = callback.data.split(":")[1]

    tg_id = callback.from_user.id
    await add_transaction(tg_id, amount, category_id)

    await callback.message.answer(f"✅ Добавлен расход {amount} руб.")
    await state.clear()
    await callback.answer()