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
    """Читает транзакции из CSV файла."""
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
                    date_str = row.get('date', '').strip()
                    amount_str = row.get('amount', '').strip().replace(',', '.')
                    description = row.get('description', '').strip()
                    category = row.get('category', '').strip()
                    trans_id = row.get('transaction_id', '').strip()

                    if not date_str or not amount_str:
                        continue

                    date_str = date_str.replace('Z', '+00:00')
                    try:
                        date = datetime.fromisoformat(date_str)
                    except ValueError:
                        date = datetime.strptime(date_str, '%Y-%m-%d')

                    amount_str = re.sub(r'[^\d.-]', '', amount_str)
                    if not amount_str:
                        continue

                    amount = Decimal(amount_str)

                    transactions.append({
                        'date': date,
                        'amount': amount,
                        'description': description,
                        'category': category if category else None,
                        'transaction_id': trans_id if trans_id else None,
                    })

                except (ValueError, KeyError):
                    continue

        return transactions

    except (FileNotFoundError, PermissionError):
        return []


def read_excel_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """Читает транзакции из Excel файла."""
    transactions: List[Dict] = []
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        import pandas as pd

        df = pd.read_excel(file_path)

        required = ['date', 'amount', 'description']
        if not all(col in df.columns for col in required):
            return []

        for _, row in df.iterrows():
            try:
                date_val = row['date']
                amount_val = row['amount']
                description = str(row['description']).strip() if pd.notna(row['description']) else ''

                if pd.isna(date_val) or pd.isna(amount_val):
                    continue

                if isinstance(date_val, (datetime, pd.Timestamp)):
                    date = date_val
                else:
                    date_str = str(date_val).strip().replace('Z', '+00:00')
                    try:
                        date = datetime.fromisoformat(date_str)
                    except ValueError:
                        date = datetime.strptime(date_str, '%Y-%m-%d')

                if isinstance(amount_val, (int, float)):
                    amount = Decimal(str(amount_val))
                else:
                    amount_str = str(amount_val).strip().replace(',', '.')
                    amount_str = re.sub(r'[^\d.-]', '', amount_str)
                    if not amount_str:
                        continue
                    amount = Decimal(amount_str)

                category = None
                if 'category' in df.columns and pd.notna(row['category']):
                    cat_val = str(row['category']).strip()
                    if cat_val not in ('nan', 'None', ''):
                        category = cat_val

                trans_id = None
                if 'transaction_id' in df.columns and pd.notna(row['transaction_id']):
                    tid_val = str(row['transaction_id']).strip()
                    if tid_val not in ('nan', 'None', ''):
                        trans_id = tid_val

                transactions.append({
                    'date': date,
                    'amount': amount,
                    'description': description,
                    'category': category,
                    'transaction_id': trans_id,
                })

            except (ValueError, KeyError):
                continue

        return transactions

    except ImportError:
        return []
    except (FileNotFoundError, PermissionError):
        return []
