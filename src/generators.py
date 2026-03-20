"""Модуль с функциями-генераторами для обработки транзакций."""

from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте."""
    for transaction in transactions:
        if (
            transaction.get("operationAmount")
            and transaction["operationAmount"].get("currency")
            and transaction["operationAmount"]["currency"].get("code") == currency
        ):
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Возвращает описания транзакций по очереди."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генерирует номера банковских карт в заданном диапазоне."""
    for number in range(start, end + 1):
        num_str = str(number).zfill(16)
        yield f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
