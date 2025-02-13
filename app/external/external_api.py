import aiohttp
import asyncio

API_KEY = "4bce26ed99e211f5b63823da"
BASE_URL = "https://v6.exchangerate-api.com/v6"

async def fetch_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Получает курс обмена между валютами с помощью aiohttp.
    """
    url = f"{BASE_URL}/{API_KEY}/latest/{from_currency.upper()}"
    print(f"Запрос курса валют: {url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"Статус ответа: {response.status}")
                if response.status != 200:
                    raise Exception(f"Ошибка API: {response.status}")

                data = await response.json()
                print("Ответ API:", data)

                if data.get("result") != "success":
                    raise Exception(f"Ошибка API: {data}")

                rates = data.get("conversion_rates")
                if not rates or to_currency.upper() not in rates:
                    raise Exception(f"Курс обмена для {to_currency.upper()} не найден.")

                return rates[to_currency.upper()]
    except Exception as e:
        print(f"Ошибка в fetch_exchange_rate: {e}")

async def fetch_supported_currencies() -> dict:
    """
    Получает список поддерживаемых валют с помощью aiohttp.
    """
    url = f"{BASE_URL}/{API_KEY}/latest/USD"
    print(f"Запрос списка валют: {url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(f"Статус ответа: {response.status}")
                if response.status != 200:
                    raise Exception(f"Ошибка API: {response.status}")

                data = await response.json()
                print("Ответ API:", data)

                if data.get("result") != "success":
                    raise Exception(f"Ошибка API: {data}")

                rates = data.get("conversion_rates")
                if not rates:
                    raise Exception("Данные о курсах валют не найдены в ответе API.")

                return rates  # Можно заменить на list(rates.keys()), если нужен только список валютных кодов
    except Exception as e:
        print(f"Ошибка в fetch_supported_currencies: {e}")

async def main():
    try:
        print("Начало тестирования...")
        rate = await fetch_exchange_rate("USD", "EUR")
        print(f"Курс USD -> EUR: {rate}")

        currencies = await fetch_supported_currencies()
        print(f"Доступные валюты: {list(currencies.keys())[:10]}")  # Выведем только первые 10 для наглядности
    except Exception as e:
        print(f"Ошибка в main: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

