# scripts/utils.py

import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Аргументы:
        file_path (str): путь к файлу

    Возвращает:
        List[Dict[str, Any]]: список транзакций или пустой список
    """
    # Проверяем файл как есть
    if os.path.exists(file_path):
        actual_path = file_path
    else:
        # Пробуем добавить расширение .json
        if os.path.exists(file_path + ".json"):
            actual_path = file_path + ".json"
        # Пробуем .json.py (как у вас)
        elif os.path.exists(file_path + ".py"):
            actual_path = file_path + ".py"
        else:
            print(f"Ошибка: файл {file_path} не найден")
            return []

    print(f"Загружаем файл: {actual_path}")

    try:
        with open(actual_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Ошибка: в файле не список")
            return []

        if len(data) == 0:
            print("Файл пустой")
            return []

        print(f"Загружено {len(data)} транзакций")
        return data

    except json.JSONDecodeError:
        print("Ошибка: файл не является правильным JSON")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []
