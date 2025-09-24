import aiohttp
from config import API_URL
from datetime import date, datetime, timedelta


async def register_user(tg_id: int, tg_username: str):
    url = f"{API_URL}/register_telegram/"
    payload = {"tg_id": tg_id, "username": tg_username}
    print("Отправляем данные в register_user:", payload)  # <-- Лог
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            text = await response.text()
            print("Ответ сервера register_user:", response.status, text)  # <-- Лог
            return await response.json()


async def add_transaction(tg_id: int, amount: float, category_name: str):
    category_id = await get_category_id(tg_id, category_name)
    if category_id is None:
        return {"error": "Категория не найдена", "category": category_name}

    url = f"{API_URL}/transactions/"
    payload = {
        "tg_id": tg_id,
        "amount": amount,
        "category": category_id,  # <-- отправляем ID категории
        "type": "expense",
        "date": str(date.today())
    }
    print("Отправляем данные в add_transaction:", payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            text = await response.text()
            print("Ответ сервера add_transaction:", response.status, text)
            if response.status == 201:
                return await response.json()
            else:
                return {"error": response.status, "details": text}


async def get_today_transactions(tg_id: int):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "date": "today"}
    print("GET today:", params)  # <-- Лог
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            text = await response.text()
            print("Ответ сервера get_today_transactions:", response.status, text)  # <-- Лог
            if response.status == 200:
                return await response.json()
            return []


async def get_week_transactions(tg_id: int):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id}  # убираем "date":"week", если сервер сам не фильтрует
    print("GET week:", params)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            text = await response.text()
            print("Ответ сервера get_week_transactions:", response.status, text)

            if response.status == 200:
                transactions = await response.json()

                # === Фильтруем только последние 7 дней ===
                today = datetime.today().date()
                week_ago = today - timedelta(days=7)

                week_transactions = []
                for tr in transactions:
                    # Превращаем строку в дату
                    tr_date = datetime.strptime(tr["date"], "%Y-%m-%d").date()

                    if week_ago <= tr_date <= today:
                        week_transactions.append(tr)

                return week_transactions

            return []


async def get_category_transactions(tg_id: int, category: str):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "category": category}
    print("GET category:", params)  # <-- Лог
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            text = await response.text()
            print("Ответ сервера get_category_transactions:", response.status, text)  # <-- Лог
            if response.status == 200:
                return await response.json()
            return []

async def get_categories(tg_id: int):
    url = f"{API_URL}/categories/"
    params = {"tg_id": tg_id}  # чтобы сервер вернул категории именно этого пользователя
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            text = await response.text()
            print("Ответ сервера get_categories:", response.status, text)
            if response.status == 200:
                return await response.json()
            return []

async def get_category_id(tg_id: int, category_name: str):
    categories = await get_categories(tg_id)
    for cat in categories:
        if cat["name"].lower() == category_name.lower():
            return cat["id"]
    return None

def calculate_week_expenses(transactions):
    total = 0
    for tr in transactions:
        if tr.get("type") == "expense":  # считаем только расходы
            total += float(tr["amount"])
    return total