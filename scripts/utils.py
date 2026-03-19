"""
Утилиты для работы с транзакциями.
"""

import json
import os
from typing import Any, Dict, List

from logger_setup import setup_logger

# Настройка логгера для модуля utils
logger = setup_logger(__name__, "utils.log")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список транзакций или пустой список в случае ошибки.
    """
    logger.info(f"Попытка загрузки транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        error_message = f"файл {file_path} не найден"
        logger.error(error_message)
        print(f"Ошибка: {error_message}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Файл {file_path} успешно загружен")

        if isinstance(data, list):
            logger.info(f"Загружено {len(data)} транзакций")
            return data
        else:
            error_message = "данные в файле не являются списком"
            logger.error(error_message)
            print(f"Ошибка: {error_message}")
            return []

    except FileNotFoundError:
        # Эта ошибка уже обработана выше, но оставим для надежности
        error_message = f"файл {file_path} не найден"
        logger.error(error_message)
        print(f"Ошибка: {error_message}")
        return []
    except json.JSONDecodeError as e:
        error_message = f"ошибка при парсинге JSON: {e}"
        logger.error(error_message)
        print(f"Ошибка: {error_message}")
        return []
    except Exception as e:
        error_message = f"неожиданная ошибка: {e}"
        logger.error(error_message)
        print(f"Ошибка: {error_message}")
        return []
