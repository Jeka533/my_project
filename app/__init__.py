"""
Пакет для обработки банковских операций.
Содержит функции для маскирования данных, генерации выписок и виджетов.
"""

from app import generators, __all__
from app import masks
from app import processing
from app import widget

__all__ = ['generators', 'masks', 'processing', 'widget']

