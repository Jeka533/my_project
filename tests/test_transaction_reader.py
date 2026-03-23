"""Тесты для чтения транзакций."""

import csv
import tempfile
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Generator

import pytest

from src.transaction_reader import CSVTransactionReader, ExcelTransactionReader, read_transactions


class TestCSVTransactionReader:
    """Тесты CSV читателя."""

    @pytest.fixture
    def csv_file(self) -> Generator[Path, None, None]:
        """Создает временный CSV файл."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "description", "category"])
            writer.writerow(["2024-01-15", "100.50", "Зарплата", "Доход"])
            writer.writerow(["2024-01-16", "-25.75", "Кофе", "Еда"])
            path = Path(f.name)

        yield path
        path.unlink()

    def test_read(self, csv_file: Path) -> None:
        """Тест чтения CSV."""
        reader = CSVTransactionReader(csv_file)
        transactions = reader.read()

        assert len(transactions) == 2
        assert transactions[0].date == datetime(2024, 1, 15)
        assert transactions[0].amount == Decimal("100.50")
        assert transactions[0].description == "Зарплата"
        assert transactions[0].category == "Доход"


class TestExcelTransactionReader:
    """Тесты Excel читателя."""

    @pytest.fixture
    def excel_file(self) -> Generator[Path, None, None]:
        """Создает временный Excel файл."""
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            path = Path(f.name)

        try:
            from openpyxl import Workbook  # type: ignore
        except ImportError:
            pytest.skip("openpyxl не установлен")
            return path

        wb = Workbook()
        ws = wb.active
        ws["A1"] = "date"
        ws["B1"] = "amount"
        ws["C1"] = "description"
        ws["D1"] = "category"
        ws["A2"] = "2024-01-15"
        ws["B2"] = 100.50
        ws["C2"] = "Зарплата"
        ws["D2"] = "Доход"
        ws["A3"] = "2024-01-16"
        ws["B3"] = -25.75
        ws["C3"] = "Кофе"
        ws["D3"] = "Еда"

        wb.save(path)
        wb.close()

        yield path
        path.unlink()

    def test_read(self, excel_file: Path) -> None:
        """Тест чтения Excel."""
        reader = ExcelTransactionReader(excel_file)
        transactions = reader.read()

        assert len(transactions) == 2
        assert transactions[0].date == datetime(2024, 1, 15)
        assert transactions[0].amount == Decimal("100.50")
        assert transactions[0].description == "Зарплата"
        assert transactions[0].category == "Доход"


class TestReadTransactions:
    """Тесты универсальной функции."""

    @pytest.fixture
    def csv_file(self) -> Generator[Path, None, None]:
        """Создает временный CSV файл."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "description"])
            writer.writerow(["2024-01-15", "100", "Тест"])
            path = Path(f.name)

        yield path
        path.unlink()

    def test_read_csv(self, csv_file: Path) -> None:
        """Тест автоматического определения CSV."""
        transactions = read_transactions(csv_file)
        assert len(transactions) == 1
        assert transactions[0].amount == Decimal("100")
