"""
Фикстуры для тестов.
"""

import os
import sys
from typing import Any, Dict, List

import pytest

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Возвращает пример транзакций для тестов."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]


@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Возвращает пример номеров карт для тестов."""
    return ["7000792289606361", "7158300734726758", "1596837868705199"]


@pytest.fixture
def sample_date() -> str:
    """Возвращает пример даты для тестов."""
    return "2024-03-11T02:26:18.671407"
