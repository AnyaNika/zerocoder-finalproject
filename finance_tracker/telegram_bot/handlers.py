from aiogram import Router, types
from aiogram.filters import Command
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

router = Router()
User = get_user_model()


# Сохраняем или находим пользователя по telegram_id
@sync_to_async
def get_or_create_user(telegram_id: int):
    user, created = User.objects.get_or_create(telegram_id=telegram_id)
    return user, created


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id

    user, created = await get_or_create_user(telegram_id)

    if created:
        await message.answer("Привет! 👋 Ты успешно зарегистрирован в системе.")
    else:
        await message.answer("С возвращением! 👋 Я тебя уже знаю.")

# @router.message(Command("start"))
# async def send_welcome(message: types.Message):
#     user_id = message.from_user.id
#     # сохраняем telegram_id в User
#     await message.answer("Привет! Твой Telegram ID сохранён. Теперь можно работать с данными.")

# @router.message(Command("start"))
# async def send_welcome(message: types.Message):
#     await message.answer("Привет! 👋 Я помогу вести учёт финансов.\nИспользуй /today, /week, /add")

@router.message(Command("today"))
async def today_stats(message: types.Message):
    await message.answer("Сегодняшние расходы: ... (позже подключим БД)")

@router.message(Command("week"))
async def week_stats(message: types.Message):
    await message.answer("Статистика за неделю: ...")

@router.message(Command("add"))
async def add_transaction(message: types.Message):
    await message.answer("Чтобы добавить расход, напиши: /add 500 еда")



