"""Тесты для модуля generators."""

import os
import sys
from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # noqa


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет"
        }
    ]


def test_filter_by_currency_usd(transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по USD."""
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)


def test_filter_by_currency_rub(transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по RUB."""
    result = list(filter_by_currency(transactions, "RUB"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_empty() -> None:
    """Тест с пустым списком."""
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_no_matches(transactions: List[Dict[str, Any]]) -> None:
    """Тест с валютой, которой нет в транзакциях."""
    assert list(filter_by_currency(transactions, "EUR")) == []


def test_transaction_descriptions(transactions: List[Dict[str, Any]]) -> None:
    """Тест получения описаний."""
    result = list(transaction_descriptions(transactions))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет"
    ]


def test_transaction_descriptions_empty() -> None:
    """Тест с пустым списком."""
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize("start, end, expected", [
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]),
    (9999999999999995, 9999999999999997, [
        "9999 9999 9999 9995",
        "9999 9999 9999 9996",
        "9999 9999 9999 9997"
    ]),
])
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    """Тест генерации номеров карт."""
    assert list(card_number_generator(start, end)) == expected


def test_card_number_generator_single() -> None:
    """Тест генерации одного номера."""
    assert list(card_number_generator(1, 1)) == ["0000 0000 0000 0001"]


def test_card_number_generator_format() -> None:
    """Тест формата номера карты."""
    result = list(card_number_generator(1234567890123456, 1234567890123456))
    assert result[0] == "1234 5678 9012 3456"
