"""
Модуль для чтения финансовых операций из CSV и Excel файлов.
"""

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Union


def read_csv_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Читает транзакции из CSV файла.

    Параметры:
    file_path (str, Path): путь к CSV файлу

    Возвращает:
    list: список словарей с транзакциями
    """
    transactions: List[Dict] = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print(f"Ошибка: файл {file_path} не содержит заголовков")
                return []

            for row_num, row in enumerate(reader, start=2):
                try:
                    if not any(row.values()):
                        continue

                    transaction: Dict = {}

                    # Дата
                    if 'date' in row and row['date']:
                        try:
                            transaction['date'] = datetime.strptime(
                                row['date'].strip(), '%Y-%m-%d'
                            )
                        except ValueError:
                            print(f"Ошибка в строке {row_num}: "
                                  f"неверный формат даты '{row['date']}'")
                            continue
                    else:
                        print(f"Ошибка в строке {row_num}: отсутствует дата")
                        continue

                    # Сумма
                    if 'amount' in row and row['amount']:
                        try:
                            amount_str = row['amount'].strip().replace(',', '.')
                            transaction['amount'] = Decimal(amount_str)
                        except Exception:
                            print(f"Ошибка в строке {row_num}: "
                                  f"неверный формат суммы '{row['amount']}'")
                            continue
                    else:
                        print(f"Ошибка в строке {row_num}: отсутствует сумма")
                        continue

                    # Описание
                    if 'description' in row:
                        transaction['description'] = row['description'].strip()
                    else:
                        transaction['description'] = ''

                    # Категория (опционально)
                    category = row.get('category', '').strip()
                    transaction['category'] = category if category else None

                    # ID транзакции (опционально)
                    transaction_id = row.get('transaction_id', '').strip()
                    transaction['transaction_id'] = transaction_id if transaction_id else None

                    transactions.append(transaction)

                except Exception as e:
                    print(f"Ошибка при обработке строки {row_num}: {e}")
                    continue

        print(f"Успешно прочитано {len(transactions)} транзакций из {file_path}")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def read_excel_transactions(file_path: Union[str, Path]) -> List[Dict]:
    """
    Читает транзакции из Excel файла.

    Параметры:
    file_path (str, Path): путь к Excel файлу

    Возвращает:
    list: список словарей с транзакциями
    """
    transactions: List[Dict] = []

    try:
        try:
            import pandas as pd
        except ImportError:
            print("Ошибка: для чтения Excel файлов необходим модуль pandas")
            print("Установите его командой: pip install pandas openpyxl")
            return []

        df = pd.read_excel(file_path)

        if df.empty:
            print(f"Файл {file_path} пуст")
            return []

        required_columns = ['date', 'amount', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Ошибка: в файле отсутствуют обязательные колонки: {missing_columns}")
            print(f"Доступные колонки: {list(df.columns)}")
            return []

        for idx, row in df.iterrows():
            try:
                transaction: Dict = {}

                # Дата
                if pd.notna(row['date']):
                    if isinstance(row['date'], (datetime, pd.Timestamp)):
                        transaction['date'] = row['date']
                    else:
                        try:
                            transaction['date'] = datetime.strptime(
                                str(row['date']), '%Y-%m-%d'
                            )
                        except Exception:
                            try:
                                transaction['date'] = pd.to_datetime(row['date'])
                            except Exception:
                                print(f"Ошибка в строке {idx + 2}: "
                                      f"неверный формат даты '{row['date']}'")
                                continue
                else:
                    print(f"Ошибка в строке {idx + 2}: отсутствует дата")
                    continue

                # Сумма
                if pd.notna(row['amount']):
                    try:
                        if isinstance(row['amount'], (int, float)):
                            transaction['amount'] = Decimal(str(row['amount']))
                        else:
                            amount_str = str(row['amount']).strip().replace(',', '.')
                            transaction['amount'] = Decimal(amount_str)
                    except Exception:
                        print(f"Ошибка в строке {idx + 2}: "
                              f"неверный формат суммы '{row['amount']}'")
                        continue
                else:
                    print(f"Ошибка в строке {idx + 2}: отсутствует сумма")
                    continue

                # Описание
                if pd.notna(row['description']):
                    transaction['description'] = str(row['description']).strip()
                else:
                    transaction['description'] = ''

                # Категория (опционально)
                if 'category' in df.columns and pd.notna(row['category']):
                    transaction['category'] = str(row['category']).strip()
                else:
                    transaction['category'] = None

                # ID транзакции (опционально)
                if 'transaction_id' in df.columns and pd.notna(row['transaction_id']):
                    transaction['transaction_id'] = str(row['transaction_id']).strip()
                else:
                    transaction['transaction_id'] = None

                transactions.append(transaction)

            except Exception as e:
                print(f"Ошибка при обработке строки {idx + 2}: {e}")
                continue

        print(f"Успешно прочитано {len(transactions)} транзакций из {file_path}")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return []
