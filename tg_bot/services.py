import aiohttp
from config import API_URL

async def get_today_transactions(tg_id: int):
    """
    Асинхронный запрос в Django API, чтобы получить транзакции за сегодня
    """
    url = f"{API_URL}/transactions/"
    params = {"tg_id": tg_id, "date": "today"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            return []