"""
Фикстуры для тестов.
"""
import pytest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_card_number():
    """Возвращает пример номера карты."""
    return "7000792289606361"


@pytest.fixture
def sample_account_number():
    """Возвращает пример номера счета."""
    return "73654108430135874305"


@pytest.fixture
def sample_date():
    """Возвращает пример даты."""
    return "2024-03-11T02:26:18.671407"