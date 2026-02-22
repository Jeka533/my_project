import sys
from pathlib import Path

import pytest

from src.widget import get_date, mask_account_card

sys.path.insert(0, str(Path(__file__).parent.parent))


# ТЕСТЫ mask_account_card
@pytest.mark.parametrize("input_str, expected", [
    ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
    ("MasterCard 5555666677778888", "MasterCard 5555 66** **** 8888"),
    ("Maestro 1111222233334444", "Maestro 1111 22** **** 4444"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 40817810099910004321", "Счет **4321"),
])
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    """Тест правильности распознавания типа и маскировки"""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("input_str", [
    "", "   ", "Visa Classic", "Счет", "Счет abc", "1234567890123456"
])
def test_mask_account_card_invalid(input_str: str) -> None:
    """Тест устойчивости к некорректным данным"""
    try:
        result = mask_account_card(input_str)
        assert isinstance(result, str)
    except (ValueError, IndexError, AttributeError):
        pass


def test_mask_account_card_none() -> None:
    """Тест обработки None"""
    with pytest.raises((TypeError, AttributeError)):
        mask_account_card(None)  # type: ignore


# ТЕСТЫ get_date
@pytest.mark.parametrize("input_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2024-02-29T12:00:00", "29.02.2024"),
    ("2024-01-01", "01.01.2024"),
])
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Тест правильности преобразования даты"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize("input_date", [
    "", "   ", "не дата", "2024", "13-13-2024"
])
def test_get_date_invalid(input_date: str) -> None:
    """Тест обработки строк без даты"""
    try:
        result = get_date(input_date)
        assert isinstance(result, str)
    except (ValueError, IndexError, AttributeError):
        pass


def test_get_date_none() -> None:
    """Тест обработки None"""
    result = get_date(None)  # type: ignore
    assert isinstance(result, str)
