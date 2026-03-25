"""
Модуль для чтения финансовых операций из CSV и Excel файлов.
"""

import csv
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Union


def get_data_path(filename: str) -> Path:
    """Возвращает путь к файлу в папке data."""
    return Path(__file__).parent.parent / "data" / filename


def read_csv_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Читает транзакции из CSV файла.
    Сохраняет ВСЕ поля из исходной строки.
    """
    transactions: List[Dict] = []
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            delimiter = ';' if ';' in f.readline() else ','
            f.seek(0)
            reader = csv.DictReader(f, delimiter=delimiter)

            for row in reader:
                try:
                    # Парсим дату
                    date_str = row.get('date', '').strip()
                    if not date_str:
                        continue

                    date_str = date_str.replace('Z', '+00:00')
                    try:
                        date = datetime.fromisoformat(date_str)
                    except ValueError:
                        date = datetime.strptime(date_str, '%Y-%m-%d')

                    # Парсим сумму
                    amount_str = row.get('amount', '').strip().replace(',', '.')
                    if not amount_str:
                        continue

                    amount_str = re.sub(r'[^\d.-]', '', amount_str)
                    if not amount_str:
                        continue

                    amount = Decimal(amount_str)

                    # Сохраняем ВСЕ данные из строки
                    transaction: Dict = {
                        'date': date,
                        'amount': amount,
                        'description': row.get('description', '').strip(),
                    }

                    # Добавляем ВСЕ остальные поля
                    for key, value in row.items():
                        if key not in ['date', 'amount', 'description']:
                            if value and value not in ('', 'nan'):
                                transaction[key] = value

                    transactions.append(transaction)

                except (ValueError, KeyError):
                    continue

        return transactions

    except (FileNotFoundError, PermissionError):
        return []


def read_excel_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Читает транзакции из Excel файла.
    Сохраняет ВСЕ поля из исходной строки.
    """
    transactions: List[Dict] = []
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        import pandas as pd

        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            try:
                # Парсим дату
                date_val = row.get('date')
                if pd.isna(date_val):
                    continue

                if isinstance(date_val, (datetime, pd.Timestamp)):
                    date = date_val
                else:
                    date_str = str(date_val).strip().replace('Z', '+00:00')
                    try:
                        date = datetime.fromisoformat(date_str)
                    except ValueError:
                        date = datetime.strptime(date_str, '%Y-%m-%d')

                # Парсим сумму
                amount_val = row.get('amount')
                if pd.isna(amount_val):
                    continue

                if isinstance(amount_val, (int, float)):
                    amount = Decimal(str(amount_val))
                else:
                    amount_str = str(amount_val).strip().replace(',', '.')
                    amount_str = re.sub(r'[^\d.-]', '', amount_str)
                    if not amount_str:
                        continue
                    amount = Decimal(amount_str)

                # Сохраняем ВСЕ данные из строки
                transaction: Dict = {
                    'date': date,
                    'amount': amount,
                    'description': str(row.get('description', '')).strip(),
                }

                # Добавляем ВСЕ остальные поля
                for col in df.columns:
                    if col not in ['date', 'amount', 'description']:
                        value = row[col]
                        if pd.notna(value) and str(value) not in ('nan', 'None', ''):
                            if isinstance(value, (datetime, pd.Timestamp)):
                                transaction[col] = value.isoformat()
                            else:
                                transaction[col] = str(value)

                transactions.append(transaction)

            except (ValueError, KeyError):
                continue

        return transactions

    except ImportError:
        return []
    except (FileNotFoundError, PermissionError):
        return []
