# scripts/utils.py

import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список транзакций или пустой список в случае ошибки.
    """
    if not os.path.exists(file_path):
        print(f"Ошибка: файл {file_path} не найден")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            pass
        else:
            print("Ошибка: данные в файле не являются списком")
            return []

        return data

    except FileNotFoundError:
        # Эта ошибка уже обработана выше, но оставим для надежности
        print(f"Ошибка: файл {file_path} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return []
