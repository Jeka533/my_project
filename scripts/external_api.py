"""Модуль для конвертации валют через внешнее API."""

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = os.getenv("EXCHANGE_API_URL")


def get_exchange_rate(currency: str) -> Optional[float]:
    """Получить курс валюты к рублю."""
    if not API_KEY or not API_URL:
        return None

    try:
        headers = {"apikey": API_KEY}
        params = {"base": "RUB", "symbols": currency}

        response = requests.get(API_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        if "rates" in data and currency in data["rates"]:
            rate_value = data["rates"][currency]
            # Убеждаемся, что rate_value - число
            if isinstance(rate_value, (int, float)):
                rate = 1.0 / float(rate_value)
                return round(rate, 4)
        return None

    except Exception:
        return None


def convert_to_rub(amount: float, currency: str) -> Optional[float]:
    """Конвертировать сумму в рубли."""
    if currency == "RUB":
        return amount

    rate = get_exchange_rate(currency)
    if rate is None:
        return None

    return round(amount * rate, 2)


def get_amount_in_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """Получить сумму транзакции в рублях."""
    try:
        amount_data = transaction.get("operationAmount", {})
        if not amount_data:
            return None

        amount = float(amount_data.get("amount", 0))
        currency = amount_data.get("currency", {}).get("code", "RUB")

        return convert_to_rub(amount, currency)
    except (ValueError, TypeError, AttributeError):
        return None


if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ МОДУЛЯ EXTERNAL API")

    print(f"API Key: {' установлен' if API_KEY else ' НЕ УСТАНОВЛЕН'}")
    print(f"API URL: {API_URL}")

    if API_KEY and API_URL:
        rate_usd = get_exchange_rate("USD")
        print(f"\nКурс USD/RUB: {rate_usd}")

        if rate_usd:
            rub = convert_to_rub(100, "USD")
            print(f"100 USD = {rub} RUB")

        test_tx = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}
        amount = get_amount_in_rub(test_tx)
        print(f"50 EUR = {amount} RUB")
