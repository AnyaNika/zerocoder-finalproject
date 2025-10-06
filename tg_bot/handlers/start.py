from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot.services import register_user
from tg_bot.keyboards import kb_expense


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    tg_id = message.from_user.id
    tg_username = message.from_user.username
    display_name = message.from_user.first_name or message.from_user.username

    data = await register_user(tg_id, tg_username)


    if data.get("created"):
        await message.answer(f"Привет, {display_name}! Я создал тебе аккаунт ✅", reply_markup=kb_expense)
    else:
        await message.answer(f"С возвращением, {display_name}! 👋", reply_markup=kb_expense)

@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start — приветствие и добавление расходов\n"
        "/today — расходы за сегодня\n"
        "/week — статистика за неделю\n"
        "/category food — траты по категории\n"
    )
    await message.answer(help_text, reply_markup=kb_expense)