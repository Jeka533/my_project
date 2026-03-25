"""Модуль для конвертации валют через внешнее API."""

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_API_URL = "https://api.apilayer.com/exchangerates_data"


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Конвертирует сумму из одной валюты в другую, используя эндпоинт /convert.

    Args:
        amount: Сумма для конвертации.
        from_currency: Код исходной валюты (например, "USD").
        to_currency: Код целевой валюты (по умолчанию "RUB").

    Returns:
        Сконвертированная сумма или None в случае ошибки.
    """
    if not API_KEY:
        print("Ошибка: не настроен API ключ")
        return None

    if to_currency == from_currency:
        return amount

    url = f"{BASE_API_URL}/convert"
    headers = {"apikey": API_KEY}
    params = {
        "to": to_currency,
        "from": from_currency,
        "amount": str(amount)
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("success") and "result" in data:
            return round(float(data["result"]), 2)
        else:
            print(f"API вернул ошибку: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

    except Exception:  # Ловим ЛЮБОЕ исключение
        return None


def get_amount_in_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """Получить сумму транзакции в рублях."""
    try:
        amount_data = transaction.get("operationAmount", {})
        if not amount_data:
            return None

        amount = float(amount_data.get("amount", 0))
        currency = amount_data.get("currency", {}).get("code", "RUB")

        return convert_currency(amount, currency, "RUB")
    except (ValueError, TypeError, AttributeError):
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ МОДУЛЯ EXTERNAL API")
    print("=" * 50)

    print(f"API Key: {' установлен' if API_KEY else ' НЕ УСТАНОВЛЕН'}")

    if API_KEY:
        # Тест конвертации USD -> RUB
        rub = convert_currency(100, "USD", "RUB")
        print(f"\n100 USD = {rub} RUB")

        # Тест с транзакцией
        test_tx = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR"}
            }
        }
        amount = get_amount_in_rub(test_tx)
        print(f"50 EUR = {amount} RUB")
