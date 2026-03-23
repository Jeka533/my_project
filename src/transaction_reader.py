"""
Модуль для чтения финансовых операций из CSV и Excel файлов.
"""

import csv
import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class Transaction:
    """Финансовая операция."""

    date: datetime
    amount: Decimal
    description: str
    category: Optional[str] = None
    transaction_id: Optional[str] = None


class CSVTransactionReader:
    """Чтение транзакций из CSV."""

    def __init__(self, file_path: Union[str, Path], encoding: str = "utf-8") -> None:
        self.file_path = Path(file_path)
        self.encoding = encoding

    def read(self) -> List[Transaction]:
        """Читает транзакции из CSV."""
        transactions: List[Transaction] = []

        with open(self.file_path, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    transaction = self._parse_row(row)
                    transactions.append(transaction)
                except (ValueError, KeyError) as e:
                    logger.error(f"Ошибка в строке: {e}")

        return transactions

    def _parse_row(self, row: Dict[str, str]) -> Transaction:
        """Парсит строку CSV."""
        date = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
        amount = Decimal(row["amount"].strip().replace(",", "."))
        description = row["description"].strip()
        category = row.get("category", "").strip() or None
        transaction_id = row.get("transaction_id", "").strip() or None

        return Transaction(
            date=date,
            amount=amount,
            description=description,
            category=category,
            transaction_id=transaction_id,
        )


class ExcelTransactionReader:
    """Чтение транзакций из Excel."""

    def __init__(self, file_path: Union[str, Path]) -> None:
        self.file_path = Path(file_path)
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Проверяет наличие openpyxl."""
        try:
            import openpyxl  # type: ignore  # noqa: F401
        except ImportError as e:
            raise ImportError("Установите openpyxl: pip install openpyxl") from e

    def read(self) -> List[Transaction]:
        """Читает транзакции из Excel."""
        import openpyxl  # type: ignore

        transactions: List[Transaction] = []
        wb = openpyxl.load_workbook(self.file_path, data_only=True)
        sheet = wb.active

        # Получаем заголовки
        headers = [cell.value.lower() if cell.value else "" for cell in sheet[1]]

        # Ищем индексы колонок
        try:
            date_idx = headers.index("date")
            amount_idx = headers.index("amount")
            desc_idx = headers.index("description")
        except ValueError as e:
            wb.close()
            raise ValueError(f"Обязательная колонка не найдена: {e}") from e

        # Опциональные колонки
        cat_idx = headers.index("category") if "category" in headers else None
        tid_idx = headers.index("transaction_id") if "transaction_id" in headers else None

        # Читаем данные
        for row in sheet.iter_rows(min_row=2):
            if not row[date_idx].value:
                continue

            try:
                transaction = self._parse_row(
                    row, date_idx, amount_idx, desc_idx, cat_idx, tid_idx
                )
                transactions.append(transaction)
            except (ValueError, AttributeError) as e:
                logger.error(f"Ошибка в строке: {e}")

        wb.close()
        return transactions

    def _parse_row(
        self,
        row: tuple,
        date_idx: int,
        amount_idx: int,
        desc_idx: int,
        cat_idx: Optional[int],
        tid_idx: Optional[int],
    ) -> Transaction:
        """Парсит строку Excel."""
        # Дата
        date_val = row[date_idx].value
        if isinstance(date_val, datetime):
            date = date_val
        else:
            date = datetime.strptime(str(date_val).strip(), "%Y-%m-%d")

        # Сумма
        amount_val = row[amount_idx].value
        if isinstance(amount_val, (int, float)):
            amount = Decimal(str(amount_val))
        else:
            amount = Decimal(str(amount_val).strip().replace(",", "."))

        # Описание
        description = str(row[desc_idx].value).strip()

        # Категория
        category = None
        if cat_idx is not None and row[cat_idx].value:
            category = str(row[cat_idx].value).strip()

        # ID
        transaction_id = None
        if tid_idx is not None and row[tid_idx].value:
            transaction_id = str(row[tid_idx].value).strip()

        return Transaction(
            date=date,
            amount=amount,
            description=description,
            category=category,
            transaction_id=transaction_id,
        )


def read_transactions(file_path: Union[str, Path]) -> List[Transaction]:
    """Универсальная функция чтения транзакций."""
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        return CSVTransactionReader(file_path).read()
    elif file_path.suffix.lower() in (".xlsx", ".xls"):
        return ExcelTransactionReader(file_path).read()
    else:
        raise ValueError(f"Неподдерживаемый формат: {file_path.suffix}")
