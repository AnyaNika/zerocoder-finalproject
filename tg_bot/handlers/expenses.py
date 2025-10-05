from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from tg_bot.services import get_categories, add_transaction
from tg_bot.keyboards import get_category_keyboard


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

    # подтягиваем категории из базы для конкретного пользователя
    tg_id = message.from_user.id
    categories = await get_categories(tg_id)

    if not categories:
        await message.answer("❌ У вас пока нет категорий. Добавьте их через личный кабинет!")
        await state.clear()
        return

    # строим клавиатуру из списка категорий
    kb_category = get_category_keyboard(categories)

    await state.set_state(AddExpense.waiting_for_category)
    await message.answer("Выберите категорию:", reply_markup=kb_category)


# ---------- выбор категории ----------
@router.callback_query(AddExpense.waiting_for_category, F.data.startswith("category:"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    category_id_str = callback.data.split(":")[1]
    tg_id = callback.from_user.id

    # Проверяем и конвертируем category_id
    try:
        category_id = int(category_id_str)
    except ValueError:
        await callback.message.answer("❌ Ошибка: некорректная категория.")
        await callback.answer()
        return

    # Проверяем наличие и тип amount
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        await callback.message.answer("❌ Ошибка: некорректная сумма.")
        await callback.answer()
        await state.clear()
        return

    # сохраняем расход
    await add_transaction(tg_id, amount, category_id)
    await callback.message.answer(f"✅ Добавлен расход {amount} руб.")
    await state.clear()
    await callback.answer()