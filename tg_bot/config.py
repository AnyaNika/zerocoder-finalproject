import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")
if not API_URL:
    raise ValueError("❌ API_URL не найден в .env")