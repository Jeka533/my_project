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
    """Тесты для read_csv_transactions."""

    def setUp(self) -> None:
        """Создание временного CSV файла."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_file = Path(self.temp_dir) / "test.csv"

    def tearDown(self) -> None:
        """Очистка временных файлов."""
        if self.csv_file.exists():
            self.csv_file.unlink()
        Path(self.temp_dir).rmdir()

    def _create_csv(self, rows: List[List[str]], headers: Optional[List[str]] = None) -> None:
        """Создание CSV файла."""
        if headers is None:
            headers = ['date', 'amount', 'description', 'category', 'transaction_id']
        with open(self.csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def test_valid_csv(self) -> None:
        """Тест корректного CSV."""
        rows = [['2024-01-15', '1500.50', 'Покупка', 'Еда', 'TXN001']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['date'], datetime(2024, 1, 15))
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))
        self.assertEqual(transactions[0]['category'], 'Еда')

    def test_csv_comma_amount(self) -> None:
        """Тест суммы с запятой."""
        rows = [['2024-01-15', '1500,50', 'Покупка', 'Еда', 'TXN001']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))

    def test_csv_missing_optional(self) -> None:
        """Тест без опциональных полей."""
        rows = [['2024-01-15', '1500.50', 'Покупка', '', '']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 1)
        self.assertIsNone(transactions[0]['category'])
        self.assertIsNone(transactions[0]['transaction_id'])

    def test_csv_missing_required(self) -> None:
        """Тест с отсутствием обязательных полей."""
        rows = [['', '1500.50', 'Покупка', 'Еда', 'TXN001']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 0)

    def test_csv_invalid_date(self) -> None:
        """Тест неверного формата даты."""
        rows = [['2024/01/15', '1500.50', 'Покупка', 'Еда', 'TXN001']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 0)

    def test_csv_invalid_amount(self) -> None:
        """Тест неверного формата суммы."""
        rows = [['2024-01-15', 'abc', 'Покупка', 'Еда', 'TXN001']]
        self._create_csv(rows)
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 0)

    def test_csv_empty(self) -> None:
        """Тест пустого файла."""
        with open(self.csv_file, 'w', encoding='utf-8') as f:
            f.write('')
        transactions = read_csv_transactions(self.csv_file)
        self.assertEqual(len(transactions), 0)

    def test_csv_not_found(self) -> None:
        """Тест несуществующего файла."""
        transactions = read_csv_transactions("missing.csv")
        self.assertEqual(len(transactions), 0)


class TestReadExcelTransactions(unittest.TestCase):
    """Тесты для read_excel_transactions."""

    def setUp(self) -> None:
        """Создание временного Excel файла."""
        try:
            import pandas as pd
            self.pd = pd
        except ImportError:
            self.pd = None
            self.skipTest("pandas не установлен")

        self.temp_dir = tempfile.mkdtemp()
        self.excel_file = Path(self.temp_dir) / "test.xlsx"

    def tearDown(self) -> None:
        """Очистка временных файлов."""
        if hasattr(self, 'excel_file') and self.excel_file.exists():
            self.excel_file.unlink()
        if hasattr(self, 'temp_dir') and Path(self.temp_dir).exists():
            Path(self.temp_dir).rmdir()

    def _create_excel(self, data: List[List[Any]], columns: Optional[List[str]] = None) -> None:
        """Создание Excel файла."""
        if columns is None:
            columns = ['date', 'amount', 'description', 'category', 'transaction_id']
        df = self.pd.DataFrame(data, columns=columns)
        df.to_excel(self.excel_file, index=False)

    def test_valid_excel(self) -> None:
        """Тест корректного Excel."""
        if self.pd is None:
            self.skipTest("pandas не установлен")
        data = [['2024-01-15', 1500.50, 'Покупка', 'Еда', 'TXN001']]
        self._create_excel(data)
        transactions = read_excel_transactions(self.excel_file)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['date'].strftime('%Y-%m-%d'), '2024-01-15')
        self.assertEqual(transactions[0]['amount'], Decimal('1500.50'))
        self.assertEqual(transactions[0]['category'], 'Еда')

    def test_excel_date_object(self) -> None:
        """Тест с объектом даты."""
        if self.pd is None:
            self.skipTest("pandas не установлен")
        data = [[datetime(2024, 1, 15), 1500.50, 'Покупка', 'Еда', 'TXN001']]
        self._create_excel(data)
        transactions = read_excel_transactions(self.excel_file)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['date'], datetime(2024, 1, 15))

    def test_excel_missing_optional(self) -> None:
        """Тест без опциональных полей."""
        if self.pd is None:
            self.skipTest("pandas не установлен")
        data = [['2024-01-15', 1500.50, 'Покупка', None, None]]
        self._create_excel(data)
        transactions = read_excel_transactions(self.excel_file)
        self.assertEqual(len(transactions), 1)
        self.assertIsNone(transactions[0]['category'])
        self.assertIsNone(transactions[0]['transaction_id'])

    def test_excel_missing_required_columns(self) -> None:
        """Тест с отсутствием обязательных колонок."""
        if self.pd is None:
            self.skipTest("pandas не установлен")
        data = [['2024-01-15', 1500.50]]
        self._create_excel(data, columns=['date', 'amount'])
        transactions = read_excel_transactions(self.excel_file)
        self.assertEqual(len(transactions), 0)

    def test_excel_empty(self) -> None:
        """Тест пустого файла."""
        if self.pd is None:
            self.skipTest("pandas не установлен")
        self._create_excel([])
        transactions = read_excel_transactions(self.excel_file)
        self.assertEqual(len(transactions), 0)

    def test_excel_not_found(self) -> None:
        """Тест несуществующего файла."""
        transactions = read_excel_transactions("missing.xlsx")
        self.assertEqual(len(transactions), 0)


if __name__ == "__main__":
    unittest.main()
