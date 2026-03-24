"""
Тесты для модуля чтения транзакций.
"""

import csv
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, List, Optional

from src.transaction_reader import read_csv_transactions, read_excel_transactions


class TestReadCSVTransactions(unittest.TestCase):
    """Тесты для функции read_csv_transactions."""

    def setUp(self) -> None:
        """Создание временного CSV файла для тестов."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = Path(self.temp_dir) / "test_transactions.csv"

    def create_csv_file(
        self,
        rows: List[List[str]],
        headers: Optional[List[str]] = None
    ) -> None:
        """Вспомогательная функция для создания CSV файла."""
        if headers is None:
            headers = ['date', 'amount', 'description', 'category', 'transaction_id']

        with open(self.csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)

    def test_read_valid_csv(self) -> None:
        """Тест чтения корректного CSV файла."""
        rows = [
            ['2024-01-15', '1500.50', 'Покупка продуктов', 'Еда', 'TXN001'],
            ['2024-01-16', '500.00', 'Транспорт', 'Транспорт', 'TXN002'],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['date'], datetime(2024, 1, 15))
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))
        self.assertEqual(transactions[0]['description'], 'Покупка продуктов')
        self.assertEqual(transactions[0]['category'], 'Еда')
        self.assertEqual(transactions[0]['transaction_id'], 'TXN001')

    def test_read_csv_with_comma_in_amount(self) -> None:
        """Тест чтения CSV с запятой в сумме."""
        rows = [
            ['2024-01-15', '1500,50', 'Покупка', 'Еда', 'TXN001'],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))

    def test_read_csv_missing_optional_fields(self) -> None:
        """Тест чтения CSV без опциональных полей."""
        rows = [
            ['2024-01-15', '1500.50', 'Покупка', '', ''],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 1)
        self.assertIsNone(transactions[0]['category'])
        self.assertIsNone(transactions[0]['transaction_id'])

    def test_read_csv_missing_required_fields(self) -> None:
        """Тест чтения CSV с отсутствием обязательных полей."""
        rows = [
            ['', '1500.50', 'Покупка', 'Еда', 'TXN001'],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 0)

    def test_read_csv_invalid_date(self) -> None:
        """Тест чтения CSV с неверным форматом даты."""
        rows = [
            ['2024/01/15', '1500.50', 'Покупка', 'Еда', 'TXN001'],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 0)

    def test_read_csv_invalid_amount(self) -> None:
        """Тест чтения CSV с неверным форматом суммы."""
        rows = [
            ['2024-01-15', 'abc', 'Покупка', 'Еда', 'TXN001'],
        ]
        self.create_csv_file(rows)

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 0)

    def test_read_csv_empty_file(self) -> None:
        """Тест чтения пустого CSV файла."""
        with open(self.csv_file, 'w', encoding='utf-8') as f:
            f.write('')

        transactions = read_csv_transactions(self.csv_file)

        self.assertEqual(len(transactions), 0)

    def test_read_csv_file_not_found(self) -> None:
        """Тест чтения несуществующего файла."""
        transactions = read_csv_transactions("non_existent_file.csv")

        self.assertEqual(len(transactions), 0)

    def tearDown(self) -> None:
        """Очистка временных файлов."""
        if self.csv_file.exists():
            self.csv_file.unlink()
        if Path(self.temp_dir).exists():
            Path(self.temp_dir).rmdir()


class TestReadExcelTransactions(unittest.TestCase):
    """Тесты для функции read_excel_transactions."""

    def setUp(self) -> None:
        """Создание временного Excel файла для тестов."""
        try:
            import pandas as pd
            self.pd = pd
        except ImportError:
            self.pd = None
            self.skipTest("pandas не установлен, пропускаем тесты Excel")

        self.temp_dir = tempfile.mkdtemp()
        self.excel_file = Path(self.temp_dir) / "test_transactions.xlsx"

    def create_excel_file(
        self,
        data: List[List[Any]],
        columns: Optional[List[str]] = None
    ) -> None:
        """Вспомогательная функция для создания Excel файла."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        if columns is None:
            columns = ['date', 'amount', 'description', 'category', 'transaction_id']

        df = self.pd.DataFrame(data, columns=columns)
        df.to_excel(self.excel_file, index=False)

    def test_read_valid_excel(self) -> None:
        """Тест чтения корректного Excel файла."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        data: List[List[Any]] = [
            ['2024-01-15', 1500.50, 'Покупка продуктов', 'Еда', 'TXN001'],
            ['2024-01-16', 500.00, 'Транспорт', 'Транспорт', 'TXN002'],
        ]
        self.create_excel_file(data)

        transactions = read_excel_transactions(self.excel_file)

        self.assertEqual(len(transactions), 2)
        if transactions[0]['date']:
            self.assertEqual(
                transactions[0]['date'].strftime('%Y-%m-%d'),
                '2024-01-15'
            )
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))
        self.assertEqual(transactions[0]['description'], 'Покупка продуктов')
        self.assertEqual(transactions[0]['category'], 'Еда')
        self.assertEqual(transactions[0]['transaction_id'], 'TXN001')

    def test_read_excel_with_date_object(self) -> None:
        """Тест чтения Excel с объектом даты."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        data: List[List[Any]] = [
            [datetime(2024, 1, 15), 1500.50, 'Покупка', 'Еда', 'TXN001'],
        ]
        self.create_excel_file(data)

        transactions = read_excel_transactions(self.excel_file)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['date'], datetime(2024, 1, 15))

    def test_read_excel_missing_optional_fields(self) -> None:
        """Тест чтения Excel без опциональных полей."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        data: List[List[Any]] = [
            ['2024-01-15', 1500.50, 'Покупка', None, None],
        ]
        self.create_excel_file(data)

        transactions = read_excel_transactions(self.excel_file)

        self.assertEqual(len(transactions), 1)
        self.assertIsNone(transactions[0]['category'])
        self.assertIsNone(transactions[0]['transaction_id'])

    def test_read_excel_missing_required_columns(self) -> None:
        """Тест чтения Excel с отсутствием обязательных колонок."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        data: List[List[Any]] = [
            ['2024-01-15', 1500.50, 'Покупка'],
        ]
        self.create_excel_file(data, columns=['date', 'amount', 'category'])

        transactions = read_excel_transactions(self.excel_file)

        self.assertEqual(len(transactions), 0)

    def test_read_excel_empty_file(self) -> None:
        """Тест чтения пустого Excel файла."""
        if self.pd is None:
            self.skipTest("pandas не установлен")

        df = self.pd.DataFrame()
        df.to_excel(self.excel_file, index=False)

        transactions = read_excel_transactions(self.excel_file)

        self.assertEqual(len(transactions), 0)

    def test_read_excel_file_not_found(self) -> None:
        """Тест чтения несуществующего файла."""
        transactions = read_excel_transactions("non_existent_file.xlsx")

        self.assertEqual(len(transactions), 0)

    def tearDown(self) -> None:
        """Очистка временных файлов."""
        if hasattr(self, 'excel_file') and self.excel_file.exists():
            self.excel_file.unlink()
        if hasattr(self, 'temp_dir') and Path(self.temp_dir).exists():
            Path(self.temp_dir).rmdir()


if __name__ == "__main__":
    unittest.main()
