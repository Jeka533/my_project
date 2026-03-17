# tests/test_utils.py

import json
import os
import sys
import tempfile

import pytest

from scripts.utils import load_transactions

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_normal_file() -> None:
    """Тест с реальным файлом"""
    for path in ["data/operations.json", "data/operations.json.py"]:
        if os.path.exists(path):
            data = load_transactions(path)
            print(f" Найдено {len(data)} транзакций")
            assert len(data) > 0
            return
    print(" Файл operations.json не найден, тест пропущен")
    pytest.skip("Нет файла с данными")


def test_file_not_found() -> None:
    """Тест с несуществующим файлом"""
    result = load_transactions("нет_такого_файла.json")
    assert result == []


def test_empty_file() -> None:
    """Тест с пустым файлом"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("")
        name = f.name

    result = load_transactions(name)
    os.remove(name)
    assert result == []


def test_invalid_json() -> None:
    """Тест с битым JSON"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{абырвалг")
        name = f.name

    result = load_transactions(name)
    os.remove(name)
    assert result == []


def test_dict_not_list() -> None:
    """Тест со словарем вместо списка"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"ключ": "значение"}, f)
        name = f.name

    result = load_transactions(name)
    os.remove(name)
    assert result == []


def test_valid_json() -> None:
    """Тест с правильным JSON"""
    test_data = [{"id": 1}, {"id": 2}, {"id": 3}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        name = f.name

    result = load_transactions(name)
    os.remove(name)
    assert len(result) == 3


if __name__ == "__main__":
    print("Запуск тестов...")
    test_file_not_found()
    test_empty_file()
    test_invalid_json()
    test_dict_not_list()
    test_valid_json()
    test_normal_file()
    print("Все тесты пройдены!")
