import functools
import sys
from typing import Any, Callable, Optional, TextIO


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции.

    Args:
        filename: Опциональный путь к файлу для записи логов.
                 Если не указан, логи выводятся в консоль.

    Returns:
        Callable: Обернутую функцию с логированием.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем куда писать логи
            output: TextIO
            if filename:
                output = open(filename, 'a', encoding='utf-8')
            else:
                output = sys.stdout

            try:
                result = func(*args, **kwargs)
                # Логируем успешное выполнение
                output.write(f"{func.__name__} ok\n")
                if filename:
                    output.close()
                return result

            except Exception as e:
                # Логируем ошибку
                error_msg = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                output.write(error_msg)
                if filename:
                    output.close()
                raise

        return wrapper

    return decorator
