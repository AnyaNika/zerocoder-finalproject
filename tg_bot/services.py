import aiohttp
from config import API_URL

async def register_user(tg_id: int, username: str):
    url = f"{API_URL}/register_telegram/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"tg_id": tg_id, "username": username}) as response:
            return await response.json()

async def get_today_transactions(tg_id: int):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "date": "today"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []

async def get_week_transactions(tg_id: int):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "date": "week"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []

async def get_category_transactions(tg_id: int, category: str):
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "category": category}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []