from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from services import register_user

router = Router()


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
        await message.answer(f"Привет, {display_name}! Я создал тебе аккаунт ✅", reply_markup=kb)
    else:
        await message.answer(f"С возвращением, {display_name}! 👋", reply_markup=kb)