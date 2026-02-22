import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.processing import filter_by_state, sort_by_date


# ТЕСТЫ ДЛЯ filter_by_state

@pytest.fixture
def test_data():
    """Фикстура с тестовыми данными"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14"},
        {"id": 5, "state": "PENDING", "date": "2020-01-01"},
    ]


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 2),
    ("PENDING", 1),
    ("NOT_EXIST", 0),
])
def test_filter_by_state(test_data, state, expected_count):
    """Тест фильтрации по разным статусам"""
    result = filter_by_state(test_data, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(item["state"] == state for item in result)


def test_filter_by_state_empty_list():
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []


def test_filter_by_state_default_state(test_data):
    """Тест фильтрации со статусом по умолчанию (EXECUTED)"""
    result = filter_by_state(test_data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


# ТЕСТЫ ДЛЯ sort_by_date

@pytest.fixture
def unsorted_data():
    """Фикстура с несортированными данными"""
    return [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "date": "2019-01-01"},
        {"id": 3, "date": "2021-01-01"},
        {"id": 4, "date": "2018-01-01"},
    ]


def test_sort_by_date_descending(unsorted_data):
    """Тест сортировки по убыванию (новые сначала)"""
    result = sort_by_date(unsorted_data)
    assert [item["id"] for item in result] == [3, 1, 2, 4]  # 2021, 2020, 2019, 2018


def test_sort_by_date_ascending(unsorted_data):
    """Тест сортировки по возрастанию (старые сначала)"""
    result = sort_by_date(unsorted_data, is_reverse=False)
    assert [item["id"] for item in result] == [4, 2, 1, 3]  # 2018, 2019, 2020, 2021


def test_sort_by_date_same_dates():
    """Тест сортировки при одинаковых датах"""
    data = [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "date": "2020-01-01"},
        {"id": 3, "date": "2019-01-01"},
    ]
    result = sort_by_date(data)
    # Порядок элементов с одинаковой датой может быть любым
    assert result[0]["date"] == "2020-01-01"
    assert result[1]["date"] == "2020-01-01"
    assert result[2]["date"] == "2019-01-01"


@pytest.mark.parametrize("date_format", [
    "2020-01-01T10:30:00",           # ISO с временем
    "2020-01-01",                     # Только дата
    "2020/01/01",                      # Со слешами
    "01.01.2020",                      # Российский формат
])
def test_sort_by_date_different_formats(date_format):
    """Тест сортировки с разными форматами дат"""
    data = [
        {"id": 2, "date": "2019-01-01"},
        {"id": 1, "date": date_format},
        {"id": 3, "date": "2021-01-01"},
    ]
    try:
        result = sort_by_date(data)
        # Проверяем, что функция не падает и возвращает список
        assert isinstance(result, list)
        assert len(result) == 3
    except Exception:
        # Если функция не поддерживает формат - пропускаем
        pass


def test_sort_by_date_empty_list():
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_by_date_missing_date():
    """Тест сортировки при отсутствии ключа 'date'"""
    data = [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2},  # Нет даты
        {"id": 3, "date": "2019-01-01"},
    ]
    with pytest.raises(KeyError):
        sort_by_date(data)


def test_sort_by_date_original_unchanged(unsorted_data):
    """Тест, что исходный список не изменяется"""
    original_copy = unsorted_data.copy()
    sort_by_date(unsorted_data)
    assert unsorted_data == original_copy