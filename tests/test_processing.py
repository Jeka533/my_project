import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date

sys.path.insert(0, str(Path(__file__).parent.parent))


# ТЕСТЫ ДЛЯ filter_by_state
@pytest.fixture
def test_data() -> List[Dict[str, Any]]:
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
def test_filter_by_state(test_data: List[Dict[str, Any]], state: str, expected_count: int) -> None:
    """Тест фильтрации по разным статусам"""
    result = filter_by_state(test_data, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(item["state"] == state for item in result)


def test_filter_by_state_empty_list() -> None:
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []


def test_filter_by_state_default_state(test_data: List[Dict[str, Any]]) -> None:
    """Тест фильтрации со статусом по умолчанию (EXECUTED)"""
    result = filter_by_state(test_data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


# ТЕСТЫ ДЛЯ sort_by_date
@pytest.fixture
def unsorted_data() -> List[Dict[str, Any]]:
    """Фикстура с несортированными данными"""
    return [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "date": "2019-01-01"},
        {"id": 3, "date": "2021-01-01"},
        {"id": 4, "date": "2018-01-01"},
    ]


def test_sort_by_date_descending(unsorted_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по убыванию (новые сначала)"""
    result = sort_by_date(unsorted_data)
    assert [item["id"] for item in result] == [3, 1, 2, 4]


def test_sort_by_date_ascending(unsorted_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по возрастанию (старые сначала)"""
    result = sort_by_date(unsorted_data, is_reverse=False)
    assert [item["id"] for item in result] == [4, 2, 1, 3]


def test_sort_by_date_same_dates() -> None:
    """Тест сортировки при одинаковых датах"""
    data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2, "date": "2020-01-01"},
        {"id": 3, "date": "2019-01-01"},
    ]
    result = sort_by_date(data)
    assert result[0]["date"] == "2020-01-01"
    assert result[1]["date"] == "2020-01-01"
    assert result[2]["date"] == "2019-01-01"


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка"""
    empty_list: List[Dict[str, Any]] = []
    assert sort_by_date(empty_list) == []


def test_sort_by_date_missing_date() -> None:
    """Тест сортировки при отсутствии ключа 'date'"""
    data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2020-01-01"},
        {"id": 2},
        {"id": 3, "date": "2019-01-01"},
    ]
    with pytest.raises(KeyError):
        sort_by_date(data)


def test_sort_by_date_original_unchanged(unsorted_data: List[Dict[str, Any]]) -> None:
    """Тест, что исходный список не изменяется"""
    original_copy = unsorted_data.copy()
    sort_by_date(unsorted_data)
    assert unsorted_data == original_copy
