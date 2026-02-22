import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.widget import mask_account_card, get_date


# ТЕСТЫ mask_account_card

@pytest.mark.parametrize("input_str, expected", [
    # Карты (разные типы)
    ("Visa Classic 1234567890123456", "Visa Classic 1234 56** **** 3456"),
    ("MasterCard 5555666677778888", "MasterCard 5555 66** **** 8888"),
    ("Maestro 1111222233334444", "Maestro 1111 22** **** 4444"),
    # Счета
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 40817810099910004321", "Счет **4321"),
])
def test_mask_account_card_valid(input_str, expected):
    """Тест правильности распознавания типа и маскировки"""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("input_str", [
    "", "   ", "Visa Classic", "Счет", "Счет abc", "1234567890123456"
])
def test_mask_account_card_invalid(input_str):
    """Тест устойчивости к некорректным данным"""
    try:
        result = mask_account_card(input_str)
        assert isinstance(result, str)
    except (ValueError, IndexError, AttributeError):
        pass


def test_mask_account_card_none():
    """Тест обработки None"""
    with pytest.raises((TypeError, AttributeError)):
        mask_account_card(None)


# ТЕСТЫ get_date

@pytest.mark.parametrize("input_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2024-02-29T12:00:00", "29.02.2024"),  # Високосный год
    ("2024-01-01", "01.01.2024"),            # Только дата
])
def test_get_date_valid(input_date, expected):
    """Тест правильности преобразования даты"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize("input_date", [
    "", "   ", "не дата", "2024", "13-13-2024"
])
def test_get_date_invalid(input_date):
    """Тест обработки строк без даты"""
    try:
        result = get_date(input_date)
        assert isinstance(result, str)
    except (ValueError, IndexError, AttributeError):
        pass


def test_get_date_none():
    """Тест обработки None - функция должна вернуть строку"""
    result = get_date(None)
    assert isinstance(result, str)
