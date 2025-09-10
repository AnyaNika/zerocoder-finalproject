from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! 👋 Я помогу вести учёт финансов.\nИспользуй /today, /week, /add")

@router.message(Command("today"))
async def today_stats(message: types.Message):
    await message.answer("Сегодняшние расходы: ... (позже подключим БД)")

@router.message(Command("week"))
async def week_stats(message: types.Message):
    await message.answer("Статистика за неделю: ...")

@router.message(Command("add"))
async def add_transaction(message: types.Message):
    await message.answer("Чтобы добавить расход, напиши: /add 500 еда")