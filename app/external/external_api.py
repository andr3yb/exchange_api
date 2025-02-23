import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"
url = f"{BASE_URL}/{API_KEY}/latest/USD"


async def fetch_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Получает курс обмена между валютами с помощью aiohttp."""
    url = f"{BASE_URL}/{API_KEY}/latest/{from_currency.upper()}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            if data.get("result") != "success":
                raise ValueError(f"Ошибка API: {data}")

            rates = data.get("conversion_rates")
            return rates[to_currency.upper()]

async def fetch_supported_currencies() -> dict:
    """Получает список поддерживаемых валют с помощью aiohttp."""
    url = f"{BASE_URL}/{API_KEY}/latest/USD"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

            if data.get("result") != "success":
                raise ValueError(f"Ошибка API: {data}")

            return data.get("conversion_rates")

async def test_external_api():
    """Простая функция для теста запроса к внешнему API."""
    url = f"{BASE_URL}/{API_KEY}/latest/USD"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            print("Ответ от Exchange API:", data)

async def main():
    try:
        print("Начало тестирования...")
        url = f"{BASE_URL}/{API_KEY}/latest/USD"
        # Тестовый запрос к внешнему API
        await test_external_api()
        
        rate = await fetch_exchange_rate("USD", "EUR")
        print(f"Курс USD -> EUR: {rate}")

        currencies = await fetch_supported_currencies()
        print(f"Доступные валюты: {list(currencies.keys())[:10]}")  # Выведем только первые 10 для наглядности
    except Exception as e:
        print(f"Ошибка в main: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
