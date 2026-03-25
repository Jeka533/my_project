"""
Модуль для настройки логирования в приложении.
"""

import logging
import os
from typing import Union


def setup_logger(name: str, log_file: str, level: Union[int, str] = logging.DEBUG) -> logging.Logger:
    """
    Настраивает и возвращает логгер для конкретного модуля.

    Args:
        name: Имя логгера (обычно __name__)
        log_file: Имя файла для логов
        level: Уровень логирования

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаём папку logs в корне проекта
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_path = os.path.join(log_directory, log_file)

    # Создаём логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем предыдущие обработчики (для перезаписи логов)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Создаём обработчик для записи в файл
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')

    # Настраиваем формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
