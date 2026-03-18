import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import pytest

# Добавляем путь к корневой папке проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.log_decorator import log  # noqa: E402


def test_log_to_console_success(capsys: pytest.CaptureFixture) -> None:
    """Тест успешного выполнения с выводом в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)

    assert result == 5
    captured = capsys.readouterr()
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys: pytest.CaptureFixture) -> None:
    """Тест ошибки выполнения с выводом в консоль."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert captured.out == "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"


def test_log_to_file_success() -> None:
    """Тест успешного выполнения с записью в файл."""

    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp_file:
        filename = tmp_file.name

    try:

        @log(filename=filename)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)

        assert result == 20

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "multiply ok\n"

    finally:
        os.unlink(filename)


def test_log_to_file_error() -> None:
    """Тест ошибки выполнения с записью в файл."""

    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp_file:
        filename = tmp_file.name

    try:

        @log(filename=filename)
        def get_item(lst: list, index: int) -> Any:
            return lst[index]

        with pytest.raises(IndexError):
            get_item([1, 2, 3], 5)

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "get_item error: IndexError. Inputs: ([1, 2, 3], 5), {}\n"

    finally:
        os.unlink(filename)


def test_log_with_multiple_arguments(capsys: pytest.CaptureFixture) -> None:
    """Тест с несколькими аргументами и keyword arguments."""

    @log()
    def process_data(a: int, b: str, c: bool = True) -> str:
        return f"{a}{b}{c}"

    result = process_data(10, "test", c=False)

    assert result == "10testFalse"
    captured = capsys.readouterr()
    assert captured.out == "process_data ok\n"
