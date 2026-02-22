import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.masks import get_mask_card_number, get_mask_account


# ТЕСТЫ КАРТЫ
@pytest.mark.parametrize("card,expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("5555666677778888", "5555 66** **** 8888"),
])
def test_card_valid(card, expected):
    assert get_mask_card_number(card) == expected


@pytest.mark.parametrize("card", [
    "123", "123456789012345", "1234 5678 9012 3456", "", "abc"
])
def test_card_invalid(card):
    assert get_mask_card_number(card) == "Введен некорректный номер карты"


def test_card_none():
    with pytest.raises((TypeError, AttributeError)):
        get_mask_card_number(None)


#  ТЕСТЫ СЧЕТА
@pytest.mark.parametrize("acc,expected", [
    ("12345678901234567890", "**7890"),
    ("00000000000000000000", "**0000"),
])
def test_account_valid(acc, expected):
    assert get_mask_account(acc) == expected


@pytest.mark.parametrize("acc", [
    "123", "12345678", "1234567890123456789", "", "abc", "1234 5678 9012 3456 7890"
])
def test_account_invalid(acc):
    assert get_mask_account(acc) == "Введен некорректный номер счета"


def test_account_none():
    with pytest.raises((TypeError, AttributeError)):
        get_mask_account(None)